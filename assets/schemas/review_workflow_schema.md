# Review Workflow Data Schema

This file documents the minimum tables required for a V1 review run.

## Required Tables

- `search_log.csv`
- `candidate_papers.csv`
- `selection_decisions.csv`
- `source_triage.csv`
- `source_inventory.csv`
- `reference_table.csv`
- `screening_table.csv`
- `extraction_table.csv`
- `coding_taxonomy.csv`
- `synthesis_matrix.csv`
- `citation_ledger.csv`

## Required Identifiers

- `source_id`: Stable ID for each ingested source.
- `extraction_id`: Stable ID for each extracted evidence item.
- `code_id`: Stable ID for each code.
- `claim_id`: Stable ID for each report claim.

## Traceability Rule

Every final-report literature claim should map:

`claim_id -> evidence_id -> source_id -> raw source`

Candidate records do not count as source evidence.

## Evidence States

- Candidate record: search/selection planning only; not citable.
- Registered source: document exists in project; not necessarily included.
- Included source: source passed triage/screening; available for extraction.
- Cited evidence: claim appears in extraction/synthesis/citation-ledger artifacts.

## Triage Rule

Before full-text extraction, classify sources as:

- `direct_fit`
- `transferable_method_fit`
- `background_only`
- `exclude`

Only `direct_fit` and selected `transferable_method_fit` sources should proceed to full-text extraction by default.

## Corpus Adequacy Rule

Before synthesis, assess whether the included-source set covers each approved review need or subquestion. If coverage is weak, run supplemental gap search or qualify the final output.
