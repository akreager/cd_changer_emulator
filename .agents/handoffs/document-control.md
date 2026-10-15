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
- With every ODF change, include a PDF render and a plain-text redline. The owner can't review a binary diff.
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
| **CP-2: Phase 1 closeout** | DC-01, DC-02; prepare DC-03 | His filled working ODS, answers to the gap list, and decision D-1 | The live TL-01 carries the Phase 1 results, the supplement and incidents are drafted for his disposition, and the gap questions are with him |
| **CP-3: Editorial consistency** | DC-05 (Markdown files only), DC-11, DC-13 (README date), DC-14, DC-15 (draft), DC-16 (revision-history tables only), DC-17 | — (all E) | The registers agree and the doc-audit skill comes back clean for those items |
| **CP-4: Propagate settled corrections** | The P and E parts of DC-06, DC-07, DC-08, DC-09 and DC-10 | — | DN-01 through DN-04 are updated, with the T parts listed under "For the architect" |

CP-1 and CP-2 don't depend on each other, and both have to be done before Phase 2A.

Not yours: the technical content of TP-01 Rev C, and the CLK wording in DC-09, which waits for the first 2A capture. The architect writes Rev C as a change list and applies it as a diff on top of the Markdown from CP-1.

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
