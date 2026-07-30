# KRC-3006 CD Changer Emulator — Documentation Index

This folder contains all project documentation for the KRC-3006 reverse engineering and CD changer emulator project.

---

## File Format

There is no mandated document format. **Markdown (`.md`) is preferred wherever it fits** — such as the design notes and this README — so documents render directly on GitHub. Table- and form-heavy documents like the test plans and logs are currently kept in Open Document Format (`.odt` / `.ods`) and open in LibreOffice or any compatible editor, but any format may be used where it serves the document best.

Formats currently in use:
- Markdown (`.md`) — design notes and READMEs
- Open Document Format (`.odt` / `.ods`) — test plans and logs
- Timing diagrams (WaveDrom `.json`)
- State machine diagrams (Mermaid `.mmd`)

---

## Naming Convention

Documents follow this structure:

```
TT-KRC3006-NN
```

| Field | Description |
|---|---|
| `TT` | Two-letter document type code (see below) |
| `KRC3006` | Project identifier — fixed for all documents in this project |
| `NN` | Two-digit sequence number, zero-padded (01, 02, 03 …) |

### Document Type Codes

| Code | Type | Description |
|---|---|---|
| `TP` | Test Plan | Defines test objectives, scope, phases, pass/fail criteria, and procedure for a body of testing work. |
| `TL` | Test Log | Companion data-collection workbook to a Test Plan. Captures actual results, observations, and outcomes as testing is executed. Always paired 1:1 with a TP of the same number. |
| `DN` | Design Note | Records design decisions, research findings, architectural intent, or reference material. Not a procedure document — captures the *why* and *what*, not the *how*. |

---

## Document Register

| Document | Title | Paired With | Status |
|---|---|---|---|
| TP-KRC3006-01 | Protocol Reverse Engineering Test Plan | TL-KRC3006-01 | **Rev B** — in progress; Phase 1 complete |
| TL-KRC3006-01 | Test Log — Companion to TP-01 | TP-KRC3006-01 | **Rev B** — Phase 1 recorded 2026-04-19 |
| TP-KRC3006-02 | Breakout Board Bare Board Testing, Assembly, and Verification | TL-KRC3006-02 | Board Serial Number 1 Completed |
| TL-KRC3006-02 | Breakout Board Test Log | TP-KRC3006-02 | Board Serial Number 1 Completed |
| TP-KRC3006-03 | Protocol Emulation Test Plan | TL-KRC3006-03 | Waiting for TP-01 Completion |
| TL-KRC3006-03 | Test Log — Companion to TP-03 | TP-KRC3006-03 | Template prepared; waiting for TP-01 Completion |
| DN-KRC3006-01 | Hardware Design Research | — | In progress |
| DN-KRC3006-02 | Schematic Analysis | — | **Rev C** — bus impedance corrected |
| DN-KRC3006-03 | Bluetooth Integration & Button Remapping | — | Concept |
| DN-KRC3006-04 | 13-Pin Mini DIN Protocol Sniffer Breakout Board | — | Complete |
| DN-KRC3006-05 | Web Application Design for Emulator Library Management | — | Draft |
| DN-KRC3006-06 | Kenwood CD Changer Error Codes | — | Complete |

TP-KRC3006-01 Rev B (2026-04-12) restricted the plan's scope to protocol reverse engineering only — emulator development and audio integration moved to TP-KRC3006-03 — replaced KDC-CX85 references with the KDC-C717, and added Phase 2B for changer-connected capture through the breakout board.

### TP-KRC3006-01 Phase Progress

| Phase | Scope | Status |
|---|---|---|
| 1 | Power-on characterization — supply, idle bus voltages, CH-CON polarity, ground continuity | Complete (2026-04-19) |
| 2A | Idle-state capture and first message decode | Not started |
| 2B | Inline bidirectional capture, head unit ↔ KDC-C717 | Not started |
| 3 | Command mapping | Not started |

---

## TP / TL Pairing

Test Plans and Test Logs are always created and maintained as a matched pair. A TP defines what will be tested and how; the companion TL is where results are recorded as work is executed. They share the same sequence number — `TP-KRC3006-01` and `TL-KRC3006-01` are two halves of the same body of test work.

When a new test plan is created, a corresponding log document must be created at the same time. A filled out *copy* of a test log is to be placed in the `records/` sub directory.

The working log in this folder stays live and accumulates results as phases are executed. Each time a phase or unit is finished, a snapshot of the filled-out log is published to `records/` and named `{TL-ID}-{phase or unit}-{YYYYMMDD}`.

### Published Records

| Record | Covers | Date |
|---|---|---|
| TL-KRC3006-01-P1-20260419 | TP-01 Phase 1 — power-on characterization | 2026-04-19 |
| TL-KRC3006-02-01-20260410 | TP-02 — breakout board serial number 1 | 2026-04-10 |

---

*This README is a living document and should be updated whenever a new document is added to the register.*
