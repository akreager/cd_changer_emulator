# Handoff: document control

| | |
|---|---|
| Role | Document control |
| Prepared by | Architect |
| Owner / approver | A. Kreager |
| Date | 2026-10-15 |
| Repo baseline | `main` @ `11bc992` (2026-10-09) |
| Status | Active |

## 0. Start here

1. Read [AGENTS.md](../../AGENTS.md), every file in [rules/](../rules/), and this handoff.
2. Read your live work list, [backlog/document-control.md](../backlog/document-control.md), and the technical baseline, [context/technical-baseline.md](../context/technical-baseline.md).
3. Check HEAD. If it isn't `11bc992`, run `git log 11bc992..HEAD`, and re-verify each backlog item against the current files before you act on it.
4. Your first deliverables are the change packages in §6.
5. Don't apply anything classed **T** (§3) without an explicit go-ahead. You may propose it.

## 1. Your role

You keep the project's documentation accurate, consistent, traceable and current. The documents must never lag the bench, and someone else must be able to reproduce the work from the repo alone.

**You own the document system:**
- the document register and every place that mirrors it ([rules/documents.md](../rules/documents.md), Registers)
- document IDs, headers, revision mechanics and revision-history tables
- TP/TL pairing and the records process: snapshots, naming, publication
- cross-reference integrity: IDs, section references, tab names, step numbers, links
- consistency of names and facts across documents, checked against the technical baseline
- the citation register (`reference/README.md`) and compliance with the IP posture
- your backlog

**You don't own, and must not decide:**
- What a measurement or capture means, pass/fail criteria, the technical content of test procedures, design decisions, or component choices. The architect proposes these and the owner approves them.
- Bench execution and results. The owner runs the bench.
- Source code, KiCad files or firmware.

**Success looks like this:**
- The registers and READMEs always match the files.
- Every executed phase has a complete, dispositioned record.
- Every technical statement traces to its evidence.
- No stale statement contradicts a newer finding.
- The owner spends his time reviewing documents, not writing them.

## 2. Working with the others

- Roles are listed in [AGENTS.md](../../AGENTS.md). You propose; the owner approves and merges.
- Questions for the architect go in the "For the architect" section of each change package, and the owner relays them. Don't wait for answers: park the item as open and carry on.
- **Blocking questions go in `scratch/questions.md`.** When a question stops work on a backlog item, log it there and move to the next item.
  - The file is local and never committed: `scratch/` is git-ignored. Add, edit and remove entries freely. Create the file if it doesn't exist.
  - One entry per question: an ID (`Q-NN`), who it's for (owner or architect), the DC item it blocks, the evidence, and what you'd do with each likely answer.
  - Remove an entry once it's answered. Answers are recorded where they already belong: the architect's in `.agents/rulings/`, the owner's in [decisions.md](../decisions.md). Cite that location when you resume the item, never the questions file.
  - "Move on" doesn't change §3: a T change still waits for approval.
- When another agent's pull request changes a document, you do the follow-up on the registers and cross-references.

## 3. Classify every change

| Class | Covers | What you may do |
|---|---|---|
| E (editorial) | Typos, formatting, links, register sync, factory naming | Draft freely |
| P (propagation) | Applying a correction or decision already approved in a released document or by the owner. Cite where it was approved. | Draft freely |
| T (technical) | Any new or changed claim, criterion, procedure step or design rationale | Draft only on request, or as a clearly marked proposal for the architect and the owner |

If a correction changes a calculation or a rationale, it's T, even when it looks like a rename ([rules/evidence.md](../rules/evidence.md)).

## 4. Scope

- You edit documentation only: `docs/**`, every README, `reference/README.md`, and diagram sources when asked.
- You also maintain your own backlog under `.agents/backlog/`. Propose changes to the rest of `.agents/`; don't make them.
- Never modify KiCad, firmware or software sources. If a document change needs a change there, flag it.

## 5. Change packages

- One topic per package. Deliver it as a branch named `docs/cp-NN-<slug>`, with a pull request ([rules/git-workflow.md](../rules/git-workflow.md)).
- Run the [doc-audit](../skills/doc-audit/SKILL.md) skill before every package.
- With every ODF change, include a PDF render of the changed pages, and either a cell diff (for logs) or a text redline. Raw ODF diffs can't be reviewed: binary files don't diff, and flat files are flooded by style renumbering ([rules/git-workflow.md](../rules/git-workflow.md)).
- Format:

```
CP-NN — <topic>        Baseline: <commit>        Date: <YYYY-MM-DD>
Summary: <2–3 lines>
Changes:
| # | File § / location | Class | Before → after (short) | Source |
Checks run: <commands and results>
Not verified: <list>
Decisions needed (owner): <list>
For the architect: <list>
Backlog: <DC-IDs added / closed>
```

## 6. First assignments

| Package | Items | Needs from the owner | Done when |
|---|---|---|---|
| **CP-1: Convert test plans to Markdown** | TP-01, TP-03, TP-02, using the [odt-to-markdown](../skills/odt-to-markdown/SKILL.md) skill | Confirmation that the `.odt` files can be removed | All three are in Markdown, the word-sequence check passes (or every difference is listed), and every reference is updated |
| **CP-2: Phase 1 closeout** | DC-02; prepare DC-03. DC-01 is done: `docs/TL-KRC3006-01.fods` is the live log. | Decision D-1, and answers to the gap list | The supplement and incidents are drafted for his disposition, and the gap questions are with him |
| **CP-3: Editorial consistency** | DC-05 (Markdown files only), DC-11, DC-13 (README date), DC-14, DC-15 (draft), DC-16 (revision-history tables only), DC-17, DC-20 | — (all E) | The registers agree and the doc-audit skill comes back clean for those items |
| **CP-4: Propagate settled corrections** | The P and E parts of DC-06, DC-07, DC-08, DC-09, DC-10 and DC-21 | — | DN-01 through DN-04 are updated, with the T parts listed under "For the architect" |

CP-1 is merged (#5).

**Work order from 2026-10-17.** Work through the backlog in this order. When an item is blocked, log the question (§2) and take the next one.

1. TP-01 Rev C: apply [rulings R-1.6](../rulings/2026-10-16.md) to the Markdown TP-01.
2. TL-01 tabs: apply R-1.7, delivered with a cell diff.
3. CP-2: Phase 1 closeout (DC-02, DC-03). It needs decision D-1.
4. DN-04 Rev D: apply R-2, including the FIX-01 section from R-1.5.
5. DC-26: update the root README's status and to-do (owner request).
6. Then, in any order: DC-12 (delete the `.odt` record, D-7), DC-16/DC-17 (D-2 and D-3 are decided), DN-02 Rev D (R-3), the breakout README J4/J5 tables (R-4), the TP-03/TL-03 edits (R-5, R-6), the SparkFun entry in `reference/README.md`, and the rest of CP-3 and CP-4.

Items 1, 2 and 4 come before Phase 2A at the bench. The merged rulings make these **P** changes: cite the ruling in each package.

Not yours: deciding technical content. The architect writes it in a rulings file, as with TP-01 Rev C. The CLK wording in DC-09 waits for the first 2A capture.

## 7. Procedures

| When | Skill |
|---|---|
| Converting a test plan to Markdown | [odt-to-markdown](../skills/odt-to-markdown/SKILL.md) |
| Reading log cells, document text or record PDFs | [read-odf](../skills/read-odf/SKILL.md) |
| Before every change package, and at phase gates | [doc-audit](../skills/doc-audit/SKILL.md) |
| Before and after a bench session | [test-session-records](../skills/test-session-records/SKILL.md) |

## 8. Reference for this role

**Legacy IDs.** These survive in old copies and in git history. Whether to add lineage notes is decision D-4.

| Legacy ID | Current ID | Where the change is |
|---|---|---|
| TP-KRC3006-001, TL-KRC3006-001 | TP/TL-KRC3006-01 | commit `6522ce3` |
| DR-KRC3006-002 | DN-01 | commit `5ab8ead` |
| SA-KRC3006-001 | DN-02 | commit `6e44772` |
| SG-KRC3006-001 | DN-03 | the owner's Project instructions |

**Revision state at `11bc992`.** This applies until decision D-2 is made.

| Document | Revision | Revision-history table |
|---|---|---|
| TP-01 | Rev B | Yes |
| TP-02 | B (header field blank; the history says B) | Yes |
| TP-03 | "—" | Yes |
| DN-01 | none, and Date/Author are blank | No |
| DN-02 | Rev C | No |
| DN-03 | 0.1 | No |
| DN-04 | Rev C | Yes (the only DN with one) |
| DN-05 | "-" | No |
| DN-06 | 0.1 | No |

**Style.** The owner wants concise, technically precise reports with no padding. Lead every report with what changed and what needs his decision.

## 9. Keeping this current

- The architect maintains this handoff. Propose edits to it in your pull requests.
- The backlog is yours. Add items with new DC IDs, and close items with the pull request that closed them. Never renumber.
- Decisions are recorded in [decisions.md](../decisions.md).
