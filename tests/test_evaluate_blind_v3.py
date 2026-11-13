import unittest

from evaluate_blind_v3 import count_detected_hallucinations, run_evaluation


class CountDetectedHallucinationsTests(unittest.TestCase):
    def test_counts_only_signatures_present_in_output(self):
        signatures = ["incorrect substitution", "changed phrase", "missing phrase"]

        count = count_detected_hallucinations(
            "The output includes an Incorrect Substitution and a changed phrase.",
            signatures,
        )

        self.assertEqual(count, 2)

    def test_returns_zero_when_no_signatures_are_present(self):
        self.assertEqual(
            count_detected_hallucinations("A corrected output.", ["hallucination"]),
            0,
        )

    def test_live_mode_is_rejected_before_loading_cached_data(self):
        with self.assertRaisesRegex(ValueError, "live API evaluation is not implemented"):
            run_evaluation(mode="live")


if __name__ == "__main__":
    unittest.main()
