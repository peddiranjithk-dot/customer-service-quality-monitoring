import unittest
from qa_monitor.scorer import score_interaction, response_time_points
from qa_monitor.analyzer import parse_transcript, sentiment_score


class TestQA(unittest.TestCase):
    good = {"id": 1, "agent": "A", "channel": "chat", "first_response_sec": 10, "resolved": "yes",
            "transcript": "Agent: Hello welcome || Customer: help || Agent: I am sorry, please wait. Refund processed. || Customer: great thanks || Agent: Anything else? Have a nice day"}
    bad = {"id": 2, "agent": "B", "channel": "chat", "first_response_sec": 500, "resolved": "no",
           "transcript": "Agent: Yes? || Customer: terrible worst || Agent: don't be stupid || Customer: awful"}

    def test_parse(self):
        self.assertEqual(len(parse_transcript(self.good["transcript"])), 5)

    def test_good_scores_high(self):
        r = score_interaction(self.good)
        self.assertEqual(r["grade"], "PASS")

    def test_bad_scores_low_and_flags_profanity(self):
        r = score_interaction(self.bad)
        self.assertEqual(r["grade"], "FAIL")
        self.assertIn("INAPPROPRIATE LANGUAGE", r["issues"])

    def test_response_time(self):
        self.assertEqual(response_time_points(30), 15)
        self.assertEqual(response_time_points(999), 0)

    def test_sentiment(self):
        self.assertGreater(sentiment_score("great thanks"), 0)
        self.assertLess(sentiment_score("terrible awful"), 0)


if __name__ == "__main__":
    unittest.main()
