#!/usr/bin/env python3
"""Convert GameWith interactive map pin coordinates into Palworld map coordinates."""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO_ROOT / "sources" / "gamewith-pin-data-snippet.json"
DEFAULT_CALIBRATION = REPO_ROOT / "sources" / "gamewith-pin-calibration.json"


@dataclass(frozen=True)
class PinRecord:
    """A GameWith map pin entry."""

    pin_id: str
    pin_type: str
    map_id: str
    loc_x: float
    loc_y: float
    name: str | None


@dataclass(frozen=True)
class CalibrationPoint:
    """A control point linking a GameWith loc pair to in-game coordinates."""

    loc_x: float
    loc_y: float
    coord_x: float
    coord_y: float
    pin_id: str | None = None
    name: str | None = None


@dataclass(frozen=True)
class LinearTransform:
    """Affine transform coefficients for x/y axes."""

    slope_x: float
    intercept_x: float
    slope_y: float
    intercept_y: float

    def apply(self, pin: PinRecord) -> tuple[float, float]:
        x = self.slope_x * pin.loc_x + self.intercept_x
        y = self.slope_y * pin.loc_y + self.intercept_y
        return x, y


def load_pin_records(path: Path) -> list[PinRecord]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    pins: list[PinRecord] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        pin_id = entry.get("id")
        loc = entry.get("loc")
        if not isinstance(pin_id, str) or not isinstance(loc, list) or len(loc) != 2:
            continue
        try:
            loc_x = float(loc[0])
            loc_y = float(loc[1])
        except (TypeError, ValueError):
            continue
        pin_type = str(entry.get("type", ""))
        map_id = str(entry.get("mapId", ""))
        name_val = entry.get("name")
        name = str(name_val) if isinstance(name_val, str) and name_val else None
        pins.append(
            PinRecord(
                pin_id=pin_id,
                pin_type=pin_type,
                map_id=map_id,
                loc_x=loc_x,
                loc_y=loc_y,
                name=name,
            )
        )
    return pins


def load_calibration_points(path: Path) -> list[CalibrationPoint]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    points: list[CalibrationPoint] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        loc = entry.get("loc")
        coords = entry.get("coords")
        if not isinstance(loc, list) or len(loc) != 2:
            continue
        if not isinstance(coords, list) or len(coords) != 2:
            continue
        try:
            loc_x = float(loc[0])
            loc_y = float(loc[1])
            coord_x = float(coords[0])
            coord_y = float(coords[1])
        except (TypeError, ValueError):
            continue
        pin_id = entry.get("id")
        name_val = entry.get("name")
        name = str(name_val) if isinstance(name_val, str) and name_val else None
        pin_id_str = str(pin_id) if isinstance(pin_id, (str, int)) else None
        points.append(
            CalibrationPoint(
                loc_x=loc_x,
                loc_y=loc_y,
                coord_x=coord_x,
                coord_y=coord_y,
                pin_id=pin_id_str,
                name=name,
            )
        )
    if not points:
        raise ValueError(f"No calibration points found in {path}")
    return points


def _solve_axis_transform(samples: Iterable[tuple[float, float]]) -> tuple[float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for loc_value, coord_value in samples:
        xs.append(loc_value)
        ys.append(coord_value)
    if len(xs) < 2:
        raise ValueError("At least two calibration points are required per axis")
    n = float(len(xs))
    sum_x = sum(xs)
    sum_y = sum(ys)
    sum_xx = sum(value * value for value in xs)
    sum_xy = sum(value * value2 for value, value2 in zip(xs, ys))
    denominator = n * sum_xx - sum_x * sum_x
    if abs(denominator) < 1e-9:
        raise ValueError("Calibration points lead to a degenerate transform")
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


def solve_linear_transform(points: Sequence[CalibrationPoint]) -> LinearTransform:
    slope_x, intercept_x = _solve_axis_transform(
        (point.loc_x, point.coord_x) for point in points
    )
    slope_y, intercept_y = _solve_axis_transform(
        (point.loc_y, point.coord_y) for point in points
    )
    return LinearTransform(
        slope_x=slope_x,
        intercept_x=intercept_x,
        slope_y=slope_y,
        intercept_y=intercept_y,
    )


def format_markdown(pins: Sequence[PinRecord], transform: LinearTransform) -> str:
    lines = [
        "| id | type | name | map | loc_x | loc_y | coord_x | coord_y |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for pin in pins:
        coord_x, coord_y = transform.apply(pin)
        lines.append(
            "| {pid} | {ptype} | {name} | {map_id} | {loc_x:.6f} | {loc_y:.6f} | {coord_x:.2f} | {coord_y:.2f} |".format(
                pid=pin.pin_id,
                ptype=pin.pin_type or "?",
                name=(pin.name or "-"),
                map_id=pin.map_id or "-",
                loc_x=pin.loc_x,
                loc_y=pin.loc_y,
                coord_x=coord_x,
                coord_y=coord_y,
            )
        )
    return "\n".join(lines)


def format_csv(pins: Sequence[PinRecord], transform: LinearTransform) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "id",
            "type",
            "name",
            "map_id",
            "loc_x",
            "loc_y",
            "coord_x",
            "coord_y",
        ]
    )
    for pin in pins:
        coord_x, coord_y = transform.apply(pin)
        writer.writerow(
            [
                pin.pin_id,
                pin.pin_type,
                pin.name or "",
                pin.map_id,
                f"{pin.loc_x:.6f}",
                f"{pin.loc_y:.6f}",
                f"{coord_x:.2f}",
                f"{coord_y:.2f}",
            ]
        )
    return buffer.getvalue().rstrip("\n")


def format_text(pins: Sequence[PinRecord], transform: LinearTransform) -> str:
    lines = []
    for pin in pins:
        coord_x, coord_y = transform.apply(pin)
        label = pin.name or pin.pin_id
        lines.append(
            f"{label} ({pin.pin_type}) -> ({coord_x:.2f}, {coord_y:.2f}) from loc ({pin.loc_x:.6f}, {pin.loc_y:.6f})"
        )
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert GameWith map pin loc pairs into Palworld map coordinates using a linear transform."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to the GameWith pin JSON snippet (default: sources/gamewith-pin-data-snippet.json).",
    )
    parser.add_argument(
        "--calibration",
        type=Path,
        default=DEFAULT_CALIBRATION,
        help="Path to calibration point JSON (default: sources/gamewith-pin-calibration.json).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "csv"),
        default="markdown",
        help="Output format for converted coordinates.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output file path. When omitted the report is printed to stdout.",
    )
    parser.add_argument(
        "--map-id",
        dest="map_ids",
        action="append",
        help="Limit output to specific mapId values (can be used multiple times).",
    )
    parser.add_argument(
        "--type",
        dest="types",
        action="append",
        help="Limit output to pin types (e.g., fasttravel, captured).",
    )
    parser.add_argument(
        "--show-residuals",
        action="store_true",
        help="Print calibration residuals to stderr after solving the transform.",
    )
    return parser.parse_args(argv)


def filter_pins(
    pins: Sequence[PinRecord],
    *,
    map_ids: Sequence[str] | None,
    types: Sequence[str] | None,
) -> list[PinRecord]:
    results: list[PinRecord] = []
    allowed_maps = {item.lower() for item in map_ids} if map_ids else None
    allowed_types = {item.lower() for item in types} if types else None
    for pin in pins:
        if allowed_maps and pin.map_id.lower() not in allowed_maps:
            continue
        if allowed_types and pin.pin_type.lower() not in allowed_types:
            continue
        results.append(pin)
    return results


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    pins = load_pin_records(args.input)
    if args.map_ids or args.types:
        pins = filter_pins(pins, map_ids=args.map_ids, types=args.types)
    if not pins:
        raise SystemExit("No pins to process after applying filters.")
    calibration_points = load_calibration_points(args.calibration)
    transform = solve_linear_transform(calibration_points)
    if args.show_residuals:
        max_x_error = 0.0
        max_y_error = 0.0
        print("Calibration residuals:", file=sys.stderr)
        for point in calibration_points:
            predicted_x = transform.slope_x * point.loc_x + transform.intercept_x
            predicted_y = transform.slope_y * point.loc_y + transform.intercept_y
            delta_x = predicted_x - point.coord_x
            delta_y = predicted_y - point.coord_y
            max_x_error = max(max_x_error, abs(delta_x))
            max_y_error = max(max_y_error, abs(delta_y))
            print(
                "  id={id} loc=({lx:.6f},{ly:.6f}) -> expected=({cx:.2f},{cy:.2f}) "
                "delta=({dx:.3f},{dy:.3f})".format(
                    id=point.pin_id or "?",
                    lx=point.loc_x,
                    ly=point.loc_y,
                    cx=point.coord_x,
                    cy=point.coord_y,
                    dx=delta_x,
                    dy=delta_y,
                ),
                file=sys.stderr,
            )
        print(
            f"  max_abs_error=({max_x_error:.3f},{max_y_error:.3f})",
            file=sys.stderr,
        )
    if args.format == "csv":
        report = format_csv(pins, transform)
    elif args.format == "text":
        report = format_text(pins, transform)
    else:
        report = format_markdown(pins, transform)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        output_text = report if report.endswith("\n") else report + "\n"
        args.output.write_text(output_text, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
