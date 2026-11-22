# Customer Service Quality Monitoring

A simple, dependency-free Python project that scores customer-service interactions (chat/call transcripts)
against a quality checklist, and produces per-interaction and per-agent reports.

## What it checks (100 points)
| Criterion | Points | How |
|---|---|---|
| Greeting | 10 | Agent's first message has a greeting |
| Empathy | 15 | Apology / understanding phrases |
| Politeness | 15 | "please", "thank you", ... |
| Closing | 10 | Agent's last message offers more help / sign-off |
| Resolution | 20 | `resolved` column (partial credit for resolution wording) |
| Response time | 15 | First response <= 60s full marks, >= 300s zero |
| Customer sentiment | 15 | Sentiment of customer's last message |
| Profanity | -20 | Penalty for inappropriate agent language |

Grades: PASS >= 75, WARN >= 60, FAIL below. All weights/keywords live in `qa_monitor/config.py`.

## Run
```bash
python main.py                                  # uses data/sample_interactions.csv
python main.py --input my_data.csv --out reports
python -m unittest discover tests               # run tests
```
Outputs: console table, `reports/quality_scores.csv`, `reports/quality_report.html` (open in browser).

## Input CSV format
`id,agent,channel,first_response_sec,resolved,transcript`
Transcript turns are separated by `||`, each as `Agent: ...` or `Customer: ...`.

## Structure
```
main.py                 entry point
qa_monitor/config.py    weights, thresholds, keywords
qa_monitor/analyzer.py  transcript parsing + sentiment/keyword checks
qa_monitor/scorer.py    scoring + grading
qa_monitor/report.py    console/CSV/HTML output
data/                   sample data
tests/                  unit tests
```

## Ideas to extend
Swap the keyword sentiment for an ML model (e.g. VADER/transformers), add speech-to-text for call audio,
store results in SQLite, or build a Flask/Streamlit dashboard.
