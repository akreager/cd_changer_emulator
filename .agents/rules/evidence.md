# Rule: evidence

This applies to every agent and to every file you write.

## Cite it or mark it TBD

- Every number, pin name, polarity, part value, timing or behavior you write cites its source. A source is one of:
  - a record ID and step, e.g. `TL-KRC3006-01-P1-20260419`, Initial Power-Up step 4
  - a capture file, e.g. `captures/P2A_idle_capture_001.sr`
  - a service manual, with its document number and page
  - a design note section, e.g. DN-KRC3006-02 §3.1
- If you can't cite it, write `[TBD — source needed: <what>]` and log it as an open item.
- Never fill a gap with a plausible value.

**Why:** an earlier draft of DN-KRC3006-04 contained fabricated connector pinout data, and the owner caught it against the service manual. In a reverse-engineering project, invented data is worse than a gap, because it gets built into hardware.

## Order of authority

1. This project's bench records and captures, for how our units actually behave.
2. The factory service manual, for factory signal names and circuit topology.
3. Community references (Mictronics, szymtro on Elektroda, pinouts.ru). These are informative only.

**Why:** documentation doesn't always match our units. The KDC-CX85 service manual documents CH-CON as active-LOW, but the Phase 1 bench measurement read active-HIGH.

## Surface conflicts; don't resolve them

When sources disagree, record both sides with citations and route the question to the architect. Don't pick a winner in the text. The live conflicts are listed in [context/technical-baseline.md](../context/technical-baseline.md).

## A correction to a calculation is a technical change

Swapping a part, a board or a value can invalidate the numbers derived from it. For example, a Pi 4 → Pi 5 change alters the power budget. Flag the derived values for the architect, and don't edit the numbers yourself. Find-and-replace is not propagation.

## Report exactly what you did

List the commands and checks you actually ran, and say what you didn't verify. Expect your claims to be audited against git and the files.
