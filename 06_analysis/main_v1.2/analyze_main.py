import csv
import itertools
import json
import statistics
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FIGURE_DIR = ROOT / "07_figures/main_v1.2"
DATA_PATH = ROOT / "05_processed_data/main_v1.2/main_v1.2_processed.csv"
INTEGRITY_PATH = ROOT / "05_processed_data/main_v1.2/integrity_report.json"
PLAN_PATH = ROOT / "00_protocol/main_run_plan_v1.2.md"
RUN_ID = "main_20260904T160520Z_d93b455f"
ARMS = ("S", "C0", "T1", "T2", "T3")
CATEGORIES = (0, 25, 50, 75, 100)
CONTRASTS = (("C0", "S"), ("T1", "C0"), ("T2", "T1"), ("T3", "T2"))


def read_data() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 80 or {row["run_id"] for row in rows} != {RUN_ID}:
        raise RuntimeError("Analysis input must be the single accepted 80-cell main run.")
    for row in rows:
        row["valid"] = row["outcome_status"] == "valid"
        row["value"] = int(row["unstake_percentage"]) if row["valid"] else None
        row["any_value"] = int(row["any_unstake"]) if row["valid"] else None
    return rows


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def exact_sign_flip(differences: list[int]) -> dict:
    n = len(differences)
    observed = abs(sum(differences) / n)
    assignments = 2 ** n
    numerator = 0
    for signs in itertools.product((-1, 1), repeat=n):
        statistic = abs(sum(sign * value for sign, value in zip(signs, differences)) / n)
        if statistic >= observed - 1e-12:
            numerator += 1
    return {
        "n": n,
        "observed_absolute_mean_difference": observed,
        "number_of_sign_assignments": assignments,
        "extreme_or_equal_assignments": numerator,
        "exact_two_sided_p_value": numerator / assignments,
        "equality_included": True,
        "zero_differences_included": True,
    }


def svg_start(title: str, width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">{title}</text>',
    ]


def distribution_svg(distributions: list[dict]) -> None:
    width, height = 820, 430
    lines = svg_start("Main-run outcome distribution by arm", width, height)
    left, top, plot_w, plot_h = 65, 55, 700, 300
    colors = {0: "#4C78A8", 25: "#72B7B2", 50: "#F2CF5B", 75: "#F58518", 100: "#E45756"}
    for tick in range(0, 17, 4):
        y = top + plot_h - tick / 16 * plot_h
        lines += [f'<line x1="{left}" y1="{y}" x2="{left+plot_w}" y2="{y}" stroke="#dddddd"/>',
                  f'<text x="{left-10}" y="{y+5}" text-anchor="end" font-family="Arial" font-size="12">{tick}</text>']
    by_arm = {arm: {row["category"]: row["count"] for row in distributions if row["arm"] == arm} for arm in ARMS}
    bar_w, gap = 22, 6
    group_w = len(CATEGORIES) * bar_w + (len(CATEGORIES)-1) * gap
    group_gap = (plot_w - len(ARMS) * group_w) / len(ARMS)
    for ai, arm in enumerate(ARMS):
        gx = left + group_gap/2 + ai * (group_w + group_gap)
        for ci, category in enumerate(CATEGORIES):
            count = by_arm[arm][category]
            h = count / 16 * plot_h
            x, y = gx + ci * (bar_w + gap), top + plot_h - h
            lines.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="{colors[category]}"/>')
        lines.append(f'<text x="{gx+group_w/2}" y="{top+plot_h+22}" text-anchor="middle" font-family="Arial" font-size="13">{arm}</text>')
    for ci, category in enumerate(CATEGORIES):
        x = 170 + ci * 105
        lines += [f'<rect x="{x}" y="390" width="13" height="13" fill="{colors[category]}"/>',
                  f'<text x="{x+18}" y="401" font-family="Arial" font-size="12">{category}%</text>']
    lines.append('</svg>')
    (FIGURE_DIR / "outcome_distribution_by_arm.svg").write_text("\n".join(lines), encoding="utf-8")


def paired_svg(contrast_rows: list[dict]) -> None:
    width, height = 760, 380
    lines = svg_start("Prespecified adjacent-arm paired differences", width, height)
    left, top, plot_w, plot_h = 100, 55, 590, 250
    xmin, xmax = -50, 50
    def x(value): return left + (value - xmin) / (xmax - xmin) * plot_w
    lines.append(f'<line x1="{x(0)}" y1="{top}" x2="{x(0)}" y2="{top+plot_h}" stroke="#333" stroke-dasharray="4 4"/>')
    for tick in (-50, -25, 0, 25, 50):
        lines += [f'<line x1="{x(tick)}" y1="{top+plot_h}" x2="{x(tick)}" y2="{top+plot_h+5}" stroke="#333"/>',
                  f'<text x="{x(tick)}" y="{top+plot_h+22}" text-anchor="middle" font-family="Arial" font-size="12">{tick}</text>']
    for i, row in enumerate(contrast_rows):
        y = top + 35 + i * 55
        lines += [f'<text x="{left-12}" y="{y+4}" text-anchor="end" font-family="Arial" font-size="13">{row["contrast"]}</text>',
                  f'<line x1="{x(row["minimum_difference"])}" y1="{y}" x2="{x(row["maximum_difference"])}" y2="{y}" stroke="#777" stroke-width="3"/>',
                  f'<circle cx="{x(row["mean_difference"])}" cy="{y}" r="6" fill="#E45756"/>']
    lines += [f'<text x="{left+plot_w/2}" y="350" text-anchor="middle" font-family="Arial" font-size="13">Percentage-point difference (line = observed min–max; dot = mean)</text>', '</svg>']
    (FIGURE_DIR / "paired_adjacent_differences.svg").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    integrity = json.loads(INTEGRITY_PATH.read_text(encoding="utf-8"))
    if integrity.get("result") != "PASS" or integrity.get("run_id") != RUN_ID:
        raise RuntimeError("Engineering acceptance must pass before analysis.")
    rows = read_data()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    arm_summary, distributions = [], []
    for arm in ARMS:
        arm_rows = [row for row in rows if row["condition"] == arm]
        values = [row["value"] for row in arm_rows if row["valid"]]
        any_values = [row["any_value"] for row in arm_rows if row["valid"]]
        arm_summary.append({
            "arm": arm, "planned_n": 16, "valid_n": len(values), "missing_n": 16-len(values),
            "mean_unstake_percentage": sum(values)/len(values),
            "median_unstake_percentage": statistics.median(values),
            "any_unstake_count": sum(any_values),
            "any_unstake_rate": sum(any_values)/len(any_values),
        })
        counts = Counter(values)
        for category in CATEGORIES:
            distributions.append({
                "arm": arm, "category": category, "count": counts[category],
                "percentage_of_valid": counts[category]/len(values)*100,
                "valid_denominator": len(values),
            })

    by_persona = {persona: {} for persona in sorted({row["persona_id"] for row in rows})}
    for row in rows:
        by_persona[row["persona_id"]][row["condition"]] = row["value"]
    matrix = [{"persona_id": persona, **{arm: by_persona[persona].get(arm) for arm in ARMS}} for persona in by_persona]

    difference_rows, contrast_summaries, permutation_results = [], [], []
    for first, second in CONTRASTS:
        label = f"{first}-{second}"
        differences, omitted = [], []
        for persona in by_persona:
            first_value, second_value = by_persona[persona].get(first), by_persona[persona].get(second)
            difference = first_value-second_value if first_value is not None and second_value is not None else None
            if difference is None:
                omitted.append(persona)
            else:
                differences.append(difference)
            difference_rows.append({
                "contrast": label, "persona_id": persona,
                "first_arm": first, "second_arm": second,
                "first_value": first_value, "second_value": second_value,
                "difference_percentage_points": difference,
                "included": difference is not None,
                "omission_reason": "one or both outcomes invalid/missing" if difference is None else "",
            })
        signs = Counter("negative" if d < 0 else "positive" if d > 0 else "zero" for d in differences)
        test = exact_sign_flip(differences)
        summary = {
            "contrast": label, "first_arm": first, "second_arm": second,
            "complete_pair_n": len(differences), "omitted_persona_ids": ";".join(omitted),
            "mean_difference": sum(differences)/len(differences),
            "median_difference": statistics.median(differences),
            "minimum_difference": min(differences), "maximum_difference": max(differences),
            "negative_count": signs["negative"], "zero_count": signs["zero"], "positive_count": signs["positive"],
            "negative_proportion": signs["negative"]/len(differences),
            "zero_proportion": signs["zero"]/len(differences),
            "positive_proportion": signs["positive"]/len(differences),
            "exact_two_sided_p_value": test["exact_two_sided_p_value"],
        }
        contrast_summaries.append(summary)
        permutation_results.append({"contrast": label, **test})

    write_csv(HERE / "arm_summary.csv", arm_summary, list(arm_summary[0]))
    write_csv(HERE / "outcome_distribution.csv", distributions, list(distributions[0]))
    write_csv(HERE / "persona_arm_outcomes.csv", matrix, ["persona_id", *ARMS])
    write_csv(HERE / "paired_differences.csv", difference_rows, list(difference_rows[0]))
    write_csv(HERE / "paired_contrast_summary.csv", contrast_summaries, list(contrast_summaries[0]))
    (HERE / "exact_sign_flip_results.json").write_text(json.dumps(permutation_results, indent=2)+"\n", encoding="utf-8")
    machine = {
        "analysis_status": "complete", "analysis_scope": "prespecified minimum scope",
        "run_id": RUN_ID, "pilot_data_included": False, "exploratory_analyses_included": False,
        "arm_summaries": arm_summary, "contrasts": contrast_summaries,
        "sign_flip_tests": permutation_results,
        "population_inference_warning": "Fixed persona profiles are not a random sample of real investors.",
    }
    (HERE / "results.json").write_text(json.dumps(machine, indent=2)+"\n", encoding="utf-8")
    distribution_svg(distributions)
    paired_svg(contrast_summaries)


if __name__ == "__main__":
    main()
