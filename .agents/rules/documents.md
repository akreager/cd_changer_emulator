# Rule: documents

This is how the project's documents work. Every agent that writes or changes a document follows it. The document control agent owns the system and applies it in detail ([handoff](../handoffs/document-control.md)).

## IDs and types

- Document IDs have the form `TT-KRC3006-NN`. TT is TP (test plan), TL (test log) or DN (design note). NN is two digits, zero-padded.
- Numbers are never reused.
- Don't assign a new ID yourself; ask document control. A new type code needs the owner's approval.
- Older IDs still appear in old copies and in git history. Document control's handoff has the mapping to current IDs.

## Test plans, logs and records

- A TP defines what's tested and how. Its TL records the results. They share a number and are created together.
- The working TL in `docs/` stays live and accumulates results phase by phase.
- When a phase or unit completes, a PDF snapshot of the whole TL goes into `docs/records/`. It's named `{TL-ID}-{phase|unit}-{YYYYMMDD}` using the completion date, e.g. `TL-KRC3006-01-P1-20260419`.
- **Records are immutable.** Never edit, re-export or overwrite anything in `docs/records/`. Corrections go in a supplement; see decision D-1.

## Formats

- Use Markdown wherever it fits: design notes, READMEs, and test plans (decision D-9).
- Test logs stay `.ods` (TL-02 is an `.odt`), because they're forms filled in at the bench in LibreOffice.
- Edit ODF files in place, in LibreOffice or with surgical edits to `content.xml`. Never regenerate one from a script.
- Records are PDFs exported from LibreOffice.
- Diagrams follow TP-01 §2.3:

  | Diagram | Format |
  |---|---|
  | Timing | WaveDrom JSON |
  | State machines | Mermaid `stateDiagram-v2` |
  | Block diagrams | draw.io `.drawio.svg` |
  | Schematics | KiCad, with IEC 60617 symbols |

  Commit both the source and the rendered file.
- **Never use Microsoft Office formats** (.docx, .xlsx, .pptx).

## Registers

These must always agree with each other and with the files:

1. `docs/README.md`: the Document Register, TP-01 Phase Progress and Published Records. This is the master.
2. The root `README.md`: the Documentation table, the Completed Test Records table and the status sections.
3. Folder READMEs that carry status text (`hardware/kicad/*/README.md`).
4. `reference/README.md` (REF-NNN) and the root README's References list.

When a document changes, the registers change with it. Document control makes those changes. Other agents list the register updates their change needs in their pull request.

## Revisions

Until decision D-2 is made, keep each document's existing revision scheme. Add a revision-history row (Rev, Date, Author, Changes) for every change.

## Naming

- **Captures** are named `P[phase]_[description]_[NNN].sr`, each with a matching `.png` (TP-01 §6). Every capture appears in its phase's Capture File Log in the TL, and every log entry has a file.
- **Signals:** give the factory name first and the published alias second, e.g. "pin 4 ON (CH-CON)". Pin 6 is "D. GND", the digital ground.
- **Units** are always explicit and correct.
- **Dates** use ISO 8601.
- **Author** is "A. Kreager", and tester initials are "AK" (pending decision D-3).
