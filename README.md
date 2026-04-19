# CD Changer Emulator

**Raspberry Pi-based CD changer emulator for vintage Kenwood car stereos**

Reverse-engineering the proprietary serial protocol used by 1990s Kenwood head units to communicate with their CD changers, and building an open-source emulator that replaces the changer with a Raspberry Pi — enabling unlimited music playback through the original stereo using its factory controls.
![Close-up front view of KRC-3006 cassette receiver](/../main/assets/KRC3006_01.jpg)

## Project Status

🔬 **Phase: Protocol Reverse Engineering** — Capturing and decoding the synchronous serial protocol between a Kenwood KRC-3006 cassette receiver and a KDC-C717 10-disc CD changer.

### Current Milestone

The pass-through breakout boards (DN-KRC3006-04) have been received and board serial number 1 has been assembled and tested per TP-KRC3006-02.
![Close-up view of assembled pass-through breakout board](/../main/assets/breakout_board_01.jpg)
KDC-CX85 changer on hand is apparently dead, further testing will be performed on a KDC-C717 CD Changer
![Close-up front view of KDC-C717 CD Autochacger](/../main/assets/KDCC717_01.jpg)

### Immediate To-Do

- [ ] **Execute Phase 1 of TP-KRC3006-01** — Power-on characterization: validate CHCON polarity (active-LOW per changer service manual), verify bus idle states, confirm O protocol selection.
- [ ] **Begin live protocol capture** — Passive logic analyzer capture of bidirectional traffic between head unit and changer through the breakout board.

### Completed

- [x] **Schematic analysis** — Detailed analysis of both KRC-3006 and KDC-CX85 service manuals. Confirmed 5V TTL bus signaling, 100Ω–2.2KΩ inline series resistors on bus signals, all total series impedances are between 200Ω and 7.6KΩ, COMMSW protocol selection, and always-live 12V on B.U. pin. (DN-KRC3006-02)
- [x] **Breakout board design** — KiCad layout with two 13-pin mini DIN connectors and 2.54mm pin headers (ground adjacent to each signal) using Kenwood signal names on silkscreen. (DN-KRC3006-04)
- [x] **Connector footprint verification** — 3D-printed mockup confirmed pin spacing before committing to fab.
- [x] **Breakout board ordered** — 3 boards, OSH Park standard fab.
- [X] **Completed TP-KRC3006-02** — Recieve, inspect, assemble and verify passthrough breakout board serial number 1.
- [X] **Set up test bench** — Prepare bench wiring, logic analyzer connections, and head unit power for breakout board arrival.
- [X] **Troubleshoot CX85** — Initial tests have shown that the CD changer laser diode may be dirty or degraded over time. Unit has been deemed inoperable. Further testing will be carried out with a KDC-C717 CD changer 

## What This Project Does

This project emulates a Kenwood CD changer on the 13-pin round DIN connector used by mid-1990s Kenwood head units. The emulator responds to all head unit commands (play, stop, next/previous track, disc selection, repeat, shuffle) and streams audio from a Raspberry Pi through the stereo's built-in amplifier.

### Features (Planned)

- **Full protocol emulation** — Head unit displays disc number and track number.
- **10 virtual disc slots** — Map folders or playlists to CD1–CD0, just like a real magazine.
- **Web-based control interface** — Manage your music library from your phone over WiFi.
- **Automotive power management** — Supercapacitor-backed graceful shutdown, cranking ride-through, battery monitoring.
- **WiFi standby mode** — When parked at home, the Pi stays on and connects to your home network for easy music transfers and system updates.
- **Custom Raspberry Pi HAT** — Single PCB with ATtiny1616 protocol controller, PCM5102A I2S DAC, automotive power supply, designed for JLCPCB or similar assembly.

## Target Hardware

| Component | Role |
|-----------|------|
| Kenwood KRC-3006 (or similar mid-90s Kenwood head unit) | The stereo — device under test |
| Kenwood KDC-C717| CD Auto Changer |
| Raspberry Pi | Media server, web interface, audio playback |
| ATtiny1616 | Real-time Kenwood protocol handler (on custom HAT) |
| PCM5102A I2S DAC | Digital-to-analog audio conversion |
| SSD | Music storage (avoids SD card corruption) |
| SparkFun USB Logic Analyzer | Protocol capture and analysis |

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
│   ├── TP-KRC3006-01.odt    # Test plan 3: Emulator test procedure (IEEE 829)
│   ├── TL-KRC3006-03.ods    # Test log 3: Companion log workbook to TP-KRC3006-03
│   ├── DN-KRC3006-01.md     # Design note 1: HAT design research
│   ├── DN-KRC3006-02.md     # Design note 2: Schematic analysis
│   ├── DN-KRC3006-03.md     # Design note 3: Bluetooth stretch goal
│   ├── DN-KRC3006-04.md     # Design note 4: Breakout board design
|   ├── DN-KRC3006-05.md     # Design note 5: Web Application Design for Emulator Library Management
|   ├── DN-KRC3006-06.md     # Design note 6: Kenwood CD Changer Error Codes
│   ├── protocol/            # Protocol captures and decoded data
│   └── records/             # Completed test logs
├── firmware/                # ATtiny1616 firmware (Arduino/megaTinyCore)
│   └── src/
├── software/                # Raspberry Pi software
│   ├── flask-app/           # Web interface
│   ├── mpd-config/          # Music player daemon configuration
│   ├── power-mgmt/          # ATtiny UART bridge and power state management
│   └── wifi-manager/        # AP/client mode switching
├── hardware/                # KiCad PCB design files
│   ├── kicad/               # Schematic and layout
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

The project follows a documentation-first approach using IEEE 829-inspired test procedures. All documentation is in the `docs/` directory. Formal documents (test plans, test logs) use Open Document Format; design notes use Markdown for GitHub rendering.

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

## Building / Contributing

This project is in early development. If you have a compatible Kenwood head unit and want to help with protocol capture, testing, or firmware development, contributions are welcome.

### Prerequisites

- [Arduino IDE](https://www.arduino.cc/en/software) with [megaTinyCore](https://github.com/SpenceKonde/megaTinyCore) installed
- [PulseView](https://sigrok.org/wiki/PulseView) for logic analyzer captures
- [KiCad](https://www.kicad.org/) for PCB design
- Python 3 with Flask for the web interface
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
