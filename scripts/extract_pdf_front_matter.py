"""Extract PDF metadata and first pages from registered sources.

This script is intended for cheap source-intake triage before full-text
extraction.

Usage:
    python scripts/extract_pdf_front_matter.py \
        --inventory literature_review/01_process/<run_id>/01_source_inventory/source_inventory.csv \
        --output literature_review/01_process/<run_id>/01_source_inventory/pdf_front_matter.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from pypdf import PdfReader


def clean(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def resolve_source_path(inventory: Path, file_path: str) -> Path:
    candidate = Path(file_path)
    if candidate.is_absolute():
        return candidate
    return (inventory.parents[3] / candidate).resolve()


def read_front_matter(path: Path, pages: int, chars: int) -> dict[str, object]:
    reader = PdfReader(str(path))
    metadata = reader.metadata or {}
    first_pages = []
    for page in reader.pages[:pages]:
        try:
            first_pages.append(page.extract_text() or "")
        except Exception as exc:  # noqa: BLE001
            first_pages.append(f"[text extraction failed: {exc}]")
    return {
        "page_count": len(reader.pages),
        "metadata": {str(key): clean(value) for key, value in metadata.items()},
        "front_text": clean("\n".join(first_pages))[:chars],
    }


def extract_front_matter(inventory: Path, output: Path, pages: int, chars: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with inventory.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            record = {
                "source_id": row["source_id"],
                "file_name": row["file_name"],
                "file_path": row["file_path"],
            }
            try:
                path = resolve_source_path(inventory, row["file_path"])
                record.update(read_front_matter(path, pages, chars))
                record["extraction_status"] = "ok"
            except Exception as exc:  # noqa: BLE001
                record["extraction_status"] = "failed"
                record["error"] = str(exc)
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--pages", type=int, default=2)
    parser.add_argument("--chars", type=int, default=6000)
    args = parser.parse_args()
    extract_front_matter(Path(args.inventory), Path(args.output), args.pages, args.chars)


if __name__ == "__main__":
    main()
