"""Register raw source files into a source inventory CSV.

Usage:
    python scripts/register_sources.py \
        --source-dir literature_review/00_raw_sources \
        --output literature_review/01_process/<run_id>/01_source_inventory/source_inventory.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}


def make_source_id(path: Path, index: int) -> str:
    stem = path.stem.lower()
    parts = []
    for char in stem:
        if char.isalnum():
            parts.append(char)
        elif parts and parts[-1] != "_":
            parts.append("_")
    normalized = "".join(parts).strip("_")
    short = "_".join(normalized.split("_")[:5])
    return f"S{index:03d}_{short}"


def register_sources(source_dir: Path, output: Path) -> None:
    files = [
        path
        for path in sorted(source_dir.rglob("*"))
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_id",
                "file_name",
                "file_path",
                "document_type",
                "ingestion_status",
                "citation_status",
                "notes",
            ],
        )
        writer.writeheader()
        for index, path in enumerate(files, start=1):
            writer.writerow(
                {
                    "source_id": make_source_id(path, index),
                    "file_name": path.name,
                    "file_path": str(path),
                    "document_type": path.suffix.lower().lstrip("."),
                    "ingestion_status": "registered",
                    "citation_status": "needs_metadata_review",
                    "notes": "",
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    register_sources(Path(args.source_dir), Path(args.output))


if __name__ == "__main__":
    main()
