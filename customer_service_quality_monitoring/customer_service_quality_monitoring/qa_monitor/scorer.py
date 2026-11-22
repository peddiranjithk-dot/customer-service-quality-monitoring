"""Turns analysis results into a 0-100 quality score."""
from . import config as C
from .analyzer import parse_transcript, analyze, sentiment_label


def response_time_points(seconds: float) -> float:
    w = C.WEIGHTS["response_time"]
    if seconds <= C.FIRST_RESPONSE_TARGET_SEC:
        return w
    if seconds >= C.FIRST_RESPONSE_MAX_SEC:
        return 0
    span = C.FIRST_RESPONSE_MAX_SEC - C.FIRST_RESPONSE_TARGET_SEC
    return round(w * (1 - (seconds - C.FIRST_RESPONSE_TARGET_SEC) / span), 1)


def grade(score: float) -> str:
    return "PASS" if score >= C.PASS_SCORE else "WARN" if score >= C.WARN_SCORE else "FAIL"


def score_interaction(row: dict) -> dict:
    a = analyze(parse_transcript(row["transcript"]))
    W = C.WEIGHTS
    resolved = str(row.get("resolved", "")).strip().lower() in ("yes", "true", "1", "y")

    pts = {
        "greeting": W["greeting"] if a["greeting"] else 0,
        "empathy": W["empathy"] if a["empathy"] else 0,
        "politeness": W["politeness"] if a["politeness"] else 0,
        "closing": W["closing"] if a["closing"] else 0,
        "resolution": W["resolution"] if resolved else (W["resolution"] * 0.25 if a["resolution_language"] else 0),
        "response_time": response_time_points(float(row.get("first_response_sec") or 0)),
        # map ending sentiment (-1..1) to 0..weight
        "sentiment": round(W["sentiment"] * (a["ending_sentiment"] + 1) / 2, 1),
    }
    total = sum(pts.values())
    if a["profanity"]:
        total -= C.PROFANITY_PENALTY
    total = max(0, min(100, round(total, 1)))

    issues = []
    if not a["greeting"]: issues.append("No proper greeting")
    if not a["empathy"]: issues.append("No empathy shown")
    if not a["politeness"]: issues.append("Lacked polite language")
    if not a["closing"]: issues.append("No proper closing")
    if not resolved: issues.append("Issue not resolved")
    if pts["response_time"] < W["response_time"] * 0.5: issues.append("Slow first response")
    if a["profanity"]: issues.append("INAPPROPRIATE LANGUAGE")
    if a["ending_sentiment"] < -0.2: issues.append("Customer left unhappy")

    return {
        "id": row["id"], "agent": row["agent"], "channel": row.get("channel", ""),
        "score": total, "grade": grade(total),
        "customer_sentiment": sentiment_label(a["customer_sentiment"]),
        "resolved": "Yes" if resolved else "No",
        "first_response_sec": row.get("first_response_sec", ""),
        "breakdown": pts, "issues": issues,
    }
