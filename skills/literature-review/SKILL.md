---
name: literature-review
description: Use when the user wants to plan, run, draft, or audit a closed-evidence literature review using user-provided PDFs, documents, extracted text, source cards, review matrices, or citation ledgers.
---

# Literature Review

This skill helps Codex run a structured literature review from a closed, user-provided evidence base.

Use it when the user asks for a literature review, source triage, evidence extraction, thematic synthesis, APA-style report drafting, or citation auditing.

## Core Principle

Only user-provided, ingested sources may be cited as literature evidence.

General model knowledge may help with workflow, wording, structure, and methodological suggestions, but it must not be treated as citable literature evidence.

If a source is not present in the user's project, ask the user to provide it or label any related statement as outside the current evidence base.

## Plugin Assets

Resolve these paths relative to the plugin root:

- `assets/templates/`: Review protocols, matrices, source cards, and report templates.
- `assets/prompts/`: Step-specific prompt patterns.
- `assets/schemas/review_workflow_schema.md`: Minimum workflow tables and traceability rules.
- `scripts/`: Helper scripts for source registration, PDF extraction, matrix creation, and citation-ledger validation.

Prefer reusing these assets over inventing new table shapes or workflow stages.

## Target Project Structure

When starting a review in a user's project, create or use this local structure:

```text
literature_review/
  00_raw_sources/
  01_process/
    <run_id>/
      matrices/
      extracted_text/
      source_cards/
      working_notes/
  02_deliverables/
    <run_id>/
  03_knowledge_base/
    source_cards/
    review_summaries/
```

Use a stable run id such as `001_topic_slug`. If the project already has an established structure, follow it and avoid unnecessary reshaping.

## Workflow

### 1. Frame The Review

Clarify or draft:

- review purpose;
- guiding question and optional subquestions;
- intended audience;
- review type;
- output format;
- inclusion and exclusion criteria.

Human approval is required for the review question, review type, output format, and inclusion/exclusion criteria.

Use `assets/templates/review_protocol.md` and the framing prompt in `assets/prompts/review_framing.md` when useful.

### 2. Register Sources

Register user-provided PDFs or documents as the only citable source base.

Create or update:

- `source_inventory.csv`;
- `reference_table.csv`;
- `ingestion_log` or equivalent notes.

Use `scripts/register_sources.py` when it fits the project layout. Do not cite candidate records or search results unless the actual source document has been acquired and ingested.

### 3. Triage Sources

Before expensive full-text extraction, classify sources using front matter, metadata, abstract, and introduction when available.

Allowed `fit_class` values:

- `direct_fit`;
- `transferable_method_fit`;
- `background_only`;
- `exclude`.

Human approval is required for source triage classifications and metadata corrections.

Use `scripts/extract_pdf_front_matter.py`, `assets/templates/matrices/source_triage.csv`, and `assets/prompts/source_triage.md` when useful.

### 4. Assess Corpus Adequacy

Before synthesis, assess whether the included corpus covers each review question or subquestion.

If coverage is weak, recommend one of:

- supplemental gap search;
- narrowed scope;
- explicit limitation in the final deliverable.

Human approval is required for the corpus adequacy judgment and any supplemental search decision.

Use `assets/templates/corpus_adequacy_assessment.md` and `assets/prompts/corpus_adequacy.md`.

### 5. Extract Evidence

Extract only source-grounded evidence from included sources.

Populate `extraction_table.csv` with:

- stable `extraction_id`;
- `source_id`;
- page or location when available;
- evidence type;
- quotation, paraphrase, or interpretation status;
- supported claim;
- relevance to the review question;
- verification status.

Preserve the distinction between direct quotation, paraphrase, and synthesis interpretation.

Use `scripts/extract_pdf_text.py`, `assets/templates/matrices/extraction_table.csv`, and `assets/prompts/evidence_extraction.md`.

### 6. Code And Synthesize

Group extracted evidence into codes, themes, concepts, and argument families.

Create or update:

- `coding_taxonomy.csv`;
- `synthesis_matrix.csv`;
- gap analysis notes;
- argument outline.

Human approval is required for the coding taxonomy and final synthesis argument.

Use `assets/prompts/synthesis.md` and the matrix templates.

### 7. Draft The Report

Draft from verified artifacts, especially:

- extraction table;
- synthesis matrix;
- citation ledger;
- reference table.

Default report structure:

1. Executive Summary
2. Introduction and Review Purpose
3. Scope and Source Base
4. Review Method
5. Thematic or Conceptual Synthesis
6. Discussion
7. Gaps and Future Research
8. Conclusion
9. References
10. Appendix: Source Table or Review Matrix

Use APA-style in-text citations and generate references from the reference table, not memory.

Use `assets/templates/reports/final_report_chapter.md` and `assets/prompts/apa_report_writer.md`.

### 8. Audit Citations

Before presenting a final report as complete, validate that every substantive literature claim maps to an evidence record.

Required traceability:

```text
claim_id -> evidence_id -> source_id -> raw source
```

No final-report literature claim should appear unless it is represented in the citation ledger.

Use `scripts/validate_citation_ledger.py`, `assets/templates/matrices/citation_ledger.csv`, and `assets/prompts/citation_audit.md`.

### 9. Update Project Knowledge

After the review is complete, save compact reusable knowledge inside the target project, not inside the plugin:

- source cards;
- review run summary;
- durable project decisions;
- domain notes approved by the user.

Do not promote raw intermediate observations as reusable knowledge without user approval.

## Evidence States

Use these states consistently:

- Candidate record: search or selection planning only; not citable.
- Registered source: document exists in the project; not necessarily included.
- Included source: source passed triage or screening; available for extraction.
- Cited evidence: claim appears in extraction, synthesis, or citation-ledger artifacts.

## Human Review Gates

Pause for explicit approval when decisions materially shape the review:

- review question and output definition;
- review type;
- search strategy and stopping rules when source discovery is required;
- inclusion and exclusion criteria;
- source triage classification;
- corpus adequacy judgment;
- final included-source list;
- coding taxonomy;
- synthesis argument;
- final report chapter.

## Behavior Rules

- Keep review artifacts in the user's current project.
- Do not write project-specific sources, process traces, or deliverables back into the plugin.
- Use existing project conventions when they exist.
- Keep source cards lean; put detailed evidence in the extraction table.
- Label unsupported content as assumption, working hypothesis, methodological suggestion, or general process guidance.
- Refuse to invent citations.
- When a script does not fit the current project layout, adapt carefully and explain the local path assumptions.
