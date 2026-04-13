# Kenwood CD Changer Emulator HAT

KiCad project for a Raspberry Pi 5 HAT that emulates a Kenwood CD changer over the proprietary "O protocol" bus. Designed for the KRC-3006 shaft-style cassette head unit, replacing a 10-disc changer with unlimited FLAC playback controlled entirely from the factory head unit.

## Current Status

**Early schematic layout.** A few of the main components have been placed (ATtiny1616, level shifters, I2S DAC, GPIO header) along with supplemental passives based on the PCM5102A reference design. No PCB layout work has begun.

Protocol reverse engineering via the breakout board (DN-KRC3006-04) is the active priority. Full command mapping must be complete before the HAT schematic can be finalized.

## Design Overview

The HAT consolidates four subsystems onto a single board:

- **ATtiny1616 protocol controller** — Handles all real-time Kenwood bus communication at 3.3V, translated to 5V bus levels via two SN74LVC8T245PWR level shifters. Communicates with the Pi over a dedicated UART.
- **PCM5102A I2S DAC** — Converts digital audio from the Pi to analog line-level output for the head unit's CD changer input.
- **Automotive power supply** — Accepts 12V from the head unit (constant B.U. and ignition-switched), regulates to 5V/3.3V with power sequencing and soft-shutdown support.
- **Connectors and interface** — 13-pin mini DIN bus connection, UPDI programming header (dedicated UART3 on GPIO4/5), status LEDs, test points.

All music logic — playlist management, FLAC decoding, library browsing — runs on the Raspberry Pi via python-mpv. The ATtiny handles only the protocol state machine and handshake timing.

## Open Constraints

Several items depend on data from the ongoing reverse engineering effort (TP-KRC3006-01):

- **CLK signal directionality** — The CX85 service manual lists CLK as I/O on the changer side. If confirmed bidirectional, the CLK channel must use an SN74LVC1T45 (independent DIR pin) instead of the fixed-direction 74LVC8T245.
- **Power sequencing** — The ATtiny must be ready to respond before the Pi finishes booting (~20s). Autonomous status responses during early boot may be required.
- **Audio ground topology** — Pins 2 (GND) and 6 (D.GND) are believed connected inside the head unit. Continuity testing during Phase 1 will confirm the grounding strategy.
- **DAC output level matching** — Analog output must match the stock changer's level to avoid volume discontinuity. To be verified during integration testing.

## Related Documentation

| Document | Description |
|----------|-------------|
| DN-KRC3006-01 | HAT design research — component selection, pin mapping, architecture |
| DN-KRC3006-02 | KRC-3006/KDC-C717 schematic analysis — bus impedance, signal conditioning |
| DN-KRC3006-04 | 13-pin mini DIN breakout board (complete, used for protocol capture) |
| TP-KRC3006-01 | Reverse engineering test plan (active) |
| TP-KRC3006-03 | Emulator development and integration test plan (waiting for TP-01) |

## License

MIT — see repository root.
