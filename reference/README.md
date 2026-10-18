# Reference Documentation

Datasheets, service manuals, and other cited reference material for the KRC-3006 CD changer emulation project.

---

## Cited References

| Ref | Title | Source | Notes |
|---|---|---|---|
| REF-001 | [KRC-3006 Owner's Manual](https://archive.org/details/manualzilla-id-6478282/mode/2up?q=kenwood+%22krc-3006%22) | Internet Archive / Manualzilla | Original owner's manual for the Kenwood KRC-3006 AM/FM cassette receiver |
| REF-002 | [Kenwood CDC Protocol Documentation](https://www.mictronics.de/) | Mictronics | Kenwood O-protocol and C-protocol command tables; primary protocol reference |
| REF-003 | [Kenwood Slim CD Changer Emulator](https://www.elektroda.pl/rtvforum/topic536235.html) | Elektroda.pl / szymtro | 8051-based emulator implementation; key community reference for protocol behavior |
| REF-004 | KRC-3006 Service Manual | *Source TBD* | Factory service manual for the KRC-3006 head unit |
| REF-005 | [KDC-CX85/CPS85 Service Manual](https://www.manualslib.com/manual/836703/Kenwood-Kdc-Cx85.html) | Factory manual hosted by ManualsLib | B51-7552-00, verified on cover; historical CX85 analysis, not C717 circuitry. |
| REF-006 | [SparkFun USB Logic Analyzer — TOL-18627](https://www.sparkfun.com/usb-logic-analyzer-24mhz-8-channel.html) | SparkFun product page, checked 2026-10-17 | R-1.1 source: 8 channels, 24 MHz maximum, 5.25 V maximum input, HIGH ≥2.0 V, LOW ≤0.8 V, >100 kΩ / 5 pF. The page warns against using the supposed GND adjacent to input 6 on affected units. |
| REF-007 | [KDC-C517FM / KDC-C717/Y Service Manual](https://www.manualslib.com/manual/850190/Kenwood-Kdc-C517fm.html) | Factory manual hosted by ManualsLib | B51-7731-00, verified on cover. Interface analysis still pending. |
| REF-008 | [KDC-C717/C667/C467 Instruction Manual](https://www.manualslib.com/manual/896906/Kenwood-Kdc-C717.html) | Factory manual hosted by ManualsLib | Public manual located; equivalence to DN-06's project copy B64-1652-00 has not been verified. Do not infer an edition number from the model alone. |

Only links and short factual citations are retained here; no manuals or datasheets are hosted. REF-004 still needs a verified public source. A public copy of REF-008 is not proof that it is the same edition as the owner's project file.

## Revision History

| Rev | Date | Author | Changes |
|---|---|---|---|
| — | 2026-10-17 | A. Kreager | DC-14 / R-1.1: add verified SparkFun limits source and public CX85/C717 manual links; record remaining source/edition gaps. |
| — | 2026-10-17 | A. Kreager | R-1.1: add the SparkFun analyzer limits source. |
