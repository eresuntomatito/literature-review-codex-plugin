"""Copy empty review matrix templates into a review-run folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


MATRIX_TARGETS = {
    "search_log.csv": "00_search_selection/search_log.csv",
    "candidate_papers.csv": "00_search_selection/candidate_papers.csv",
    "selection_decisions.csv": "00_search_selection/selection_decisions.csv",
    "source_triage.csv": "00_triage/source_triage.csv",
    "source_inventory.csv": "01_source_inventory/source_inventory.csv",
    "reference_table.csv": "01_source_inventory/reference_table.csv",
    "screening_table.csv": "03_screening/screening_table.csv",
    "extraction_table.csv": "04_extraction/extraction_table.csv",
    "coding_taxonomy.csv": "05_coding/coding_taxonomy.csv",
    "synthesis_matrix.csv": "06_synthesis/synthesis_matrix.csv",
    "citation_ledger.csv": "06_synthesis/citation_ledger.csv",
}


def create_matrices(template_dir: Path, run_dir: Path, overwrite: bool) -> None:
    for template_name, relative_target in MATRIX_TARGETS.items():
        source = template_dir / template_name
        target = run_dir / relative_target
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not overwrite:
            continue
        shutil.copyfile(source, target)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template-dir", default="assets/templates/matrices")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    create_matrices(Path(args.template_dir), Path(args.run_dir), args.overwrite)


if __name__ == "__main__":
    main()
