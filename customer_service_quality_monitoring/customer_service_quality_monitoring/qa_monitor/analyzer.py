"""Parsing transcripts and simple rule-based text analysis."""
import re
from . import config as C


def parse_transcript(text: str):
    """Transcript format: 'Agent: hi || Customer: hello || Agent: ...' -> list of (speaker, message)."""
    turns = []
    for part in text.split("||"):
        part = part.strip()
        if ":" not in part:
            continue
        speaker, msg = part.split(":", 1)
        turns.append((speaker.strip().lower(), msg.strip()))
    return turns


def _contains_any(text: str, words) -> bool:
    text = " " + text.lower() + " "
    return any(w in text for w in words)


def count_hits(text: str, words) -> int:
    text = " " + text.lower() + " "
    return sum(text.count(w) for w in words)


def sentiment_score(text: str) -> float:
    """Returns -1.0 (very negative) to +1.0 (very positive)."""
    pos, neg = count_hits(text, C.POSITIVE_WORDS), count_hits(text, C.NEGATIVE_WORDS)
    total = pos + neg
    return 0.0 if total == 0 else round((pos - neg) / total, 2)


def sentiment_label(score: float) -> str:
    return "Positive" if score > 0.2 else "Negative" if score < -0.2 else "Neutral"


def analyze(turns):
    agent = " ".join(m for s, m in turns if s == "agent")
    customer = " ".join(m for s, m in turns if s == "customer")
    first_agent = next((m for s, m in turns if s == "agent"), "")
    last_agent = next((m for s, m in reversed(turns) if s == "agent"), "")
    cust_turns = [m for s, m in turns if s == "customer"]
    last_customer = cust_turns[-1] if cust_turns else ""
    return {
        "greeting": _contains_any(first_agent, C.GREETING_WORDS),
        "empathy": _contains_any(agent, C.EMPATHY_WORDS),
        "politeness": _contains_any(agent, C.POLITE_WORDS),
        "closing": _contains_any(last_agent, C.CLOSING_WORDS),
        "resolution_language": _contains_any(agent, C.RESOLUTION_WORDS),
        "profanity": any(re.search(r"\b" + re.escape(w) + r"\b", agent.lower()) for w in C.PROFANITY),
        "customer_sentiment": sentiment_score(customer),
        "ending_sentiment": sentiment_score(last_customer),
    }
