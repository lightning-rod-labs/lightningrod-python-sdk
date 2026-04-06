#!/usr/bin/env python3
"""
Plot AutoAgent optimization progress from results.tsv.

Usage:
    python evals/plot_progress.py                    # interactive plot
    python evals/plot_progress.py -o progress.png    # save to file

results.tsv format (tab-separated, appended by the meta-agent):
    experiment  avg_score  task_scores  status  description
    1           0.42       {...}        keep    added bias detection heuristic
    2           0.38       {...}        discard worse on positive tests
    3           0.51       {...}        keep    refined data source routing
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    sys.exit(1)


RESULTS_FILE = Path(__file__).parent / "results.tsv"


def load_results(path: Path) -> list[dict]:
    rows = []
    with open(path) as f:
        header = f.readline().strip().split("\t")
        for line in f:
            vals = line.strip().split("\t")
            if len(vals) < len(header):
                continue
            row = dict(zip(header, vals))
            row["experiment"] = int(row["experiment"])
            row["avg_score"] = float(row["avg_score"])
            if "task_scores" in row and row["task_scores"]:
                try:
                    row["task_scores"] = json.loads(row["task_scores"])
                except json.JSONDecodeError:
                    row["task_scores"] = {}
            rows.append(row)
    return rows


def plot(rows: list[dict], output: str | None = None):
    experiments = [r["experiment"] for r in rows]
    scores = [r["avg_score"] for r in rows]
    statuses = [r.get("status", "keep") for r in rows]

    # Compute running best
    running_best = []
    best = 0.0
    for s, status in zip(scores, statuses):
        if status == "keep":
            best = max(best, s)
        running_best.append(best)

    # Check if we have per-task scores for a breakdown subplot
    has_task_scores = any(
        isinstance(r.get("task_scores"), dict) and r["task_scores"]
        for r in rows
    )
    nrows = 2 if has_task_scores else 1
    fig, axes = plt.subplots(nrows, 1, figsize=(12, 5 * nrows),
                             sharex=True, squeeze=False)
    ax = axes[0, 0]

    # --- Top panel: aggregate score ---

    # Running best line
    ax.step(experiments, running_best, where="post", color="#2ecc71",
            linewidth=2.5, label="Running best", zorder=3)

    # Individual trials
    keep_x = [e for e, st in zip(experiments, statuses) if st == "keep"]
    keep_y = [s for s, st in zip(scores, statuses) if st == "keep"]
    disc_x = [e for e, st in zip(experiments, statuses) if st == "discard"]
    disc_y = [s for s, st in zip(scores, statuses) if st == "discard"]

    ax.scatter(keep_x, keep_y, color="#2ecc71", s=60, zorder=4,
               label="Kept", edgecolors="white", linewidth=0.5)
    ax.scatter(disc_x, disc_y, color="#e74c3c", s=40, zorder=4,
               label="Discarded", marker="x", linewidth=1.5)

    # Annotate kept experiments with descriptions
    for r in rows:
        if r.get("status") == "keep" and r.get("description"):
            ax.annotate(
                r["description"][:40],
                (r["experiment"], r["avg_score"]),
                textcoords="offset points", xytext=(8, 8),
                fontsize=7, color="#555", rotation=15,
            )

    ax.set_ylabel("Average Score", fontsize=12)
    ax.set_title("Lightningrod Assistant — AutoAgent Optimization Progress", fontsize=14)
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
    ax.set_ylim(0, 1.05)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.legend(loc="lower right")
    ax.grid(True, alpha=0.3)

    # --- Bottom panel: per-task breakdown ---

    if has_task_scores:
        ax2 = axes[1, 0]

        # Collect all task names across all rows
        all_tasks = sorted({
            t for r in rows
            if isinstance(r.get("task_scores"), dict)
            for t in r["task_scores"]
        })

        colors = plt.cm.Set2.colors  # type: ignore[attr-defined]
        for i, task in enumerate(all_tasks):
            task_exp = []
            task_vals = []
            for r in rows:
                ts = r.get("task_scores")
                if isinstance(ts, dict) and task in ts:
                    task_exp.append(r["experiment"])
                    task_vals.append(ts[task])
            color = colors[i % len(colors)]
            short_name = task.replace("positive-", "+").replace("bias-", "b:")
            ax2.plot(task_exp, task_vals, marker="o", markersize=4,
                     color=color, label=short_name, linewidth=1.2, alpha=0.8)

        ax2.set_xlabel("Experiment #", fontsize=12)
        ax2.set_ylabel("Task Score", fontsize=12)
        ax2.set_title("Per-Task Scores", fontsize=12)
        ax2.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
        ax2.set_ylim(0, 1.05)
        ax2.legend(loc="lower right", fontsize=7, ncol=2)
        ax2.grid(True, alpha=0.3)

    fig.tight_layout()

    if output:
        fig.savefig(output, dpi=150)
        print(f"Saved to {output}")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plot AutoAgent progress")
    parser.add_argument("-o", "--output", help="Save chart to file (e.g. progress.png)")
    parser.add_argument("-f", "--file", default=str(RESULTS_FILE),
                        help="Path to results.tsv")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"No results file at {path}. Run some experiments first.")
        sys.exit(1)

    rows = load_results(path)
    if not rows:
        print("No data rows in results.tsv")
        sys.exit(1)

    plot(rows, args.output)


if __name__ == "__main__":
    main()
