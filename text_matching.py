import re


VOICE_SCORING_REVISION = "lexical-marker-f1-v2"
WORD_PATTERN = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)


def contains_phrase(text, phrase):
    """Match a case-insensitive phrase without matching inside another word."""
    pattern = r"(?<!\w)" + re.escape(phrase.casefold()) + r"(?!\w)"
    return re.search(pattern, text.casefold()) is not None


def _phrase_spans(text, phrase):
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return [(match.start(), match.end()) for match in re.finditer(pattern, text, re.IGNORECASE)]


def _word_tokens(text):
    return [
        (match.group(0).casefold(), match.start(), match.end())
        for match in WORD_PATTERN.finditer(text)
    ]


def _target_records(targets, dialect_equivalents):
    records = []
    for source, accepted in (targets or {}).items():
        if isinstance(accepted, str):
            accepted = [accepted]
        candidates = list(accepted)
        for candidate in accepted:
            equivalents = dialect_equivalents.get(candidate, [])
            if isinstance(equivalents, str):
                equivalents = [equivalents]
            candidates.extend(equivalents)
        records.append((source, list(dict.fromkeys(candidates))))
    return records


def _remove_spanned_tokens(tokens, spans):
    return [
        item
        for item in tokens
        if not any(
            item[1] < span_end and span_start < item[2]
            for span_start, span_end in spans
        )
    ]


def _replace_sequence(tokens, old, new):
    if not old:
        return tokens
    result = []
    index = 0
    while index < len(tokens):
        if tokens[index:index + len(old)] == old:
            result.extend(new)
            index += len(old)
        else:
            result.append(tokens[index])
            index += 1
    return result


def _contains_token_sequence(tokens, phrase):
    if not phrase:
        return False
    return any(
        tokens[index:index + len(phrase)] == phrase
        for index in range(len(tokens) - len(phrase) + 1)
    )


def _longest_common_subsequence_length(left, right):
    previous = [0] * (len(right) + 1)
    for left_token in left:
        current = [0]
        for index, right_token in enumerate(right, start=1):
            if left_token == right_token:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[index - 1]))
        previous = current
    return previous[-1]


def score_writer_voice(
    input_text,
    output_text,
    spelling_targets=None,
    grammar_targets=None,
    voice_markers=None,
    dialect_equivalents=None,
    forbidden_rewrites=None,
):
    """Score lexical preservation and curated voice markers outside correction spans.

    Correctable source spans and their accepted outputs are excluded so missed
    or successful spelling/grammar edits are scored by their own pillars.
    """
    equivalents = dialect_equivalents or {}
    records = _target_records(spelling_targets, equivalents) + _target_records(
        grammar_targets, equivalents
    )
    input_spans = []
    output_spans = []

    for source, accepted in records:
        source_matches = _phrase_spans(input_text, source)
        if not source_matches:
            continue
        source_span = source_matches[0]
        input_spans.append(source_span)

        candidates = [source] + [item for item in accepted if item != source]
        expected_position = source_span[0] / max(len(input_text), 1) * len(output_text)
        output_matches = []
        for candidate in candidates:
            output_matches.extend(_phrase_spans(output_text, candidate))
        available = [
            span
            for span in output_matches
            if not any(span[0] < used_end and used_start < span[1] for used_start, used_end in output_spans)
        ]
        if available:
            output_spans.append(min(available, key=lambda span: abs(span[0] - expected_position)))

    source_tokens = _remove_spanned_tokens(
        _word_tokens(input_text),
        input_spans,
    )
    source_tokens = [token for token, _, _ in source_tokens]
    output_tokens = _remove_spanned_tokens(_word_tokens(output_text), output_spans)
    output_tokens = [token for token, _, _ in output_tokens]

    for canonical_text, variants in equivalents.items():
        if isinstance(variants, str):
            variants = [variants]
        canonical = [token for token, _, _ in _word_tokens(canonical_text)]
        for variant in variants:
            alternative = [token for token, _, _ in _word_tokens(variant)]
            if alternative != canonical:
                output_tokens = _replace_sequence(output_tokens, alternative, canonical)

    matched = _longest_common_subsequence_length(source_tokens, output_tokens)
    recall = matched / len(source_tokens) if source_tokens else (1.0 if not output_tokens else 0.0)
    precision = matched / len(output_tokens) if output_tokens else (1.0 if not source_tokens else 0.0)
    lexical_f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    markers = list(voice_markers or [])
    output_marker_tokens = [
        token for token, _, _ in _word_tokens(output_text)
    ]
    matched_markers = 0
    for marker in markers:
        variants = [marker]
        for canonical, alternatives in equivalents.items():
            if isinstance(alternatives, str):
                alternatives = [alternatives]
            group = [canonical] + list(alternatives)
            if marker.casefold() in [item.casefold() for item in group]:
                variants.extend(group)
        if any(
            _contains_token_sequence(
                output_marker_tokens,
                [token for token, _, _ in _word_tokens(variant)],
            )
            for variant in variants
        ):
            matched_markers += 1
    marker_retention = matched_markers / len(markers) if markers else 1.0

    over_edit_count = sum(
        1 for phrase in (forbidden_rewrites or [])
        if contains_phrase(output_text, phrase)
    )
    score = lexical_f1 * marker_retention
    return {
        "score": round(score * 100.0, 2),
        "precision": round(precision * 100.0, 2),
        "recall": round(recall * 100.0, 2),
        "lexical_f1": round(lexical_f1 * 100.0, 2),
        "voice_marker_retention": round(marker_retention * 100.0, 2),
        "over_edit_count": over_edit_count,
        "matched_tokens": matched,
        "source_tokens": len(source_tokens),
        "output_tokens": len(output_tokens),
    }


def aggregate_writer_voice(metrics):
    """Aggregate passage-level voice signals and apply one suite-wide rewrite penalty."""
    if not metrics:
        raise ValueError("at least one passage metric is required")
    base_score = sum(item["score"] for item in metrics) / len(metrics)
    lexical_f1 = sum(item["lexical_f1"] for item in metrics) / len(metrics)
    marker_retention = sum(
        item["voice_marker_retention"] for item in metrics
    ) / len(metrics)
    over_edit_count = sum(item["over_edit_count"] for item in metrics)
    penalty = min(over_edit_count * 10.0, 80.0)
    return {
        "score": round(base_score * (1.0 - penalty / 100.0), 2),
        "lexical_f1": round(lexical_f1, 2),
        "voice_marker_retention": round(marker_retention, 2),
        "over_edit_count": over_edit_count,
        "over_edit_penalty": round(penalty, 2),
    }
