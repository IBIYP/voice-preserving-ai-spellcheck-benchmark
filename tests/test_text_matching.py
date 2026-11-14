import unittest

from text_matching import contains_phrase


class ContainsPhraseTests(unittest.TestCase):
    def test_requires_word_boundaries(self):
        self.assertFalse(contains_phrase("You that concert was great", "yo"))
        self.assertFalse(contains_phrase("FRR FRR", "fr"))

    def test_matches_words_and_phrases_with_punctuation(self):
        self.assertTrue(contains_phrase("Straight fire, no cap!", "straight fire"))
        self.assertTrue(contains_phrase("They lost his tick.", "tick"))


if __name__ == "__main__":
    unittest.main()
