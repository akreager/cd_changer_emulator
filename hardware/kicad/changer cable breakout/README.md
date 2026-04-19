# KRC-3006 Pass-Through Breakout Board (DN-KRC3006-04)

## Purpose

This KiCad project implements a passive, pass-through breakout board for the Kenwood KRC-3006 head unit's 13-pin mini DIN connector. The board provides:

- **Signal routing** between the KRC-3006 and connected CD autochanger.
- **Accessible test points** for bus signal analysis and protocol reverse engineering.
- **Isolated audio path** with independent head unit and changer TRS audio jack connectors.

## Current Status

**COMPLETE AND TESTED** — Boards received 2026-03-28 from OSH Park. Assembly and verification of S/N 1 completed 4/5. Breakout board is fully functional and ready for protocol reverse engineering work.  
![Picture of assembled break-out board](/../main/assets/breakout_board_01.jpg)

## Schematic Summary

| Ref Des | Component | Function |
|---|-------|-------|
| J1 | SDD-130J, 13-pin mini DIN female | Head unit side connector (front side) |
| J2 | SDD-130J, 13-pin mini DIN female | Changer side connector (back side) |
| J3 | 1×11 female pin header, 2.54 mm pitch | Digital/control signal test points |
| J4 | STX-3100-3NB, 3.5 mm TRS audio jack | Head unit side audio breakout |
| J5 | STX-3100-3NB, 3.5 mm TRS audio jack | Changer side audio breakout |

## J1/J2 Pinout

| Pin | Signal | Description |
|-----|--------|-----------|
| 1 | REQ H (Active Low)  | Request handshake output from head unit. |
| 2 | GND | Audio ground. |
| 3 | B.U.  | Battery Unswitched. |
| 4 | ON  | Changer connect/enable signal. |
| 5 | MUTE  | Mute request line. |
| 6 | D. GND | Digital ground. |
| 7 | RESET  | Reset pulse output to changer. |
| 8 | R CH  | Right audio channel, analog. |
| 9 | REQ C (Active Low)  | Request handshake output from changer to head unit. |
| 10 | DATA C  | Serial data from changer to head unit. |
| 11 | DATA H  | Serial data from head unit to changer. |
| 12 | L CH  | Left audio channel, analog. |
| 13 | CLK (Active Low)  | Synchronous clock. |

## J3 Pinout

|  J3 Pin  |  J1 Pin  |  Signal  |
| --- | --- | --- |
| 1 | 2 |  GND  |
| 2 | 4 |  ON (CH-CON)  |
| 3 | 3 |  B.U. (+14V)  |
| 4 | 7 |  RESET  |
| 5 | 6 |  D. GND  |
| 6 | 1 |  REQ H (Active Low)  |
| 7 | 9 |  REQ C (Active Low)  |
| 8 | 5 |  MUTE  |
| 9 | 10 |  DATA C  |
| 10 | 11 |  DATA H  |
| 11 | 13 |  CLK (Active Low)  |

## J4 Pinout

| J4 Pin | J1 Pin | Signal |
| --- | --- | --- |
| 1 | 2 | GND |
| 2 | 8 | L CH to head unit |
| 3 | 12 | R CH to Head unit |

## J5 Pinout

| J5 Pin | J2 Pin | Signal |
| --- | --- | --- |
| 1 | 2 | GND |
| 2 | 8 | L CH from changer |
| 3 | 12 | R CH from changer |

## Audio Interception

The audio channels (Pin 8 - R CH and Pin 12  L CH) are not routed as a direct pass-through between J1 and J2. Instead, they are broken out to two 3.5 mm TRS audio jacks mounted on the right edge of the board:

- **J4** — Head unit side audio. Tip = R CH, Ring = L CH, Sleeve = GND.
- **J5** — Changer side audio. Tip = R CH, Ring = L CH, Sleeve = GND.

The audio jacks use a standard 3-conductor (TRS) footprint with no switching contacts. When nothing is plugged in, the audio pins on both the head unit and changer sides float.

This topology enables three operating modes:

| Mode | Configuration | Use Case |
|---|---|---|
| **Audio pass-through** | Connect J4 to J5 with a male-to-male 3.5 mm TRS cable. | Normal protocol capture with authentic changer audio reaching the head unit. |
| **Audio intercept** | Connect monitoring equipment (oscilloscope, audio recorder, powered speakers) to J5. | Listen to or record the changer's audio output without routing it to the head unit. |
| **Audio injection** | Connect an external audio source to J4. Leave J5 disconnected or connected to monitoring equipment. | Feed test tones or music from a phone, DAC, or Raspberry Pi directly into the head unit's audio input path. Useful for verifying the audio path independently of changer protocol state. |

Audio pass-through requires the external cable. The board cannot function as a fully transparent sniffer without it. This is an intentional design decision — the separate jacks provide flexibility that a hardwired pass-through cannot.

## Next Steps

This board is now ready to support:
1. **TP-KRC3006-01 Phase 1** — Passive capture of KRC-3006 ↔ KDC-C717 traffic
2. **TP-KRC3006-01 Phase 2a/2b** — Analysis with head unit alone, then with real changer through breakout
3. **TP-KRC3006-03** — Emulator development and integration testing

## References

- Service manual: Kenwood KRC-3006 Cassette Head Unit
- Service manual: Kenwood KDC-C717 CD Changer
- Related design docs: DN-KRC3006-02 (Schematic Analysis), DN-KRC3006-04
