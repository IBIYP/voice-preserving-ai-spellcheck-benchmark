import unittest

from text_matching import aggregate_writer_voice, contains_phrase, score_writer_voice


class ContainsPhraseTests(unittest.TestCase):
    def test_requires_word_boundaries(self):
        self.assertFalse(contains_phrase("You that concert was great", "yo"))
        self.assertFalse(contains_phrase("FRR FRR", "fr"))

    def test_matches_words_and_phrases_with_punctuation(self):
        self.assertTrue(contains_phrase("Straight fire, no cap!", "straight fire"))
        self.assertTrue(contains_phrase("They lost his tick.", "tick"))


class WriterVoiceScoreTests(unittest.TestCase):
    def test_correcting_an_annotated_typo_does_not_reduce_voice_score(self):
        source = "Yo, fr I ain't riding that damn olde bike; it is weird as hell."
        output = "Yo, fr I ain't riding that damn old bike; it is weird as hell."
        result = score_writer_voice(
            source,
            output,
            spelling_targets={"olde": ["old"]},
            voice_markers=["fr", "ain't", "damn", "weird as hell"],
        )
        self.assertEqual(result["score"], 100.0)

    def test_dialect_equivalent_is_preserved(self):
        result = score_writer_voice(
            "We been waiting, rockin slow.",
            "We been waiting, rocking slow.",
            voice_markers=["rockin"],
            dialect_equivalents={"rockin": ["rockin", "rocking"]},
        )
        self.assertEqual(result["score"], 100.0)

    def test_dialect_equivalent_spelling_is_preserved_outside_voice_markers(self):
        result = score_writer_voice(
            "The colour is bright; my freind called it red.",
            "The color is bright; my friend called it red.",
            spelling_targets={"freind": ["friend"]},
            dialect_equivalents={"colour": ["colour", "color"]},
        )
        self.assertEqual(result["score"], 100.0)

    def test_punctuation_change_does_not_break_marker_retention(self):
        result = score_writer_voice(
            "We ran the pick and roll, fr.",
            "We ran the pick-and-roll, fr.",
            voice_markers=["pick and roll", "fr"],
        )
        self.assertEqual(result["voice_marker_retention"], 100.0)

    def test_rewriting_profanity_and_idiomatic_phrasing_lowers_score(self):
        source = "Yo, fr I ain't riding that damn olde bike; it is weird as hell."
        output = "Hello, I will not ride that unsuitable bicycle; it is strange."
        result = score_writer_voice(
            source,
            output,
            spelling_targets={"olde": ["old"]},
            voice_markers=["fr", "ain't", "damn", "weird as hell"],
        )
        self.assertLess(result["score"], 70.0)

    def test_unprompted_additions_reduce_score(self):
        result = score_writer_voice(
            "Keep this weird phrase, fr.",
            "Keep this weird phrase, fr, in a polished corporate tone.",
            voice_markers=["weird phrase", "fr"],
        )
        self.assertLess(result["score"], 100.0)

    def test_explicit_over_edit_signatures_reduce_voice_score(self):
        source = "I ain't done yet, damn."
        output = "I ain't done yet, damn. Professional rewrite."
        baseline = score_writer_voice(source, output, voice_markers=["ain't", "damn"])
        flagged = score_writer_voice(
            source,
            output,
            voice_markers=["ain't", "damn"],
            forbidden_rewrites=["professional rewrite"],
        )
        self.assertEqual(flagged["over_edit_count"], 1)
        self.assertLess(
            aggregate_writer_voice([flagged])["score"],
            aggregate_writer_voice([baseline])["score"],
        )


if __name__ == "__main__":
    unittest.main()
