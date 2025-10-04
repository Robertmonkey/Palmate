#!/usr/bin/env python3
"""Validate that critical guide datasets have not regressed."""

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, Tuple

BASELINE_PATH = Path(__file__).with_name("data_integrity_baseline.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the size of core Palmate datasets and optionally "
            "raise the stored baselines to the current snapshot."
        )
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=BASELINE_PATH,
        help="Path to the baseline JSON file (defaults to data_integrity_baseline.json next to this script).",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update the baseline file to match the current dataset metrics.",
    )
    return parser.parse_args()


def load_baseline(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Baseline file not found: {path}")
    return json.loads(path.read_text())


def count_lines(text: str) -> int:
    if not text:
        return 0
    lines = text.count("\n")
    if not text.endswith("\n"):
        lines += 1
    return lines


def follow_json_path(data: Any, path: Iterable[Any]) -> Any:
    value = data
    for part in path:
        if isinstance(value, dict):
            if part not in value:
                raise KeyError(f"Missing key '{part}' while navigating baseline json_path")
            value = value[part]
        elif isinstance(value, list) and isinstance(part, int):
            if not (0 <= part < len(value)):
                raise IndexError(f"List index {part} out of bounds while navigating baseline json_path")
            value = value[part]
        else:
            raise TypeError(
                "json_path traversal expected dict or list but encountered "
                f"{type(value).__name__} at segment '{part}'"
            )
    return value


def collect_metrics(file_path: Path, spec: Dict[str, Any]) -> Dict[str, Any]:
    text = file_path.read_text()
    metrics: Dict[str, Any] = {"line_count": count_lines(text)}
    if "json_path" in spec or "min_entry_count" in spec:
        data = json.loads(text)
        target = follow_json_path(data, spec.get("json_path", []))
        if isinstance(target, (list, dict)):
            metrics["entry_count"] = len(target)
        else:
            raise TypeError(
                f"json_path for {file_path} resolved to {type(target).__name__}; expected list or dict"
            )
    return metrics


def format_metric(metric: Tuple[str, Any]) -> str:
    key, value = metric
    return f"{key.replace('_', ' ')}={value}"


def verify_metrics(file_path: Path, spec: Dict[str, Any], metrics: Dict[str, Any]) -> Tuple[bool, str]:
    problems = []
    min_line_count = spec.get("min_line_count")
    if min_line_count is not None and metrics["line_count"] < min_line_count:
        problems.append(
            f"line count {metrics['line_count']} dropped below baseline {min_line_count}"
        )
    min_entry_count = spec.get("min_entry_count")
    if min_entry_count is not None:
        if "entry_count" not in metrics:
            problems.append("baseline requires entry_count but json_path did not resolve to a list/dict")
        elif metrics["entry_count"] < min_entry_count:
            problems.append(
                f"entry count {metrics['entry_count']} dropped below baseline {min_entry_count}"
            )
    summary = f"{file_path}: " + ", ".join(format_metric(item) for item in metrics.items())
    return (not problems, summary if not problems else summary + " -> " + "; ".join(problems))


def update_baseline(
    baseline: Dict[str, Any], file_path: Path, spec: Dict[str, Any], metrics: Dict[str, Any]
) -> None:
    current_min = spec.get("min_line_count", 0)
    if metrics["line_count"] > current_min:
        spec["min_line_count"] = metrics["line_count"]
    if "entry_count" in metrics:
        current_entry_min = spec.get("min_entry_count", 0)
        if metrics["entry_count"] > current_entry_min:
            spec["min_entry_count"] = metrics["entry_count"]
    baseline.setdefault("files", {})[str(file_path)] = spec


def main() -> int:
    args = parse_args()
    baseline = load_baseline(args.baseline)
    files_spec = baseline.get("files", {})
    all_ok = True
    updated_specs: Dict[str, Dict[str, Any]] = {}

    for relative_path, spec in files_spec.items():
        file_path = Path(relative_path)
        if not file_path.exists():
            print(f"Missing expected file: {relative_path}", file=sys.stderr)
            all_ok = False
            continue
        metrics = collect_metrics(file_path, spec)
        ok, message = verify_metrics(file_path, spec, metrics)
        print(message)
        if not ok:
            all_ok = False
        updated_specs[relative_path] = dict(spec)
        if args.update:
            update_baseline(baseline, Path(relative_path), updated_specs[relative_path], metrics)

    if args.update:
        args.baseline.write_text(json.dumps(baseline, indent=2))
        print(f"Baseline updated at {args.baseline}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
