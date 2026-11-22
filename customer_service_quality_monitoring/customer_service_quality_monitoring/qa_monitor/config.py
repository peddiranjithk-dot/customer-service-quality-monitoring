"""Scoring weights, thresholds and keyword lists. Edit these to tune the QA rules."""

# Max points per criterion (sum = 100)
WEIGHTS = {
    "greeting": 10,
    "empathy": 15,
    "politeness": 15,
    "closing": 10,
    "resolution": 20,
    "response_time": 15,
    "sentiment": 15,
}

PROFANITY_PENALTY = 20          # points removed if agent uses inappropriate language
FIRST_RESPONSE_TARGET_SEC = 60  # full marks if first reply is within this time
FIRST_RESPONSE_MAX_SEC = 300    # zero marks beyond this time

PASS_SCORE = 75                 # >= pass
WARN_SCORE = 60                 # >= warn (needs coaching), below = fail

GREETING_WORDS = ["hello", "hi ", "good morning", "good afternoon", "good evening", "welcome", "thank you for contacting", "thanks for calling"]
EMPATHY_WORDS = ["sorry", "apologize", "apologies", "understand", "i can imagine", "frustrating", "i appreciate your patience", "happy to help"]
POLITE_WORDS = ["please", "thank you", "thanks", "sure", "certainly", "happy to", "my pleasure", "glad to"]
CLOSING_WORDS = ["anything else", "is there anything", "have a great day", "have a nice day", "thank you for contacting", "thanks for contacting", "take care", "goodbye"]
RESOLUTION_WORDS = ["resolved", "fixed", "refund", "processed", "replaced", "done", "completed", "sorted", "taken care"]
PROFANITY = ["stupid", "idiot", "shut up", "dumb", "hell", "damn", "crap", "useless customer"]

POSITIVE_WORDS = ["thanks", "thank you", "great", "good", "perfect", "excellent", "awesome", "helpful", "happy", "love", "resolved", "works", "appreciate"]
NEGATIVE_WORDS = ["angry", "terrible", "worst", "bad", "awful", "horrible", "waste", "useless", "unacceptable", "disappointed", "frustrated", "never", "cancel", "complaint", "still not", "not working", "rude"]
