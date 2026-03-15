# KRC-3006 CD Changer Emulator — Documentation Index

This folder contains all project documentation for the KRC-3006 reverse engineering and CD changer emulator project.

---

## File Format

All documents are authored in **Open Document Format (.odt)** unless the document type is inherently plain-text (e.g., Markdown). Microsoft Office formats (.docx, .xlsx, etc.) are not used. ODF files can be opened with LibreOffice, which is the recommended editor for this project.

Exceptions:
- Markdown (`.md`) files such as this README
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
| TP-KRC3006-01 | Initial Overarching Test Plan | TL-KRC3006-01 | In progress |
| TL-KRC3006-01 | Test Log — Companion to TP-01 | TP-KRC3006-01 | In progress |
| TP-KRC3006-02 | Breakout Board Bare Board Testing, Assembly, and Verification | TL-KRC3006-02 | In progress |
| TL-KRC3006-02 | Breakout Board Test Log | TP-KRC3006-02 | In progress |
| DN-KRC3006-01 | Hardware Design Research | — | In progress |
| DN-KRC3006-02 | Schematic Analysis | — | In progress |
| DN-KRC3006-03 | Bluetooth Integration & Button Remapping | — | Concept |
| DN-KRC3006-04 | 13-Pin Mini DIN Protocol Sniffer Breakout Board | — | Complete |

---

## TP / TL Pairing

Test Plans and Test Logs are always created and maintained as a matched pair. A TP defines what will be tested and how; the companion TL is where results are recorded as work is executed. They share the same sequence number — `TP-KRC3006-01` and `TL-KRC3006-01` are two halves of the same body of test work.

When a new test plan is created, a corresponding log document must be created at the same time.

---

*This README is a living document and should be updated whenever a new document is added to the register.*
