# Literature Review Codex Plugin

A Codex plugin for running closed-evidence literature reviews from user-provided sources.

The plugin helps with review planning, source registration, triage, corpus adequacy checks, evidence extraction, thematic synthesis, APA-style report drafting, and citation auditing.

## Core Evidence Rule

Only user-provided, ingested documents may be cited as literature evidence.

Codex may use general knowledge to help with workflow, structure, and writing quality, but it must not invent or cite literature claims from memory. Final-report claims should trace through:

```text
claim_id -> evidence_id -> source_id -> raw source
```

## What Is Included

```text
.codex-plugin/plugin.json
skills/literature-review/SKILL.md
scripts/
assets/
  prompts/
  schemas/
  templates/
examples/
```

## What Is Not Included

Review-specific evidence and outputs should live in the project where the review is being run, not inside this plugin.

The repository intentionally ignores:

```text
00_raw_sources/
01_process/
02_deliverables/
```

Those folders are useful during review work, but they should not be distributed as plugin logic.

## Install From GitHub

The recommended sharing model is:

1. Publish this repository to GitHub.
2. Clone it on another computer that has Codex installed.
3. Install or enable the plugin from that local clone using the Codex plugin interface available on that machine.

Example local setup:

```powershell
git clone https://github.com/<your-user-or-org>/literature-review-codex-plugin.git
cd literature-review-codex-plugin
```

If your Codex installation uses a local plugin marketplace, point the marketplace entry to this cloned folder or copy the repository into your local plugins directory.

## Usage

Open a separate review project and provide source files there, for example:

```text
my-review-project/
  literature_review/
    00_raw_sources/
      source-a.pdf
      source-b.pdf
```

Then ask Codex:

```text
Use the literature review plugin to run a structured narrative review from the PDFs in literature_review/00_raw_sources.
```

Other useful prompts:

```text
Use the literature review plugin to create the review protocol and source matrices for this topic.
```

```text
Use the literature review plugin to extract evidence from the included sources and build a synthesis matrix.
```

```text
Use the literature review plugin to audit this draft against the citation ledger.
```

## Workflow

1. Frame the review.
2. Register user-provided sources.
3. Triage source fit.
4. Assess corpus adequacy.
5. Extract evidence.
6. Code and synthesize.
7. Draft the APA-style report chapter.
8. Audit citation traceability.
9. Update project knowledge.

Human approval is required at major gates: review question, review type, inclusion criteria, source triage, corpus adequacy, coding taxonomy, synthesis argument, and final chapter.

## Version

Current version: `0.1.0`

This first version is intentionally practical and lightweight. It packages the operating model, templates, prompts, schemas, and helper scripts needed to run a structured narrative review with citation traceability.
