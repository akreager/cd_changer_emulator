# Decisions

These are the decisions that shape how agents work on this project. The owner decides and the architect records. IDs are permanent.

| ID | Decision | Status | Outcome, or the architect's recommendation |
|---|---|---|---|
| D-1 | How to correct a published record | Open | **Recommended:** never touch the original. Publish a supplement, `{record}-S1.pdf` (e.g. `TL-KRC3006-01-P1-20260419-S1.pdf`), with the errata, the missing dispositions and the incidents, dated and initialed. List it under the original in both records tables. |
| D-2 | Revision and status scheme | Open | **Recommended:** letters for released revisions (A, B, C…), and "Draft" before the first release. Status is Draft, Released or Superseded. TP execution progress stays in the `docs/README.md` phase table. Every document gets a standard header block and a revision-history table. |
| D-3 | Authorship | Open | **Recommended:** every document gets Author "A. Kreager". If AI drafting is to be disclosed, add one generic line ("Drafted with AI assistance; reviewed by the author") with no model names. Log cells use the initials "AK". |
| D-4 | Lineage notes for legacy IDs | Open | **Recommended:** add a one-line "Supersedes:" entry to the headers of DN-01, DN-02, DN-03 and TP/TL-01. |
| D-5 | Where agent documents live | **Decided 2026-10-15** | In this repository: `AGENTS.md` at the root and the `.agents/` workspace. The copy of the document-control handoff in the owner's claude.ai Project is retired. |
| D-6 | Agent write access | Open | **Recommended:** branches and pull requests only, with the owner reviewing and merging. Until this is decided, [rules/git-workflow.md](rules/git-workflow.md) applies. |
| D-7 | `TL-KRC3006-02-01-20260401.odt` in `docs/records/` | Open | **Recommended:** export it to PDF, list it as TL-02's Phase 1 snapshot, and remove the ODT. Git history keeps the original. |
| D-8 | `assets/changer_pins.png`, a crop of the factory pin table | Open | **Recommended:** low priority. Keep it, or redraw it as a Markdown table. |
| D-9 | Test plan format | **Decided 2026-10-15** | Convert all three test plans to Markdown now (document control CP-1, skill [odt-to-markdown](skills/odt-to-markdown/SKILL.md)). Technical revisions follow as diffs. Test logs stay spreadsheets; their format is D-10. |
| D-10 | Test log format | **Decided 2026-10-15** | Flat ODF: `.fods` for the spreadsheet logs and `.fodt` for TL-02. Git stores and diffs these as text. Review changes as cell diffs ([rules/git-workflow.md](rules/git-workflow.md)), because LibreOffice renumbers styles on every save. Existing logs convert at their next change (backlog DC-20). |
| D-11 | When a live test log is committed | Open | So far the owner has held a log back until all of its phases are done, but `docs/README.md` says the working log stays live and builds up results phase by phase. **Recommended:** commit the `.fods` log when each phase completes, in the same pull request as that phase's PDF record. With cell diffs, each commit then shows exactly what the phase added. |
