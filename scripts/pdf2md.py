"""Convert PCG source PDFs to Markdown.

Preserves bold/italic styling, detects headers from font sizes, keeps
internal links, and handles synthetic italic (shear-matrix text used
for facultative accounts).

Usage:
    uv run pdf2md.py [--year YEAR] [--all] [--output-dir DIR]

Examples:
    uv run pdf2md.py --year 2026          # Convert PDFs for a specific year
    uv run pdf2md.py --all                # Convert all PDFs across all years
    uv run pdf2md.py --all --output-dir out  # Specify a custom output directory
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import pymupdf

SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"

# Body text is 10 pt in these PDFs.  Anything above these thresholds
# is promoted to a Markdown heading.
_HEADING_THRESHOLDS: list[tuple[float, int]] = [
    # (min font size, heading level)
    (20.0, 1),  # Livre
    (14.0, 2),  # Title page items
    (12.0, 3),  # Chapitre
    (10.6, 4),  # Section / Sous-section (bold 10.6)
]

# Repetitive header / footer patterns.
_HEADER_RE = re.compile(
    r"^Version (?:du )?1er? janvier \d{4}\s*$",
)
_PAGE_NUMBER_RE = re.compile(
    r"^Page \d+ sur \d+\s*$",
)
_RECUEIL_HEADER_RE = re.compile(
    r"^RECUEIL DES NORMES COMPTABLES FRANÇAISES\s*$",
)
_RECUEIL_VERSION_RE = re.compile(
    r"^Version du 1er? janvier \d{4}\s*$",
)


def _is_header_or_footer(text: str) -> bool:
    """Return True if *text* matches a known repetitive header/footer."""
    return bool(
        _HEADER_RE.match(text)
        or _PAGE_NUMBER_RE.match(text)
        or _RECUEIL_HEADER_RE.match(text)
        or _RECUEIL_VERSION_RE.match(text)
    )


def _detect_sheared_lines(page: pymupdf.Page) -> list[bool]:
    """Detect which text lines use a synthetic italic (shear transform).

    Same algorithm as ``pdf2html._detect_sheared_lines``: comparing the
    first character's origin x with its bounding-box x0.  A difference
    greater than 0.5 pt indicates a shear.

    Returns one boolean per text line (in rawdict block/line order).
    """
    raw_blocks = page.get_text("rawdict")["blocks"]
    result: list[bool] = []

    for block in raw_blocks:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            is_sheared = False
            for span in line["spans"]:
                chars = span.get("chars")
                if not chars:
                    continue
                c0 = chars[0]
                if c0["origin"][0] - c0["bbox"][0] > 0.5:
                    is_sheared = True
                    break
            result.append(is_sheared)

    return result


def _heading_level(size: float) -> int | None:
    """Return the Markdown heading level for a given font *size*, or None."""
    for min_size, level in _HEADING_THRESHOLDS:
        if size >= min_size:
            return level
    return None


def _build_link_map(
    page: pymupdf.Page,
) -> list[tuple[pymupdf.Rect, str]]:
    """Build a list of (rect, href) for links on *page*."""
    result: list[tuple[pymupdf.Rect, str]] = []
    for link in page.get_links():
        kind = link.get("kind")
        rect = link.get("from")
        if rect is None:
            continue
        r = pymupdf.Rect(rect)

        if kind == pymupdf.LINK_GOTO:
            target_page = link.get("page", 0)
            result.append((r, f"#page-{target_page + 1}"))
        elif kind == pymupdf.LINK_URI:
            uri = link.get("uri", "")
            if uri:
                result.append((r, uri))
    return result


def _find_link_for_line(
    line_rect: tuple[float, float, float, float],
    link_map: list[tuple[pymupdf.Rect, str]],
) -> str | None:
    """Find a link whose rect overlaps with *line_rect*.

    Returns the href string or None.
    """
    lx0, ly0, lx1, ly1 = line_rect
    line_r = pymupdf.Rect(lx0, ly0, lx1, ly1)
    for rect, href in link_map:
        if rect.intersects(line_r):
            return href
    return None


def _wrap_style(text: str, *, bold: bool, italic: bool) -> str:
    """Wrap *text* with Markdown bold/italic markers."""
    if bold and italic:
        return f"***{text}***"
    if bold:
        return f"**{text}**"
    if italic:
        return f"*{text}*"
    return text


def _merge_styled_runs(
    runs: list[tuple[str, bool, bool]],
) -> str:
    """Merge consecutive runs sharing the same (bold, italic) style.

    Each *run* is ``(text, is_bold, is_italic)``.  Adjacent runs with
    identical style flags are concatenated before Markdown markers are
    applied, avoiding artefacts like ``**C****HAPITRE**``.
    """
    if not runs:
        return ""

    groups: list[tuple[str, bool, bool]] = []
    cur_text, cur_b, cur_i = runs[0]

    for text, b, i in runs[1:]:
        if b == cur_b and i == cur_i:
            cur_text += text
        else:
            groups.append((cur_text, cur_b, cur_i))
            cur_text, cur_b, cur_i = text, b, i
    groups.append((cur_text, cur_b, cur_i))

    parts: list[str] = []
    for text, bold, italic in groups:
        parts.append(_wrap_style(text, bold=bold, italic=italic))
    return "".join(parts)


def _process_page(
    page: pymupdf.Page,
    page_num: int,
) -> list[str]:
    """Extract Markdown lines from a single PDF page.

    Returns a list of Markdown strings (one per logical text line).
    """
    blocks = page.get_text("dict")["blocks"]
    sheared = _detect_sheared_lines(page)
    link_map = _build_link_map(page)

    lines: list[str] = []
    lines.append(f'<a id="page-{page_num + 1}"></a>')
    lines.append("")

    shear_idx = 0

    for block in blocks:
        if block["type"] != 0:  # skip images
            continue

        for line in block["lines"]:
            spans: list[dict[str, Any]] = line["spans"]

            # Determine if this line is synthetically italic.
            line_is_sheared = False
            if shear_idx < len(sheared):
                line_is_sheared = sheared[shear_idx]
                shear_idx += 1

            # Collect styled runs and determine dominant style.
            runs: list[tuple[str, bool, bool]] = []
            dominant_size = 0.0
            line_has_content = False

            for span in spans:
                text = span["text"]
                if not text.strip():
                    if text:
                        runs.append((text, False, False))
                    continue

                line_has_content = True
                flags = span["flags"]
                size = span["size"]
                is_bold = bool(flags & (1 << 4))
                is_italic = bool(flags & (1 << 1)) or line_is_sheared

                # Track the largest span for heading detection.
                if size > dominant_size:
                    dominant_size = size

                runs.append((text, is_bold, is_italic))

            if not line_has_content:
                continue

            joined = _merge_styled_runs(runs).strip()
            if not joined:
                continue

            # Skip headers/footers.
            plain = re.sub(r"[*]+", "", joined).strip()
            if _is_header_or_footer(plain):
                continue

            # Check if this line should be a heading.
            heading = _heading_level(dominant_size)
            if heading is not None:
                # Strip all bold/italic markers from heading text
                # (the # prefix is sufficient).
                heading_text = re.sub(r"\*+", "", joined).strip()
                joined = f"{'#' * heading} {heading_text}"
                # Ensure a blank line before headings.
                if lines and lines[-1] != "":
                    lines.append("")

            # Wrap in a link if one overlaps this line.
            href = _find_link_for_line(line["bbox"], link_map)
            if href and heading is None:
                joined = f"[{joined}]({href})"

            lines.append(joined)

    return lines


def _collapse_blank_lines(text: str) -> str:
    """Collapse runs of 3+ blank lines down to 2."""
    return re.sub(r"\n{3,}", "\n\n", text)


def convert_pdf_to_md(pdf_path: Path, md_path: Path) -> None:
    """Convert a single PDF file to Markdown.

    Preserves bold/italic styling, headers (detected from font size),
    internal links, and synthetic italic (shear-matrix text).
    """
    doc = pymupdf.open(pdf_path)

    all_lines: list[str] = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_lines = _process_page(page, page_num)
        all_lines.extend(page_lines)
        all_lines.append("")

    doc.close()

    output = "\n".join(all_lines)
    output = _collapse_blank_lines(output)
    output = output.strip() + "\n"

    md_path.write_text(output, encoding="utf-8")


def discover_pdfs(year: str | None) -> list[Path]:
    """Find PDF files in the sources directory, optionally filtered by year."""
    if year:
        year_dir = SOURCES_DIR / year
        if not year_dir.is_dir():
            print(
                f"Error: no source directory found for year {year} at {year_dir}",
                file=sys.stderr,
            )
            sys.exit(1)
        return sorted(year_dir.glob("*.pdf"))

    # All years
    return sorted(SOURCES_DIR.rglob("*.pdf"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PCG source PDFs to Markdown.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--year", help="Year to process (e.g. 2026)")
    group.add_argument("--all", action="store_true", help="Process all years")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for Markdown files (default: same directory as source PDF)",
    )

    args = parser.parse_args()

    pdfs = discover_pdfs(args.year if not args.all else None)

    if not pdfs:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(pdfs)} PDF(s) to convert.\n")

    for pdf_path in pdfs:
        if args.output_dir:
            out_dir = Path(args.output_dir)
            relative = pdf_path.relative_to(SOURCES_DIR)
            md_path = out_dir / relative.with_suffix(".md")
        else:
            md_path = pdf_path.with_suffix(".md")

        md_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"  {pdf_path.relative_to(SOURCES_DIR)} -> {md_path}")
        try:
            convert_pdf_to_md(pdf_path, md_path)
        except Exception as exc:
            print(f"    ERROR: {exc}", file=sys.stderr)
            continue

    print("\nDone.")


if __name__ == "__main__":
    main()
