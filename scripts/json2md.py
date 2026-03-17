"""Generate Markdown files from PCG JSON data.

Usage:
    uv run json2md.py [--year YEAR] [--all] [--output-dir DIR]

Examples:
    uv run json2md.py --year 2026          # Generate Markdown for a specific year
    uv run json2md.py --all                # Generate Markdown for all years
    uv run json2md.py --all --output-dir out  # Specify a custom output directory
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VERSIONS_DIR = Path(__file__).resolve().parent.parent / "versions"

# System value display names.
_SYSTEM_LABELS: dict[str, str] = {
    # 2025+ classification
    "minimal": "minimal",
    "facultatif": "facultatif",
    # 2023-2024 classification
    "condensed": "abrégé",
    "base": "base",
    "developed": "développé",
}


def _system_label(system: str) -> str:
    """Return a human-readable label for a system classification value."""
    return _SYSTEM_LABELS.get(system, system)


def _render_accounts(
    accounts: list[dict[str, Any]],
    depth: int = 0,
) -> list[str]:
    """Recursively render nested accounts as indented Markdown lines.

    Each account is rendered as:
        <indent>- **<number>** — <label> (*<system>*)

    Sub-accounts are indented one level deeper.
    """
    lines: list[str] = []
    indent = "  " * depth

    for acct in accounts:
        number = acct["number"]
        label = acct["label"]
        system = _system_label(acct["system"])

        lines.append(f"{indent}- **{number}** — {label} (*{system}*)")

        children = acct.get("accounts", [])
        if children:
            lines.extend(_render_accounts(children, depth + 1))

    return lines


def _render_diff(diff: dict[str, Any]) -> list[str]:
    """Render the diff section as Markdown."""
    lines: list[str] = []
    year_from = diff["from"]
    year_to = diff["to"]

    lines.append(f"## Différences {year_from} → {year_to}")
    lines.append("")

    # Added
    added: list[dict[str, Any]] = diff.get("added", [])
    lines.append(f"### Comptes ajoutés ({len(added)})")
    lines.append("")
    if added:
        for acct in added:
            system = _system_label(acct["system"])
            lines.append(
                f"- **{acct['number']}** — {acct['label']} (*{system}*)"
            )
    else:
        lines.append("Aucun.")
    lines.append("")

    # Removed
    removed: list[dict[str, Any]] = diff.get("removed", [])
    lines.append(f"### Comptes supprimés ({len(removed)})")
    lines.append("")
    if removed:
        for acct in removed:
            system = _system_label(acct["system"])
            lines.append(
                f"- **{acct['number']}** — {acct['label']} (*{system}*)"
            )
    else:
        lines.append("Aucun.")
    lines.append("")

    # Modified
    modified: list[dict[str, Any]] = diff.get("modified", [])
    lines.append(f"### Comptes modifiés ({len(modified)})")
    lines.append("")
    if modified:
        for acct in modified:
            parts: list[str] = []
            label_change = acct.get("label")
            system_change = acct.get("system")
            if label_change:
                parts.append(
                    f"libellé : « {label_change['from']} » → « {label_change['to']} »"
                )
            if system_change:
                parts.append(
                    f"système : *{_system_label(system_change['from'])}*"
                    f" → *{_system_label(system_change['to'])}*"
                )
            lines.append(f"- **{acct['number']}** — {' ; '.join(parts)}")
    else:
        lines.append("Aucun.")
    lines.append("")

    return lines


def convert_json_to_md(json_path: Path, md_path: Path) -> None:
    """Convert a PCG JSON file to a Markdown document."""
    data = json.loads(json_path.read_text(encoding="utf-8"))

    version: int = data["version"]
    nested: list[dict[str, Any]] = data["nested"]
    diff: dict[str, Any] | None = data.get("diff")

    flat: list[dict[str, Any]] = data["flat"]
    total = len(flat)

    lines: list[str] = []

    # Title
    lines.append(f"# Plan Comptable Général — {version}")
    lines.append("")
    lines.append(f"*{total} comptes*")
    lines.append("")

    # Accounts
    lines.append("## Plan des comptes")
    lines.append("")
    lines.extend(_render_accounts(nested))
    lines.append("")

    # Diff
    if diff:
        lines.extend(_render_diff(diff))

    md_path.write_text("\n".join(lines), encoding="utf-8")


def discover_jsons(year: str | None) -> list[Path]:
    """Find PCG JSON files in the versions directory, optionally filtered by year."""
    if year:
        year_dir = VERSIONS_DIR / year
        if not year_dir.is_dir():
            print(
                f"Error: no version directory found for year {year} at {year_dir}",
                file=sys.stderr,
            )
            sys.exit(1)
        return sorted(year_dir.glob("pcg_*.json"))

    # All years — exclude schema files.
    return sorted(
        p
        for p in VERSIONS_DIR.rglob("pcg_*.json")
        if not p.name.endswith(".schema.json")
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Markdown files from PCG JSON data.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--year", help="Year to process (e.g. 2026)")
    group.add_argument("--all", action="store_true", help="Process all years")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for Markdown files (default: same directory as source JSON)",
    )

    args = parser.parse_args()

    jsons = discover_jsons(args.year if not args.all else None)

    if not jsons:
        print("No JSON files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(jsons)} JSON file(s) to convert.\n")

    for json_path in jsons:
        if args.output_dir:
            out_dir = Path(args.output_dir)
            relative = json_path.relative_to(VERSIONS_DIR)
            md_path = out_dir / relative.with_suffix(".md")
        else:
            md_path = json_path.with_suffix(".md")

        md_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"  {json_path.relative_to(VERSIONS_DIR)} -> {md_path}")
        try:
            convert_json_to_md(json_path, md_path)
        except Exception as exc:
            print(f"    ERROR: {exc}", file=sys.stderr)
            continue

    print("\nDone.")


if __name__ == "__main__":
    main()
