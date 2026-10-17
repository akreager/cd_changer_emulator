# Technical baseline

This file records what's settled, what's still open, and where the sources are. The architect maintains it.

- Every document and every agent's work must agree with the **settled** items.
- Anything that touches an **open** item must present it as open.

As of `main` @ `11bc992` (2026-10-09).

## Hardware

- **HAT:**
  - ATtiny1616 protocol controller, running at 3.3 V
  - two SN74LVC8T245PWR level shifters, one per direction
  - PCM5102A DAC
  - Raspberry Pi 5 with a 1 TB NVMe drive
- **Software direction (DN-05):** FastAPI, SQLite (WAL + FTS5), HTMX, Alpine.js, DaisyUI, python-mpv and ZeroMQ. Older documents still name Flask, MPD and the Pi 4.
- **Bench equipment (TP-01 §3):**

  | Ref ID | Item |
  |---|---|
  | KEN-01 | KRC-3006 head unit (device under test) |
  | KEN-02 | KDC-C717 changer (reference changer) |
  | MOD-03 | Pass-through breakout board S/N 1 (DN-04, verified per TP-02) |
  | LA-01 | SparkFun TOL-18627 logic analyzer, used with PulseView |
  | PWR-02 | Staged power adapter |

  The KDC-CX85 is retired because its laser failed (DN-06).

## Where the work stands

- TP-01 Phase 1 is complete (2026-04-19), but its record has gaps (backlog DC-02).
- Phases 2A, 2B and 3 haven't started. No captures exist yet.
- The HAT design was committed in `96d09e0` (2026-10-16) as the owner's initial-state commit. It hasn't been reviewed for completeness. The owner's notes of 2026-07-29 described it as follows (not yet verified against that commit):
  - It has U1–U4 (ATtiny1616, 2× SN74LVC8T245, PCM5102A), the 40-pin Pi header J1, the SDD-130J changer port J3, R1–R4, C1–C12 and D1.
  - The automotive power section (regulators, supercap, TVS) isn't drawn.
  - The PCB has 4 footprints and no tracks, vias or zones.
  - J1 uses KiCad's `Raspberry_Pi_4` symbol as a stand-in for the Pi 5. The pinout is the same, but a generated BOM will name the wrong board.
- Firmware and software haven't started. The planned firmware interfaces (DN-01) are:
  - SPI slave on PA3 (SCK ← CLK), PA4 (MOSI ← DATA H) and PA5 (MISO → DATA C)
  - USART0 to the Pi on PA1/PA2
  - UPDI from Pi UART3 (GPIO4/5, `dtoverlay=uart3`)
  - the PCM5102A driven through the `hifiberry-dac` overlay

## Settled

| Fact | Source |
|---|---|
| Factory pin names (connector E06-1301-05): 1 /REQ H, 2 GND, 3 B.U, 4 ON, 5 MUTE, 6 D. GND, 7 RESET, 8 R ch, 9 /REQ C, 10 DATA C, 11 DATA H, 12 L ch, 13 /CLK. Here "/" stands for the factory overbar (active-low). Published aliases (CH-REQH, CH-CON, CH-MUTE, AGND, …) are secondary. | KRC-3006 service manual pin table (`assets/changer_pins.png`); DN-02 §1 |
| Head-unit inline series resistors: REQ H 100 Ω (R144), DATA H 100 Ω (R143), CLK 2.2 K (R129), REQ C 2.2 K (R131), DATA C 2.2 K (R130), ON 4.7 K (R142), MUTE 7.5 K (R140), RESET 1 K (R141). R145 and R146 (100 K) are pull-downs to GND on DATA H and CLK, not series elements. The bus is 5 V TTL/CMOS with fast edges. This supersedes every "100K series", "~200K total" and "slow/rounded edge" statement. | DN-02 Rev C §3.1 and §12, read from the schematic. The pull-downs haven't been verified on the bench (see Open). |
| The KDC-CX85's changer-side inline resistors are a uniform 100 Ω (R9–R16). | DN-02 §12 |
| Pin 2 and pin 6 are continuous inside the head unit. | TL-KRC3006-01-P1-20260419 |
| The head unit won't select CD-CH unless a changer is connected, so captures must be inline. | Owner observation, stated in the root README. It isn't in any test record yet (backlog DC-02). |
| The KDC-C717 is the reference changer. The KDC-CX85 is retired. | DN-06 |
| The level shifters are SN74LVC8T245. The TXB0108 and TXS0108E were rejected. | DN-01. The rationale text still needs correcting (backlog DC-06). |
| The ATtiny1616 runs at 3.3 V. UPDI uses Pi UART3 (GPIO4/5). | DN-01 |
| The HAT puts a 100 Ω inline series resistor on every bus signal, matching the KDC-CX85's protection scheme. | HAT README |
| The KDC-CX85's J2 is an independent output driven by its MCU, with its own signal lines. It isn't a pass-through of J1, so it can't be used as a monitoring tap. | Owner finding. It isn't in a DN yet. |
| The KRC-3006 can't display elapsed time. In CD changer mode its display toggles between track number and clock, and shows the track and disc numbers only. | KRC-3006 instruction manual, "Clock display" and "CD auto changer mode" ([rulings R-5](../rulings/2026-10-16.md)) |
| The web app covers library, playlist and magazine management only. It has no playback controls; every playback command comes from the head unit. It handles FLAC only, and its main devices are phones and tablets. "Magazine overflow" (playlists of playlists) allows more than 10 playlists per magazine, moving to the next bank when disc 10 finishes. | DN-05 §5.2 |

## Open

Never state these as settled.

| Question | Current evidence | Resolved by |
|---|---|---|
| ON / CH-CON (pin 4) polarity | Measured active-HIGH. The KDC-CX85 service manual says active-LOW. | Phase 2 decoded traffic |
| DATA C (pin 10) idle level | Measured ~5.1 V. The DN analysis predicted LOW. | Phase 2A/2B |
| CLK idle level | Phase 1 read 5.15 V DC with bursts at ≤ ~100 Hz, so CLK sits HIGH between bursts, which matches the overbar. DN-02 §3.1 and the HAT README say the pull-down "defines idle LOW"; that's only true when the line is undriven. | The first 2A capture. The architect then corrects the wording. |
| CLK direction | The KDC-CX85 service manual lists CLK as I/O. | Phase 2B. If CLK is bidirectional, the fallback is an SN74LVC1T45. |
| Bit clock rate | 125 kHz is assumed (TP-01, DN-02), but it hasn't been measured. | Phase 2A |
| Time data in the protocol | The KRC-3006 can't display elapsed time (settled, below), but the status frames may still carry it. | Phase 2B time-field check ([rulings R-1.4](../rulings/2026-10-16.md)) |
| RESET idle level | Measured 0 V at idle. TP-01 expected HIGH. | Phase 2A |
| MUTE polarity | Phase 1 read 0 V at idle and 3.5 V "logic high enable". DN-02 §16.4 calls MUTE active-LOW and changer-driven. | Phase 2A, CH7 ([rulings R-1.3](../rulings/2026-10-16.md)) |
| Pull-downs R145/R146 confirmed on the bench | Not measured yet. This is DN-02 §8 item 3, and TP-01 Rev B doesn't include it. | TP-01 Rev C |
| KDC-C717 changer-side interface | Not analyzed. Part 2 of DN-02 covers the KDC-CX85. | Architect |
| Pi ↔ ATtiny UART baud rate | Deliberately unspecified (decision D-12). DN-01 and DN-05 still say 115200 baud, 8N1, and the owner's earlier notes said 9600 (backlog DC-21). | Chosen during hardware testing (TP-03) |

## Sources outside this repository

The service manuals aren't committed, because of the IP posture ([rules/ip-posture.md](../rules/ip-posture.md)). Agents working in the owner's claude.ai Project can read these scans there. They're scanned images, so render the pages to read them.

| File | What it is |
|---|---|
| `krc3006.pdf` | KRC-3006 service manual (24 pp) |
| `schematic_20090202_0004.PDF` | KRC-3006 schematic diagram, large-format scan |
| `schematic_20090202_0003.PDF` | KRC-3006 exploded views and parts list |
| `KRC3006 OM.PDF` | KRC-3006 owner's manual |
| `KDCC717 SM.pdf` | KDC-C517FM/KDC-C717 service manual (B51-7731-00) |
| `KDCC717 OM.pdf` | KDC-C717 owner's manual |

The KDC-CX85 service manual (B51-7552-00) is DN-02's changer-side source. It isn't in the Project.
