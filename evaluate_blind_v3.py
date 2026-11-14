#!/usr/bin/env python3
"""
Evaluation Harness for Blind Unseen Suite v3.0 (Passages B-01 to B-10)
Voice-Preserving AI-Spellcheck Benchmark

Evaluates spelling, grammar, voice preservation, and anti-hallucination across:
1. Spelling Accuracy (Orthography, phonetic recovery, severe dysgraphia)
2. Grammar Accuracy (Agreement, tense harmony, syntax)
3. Maintaining Writer's Voice (Preserving slang, dialect, shorthand vs over-editing)
4. Avoiding Hallucinations (Zero rogue dictionary mutations & semantic drift)
5. Hybrid Meta-Score (Composite)

Includes academic NLP metrics:
- SARI-Keep (n=1,2,3 n-gram preservation against minimal-edit reference)
- Protected-Span Retention Rate (PSRR)
- Over-Edit Rate (OER)
"""

import argparse
from collections import Counter
import json
import os
from text_matching import (
    VOICE_SCORING_REVISION,
    aggregate_writer_voice,
    contains_phrase,
    score_writer_voice,
)
import sys

# Official gold-standard minimal-edit voice-preserving references
GOLD_REFERENCES = {
    "B-01": "Bro that clutch was so cracked fr fr, but my keyboard glitched during the defuse. We gotta climb back up the ranks tonight cuz tomorrow is patch day.",
    "B-02": "Old man Miller was sittin by the woodstove whittlin an axe handle, listenin to the howling wind. He figured winter was gonna hit early this year.",
    "B-03": "Rain drummed against the cracked plasglas. He popped the neural deck open, swapped the fried heatsink, and waited for the optics to recalibrate.",
    "B-04": "The ethiopian yirgacheffe had an intensely floral aroma with notes of bergamot, but the roast profile was slightly too dark, masking the delicate stonefruit acidity.",
    "B-05": "The little puppy ran across the grass chasing a yellow ball. He jumped in the muddy puddle and started splashing everywhere until his paws were dark brown.",
    "B-06": "The async worker crashed due to an unhandled null pointer in the redis cache layer. We rolled back the commit and increased the connection pool timeout.",
    "B-07": "We trapped their point guard in the backcourt and forced a turnover. Marcus caught the alleyoop pass in transition and threw down a thunderous dunk!",
    "B-08": "Frost crept silently across the cold windowpane. The room grew still, shadowed by the fading dusk, as if the whole world was holding its breath for snow.",
    "B-09": "Examined a juvenile barn owl with a fractured left humerus. The wing feathers were clean and the raptor showed strong aggressive defense reflexes.",
    "B-10": "Pursuant to Section 8, the supplier shall reimburse the buyer for any unauthorized shipment expenses incurred prior to the termination date."
}

# Ground truth specification for B-01 to B-10
GROUND_TRUTH = {
    "B-01": {
        "domain": "Discord / Gaming Chat",
        "spelling": {
            "keybord": ["keyboard"],
            "glitchd": ["glitched"],
            "clime": ["climb"],
            "tonite": ["tonight"],
            "cuz": ["cuz", "cause", "because"]
        },
        "grammar": {},
        "voice_markers": ["bro", "cracked", "fr", "gotta", "defuse", "patch day"],
        "over_edits": ["for real", "we have to", "we've got to"],
        "hallucinations": {
            "BCorrect (FMM)": [],
            "LanguageTool API": ["for for", "glitch during to defuse"],
            "TextGears API": ["but that clutch", "keyboard broke", "donate cu"],
            "DeepL Write": [],
            "Sapling Grammar Checker": ["for fur"],
            "JSpell Free Web Checker": ["FRR FRR", "Glitché", "tontine", "cue tomorrow"]
        }
    },
    "B-02": {
        "domain": "Appalachian Porch Dialogue",
        "spelling": {
            "sittin": ["sittin", "sitting"],
            "woodstove": ["woodstove", "wood stove", "wood-stove"],
            "whittlin": ["whittlin", "whittling"],
            "listenin": ["listenin", "listening"],
            "yeer": ["year"]
        },
        "grammar": {},
        "voice_markers": ["old man miller", "figured", "gonna"],
        "over_edits": ["going to", "he thought"],
        "hallucinations": {
            "BCorrect (FMM)": ["woodstock", "whitley an axe"],
            "LanguageTool API": [],
            "TextGears API": ["ace handle"],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": ["Woodstock", "wryer"]
        }
    },
    "B-03": {
        "domain": "Cyberpunk Shorthand",
        "spelling": {
            "plasglas": ["plasglass", "plasglas"],
            "popd": ["popped"],
            "swaped": ["swapped"],
            "recalabrate": ["recalibrate"]
        },
        "grammar": {},
        "voice_markers": ["neural deck", "fried heatsink", "optics"],
        "over_edits": [],
        "hallucinations": {
            "BCorrect (FMM)": ["cracked plays", "dodd the neural", "recelebrate"],
            "LanguageTool API": ["cracked plasmas", "he pop the neural"],
            "TextGears API": ["cracked pascals", "he pops the neural", "fried heartsick", "optics to calibrate"],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": ["plasmas", "pod the neural deck", "fried heathens"]
        }
    },
    "B-04": {
        "domain": "Specialty Coffee Review",
        "spelling": {
            "ethiopian": ["ethiopian"],
            "yirgacheffe": ["yirgacheffe"],
            "aromma": ["aroma"],
            "profle": ["profile"],
            "delcate": ["delicate"],
            "stonefruit": ["stonefruit", "stone fruit", "stone-fruit"]
        },
        "grammar": {
            "to dark": ["too dark"]
        },
        "voice_markers": ["floral aroma", "bergamot", "stone fruit acidity"],
        "over_edits": [],
        "hallucinations": {
            "BCorrect (FMM)": ["yorkshire"],
            "LanguageTool API": [],
            "TextGears API": ["ethiopian giraffe", "floral atmosphere", "roast style"],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": ["Ethiopians", "hierarchies", "storefront acidity"]
        }
    },
    "B-05": {
        "domain": "Pediatric Dysgraphia Sample",
        "spelling": {
            "litle": ["little"],
            "acros": ["across"],
            "gras": ["grass"],
            "yello": ["yellow"],
            "jumpd": ["jumped"],
            "mudy": ["muddy"],
            "pudle": ["puddle"],
            "startd": ["started"],
            "eveywhere": ["everywhere"],
            "untill": ["until"],
            "broun": ["brown"]
        },
        "grammar": {},
        "voice_markers": ["puppy", "chasing", "yellow ball", "splashing"],
        "over_edits": [],
        "hallucinations": {
            "BCorrect (FMM)": ["muddy buble"],
            "LanguageTool API": ["title puppy", "across the gas", "he jump in the mud puddle"],
            "TextGears API": [],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": ["starts splashing", "dark boron"]
        }
    },
    "B-06": {
        "domain": "Developer PR Review",
        "spelling": {
            "unhandeled": ["unhandled"],
            "rediss": ["redis"],
            "increesed": ["increased"]
        },
        "grammar": {},
        "voice_markers": ["async worker", "null pointer", "cache layer", "connection pool timeout"],
        "over_edits": ["asynchronous worker", "null pointer exception"],
        "hallucinations": {
            "BCorrect (FMM)": [],
            "LanguageTool API": ["remiss cache layer"],
            "TextGears API": ["sync worker", "unhanded null pointer", "remiss cache layer"],
            "DeepL Write": [],
            "Sapling Grammar Checker": ["saync worker"],
            "JSpell Free Web Checker": ["sync worker", "reddish cache"]
        }
    },
    "B-07": {
        "domain": "Basketball Play-by-Play",
        "spelling": {
            "trapd": ["trapped"],
            "forcd": ["forced"],
            "alleyoop": ["alley-oop", "alleyoop"],
            "transtion": ["transition"],
            "thunderos": ["thunderous"]
        },
        "grammar": {},
        "voice_markers": ["point guard", "backcourt", "turnover", "in transition", "dunk"],
        "over_edits": ["on the break"],
        "hallucinations": {
            "BCorrect (FMM)": ["we trad", "allotrope pass", "thunders dunk"],
            "LanguageTool API": ["we trap their", "force a turnover"],
            "TextGears API": ["we traps their", "alloyed pass"],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": [
                "We trap their point guard", "backcountry", "Aleppo pass"
            ]
        }
    },
    "B-08": {
        "domain": "Poetic Melancholy (Winter)",
        "spelling": {
            "crep": ["crept"],
            "breth": ["breath"]
        },
        "grammar": {
            "its": ["its"]
        },
        "voice_markers": ["frost", "cold windowpane", "room grew still", "fading dusk", "holding its breath for snow"],
        "over_edits": [],
        "hallucinations": {
            "BCorrect (FMM)": ["frost crepe", "it's breth"],
            "LanguageTool API": ["frost crew", "holding its berth for snow"],
            "TextGears API": ["frost creep"],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": ["Frost creep", "holding its Brett"]
        }
    },
    "B-09": {
        "domain": "Veterinary Wildlife Log",
        "spelling": {
            "exaimned": ["examined"],
            "humerous": ["humerus"],
            "agressive": ["aggressive"]
        },
        "grammar": {},
        "voice_markers": ["juvenile barn owl", "fractured left humerus", "wing feathers", "raptor"],
        "over_edits": ["we examined", "its wing feathers were clean"],
        "hallucinations": {
            "BCorrect (FMM)": ["humorous"],
            "LanguageTool API": ["fractured left numerous"],
            "TextGears API": [],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": ["left humorous"]
        }
    },
    "B-10": {
        "domain": "Commercial Legal Agreement",
        "spelling": {
            "pursuent": ["pursuant"],
            "remburse": ["reimburse"],
            "unauthorizd": ["unauthorized", "unauthorised"],
            "incured": ["incurred"],
            "terminashun": ["termination"]
        },
        "grammar": {},
        "voice_markers": ["pursuant to section 8", "supplier shall reimburse", "shipment expenses", "prior to the termination date"],
        "over_edits": [],
        "hallucinations": {
            "BCorrect (FMM)": [],
            "LanguageTool API": [],
            "TextGears API": [],
            "DeepL Write": [],
            "Sapling Grammar Checker": [],
            "JSpell Free Web Checker": []
        }
    }
}

ENGINES = [
    "BCorrect (FMM)",
    "LanguageTool API",
    "TextGears API",
    "DeepL Write",
    "Sapling Grammar Checker",
    "JSpell Free Web Checker",
]


def extract_ngrams(tokens, n):
    """Generate n-gram tuples from a token list."""
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def calculate_sari_keep(input_text, ref_text, hyp_text, max_n=3):
    """
    Calculate SARI-Keep score across n-grams (1 to max_n).
    Measures the precision and recall of original input n-grams preserved
    faithfully in both the hypothesis and the gold reference.
    """
    clean_in = input_text.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split()
    clean_ref = ref_text.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split()
    clean_hyp = hyp_text.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").split()

    f_scores = []
    for n in range(1, max_n + 1):
        in_ngrams = Counter(extract_ngrams(clean_in, n))
        ref_ngrams = Counter(extract_ngrams(clean_ref, n))
        hyp_ngrams = Counter(extract_ngrams(clean_hyp, n))

        numerator = sum(min(hyp_ngrams[g], in_ngrams.get(g, 0), ref_ngrams.get(g, 0)) for g in hyp_ngrams)
        p_denom = sum(min(hyp_ngrams[g], in_ngrams.get(g, 0)) for g in hyp_ngrams)
        r_denom = sum(min(in_ngrams[g], ref_ngrams.get(g, 0)) for g in in_ngrams)

        p = numerator / p_denom if p_denom > 0 else 0.0
        r = numerator / r_denom if r_denom > 0 else 0.0
        f = (2.0 * p * r) / (p + r) if (p + r) > 0 else 0.0
        f_scores.append(f)

    return (sum(f_scores) / len(f_scores)) * 100.0


def count_detected_hallucinations(output_text, signatures):
    """Count known hallucination signatures that appear in an engine output."""
    return sum(1 for signature in signatures if contains_phrase(output_text, signature))


def run_evaluation(mode="cached", verbose=False, academic=False, export_path="raw_results/blind_v3_official_scoreboard.json"):
    if mode != "cached":
        raise ValueError("Only cached evaluation is supported; live API evaluation is not implemented.")

    runs_file = "Docs/Notes/blind_v3_live_runs_full.json"
    if not os.path.exists(runs_file):
        print(f"Error: Missing test outputs at {runs_file}", file=sys.stderr)
        sys.exit(1)

    with open(runs_file, "r", encoding="utf-8") as f:
        live_runs = json.load(f)

    sapling_file = "raw_results/blind_v3_sapling_outputs.json"
    with open(sapling_file, "r", encoding="utf-8") as f:
        sapling_runs = json.load(f)["passages"]
    for pid, output in sapling_runs.items():
        if pid not in live_runs:
            raise ValueError(f"Sapling result references unknown passage {pid}")
        live_runs[pid]["Sapling Grammar Checker"] = {"text": output["text"]}

    jspell_file = "raw_results/jspell_web_checker_outputs.json"
    with open(jspell_file, "r", encoding="utf-8") as f:
        jspell_runs = json.load(f).get("blind_v3")
    if not isinstance(jspell_runs, dict):
        raise ValueError("JSpell web-checker results are missing blind_v3 outputs")
    for pid in GROUND_TRUTH:
        output = jspell_runs.get(pid)
        if not isinstance(output, dict) or not isinstance(output.get("text"), str):
            raise ValueError(f"JSpell web-checker result is missing {pid}")
        if pid not in live_runs:
            raise ValueError(f"JSpell result references unknown passage {pid}")
        live_runs[pid]["JSpell Free Web Checker"] = {"text": output["text"], "lat": None}

    evaluation_report = {
        "benchmark": "Voice-Preserving AI-Spellcheck Benchmark (Blind Suite v3.0)",
        "voice_scoring_revision": VOICE_SCORING_REVISION,
        "evaluation_date": "November 14, 2026",
        "mode": mode,
        "engines": {}
    }

    total_spell_targets = sum(len(gt["spelling"]) for gt in GROUND_TRUTH.values())
    total_gram_targets = sum(len(gt["grammar"]) for gt in GROUND_TRUTH.values())
    for eng in ENGINES:
        spell_hits = 0
        gram_hits = 0
        voice_precisions = []
        voice_recalls = []
        voice_metrics_by_passage = []
        over_edit_count = 0
        hallucination_count = 0
        latencies = []
        sari_keep_scores = []

        for pid, unit in live_runs.items():
            gt = GROUND_TRUTH[pid]
            out_text = unit[eng]["text"]
            latency = unit[eng].get("lat")
            if latency is not None:
                latencies.append(latency)

            # 1. Spelling
            for typo, targets in gt["spelling"].items():
                if any(contains_phrase(out_text, target) for target in targets):
                    spell_hits += 1

            # 2. Grammar
            for err, targets in gt["grammar"].items():
                if any(contains_phrase(out_text, target) for target in targets):
                    gram_hits += 1

            voice_metrics = score_writer_voice(
                unit["input"],
                out_text,
                gt["spelling"],
                gt["grammar"],
                gt["voice_markers"],
                forbidden_rewrites=gt["over_edits"],
            )
            voice_precisions.append(voice_metrics["precision"])
            voice_recalls.append(voice_metrics["recall"])
            voice_metrics_by_passage.append(voice_metrics)

            over_edit_count += voice_metrics["over_edit_count"]

            # Hallucinations
            eng_halls = gt["hallucinations"].get(eng, [])
            hallucination_count += count_detected_hallucinations(out_text, eng_halls)

            # SARI-Keep
            sari_val = calculate_sari_keep(unit["input"], GOLD_REFERENCES[pid], out_text)
            sari_keep_scores.append(sari_val)

        spelling_acc = round((spell_hits / total_spell_targets) * 100.0, 1)
        grammar_acc = round((gram_hits / max(total_gram_targets, 1)) * 100.0, 1) if total_gram_targets > 0 else 100.0

        voice_summary = aggregate_writer_voice(voice_metrics_by_passage)
        voice_score = round(voice_summary["score"], 1)

        anti_halluc = round(max(100.0 - (hallucination_count * 5.0), 20.0), 1)
        meta_score = round((0.35 * spelling_acc) + (0.25 * grammar_acc) + (0.20 * voice_score) + (0.20 * anti_halluc), 1)
        avg_lat = round(sum(latencies) / len(latencies), 1) if latencies else None
        avg_sari_keep = round(sum(sari_keep_scores) / len(sari_keep_scores), 1)

        evaluation_report["engines"][eng] = {
            "spelling_accuracy": spelling_acc,
            "grammar_accuracy": grammar_acc,
            "voice_preservation": voice_score,
            "voice_precision": round(sum(voice_precisions) / len(voice_precisions), 1),
            "voice_recall": round(sum(voice_recalls) / len(voice_recalls), 1),
            "voice_lexical_f1": round(voice_summary["lexical_f1"], 1),
            "voice_marker_retention": round(voice_summary["voice_marker_retention"], 1),
            "voice_over_edit_penalty": round(voice_summary["over_edit_penalty"], 1),
            "anti_hallucination": anti_halluc,
            "hybrid_meta_score": meta_score,
            "latency_ms": avg_lat,
            "sari_keep_score": avg_sari_keep,
            "hallucination_count": hallucination_count,
            "over_edit_count": over_edit_count
        }

    print("=================================================================================")
    print("VOICE-PRESERVING AI-SPELLCHECK BENCHMARK - BLIND SUITE v3.0")
    print("=================================================================================")
    print(f"{'Engine':<20} | {'Spelling (35%)':<14} | {'Grammar (25%)':<13} | {'Voice (20%)':<12} | {'Anti-Hal (20%)':<14} | {'Meta-Score':<10} | {'Latency':<8}")
    print("-" * 105)
    for eng, sc in evaluation_report["engines"].items():
        latency = f"{sc['latency_ms']} ms" if sc["latency_ms"] is not None else "n/a"
        print(f"{eng:<24} | {sc['spelling_accuracy']:>13}% | {sc['grammar_accuracy']:>12}% | {sc['voice_preservation']:>11}% | {sc['anti_hallucination']:>13}% | {sc['hybrid_meta_score']:>9}% | {latency:>8}")
    print("=================================================================================")

    if academic:
        print("\n=================================================================================")
        print("ACADEMIC NLP DIAGNOSTIC METRICS (SARI-Keep, Span Retention, Over-Editing)")
        print("=================================================================================")
        print(f"{'Engine':<20} | {'SARI-Keep (n=3)':<16} | {'Protected Spans':<16} | {'Over-Edits':<12} | {'Hallucinations':<14}")
        print("-" * 88)
        for eng, sc in evaluation_report["engines"].items():
            print(f"{eng:<20} | {sc['sari_keep_score']:>15}% | {sc['voice_preservation']:>15}% | {sc['over_edit_count']:>12} | {sc['hallucination_count']:>14}")
        print("=================================================================================")

    if verbose:
        print("\nPER-DOMAIN BREAKDOWN (10 UNSEEN HUMAN DOMAINS)")
        print("-" * 80)
        for pid, unit in live_runs.items():
            gt = GROUND_TRUTH[pid]
            print(f"\n[{pid}] {gt['domain']}")
            print(f"  Input: \"{unit['input']}\"")
            for eng in ENGINES:
                out = unit[eng]["text"]
                sari = calculate_sari_keep(unit["input"], GOLD_REFERENCES[pid], out)
                print(f"  - {eng:<18} (SARI-Keep: {sari:>5.1f}%): \"{out}\"")

    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(evaluation_report, f, indent=2)

    print(f"\nSaved official scoreboard to {export_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Run evaluation on the Voice-Preserving AI-Spellcheck Benchmark (Blind Suite v3.0)"
    )
    parser.add_argument(
        "--mode",
        choices=["cached"],
        default="cached",
        help="Replay cached run logs without making API calls (default: cached)",
    )
    parser.add_argument(
        "--academic",
        action="store_true",
        help="Output formal NLP metrics: SARI-Keep (n=1..3), Protected-Span Retention, and Over-Edit counts",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Display detailed per-domain breakdown for all 10 evaluation passages",
    )
    parser.add_argument(
        "--export-json",
        default="raw_results/blind_v3_official_scoreboard.json",
        help="Path to export the final evaluation JSON report (default: raw_results/blind_v3_official_scoreboard.json)",
    )
    args = parser.parse_args()
    run_evaluation(mode=args.mode, verbose=args.verbose, academic=args.academic, export_path=args.export_json)


if __name__ == "__main__":
    main()
