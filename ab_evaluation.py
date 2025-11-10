#!/usr/bin/env python3

import argparse
from pathlib import Path
import re
import glob
import sys

def parse_score_from_report(file_path: Path) -> tuple[float | None, dict[str, float]]:
    """
    Parses the total score and category scores from a benchmark report file.
    Returns: (total_score, category_scores_dict)
    """
    if not file_path.exists():
        return None, {}

    content = file_path.read_text()

    # Parse total score
    total_score = None
    match = re.search(r"Total Score:\s+([\d.]+)\/", content)
    if match:
        total_score = float(match.group(1))

    # Parse category scores
    category_scores = {}

    # Find the CATEGORY BREAKDOWN section
    category_section = re.search(
        r"CATEGORY BREAKDOWN\s*-+\s*(.*?)\s*(?:DIFFICULTY|=+)",
        content,
        re.DOTALL
    )

    if category_section:
        category_text = category_section.group(1)
        # Match lines like: "Basic Syntax          23.00/ 25 ( 92.0%) [5 tests]"
        category_matches = re.findall(
            r"([A-Za-z\s]+?)\s+(\d+\.?\d*)\/\s*(\d+)",
            category_text
        )

        for category_name, score, max_score in category_matches:
            category_name = category_name.strip()
            category_scores[category_name] = float(score)

    return total_score, category_scores

def get_average_score(directory: Path) -> tuple[float, list[float], int, dict[str, list[float]]]:
    """
    Finds all .txt files in a directory and calculates their average score.
    Returns: (average_score, list_of_scores, file_count, category_scores_by_category)
    """
    scores = []
    category_data = {}  # {category_name: [scores]}
    file_paths = glob.glob(str(directory / "*.txt"))

    if not file_paths:
        print(f"Warning: No .txt files found in directory: {directory}", file=sys.stderr)
        return 0.0, [], 0, {}

    for file_path in file_paths:
        total_score, category_scores = parse_score_from_report(Path(file_path))
        if total_score is not None:
            scores.append(total_score)

            # Collect category scores
            for category, score in category_scores.items():
                if category not in category_data:
                    category_data[category] = []
                category_data[category].append(score)

    if not scores:
        print(f"Warning: Could not parse any scores from files in: {directory}", file=sys.stderr)
        return 0.0, [], len(file_paths), {}

    return sum(scores) / len(scores), scores, len(file_paths), category_data

def compare_directories(dir1: Path, dir2: Path, dir1_label: str = "Directory 1", dir2_label: str = "Directory 2"):
    """
    Compares the average scores between two directories.
    """
    print("\n" + "=" * 80)
    print(f"A/B Test Comparison")
    print("=" * 80)

    # Calculate average scores
    avg_score_1, scores_1, count_1, categories_1 = get_average_score(dir1)
    avg_score_2, scores_2, count_2, categories_2 = get_average_score(dir2)

    # --- Report Results ---
    print(f"\n{dir1_label}: {dir1}")
    print(f"  Files analyzed: {count_1}")
    print(f"  Scores parsed: {len(scores_1)}")
    if scores_1:
        print(f"  Individual scores: {[f'{s:.2f}' for s in scores_1]}")
    print(f"  Average Score: {avg_score_1:.2f}")

    print(f"\n{dir2_label}: {dir2}")
    print(f"  Files analyzed: {count_2}")
    print(f"  Scores parsed: {len(scores_2)}")
    if scores_2:
        print(f"  Individual scores: {[f'{s:.2f}' for s in scores_2]}")
    print(f"  Average Score: {avg_score_2:.2f}")

    # --- Overall Comparison ---
    print("\n" + "=" * 80)
    print("OVERALL COMPARISON")
    print("=" * 80)

    if not scores_1 or not scores_2:
        print("Unable to compare: insufficient data")
        return

    # Treat dir2 as new version, dir1 as baseline
    difference = avg_score_2 - avg_score_1
    percentage_change = (difference / avg_score_1 * 100) if avg_score_1 != 0 else float('inf')

    if difference > 0:
        print(f"{dir2_label} is better by {difference:.2f} points ({percentage_change:+.2f}%)")
    elif difference < 0:
        print(f"{dir1_label} is better by {-difference:.2f} points ({percentage_change:+.2f}%)")
    else:
        print("No difference in average scores.")

    # --- Category Comparison ---
    print("\n" + "=" * 80)
    print("CATEGORY BREAKDOWN COMPARISON")
    print("=" * 80)

    # Get all unique categories
    all_categories = set(categories_1.keys()) | set(categories_2.keys())

    if not all_categories:
        print("No category data available for comparison")
        return

    # Calculate average scores per category
    category_averages_1 = {cat: sum(scores) / len(scores) for cat, scores in categories_1.items()}
    category_averages_2 = {cat: sum(scores) / len(scores) for cat, scores in categories_2.items()}

    # Print header
    print(f"\n{'Category':<25} {dir1_label[:15]:>15} {dir2_label[:15]:>15} {'Difference':>12} {'Change':>10}")
    print("-" * 80)

    # Sort categories alphabetically for consistent output
    for category in sorted(all_categories):
        avg_1 = category_averages_1.get(category, 0.0)
        avg_2 = category_averages_2.get(category, 0.0)
        # Treat dir2 as new version, dir1 as baseline
        diff = avg_2 - avg_1
        pct_change = (diff / avg_1 * 100) if avg_1 != 0 else 0.0

        # Determine indicator (positive diff means dir2 is better)
        if abs(diff) < 0.01:
            indicator = "="
        elif diff > 0:
            indicator = "✓"
        else:
            indicator = "✗"

        print(f"{category:<25} {avg_1:>15.2f} {avg_2:>15.2f} {diff:>11.2f} {pct_change:>9.2f}% {indicator}")

    print("=" * 80 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Compare average scores between two directories of benchmark reports."
    )
    parser.add_argument(
        "dir1",
        type=str,
        help="Path to the first directory"
    )
    parser.add_argument(
        "dir2",
        type=str,
        help="Path to the second directory"
    )
    parser.add_argument(
        "--label1",
        type=str,
        default="Directory 1",
        help="Label for the first directory (default: 'Directory 1')"
    )
    parser.add_argument(
        "--label2",
        type=str,
        default="Directory 2",
        help="Label for the second directory (default: 'Directory 2')"
    )

    args = parser.parse_args()

    dir1 = Path(args.dir1)
    dir2 = Path(args.dir2)

    if not dir1.exists() or not dir1.is_dir():
        print(f"Error: {dir1} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    if not dir2.exists() or not dir2.is_dir():
        print(f"Error: {dir2} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    compare_directories(dir1, dir2, args.label1, args.label2)

if __name__ == "__main__":
    main()
