# Prompt: Source Intake Triage

Use this prompt before full-text extraction or source-card generation.

## Instruction

Classify each registered source using only title, abstract, metadata, and front matter. Do not use model memory. Do not infer details that are absent from the available text.

## Fit Classes

- `direct_fit`: The source directly addresses the review question.
- `transferable_method_fit`: The source is not directly about the topic but provides methods, workflow logic, safeguards, or concepts that can transfer.
- `background_only`: The source may provide context but should not drive synthesis.
- `exclude`: The source is not relevant enough for the current review.

## Required Output

Populate `source_triage.csv` with:

- source_id
- front_matter_available
- fit_class
- fit_rationale
- recommended_next_step
- metadata_priority
- requires_human_review
- reviewer_notes

## Rules

- Prefer uncertainty over overclaiming.
- Do not recommend full-text extraction for `exclude`.
- Do not recommend rich source cards for `background_only` unless the reviewer requests them.
- Mark domain-specific but methodologically useful sources as `transferable_method_fit`.

