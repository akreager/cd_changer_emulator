# Kenwood CD Changer Emulator HAT

KiCad project for a Raspberry Pi 5 HAT that emulates a Kenwood CD changer over the proprietary "O protocol" bus. Designed for the KRC-3006 shaft-style cassette head unit, replacing a 10-disc changer with unlimited FLAC playback controlled entirely from the factory head unit.

## Current Status

**Early schematic layout.** The protocol and audio front end is placed — ATtiny1616, two SN74LVC8T245 level shifters, PCM5102A DAC, 40-pin Pi header, and the 13-pin mini DIN changer port — along with supporting passives based on the PCM5102A reference design. The automotive power supply section has not been drawn yet, and no PCB layout work has begun.

Protocol reverse engineering via the breakout board (DN-KRC3006-04) is the active priority. Full command mapping must be complete before the HAT schematic can be finalized.

## Design Overview

The HAT consolidates four subsystems onto a single board:

- **ATtiny1616 protocol controller** — Handles all real-time Kenwood bus communication at 3.3V, translated to 5V bus levels via two SN74LVC8T245PWR level shifters. Communicates with the Pi over a dedicated UART.
- **PCM5102A I2S DAC** — Converts digital audio from the Pi to analog line-level output for the head unit's CD changer input.
- **Automotive power supply** — Accepts 12V from the head unit (constant B.U. and ignition-switched), regulates to 5V/3.3V with power sequencing and soft-shutdown support.
- **Connectors and interface** — 13-pin mini DIN bus connection, UPDI programming header (dedicated UART3 on GPIO4/5), status LEDs, test points.

Every bus signal will carry a 100 Ω inline series resistor, matching the protection scheme the KDC-CX85 uses on its own connector. Per DN-KRC3006-02 Rev C the bus is a conventional fast 5V TTL/CMOS bus — the head unit's own series resistors range from 100 Ω to 7.5 KΩ and the 100K parts on DATA H and CLK are pull-downs to ground that define the idle-LOW state, not series elements. No edge-rate compensation or Schmitt-trigger conditioning is needed.

All music logic — playlist management, FLAC decoding, library browsing — runs on the Raspberry Pi via python-mpv. The ATtiny handles only the protocol state machine and handshake timing.

## Settled by Phase 1 Testing

TP-KRC3006-01 Phase 1 (power-on characterization, 2026-04-19) resolved two questions that affect this board:

- **Audio ground topology** — Pins 2 (GND) and 6 (D.GND) measured continuous inside the head unit. They can be treated as a single ground on the HAT.
- **CH-CON (Pin 4) polarity** — Measured active-HIGH: the line rises when the changer source is selected. This conflicts with the KDC-CX85 service manual, which documents it as active-LOW, so it will be re-confirmed against decoded traffic in Phase 2 before the input stage is committed.

Phase 1 also found Pin 10 (CH-DATAC) idling near 5 V rather than the LOW state the schematic analysis predicted. That is still unexplained and may affect how the HAT drives or reads that line.

## Open Constraints

Several items still depend on data from the ongoing reverse engineering effort (TP-KRC3006-01):

- **CLK signal directionality** — The CX85 service manual lists CLK as I/O on the changer side. If Phase 2B confirms it is bidirectional, the CLK channel must use an SN74LVC1T45 (independent DIR pin) instead of the fixed-direction 74LVC8T245.
- **Power sequencing** — The ATtiny must be ready to respond before the Pi finishes booting (~20s). Autonomous status responses during early boot may be required.
- **DAC output level matching** — Analog output must match the stock changer's level to avoid volume discontinuity. To be verified during integration testing.

## Related Documentation

| Document | Description |
|----------|-------------|
| DN-KRC3006-01 | HAT design research — component selection, pin mapping, architecture |
| DN-KRC3006-02 Rev C | KRC-3006 and KDC-CX85 schematic analysis — bus impedance, signal conditioning |
| DN-KRC3006-04 | 13-pin mini DIN breakout board (complete, used for protocol capture) |
| TP-KRC3006-01 Rev B | Reverse engineering test plan (active — Phase 1 complete, Phase 2A next) |
| TP-KRC3006-03 | Emulator development and integration test plan (waiting for TP-01) |

## License

MIT — see repository root.
