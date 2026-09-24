"""Create English presentation figures from the frozen main-v1.2 outputs.

This script is descriptive only. It does not call an API, alter source data, add
confidence intervals, or recompute an alternative specification.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "06_analysis/main_v1.2"
OUTPUT = ROOT / "07_figures/main_v1.2/presentation"
OUTPUT.mkdir(parents=True, exist_ok=True)

ARMS = ["S", "C0", "T1", "T2", "T3"]
ARM_COLORS = {
    "S": "#6B7280",
    "C0": "#4C78A8",
    "T1": "#72B7B2",
    "T2": "#F2A65A",
    "T3": "#E45756",
}
CATEGORY_COLORS = {
    0: "#4C78A8",
    25: "#72B7B2",
    50: "#F2CF5B",
    75: "#F58518",
    100: "#E45756",
}
INK = "#18212F"
MUTED = "#667085"
GRID = "#D9E1EA"
BACKGROUND = "#F8FAFC"


def read_csv(name):
    with (ANALYSIS / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 17,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.edgecolor": "#CBD5E1",
        "axes.linewidth": 0.8,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "savefig.facecolor": "white",
        "savefig.bbox": "tight",
    })


def finish(fig, name):
    fig.savefig(OUTPUT / f"{name}.png", dpi=300, bbox_inches="tight", pad_inches=0.18)
    fig.savefig(OUTPUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def subtitle(fig, text, y=0.93):
    fig.text(0.5, y, text, ha="center", color=MUTED, fontsize=10)


def rounded_box(ax, xy, width, height, title, body, color, title_size=13):
    x, y = xy
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        facecolor="white", edgecolor=color, linewidth=2,
    )
    ax.add_patch(box)
    ax.add_patch(FancyBboxPatch(
        (x, y + height - 0.12), width, 0.12,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        facecolor=color, edgecolor=color, linewidth=0,
    ))
    ax.text(x + width/2, y + height - 0.06, title, ha="center", va="center",
            color="white", fontsize=title_size, fontweight="bold")
    ax.text(x + width/2, y + (height - 0.12)/2, body, ha="center", va="center",
            fontsize=10, color=INK, linespacing=1.35)


def experimental_design_flow():
    fig, ax = plt.subplots(figsize=(13.5, 4.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.suptitle("Experimental Design and Analysis Flow", y=0.98)
    subtitle(fig, "One frozen, fully crossed LLM-agent experiment; Pilot data are excluded from main results", 0.91)
    boxes = [
        (0.025, "16 Fixed Personas", "4 binary dimensions\n2 × 2 × 2 × 2", "#4C78A8"),
        (0.225, "Five Response Arms", "S · C0 · T1 · T2 · T3\ncanonical wording", "#72B7B2"),
        (0.425, "80 Independent Cells", "fresh context per cell\nno response chaining", "#F2A65A"),
        (0.625, "Main Execution", "80/80 API successes\n79/80 valid parses", "#E07A5F"),
        (0.825, "Prespecified Analysis", "arm summaries + four\nadjacent paired contrasts", "#8B5CF6"),
    ]
    for x, title, body, color in boxes:
        rounded_box(ax, (x, 0.29), 0.15, 0.36, title, body, color, 11.5)
    for i in range(4):
        x1 = boxes[i][0] + 0.155; x2 = boxes[i+1][0] - 0.008
        ax.add_patch(FancyArrowPatch((x1, 0.47), (x2, 0.47), arrowstyle="-|>",
                                     mutation_scale=15, color="#94A3B8", linewidth=1.7))
    ax.text(0.5, 0.12, "Main run: main_20260904T160520Z_d93b455f  •  Zhipu GLM-4.7  •  temperature 0.2",
            ha="center", color=MUTED, fontsize=10)
    finish(fig, "01_experimental_design_flow")


def response_ladder():
    fig, ax = plt.subplots(figsize=(13.5, 6.2))
    ax.set_xlim(-0.25, 6.65); ax.set_ylim(-0.15, 4.85); ax.axis("off")
    fig.suptitle("Nested Crisis-Response Packages", y=0.98)
    subtitle(fig, "Each adjacent response arm adds one layer; S is organizational silence", 0.92)
    labels = [
        ("S", "Silence", "No official response"),
        ("C0", "Acknowledgment", "Minimal incident acknowledgment"),
        ("T1", "Reassurance", "+ generic reassurance"),
        ("T2", "Corrective Plan", "+ specific remediation plan"),
        ("T3", "Executed Action", "+ publicly verifiable on-chain action"),
    ]
    for i, (arm, title, body) in enumerate(labels):
        x, y = i * 1.28, i * 0.82
        box = FancyBboxPatch((x, y), 1.48, 0.72, boxstyle="round,pad=0.02,rounding_size=0.04",
                             facecolor=ARM_COLORS[arm], edgecolor="white", linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + 0.74, y + 0.48, f"{arm}  {title}", ha="center", va="center",
                color="white", fontweight="bold", fontsize=11)
        ax.text(x + 0.74, y + 0.20, body, ha="center", va="center",
                color="white", fontsize=8.2)
        if i < 4:
            ax.add_patch(FancyArrowPatch((x + 1.30, y + 0.72), (x + 1.58, y + 0.91),
                                         arrowstyle="-|>", mutation_scale=13,
                                         color="#94A3B8", linewidth=1.5))
    fig.text(0.5, 0.035,
             "Interpretation: package comparisons—not a clean one-dimensional manipulation of credibility",
             ha="center", color=MUTED, fontsize=9.5)
    finish(fig, "02_response_package_ladder")


def arm_means():
    rows = read_csv("arm_summary.csv")
    means = [float(row["mean_unstake_percentage"]) for row in rows]
    ns = [int(row["valid_n"]) for row in rows]
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    bars = ax.bar(ARMS, means, color=[ARM_COLORS[a] for a in ARMS], width=0.68)
    ax.set_title("Mean Unstaking Percentage by Response Arm", pad=22)
    ax.text(0.5, 1.01, "Canonical main run; valid arm-specific denominators",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)
    ax.set_ylabel("Mean unstaking percentage")
    ax.set_ylim(0, 30)
    ax.set_yticks(range(0, 31, 5), [f"{v}%" for v in range(0, 31, 5)])
    ax.grid(axis="y", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value, n in zip(bars, means, ns):
        ax.text(bar.get_x()+bar.get_width()/2, value+0.7, f"{value:.2f}%",
                ha="center", fontweight="bold", fontsize=11)
        ax.text(bar.get_x()+bar.get_width()/2, 0.7, f"n={n}", ha="center",
                color="white", fontsize=9, fontweight="bold")
    fig.text(0.5, 0.015, "S has one prespecified missing value (P11_S); no value was imputed.",
             ha="center", color=MUTED, fontsize=9)
    finish(fig, "03_mean_unstaking_by_arm")


def stacked_distribution():
    rows = read_csv("outcome_distribution.csv")
    data = {arm: {} for arm in ARMS}
    for row in rows:
        data[row["arm"]][int(row["category"])] = float(row["percentage_of_valid"])
    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    left = np.zeros(len(ARMS))
    for category in (0, 25, 50, 75, 100):
        values = np.array([data[arm][category] for arm in ARMS])
        bars = ax.barh(ARMS, values, left=left, color=CATEGORY_COLORS[category],
                       label=f"{category}%", height=0.62)
        for bar, value in zip(bars, values):
            if value >= 6:
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_y()+bar.get_height()/2,
                        f"{value:.1f}%", ha="center", va="center", color="white",
                        fontsize=9, fontweight="bold")
        left += values
    ax.invert_yaxis(); ax.set_xlim(0, 100)
    ax.set_xlabel("Share of valid responses")
    ax.set_title("Distribution of Unstaking Choices", pad=22)
    ax.text(0.5, 1.01, "100% stacked bars; 79 valid responses across five arms",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)
    ax.set_xticks(range(0, 101, 20), [f"{v}%" for v in range(0, 101, 20)])
    ax.grid(axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.14), frameon=False,
              title="Selected unstaking percentage")
    finish(fig, "04_stacked_outcome_distribution")


def persona_differences():
    rows = read_csv("paired_differences.csv")
    contrasts = ["C0-S", "T1-C0", "T2-T1", "T3-T2"]
    fig, axes = plt.subplots(1, 4, figsize=(14, 5.4), sharey=True)
    rng = np.random.default_rng(1209)
    for ax, contrast in zip(axes, contrasts):
        selected = [row for row in rows if row["contrast"] == contrast and row["included"] == "True"]
        values = np.array([float(row["difference_percentage_points"]) for row in selected])
        jitter = rng.uniform(-0.10, 0.10, len(values))
        ax.scatter(jitter, values, s=52, color="#4C78A8", alpha=0.78,
                   edgecolor="white", linewidth=0.7, zorder=3)
        mean = values.mean()
        ax.scatter([0], [mean], marker="D", s=90, color="#E45756", edgecolor="white",
                   linewidth=0.9, zorder=4, label="Mean")
        ax.axhline(0, color="#475569", linewidth=1, linestyle="--")
        ax.set_xlim(-0.3, 0.3); ax.set_xticks([])
        ax.set_title(contrast, fontsize=13, pad=10)
        ax.text(0, -46, f"n={len(values)}\nmean={mean:+.2f} pp", ha="center",
                color=MUTED, fontsize=9)
        ax.grid(axis="y", color=GRID, linewidth=0.7); ax.set_axisbelow(True)
        ax.spines[["top", "right", "bottom"]].set_visible(False)
    axes[0].set_ylabel("Persona-level difference (percentage points)")
    axes[0].set_ylim(-52, 30)
    fig.subplots_adjust(top=0.82)
    fig.suptitle("Persona-Level Adjacent-Arm Differences", y=0.985, fontsize=17, fontweight="bold")
    fig.text(0.5, 0.90, "Blue circles are fixed personas; red diamonds are contrast means",
             ha="center", color=MUTED, fontsize=10)
    finish(fig, "05_persona_paired_differences")


def contrast_summary():
    rows = read_csv("paired_contrast_summary.csv")
    labels = [row["contrast"] for row in rows]
    means = np.array([float(row["mean_difference"]) for row in rows])
    mins = np.array([float(row["minimum_difference"]) for row in rows])
    maxs = np.array([float(row["maximum_difference"]) for row in rows])
    pvals = [float(row["exact_two_sided_p_value"]) for row in rows]
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10.2, 5.8))
    ax.hlines(y, mins, maxs, color="#94A3B8", linewidth=5, alpha=0.75)
    ax.scatter(means, y, s=120, color=[ARM_COLORS[row["first_arm"]] for row in rows],
               edgecolor="white", linewidth=1.2, zorder=3)
    ax.axvline(0, color="#334155", linewidth=1.2, linestyle="--")
    for yi, mean, p in zip(y, means, pvals):
        ax.text(31, yi, f"mean {mean:+.2f} pp   p={p:.4f}", va="center", fontsize=10)
    ax.set_yticks(y, labels); ax.invert_yaxis(); ax.set_xlim(-30, 56)
    ax.set_xlabel("First arm minus second arm (percentage points)")
    ax.set_title("Prespecified Adjacent-Arm Paired Contrasts", pad=22)
    ax.text(0.5, 1.01, "Dot = mean; line = observed min–max (not a confidence interval)",
            transform=ax.transAxes, ha="center", color=MUTED, fontsize=10)
    ax.grid(axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    fig.text(0.5, 0.01, "Exact two-sided sign-flip p-values describe 16 fixed profiles, not a sampled human population.",
             ha="center", color=MUTED, fontsize=9)
    finish(fig, "06_paired_contrast_summary")


def quality_funnel():
    stages = ["Planned cells", "API responses", "Valid strict parses", "C0−S complete pairs"]
    values = [80, 80, 79, 15]
    colors = ["#4C78A8", "#72B7B2", "#F2A65A", "#8B5CF6"]
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.set_xlim(0, 100); ax.set_ylim(-0.7, 3.8); ax.axis("off")
    fig.suptitle("Main-Run Data Quality and Analysis Denominators", y=0.98)
    subtitle(fig, "The single malformed P11_S response remains missing; it is never coded as 0%", 0.91)
    max_width = 76
    for idx, (stage, value, color) in enumerate(zip(stages, values, colors)):
        width = max_width * (value / 80) if idx < 3 else max_width * (15 / 16)
        x = 50 - width/2; y = 2.75 - idx*0.82
        box = FancyBboxPatch((x, y), width, 0.58, boxstyle="round,pad=0.01,rounding_size=0.12",
                             facecolor=color, edgecolor="white")
        ax.add_patch(box)
        denominator = "/80" if idx < 3 else "/16 possible pairs"
        ax.text(50, y+0.29, f"{stage}: {value}{denominator}", ha="center", va="center",
                color="white", fontsize=12, fontweight="bold")
    ax.text(50, -0.35, "Other adjacent contrasts retain 16/16 complete persona pairs",
            ha="center", color=MUTED, fontsize=10)
    finish(fig, "07_data_quality_funnel")


def main():
    style()
    experimental_design_flow()
    response_ladder()
    arm_means()
    stacked_distribution()
    persona_differences()
    contrast_summary()
    quality_funnel()
    print(f"Created 7 English figures as PNG and SVG in {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
