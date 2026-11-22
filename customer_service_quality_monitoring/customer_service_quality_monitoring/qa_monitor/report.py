"""Aggregation + output (console, CSV, HTML)."""
import csv
import html
from collections import defaultdict
from datetime import datetime


def agent_summary(results):
    by = defaultdict(list)
    for r in results:
        by[r["agent"]].append(r)
    rows = []
    for agent, rs in by.items():
        avg = round(sum(r["score"] for r in rs) / len(rs), 1)
        res = round(100 * sum(r["resolved"] == "Yes" for r in rs) / len(rs))
        rows.append({"agent": agent, "interactions": len(rs), "avg_score": avg, "resolution_rate": res,
                     "fails": sum(r["grade"] == "FAIL" for r in rs)})
    return sorted(rows, key=lambda x: -x["avg_score"])


def print_console(results, summary):
    print(f"\n{'ID':<6}{'Agent':<12}{'Channel':<8}{'Score':<7}{'Grade':<6}Issues")
    print("-" * 80)
    for r in results:
        print(f"{r['id']:<6}{r['agent']:<12}{r['channel']:<8}{r['score']:<7}{r['grade']:<6}{'; '.join(r['issues']) or '-'}")
    print(f"\n{'Agent':<12}{'Calls':<7}{'Avg Score':<11}{'Resolved %':<12}Fails")
    print("-" * 50)
    for s in summary:
        print(f"{s['agent']:<12}{s['interactions']:<7}{s['avg_score']:<11}{s['resolution_rate']:<12}{s['fails']}")
    overall = round(sum(r["score"] for r in results) / len(results), 1) if results else 0
    print(f"\nOverall average quality score: {overall}\n")


def write_csv(results, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "agent", "channel", "score", "grade", "sentiment", "resolved", "issues"])
        for r in results:
            w.writerow([r["id"], r["agent"], r["channel"], r["score"], r["grade"],
                        r["customer_sentiment"], r["resolved"], "; ".join(r["issues"])])


def write_html(results, summary, path):
    e = html.escape
    color = {"PASS": "#2e7d32", "WARN": "#ed6c02", "FAIL": "#c62828"}
    overall = round(sum(r["score"] for r in results) / len(results), 1) if results else 0
    agent_rows = "".join(
        f"<tr><td>{e(s['agent'])}</td><td>{s['interactions']}</td><td>{s['avg_score']}</td>"
        f"<td>{s['resolution_rate']}%</td><td>{s['fails']}</td></tr>" for s in summary)
    call_rows = "".join(
        f"<tr><td>{e(str(r['id']))}</td><td>{e(r['agent'])}</td><td>{e(r['channel'])}</td><td>{r['score']}</td>"
        f"<td style='color:{color[r['grade']]};font-weight:bold'>{r['grade']}</td>"
        f"<td>{e(r['customer_sentiment'])}</td><td>{e('; '.join(r['issues']) or '-')}</td></tr>" for r in results)
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Customer Service Quality Report</title>
<style>body{{font-family:Arial,sans-serif;margin:30px;background:#f5f6fa}}h1{{color:#1a237e}}
.card{{background:#fff;padding:16px 24px;border-radius:8px;display:inline-block;box-shadow:0 1px 4px #0002;margin-bottom:20px}}
.card b{{font-size:32px;color:#1a237e}}table{{border-collapse:collapse;width:100%;background:#fff;margin-bottom:30px}}
th,td{{padding:8px 12px;border-bottom:1px solid #ddd;text-align:left}}th{{background:#1a237e;color:#fff}}</style></head><body>
<h1>Customer Service Quality Report</h1><p>Generated {datetime.now():%Y-%m-%d %H:%M}</p>
<div class="card">Overall score<br><b>{overall}</b></div>
<div class="card">Interactions<br><b>{len(results)}</b></div>
<h2>Agent Performance</h2><table><tr><th>Agent</th><th>Interactions</th><th>Avg Score</th><th>Resolution</th><th>Fails</th></tr>{agent_rows}</table>
<h2>Interaction Details</h2><table><tr><th>ID</th><th>Agent</th><th>Channel</th><th>Score</th><th>Grade</th><th>Sentiment</th><th>Issues</th></tr>{call_rows}</table>
</body></html>"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
