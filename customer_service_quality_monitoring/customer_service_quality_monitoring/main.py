"""Run: python main.py [--input data/sample_interactions.csv] [--out reports]"""
import argparse
import csv
import os

from qa_monitor.scorer import score_interaction
from qa_monitor.report import agent_summary, print_console, write_csv, write_html


def main():
    p = argparse.ArgumentParser(description="Customer Service Quality Monitoring")
    p.add_argument("--input", default="data/sample_interactions.csv")
    p.add_argument("--out", default="reports")
    args = p.parse_args()

    with open(args.input, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    results = [score_interaction(r) for r in rows]
    summary = agent_summary(results)

    os.makedirs(args.out, exist_ok=True)
    print_console(results, summary)
    write_csv(results, os.path.join(args.out, "quality_scores.csv"))
    write_html(results, summary, os.path.join(args.out, "quality_report.html"))
    print(f"Reports saved in '{args.out}/' (quality_scores.csv, quality_report.html)")


if __name__ == "__main__":
    main()
