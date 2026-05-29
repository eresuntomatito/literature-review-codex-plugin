"""Extract full text from registered PDF sources.

Use this after triage, preferably only for included or high-value
transferable sources.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from pypdf import PdfReader


def safe_name(source_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", source_id)


def clean(text: str) -> str:
    return " ".join(text.split())


def resolve_source_path(inventory: Path, file_path: str) -> Path:
    candidate = Path(file_path)
    if candidate.is_absolute():
        return candidate
    return (inventory.parents[3] / candidate).resolve()


def wanted(row: dict[str, str], include_source_ids: set[str]) -> bool:
    return not include_source_ids or row["source_id"] in include_source_ids


def extract_pdf_text(inventory: Path, output_dir: Path, include_source_ids: set[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with inventory.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        if not wanted(row, include_source_ids):
            continue
        path = resolve_source_path(inventory, row["file_path"])
        if path.suffix.lower() != ".pdf":
            continue
        reader = PdfReader(str(path))
        out_path = output_dir / f"{safe_name(row['source_id'])}.txt"
        with out_path.open("w", encoding="utf-8") as out:
            out.write(f"source_id: {row['source_id']}\n")
            out.write(f"file_name: {row['file_name']}\n")
            out.write(f"page_count: {len(reader.pages)}\n\n")
            for index, page in enumerate(reader.pages, start=1):
                try:
                    text = clean(page.extract_text() or "")
                except Exception as exc:  # noqa: BLE001
                    text = f"[text extraction failed: {exc}]"
                out.write(f"\n\n--- page {index} ---\n{text}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--source-id",
        action="append",
        default=[],
        help="Optional source_id to extract. Repeat to extract multiple sources.",
    )
    args = parser.parse_args()
    extract_pdf_text(Path(args.inventory), Path(args.output_dir), set(args.source_id))


if __name__ == "__main__":
    main()

