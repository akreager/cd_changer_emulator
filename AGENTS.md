# AGENTS.md

These are instructions for AI agents working in this repository. People should start with [README.md](README.md).

## The project

This is an open-source (MIT) Raspberry Pi 5 HAT that emulates a Kenwood CD changer on the 13-pin mini DIN "O protocol" bus. With it, a KRC-3006 cassette head unit can play a FLAC library from its factory controls.

The project is documentation-first. `docs/` is the record of what is known, and anyone should be able to reproduce the work from this repo alone. The current phase is protocol reverse engineering under TP-KRC3006-01.

If anything in these agent files disagrees with `docs/`, `docs/` wins. Report the disagreement to the architect.

- Status and milestones: [README.md](README.md#project-status)
- Document register: [docs/README.md](docs/README.md)
- What's technically settled and what's still open: [.agents/context/technical-baseline.md](.agents/context/technical-baseline.md)

## Start here

1. Read this file and every file in [`.agents/rules/`](.agents/rules/). The rules apply to every agent.
2. If you were given a role, read its handoff in [`.agents/handoffs/`](.agents/handoffs/) and its backlog in [`.agents/backlog/`](.agents/backlog/).
3. Before you start a task, check the skills table below. If a skill matches, read its `SKILL.md` and follow it.
4. Check [`.agents/decisions.md`](.agents/decisions.md) before you assume how something should be done.

## Roles

| Role | Owns | Handoff |
|---|---|---|
| Owner (A. Kreager) | Bench work and results, approvals, merges to `main` | — |
| Architect | Technical direction, the technical content of test plans, design decisions, resolving conflicts between sources, and this agent workspace | — |
| Document control | The document system: register, revisions, records, cross-references, consistency | [document-control.md](.agents/handoffs/document-control.md) |

Every new role gets a handoff before it starts. Agents don't talk to each other directly. Put questions for another role in your pull request or report, and the owner relays them.

## Rules

This is a summary. The files in [`.agents/rules/`](.agents/rules/) are authoritative. If this summary and a rules file disagree, follow the rules file and say so in your report.

1. **Evidence or nothing.** Cite a source for every number, pin name, polarity, part value or behavior. If you can't, write `[TBD — source needed: <what>]`. Never fill a gap with a plausible value. ([evidence.md](.agents/rules/evidence.md))
2. **Surface conflicts; don't resolve them.** When the bench, the service manual and the documents disagree, record both sides and route the question to the architect. ([evidence.md](.agents/rules/evidence.md))
3. **Stay in your role.** Change only what your role owns, and flag everything else.
4. **Never push to `main`.** Work on a branch and open a pull request. Say exactly what you changed, what you checked and what you didn't. ([git-workflow.md](.agents/rules/git-workflow.md))
5. **Published records are immutable.** Never edit anything in `docs/records/`. ([documents.md](.agents/rules/documents.md))
6. **IP posture.** Use no service-manual text or figures beyond short factual items, never commit manuals or datasheets, and keep brand names off hardware silkscreen. ([ip-posture.md](.agents/rules/ip-posture.md))
7. **Formats.** Use Markdown wherever it fits. Test logs are flat ODF spreadsheets (`.fods`), reviewed as cell diffs. Never use Microsoft Office formats or tools. ([documents.md](.agents/rules/documents.md))
8. **Ask the owner first** before you delete or rename a file, change a document ID, create a new document, touch a published record, or change a pass/fail criterion.
9. **Write for a busy reviewer.** Be concise and technically precise. Lead with what changed and what needs a decision.

## Skills

| Skill | Use it when you're |
|---|---|
| [odt-to-markdown](.agents/skills/odt-to-markdown/SKILL.md) | Converting a test plan from `.odt` to Markdown without changing its content |
| [read-odf](.agents/skills/read-odf/SKILL.md) | Reading or diffing the cells of a `.fods` or `.ods` log, the text of an `.odt`, or a record PDF |
| [doc-audit](.agents/skills/doc-audit/SKILL.md) | Checking that registers, links and documents agree: before every change package, and at phase gates |
| [test-session-records](.agents/skills/test-session-records/SKILL.md) | Preparing for a bench session, or closing one out: logs, captures, records |

## Repository map

| Path | What's there |
|---|---|
| `docs/` | Test plans (TP), test logs (TL) and design notes (DN). `docs/records/` holds the published PDF records. |
| `captures/`, `diagrams/`, `docs/protocol/` | Logic analyzer captures, diagram sources and decoded protocol data |
| `hardware/kicad/` | Breakout board (complete) and emulator HAT (in progress) |
| `firmware/`, `software/` | ATtiny1616 firmware and Pi software (not started) |
| `reference/README.md` | Citation register. It holds links only, never hosted manuals. |
| `.agents/` | This workspace: rules, context, decisions, rulings, handoffs, backlogs and skills ([index](.agents/README.md)) |
| `scratch/` | The owner's working files. Git ignores it, so never rely on it for history. |

## Working with the repo

- Fetch single files from `raw.githubusercontent.com/akreager/cd_changer_emulator/main/<path>`, or clone. Avoid the GitHub API without authentication; it's rate-limited.
- `grep -n` with targeted keywords is the fastest way to find stale references in the long design notes.
- The owner's local working tree can be ahead of `main`. Ask before you describe work the repo doesn't show. Committed isn't the same as complete either: the HAT design is an initial-state commit that hasn't been reviewed ([technical baseline](.agents/context/technical-baseline.md)).
