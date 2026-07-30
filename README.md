# CD Changer Emulator

**Raspberry Pi-based CD changer emulator for vintage Kenwood car stereos**

Reverse-engineering the proprietary serial protocol used by 1990s Kenwood head units to communicate with their CD changers, and building an open-source emulator that replaces the changer with a Raspberry Pi — enabling unlimited music playback through the original stereo using its factory controls.
![Close-up front view of KRC-3006 cassette receiver](/../main/assets/KRC3006_01.jpg)

## Project Status

🔬 **Phase: Protocol Reverse Engineering** — Capturing and decoding the synchronous serial protocol between a Kenwood KRC-3006 cassette receiver and a KDC-C717 10-disc CD changer.

### Current Milestone

**Phase 1 of TP-KRC3006-01 — power-on characterization — is complete.** Executed 2026-04-19 on the KRC-3006 with a KDC-C717 changer connected through the pass-through breakout board. Every recorded step passed; results are published in [TL-KRC3006-01-P1-20260419](./docs/records/TL-KRC3006-01-P1-20260419.pdf).

Findings that matter for the emulator design:

- **CH-CON (Pin 4) measures active-HIGH** — the line rises when the changer source is selected. This *conflicts* with the KDC-CX85 service manual, which documents it as active-LOW. To be re-confirmed against decoded traffic in Phase 2.
- **Pin 2 (GND) and Pin 6 (D.GND) show continuity** inside the head unit, which settles the grounding strategy for the HAT.
- **CLK (Pin 13) is gated, not continuous** — 0 Hz at idle, 31.6 Hz during playback, briefly ~100 Hz on a track change before settling back. These are DMM frequency readings on a gated line, not bit-rate measurements; bit-level clock timing awaits logic analyzer capture in Phase 2A.
- **Pin 10 (CH-DATAC) idles near 5 V**, not the LOW state predicted by the schematic analysis. Unexplained — still open.
- **The KDC-C717 is functional** — displays E-01 with no magazine, then loads and plays on insertion.

Testing runs inline through the DN-KRC3006-04 pass-through breakout board, serial number 1, assembled and verified per TP-KRC3006-02:
![Close-up view of assembled pass-through breakout board](/../main/assets/breakout_board_01.jpg)

The KDC-CX85 originally used as the reference changer was diagnosed with a dead or degraded laser diode and retired. All further testing uses the KDC-C717:
![Close-up front view of KDC-C717 CD auto changer](/../main/assets/KDCC717_01.jpg)

For reference, the 13-pin mini DIN changer connector pinout:
![Kenwood 13-pin mini DIN CD changer connector pinout and signal names](/../main/assets/changer_pins.png)

### Immediate To-Do

- [ ] **Execute Phase 2A of TP-KRC3006-01** — Idle-state logic analyzer capture and first message decode: establish the bit clock, polling interval, and frame structure.
- [ ] **Execute Phase 2B** — Inline bidirectional capture of head unit ↔ KDC-C717 traffic. Inline capture is mandatory: the head unit will not switch to the changer source unless a changer is electrically present, so isolated head unit testing is impractical.
- [ ] **Execute Phase 3** — Command mapping: correlate each head unit control to its bus command and the changer's response, and compare against the Mictronics tables.
- [ ] **Resolve CLK directionality** — The CX85 service manual lists CLK as I/O. If Phase 2B confirms it is bidirectional, the fixed-direction SN74LVC8T245 will not work for CLK; an SN74LVC1T45 (independent DIR pin) is the planned substitute.
- [ ] **Continue the emulator HAT schematic** — The protocol and audio front end is placed (ATtiny1616, two SN74LVC8T245 level shifters, PCM5102A DAC, 40-pin Pi header, 13-pin mini DIN changer port, supporting passives). The automotive power supply section is not yet drawn and no PCB layout has begun; the schematic cannot be finalized until command mapping is complete.

### Completed

- [x] **Schematic analysis** — Detailed analysis of both KRC-3006 and KDC-CX85 service manuals. Confirmed 5V TTL bus signaling, inline series resistors of 100Ω–7.5KΩ on the head unit side against a uniform 100Ω on the changer side, all total series impedances between 200Ω and 7.6KΩ, COMMSW protocol selection, and always-live 12V on the B.U. pin. **Rev C corrected an earlier error:** R145/R146 (100K) are pull-downs to ground that define the idle-LOW state on DATA H and CLK — they are *not* inline series elements, and bus edges are consequently fast (τ ≈ 2 ns), not slow. No edge-rate compensation is needed. (DN-KRC3006-02 Rev C)
- [x] **Breakout board design** — KiCad layout with two 13-pin mini DIN connectors and 2.54mm pin headers (ground adjacent to each signal) using Kenwood signal names on silkscreen. (DN-KRC3006-04)
- [x] **Connector footprint verification** — 3D-printed mockup confirmed pin spacing before committing to fab.
- [x] **Breakout board ordered** — 3 boards, OSH Park standard fab.
- [X] **Completed TP-KRC3006-02** — Receive, inspect, assemble and verify pass-through breakout board serial number 1.
- [X] **Set up test bench** — Bench wiring, logic analyzer connections, and a custom staged power adapter with two toggle switches that simulate constant and ignition-switched power independently.
- [X] **Troubleshoot CX85** — Initial tests showed the CD changer laser diode is dirty or degraded (E-04, all discs unreadable). Unit deemed inoperable and retired. Further testing is carried out with a KDC-C717 CD changer. (DN-KRC3006-06)
- [X] **Completed Phase 1 of TP-KRC3006-01** — Power-on characterization with the KDC-C717 inline: supply and idle current draw, 13-pin DIN idle voltages on every signal pin, CH-CON polarity, CLK gating behavior, and pin 2 ↔ pin 6 ground continuity. Record: TL-KRC3006-01-P1-20260419.

## What This Project Does

This project emulates a Kenwood CD changer on the 13-pin round DIN connector used by mid-1990s Kenwood head units. The emulator responds to all head unit commands (play, stop, next/previous track, disc selection, repeat, shuffle) and streams audio from a Raspberry Pi through the stereo's built-in amplifier.

### Features (Planned)

- **Full protocol emulation** — Head unit displays disc number and track number.
- **10 virtual disc slots** — Map playlists to CD1–CD0, just like a real magazine. "Magazine overflow" (a playlist of playlists) allows more than ten playlists per magazine, wrapping to the next bank automatically when disc 10 finishes.
- **Web-based library management** — Build playlists and load virtual magazines from your phone over WiFi. FLAC-only library. By design there are **no playback controls in the web UI** — every transport command comes from the head unit, the same as a real changer. (DN-KRC3006-05)
- **Automotive power management** — Supercapacitor-backed graceful shutdown, cranking ride-through, battery monitoring.
- **WiFi standby mode** — When parked at home, the Pi stays on and connects to your home network for easy music transfers and system updates.
- **Custom Raspberry Pi HAT** — Single PCB with ATtiny1616 protocol controller, PCM5102A I2S DAC, automotive power supply, designed for JLCPCB or similar assembly.

## Target Hardware

| Component | Role |
|-----------|------|
| Kenwood KRC-3006 (or similar mid-90s Kenwood head unit) | The stereo — device under test |
| Kenwood KDC-C717 | CD auto changer — reference changer for protocol capture |
| Raspberry Pi 5 | Media server, web interface, audio playback |
| ATtiny1616 | Real-time Kenwood protocol handler (on custom HAT), run at 3.3V to match Pi GPIO natively |
| SN74LVC8T245PWR ×2 | 3.3V ↔ 5V bus level shifting, one per direction |
| PCM5102A I2S DAC | Digital-to-analog audio conversion |
| 1 TB NVMe SSD | Music storage (avoids SD card corruption) |
| SparkFun TOL-18627 USB Logic Analyzer | Protocol capture and analysis |
| Custom staged power adapter | Two toggle switches simulating constant and ignition power independently on the bench |

## Target Vehicle

Any vintage automobile still using a Kenwood head unit with CD changer control. I am building this and testing around a KRC-3006 head unit due to it being the only shaft style cassette deck with a CD changer control port. My vehicle for this project is a 1985 Chevrolet C10 Silverado. The power supply design accounts for the electrically noisy environment of older vehicles without modern filtering.

## Repository Structure

```
cd_changer_emulator/
├── assets/                  # Project assets. Photos and screenshots.
├── docs/                    # Project documentation
│   ├── TP-KRC3006-01.odt    # Test plan 1: Protocol capture test procedure (IEEE 829)
│   ├── TL-KRC3006-01.ods    # Test log 1: Companion log workbook to TP-KRC3006-01
│   ├── TP-KRC3006-02.odt    # Test plan 2: Breakout board test plan
│   ├── TL-KRC3006-02.odt    # Test log 2: Breakout board test log
│   ├── TP-KRC3006-03.odt    # Test plan 3: Emulator test procedure (IEEE 829)
│   ├── TL-KRC3006-03.ods    # Test log 3: Companion log workbook to TP-KRC3006-03
│   ├── DN-KRC3006-01.md     # Design note 1: HAT design research
│   ├── DN-KRC3006-02.md     # Design note 2: Schematic analysis
│   ├── DN-KRC3006-03.md     # Design note 3: Bluetooth stretch goal
│   ├── DN-KRC3006-04.md     # Design note 4: Breakout board design
│   ├── DN-KRC3006-05.md     # Design note 5: Web application design for library management
│   ├── DN-KRC3006-06.md     # Design note 6: Kenwood CD changer error codes
│   ├── protocol/            # Decoded protocol data
│   └── records/             # Completed, filled-out test logs (published as PDF)
├── firmware/                # ATtiny1616 firmware (Arduino/megaTinyCore)
│   └── src/
├── software/                # Raspberry Pi software
│   ├── flask-app/           # Web interface — legacy name; being superseded by FastAPI
│   ├── mpd-config/          # Legacy name; playback is moving to python-mpv
│   ├── power-mgmt/          # ATtiny UART bridge and power state management
│   └── wifi-manager/        # AP/client mode switching
├── hardware/                # KiCad PCB design files
│   ├── kicad/
│   │   ├── changer cable breakout/  # Pass-through breakout board (complete, fabbed)
│   │   ├── emulator hat/            # Raspberry Pi HAT (schematic in progress)
│   │   └── lib/                     # Shared custom symbols and footprints
│   ├── gerbers/             # Manufacturing files
│   └── bom/                 # Bill of materials with JLCPCB part numbers
├── captures/                # Logic analyzer captures (.sr files)
├── diagrams/                # WaveDrom timing, Mermaid state machines, draw.io blocks
└── reference/               # Datasheets, protocol documentation, forum archives
```

## Kenwood Compatibility

This project targets the **"O protocol"** (Old protocol) used by Kenwood head units with the round 13-pin DIN CD changer connector, roughly 1990–1998. Known compatible head units include models in the KRC series (cassette receivers) and some KDC series (CD receivers) from that era [citation needed].

Later Kenwood units with a rectangular changer connector use the "C protocol" (New protocol), which has different command encoding. This project does not currently target the C protocol, but the hardware and architecture could be adapted [citation needed].

## Documentation

The project follows a documentation-first approach using IEEE 829-inspired test procedures. All documentation lives in the `docs/` directory. Markdown is preferred wherever it fits, so design notes are written in Markdown and render directly on GitHub. The test plans and companion logs are currently kept in Open Document Format because they are table- and form-heavy, but no particular document format is required.

Test plans and test logs are created and maintained as matched pairs sharing a sequence number — `TP-KRC3006-01` defines what gets tested and how, and `TL-KRC3006-01` is where results are recorded. Filled-out copies of a log are published as PDF in `docs/records/` as each phase completes.

| Document Name | Type | Description |
|----|------|-------------|
| [TP-KRC3006-01](./docs/TP-KRC3006-01.odt) | Test Plan | Initial test plan for capturing messages between CD changer and head unit |
| [TL-KRC3006-01](./docs/TL-KRC3006-01.ods) | Test Log | Companion log workbook to TP-KRC3006-01 |
| [TP-KRC3006-02](./docs/TP-KRC3006-02.odt) | Test Plan | Breakout board test plan |
| [TL-KRC3006-02](./docs/TL-KRC3006-02.odt) | Test Log | Breakout board test log |
| [TP-KRC3006-03](./docs/TP-KRC3006-03.odt) | Test Plan | Test plan for creating and testing protocol emulation through full audio integration |
| [TL-KRC3006-03](./docs/TL-KRC3006-03.ods) | Test Log | Companion log workbook to TP-KRC3006-03 |
| [DN-KRC3006-01](./docs/DN-KRC3006-01.md) | Design Note | HAT design research — ATtiny1616 selection, PCM5102A DAC circuit, automotive power supply with supercap, WiFi architecture, JLCPCB assembly |
| [DN-KRC3006-02](./docs/DN-KRC3006-02.md) | Design Note | Schematic analysis — KRC-3006 head unit and KDC-CX85 changer signal routing, series resistor values, protocol variant identification |
| [DN-KRC3006-03](./docs/DN-KRC3006-03.md) | Design Note | Bluetooth stretch goal — wireless audio streaming while retaining factory head unit controls |
| [DN-KRC3006-04](./docs/DN-KRC3006-04.md) | Design Note | Breakout board design — pass-through 13-pin mini DIN breakout with logic analyzer headers |
| [DN-KRC3006-05](./docs/DN-KRC3006-05.md) | Design Note | Web Application Design for Emulator Library Management |
| [DN-KRC3006-06](./docs/DN-KRC3006-06.md) | Design Note | Kenwood CD Changer Error Codes |

Per-document revision status is tracked in the [documentation index](./docs/README.md).

### Completed Test Records

| Record | Covers | Date |
|----|------|------|
| [TL-KRC3006-01-P1-20260419](./docs/records/TL-KRC3006-01-P1-20260419.pdf) | TP-KRC3006-01 Phase 1 — power-on characterization | 2026-04-19 |
| [TL-KRC3006-02-01-20260410](./docs/records/TL-KRC3006-02-01-20260410.pdf) | TP-KRC3006-02 — breakout board serial number 1 | 2026-04-10 |

## Building / Contributing

This project is in early development. If you have a compatible Kenwood head unit and want to help with protocol capture, testing, or firmware development, contributions are welcome.

### Prerequisites

- [Arduino IDE](https://www.arduino.cc/en/software) with [megaTinyCore](https://github.com/SpenceKonde/megaTinyCore) installed
- [PulseView](https://sigrok.org/wiki/PulseView) for logic analyzer captures
- [KiCad](https://www.kicad.org/) for PCB design
- Python 3 with [FastAPI](https://fastapi.tiangolo.com/) for the web interface and [python-mpv](https://github.com/jaseg/python-mpv) for playback
- [LibreOffice](https://www.libreoffice.org/) to open the test plans and logs (`.odt` / `.ods`)
- A UPDI programmer for the ATtiny1616 ([Adafruit UPDI Friend](https://www.adafruit.com/product/5879) or DIY with a serial adapter and resistor)

## References

- [Mictronics CDC Protocol Documentation](https://www.mictronics.de/) (Kenwood command tables)
- [Elektroda.pl Kenwood Slim CD Changer Emulator](https://www.elektroda.pl/rtvforum/topic536235.html) (szymtro's 8051 implementation)
- [AVRFreaks: Kenwood CD Changer → Serial Strings](https://www.avrfreaks.net/forum/kenwood-cd-changer-serial-strings)
- [Pinouts.ru: Kenwood 13-pin DIN connector](https://old.pinouts.ru/CarAudio/kenwood_cd_changer_pinout.shtml)
- [SpenceKonde/megaTinyCore](https://github.com/SpenceKonde/megaTinyCore) (ATtiny1616 Arduino support)
- [pyupdi / pymcuprog](https://github.com/mraardvark/pyupdi) (UPDI programming from Raspberry Pi)

## License

This project is licensed under the [MIT License](LICENSE) — you're free to use, modify, and distribute this project for any purpose, including commercial use.
