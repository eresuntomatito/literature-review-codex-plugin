"""Validate that citation ledger rows have source and evidence links."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REQUIRED_FIELDS = ["claim_id", "claim_text", "source_id", "evidence_id"]


def validate(path: Path) -> int:
    if not path.exists():
        print(f"Missing citation ledger: {path}")
        return 1
    failures = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing_columns = [field for field in REQUIRED_FIELDS if field not in (reader.fieldnames or [])]
        if missing_columns:
            print(f"Missing required columns: {', '.join(missing_columns)}")
            return 1
        for row_number, row in enumerate(reader, start=2):
            missing = [field for field in REQUIRED_FIELDS if not row.get(field, "").strip()]
            if missing:
                failures += 1
                print(f"Row {row_number} missing: {', '.join(missing)}")
    if failures:
        print(f"Citation ledger validation failed with {failures} incomplete rows.")
        return 1
    print("Citation ledger validation passed.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("citation_ledger")
    args = parser.parse_args()
    raise SystemExit(validate(Path(args.citation_ledger)))


if __name__ == "__main__":
    main()

