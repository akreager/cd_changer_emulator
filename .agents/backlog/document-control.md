# Backlog: document control

This is the live work list for the document control agent ([handoff](../handoffs/document-control.md)).

- IDs are permanent. Add new items with the next free DC number.
- Close an item by setting its status to `Closed (#PR)`.
- Items DC-01 to DC-19 were verified against `main` @ `11bc992` (2026-10-09). Line numbers are as of that commit; find each passage by its quoted text. Later items give the date they were added.

CP-1 status: Closed ([#5](https://github.com/akreager/cd_changer_emulator/pull/5)); merged before this work.

Work update (2026-10-17, baseline `b814b06`): approved rulings R-1–R-6 applied in review drafts. TP-01/TL-01 Rev C, DN-04 Rev D and FIX-01 instructions are prepared; Phase 1 supplement/disposition questions remain local pending D-1 and owner answers. DN-02 Rev D, breakout labels, TP-03/TL-03 and D-10 conversions are prepared, with remaining technical decisions listed below. No bench result or published record has been changed.

Review packages (drafts, review in order): [#8 — Phase 2 readiness](https://github.com/akreager/cd_changer_emulator/pull/8), [#9 — emulation rulings](https://github.com/akreager/cd_changer_emulator/pull/9), [#10 — format/reference hygiene](https://github.com/akreager/cd_changer_emulator/pull/10). The later PRs target the preceding branch; the owner merges and retargets in sequence. Draft preparation does not close owner dispositions or establish bench acceptance.

Priorities:
- **P1:** close out Phase 1 and make TL-01 live. This must happen before any Phase 2A data exists.
- **P2:** propagate settled corrections.
- **P3:** register and README hygiene.
- **P4:** presentation.

## P1 — Phase 1 closeout

### DC-01 · E/P — The live TL-01 is still the blank template
- Status: Closed 2026-10-15, by commit "docs: commit TL-KRC3006-01 as the live log, in flat ODF". The restored log is `docs/TL-KRC3006-01.fods`, and its cell values are identical to the owner's file.
- Finding: `docs/TL-KRC3006-01.ods` is the blank Rev B template, and its generator is ODFPY. The Phase 1 results exist only in the PDF record, so Phase 2A results would go into a log that doesn't contain Phase 1.
- Evidence: the template's `content.xml` has no results, but `docs/records/TL-KRC3006-01-P1-20260419.pdf` does.
- Update 2026-10-15:
  - This was deliberate. The owner holds a filled log back until all of its phases are done.
  - The filled log is untracked in his local clone, as `docs/records/TL-KRC3006-01-20260419.ods`. All 156 Phase 1 values match the published record.
  - It was re-saved by Excel on 2026-06-03, which renamed the sheets and dropped the page setup. The architect has restored both and converted the log to `.fods`.
- Action: if D-11 says to commit each phase, commit the restored log as `docs/TL-KRC3006-01.fods`. Either way, make `docs/README.md`'s rule for the working log match D-11.

### DC-02 · T (the owner dispositions) — The Phase 1 record has gaps
- Update 2026-10-17: Supplement and gap questions drafted locally for owner disposition; original record and 146 nonempty Phase 1 live-log cells preserved. Publication awaits D-1 and completed entries. Added questions for untested audio pins and the date/setup of the changer-present observation.
- Status: Open
- Findings in the record:
  - The Overall Result is blank.
  - The pin 2↔6 continuity test has no P/F.
  - Step 4 records the idle current as ".49V". The unit is wrong for a current, the value is below the 0.5–1.5 A expectation, and the step is marked PASS. Step 3's note says ".4A".
  - The pin 2 note "7.5 OHM" doesn't say what was measured, or to what.
  - Pin 6 is noted as "REFERENCE", but TP-01 §4.1.3 says to measure relative to pin 2.
  - No incidents are logged for these deviations:
    - ON polarity was the opposite of TP-01's expectation.
    - MUTE and RESET idle at 0 V, against an expected HIGH.
    - DATA C idles HIGH, against an expected LOW.
    - Phase 1 ran with the C717 and MOD-03 connected. TP-01 §4.1 says "no changer connected" and names MOD-02.
  - The equipment register's date, tester and serials are blank, and so are the PSU and DMM models. MOD-03 S/N 1 isn't recorded.
  - No test record contains the "won't select CD-CH without a changer" observation.
- Evidence: the record PDF (pages 1, 2 and 6) and TP-01 §4.1–4.1.3.
- Action:
  - Draft a Phase 1 supplement under decision D-1. List each gap, with a blank for the owner's disposition.
  - Draft the incidents as Observations for the owner to confirm.
  - Ask the owner when and where the CD-CH observation was made.
  - Publish only after the owner completes the supplement.

### DC-03 · E — The template, the TP and the record disagree
- Update 2026-10-17: Prepared the step 1–5 crosswalk and proposed future Tester/P/F columns in the closeout draft. Do not invent the missing step 1 or relabel April results. Historical correction/disposition awaits owner evidence.
- Status: Open
- Finding: the Initial Power-Up steps don't line up:
  - TL-01 template: steps 1–4
  - TP-01 §4.1.2: steps 1–5
  - record: steps 2–5

  The record also drops the template's Tester column (power-up table) and its P/F column (voltage table).
- Evidence: the template's `content.xml`, record page 2, and TP-01 §4.1.2.
- Action: reconcile these in the next TL-01 revision, matched to TP-01 Rev C. Wait for the architect's Rev C content first.

### DC-04 · T (architect) + E — TP-01 Rev B defects
- Update 2026-10-17: R-1 applied: TP-01 Rev C and matching TL-01 forms drafted; TP-03 phase references clarified. R-1.4 ignition timing-reference method still needs an architect ruling (new DC-28). Trace table prepared in the review report.
- Status: Open
- Findings:
  - (a) Phase 2A is head-unit-only: select CD-CH with no changer connected, and expect DATA C to be "completely flat". That contradicts the inline-capture finding.
  - (b) Phase 1's objective ("no changer connected") and entry criteria (MOD-02) don't match how Phase 1 was actually run.
  - (c) Phase 2A points to the tab "Phase 2 — Idle Capture", but the tab is named "Phase 2A — Idle Capture".
  - (d) The pin table calls pin 2 "Digital Ground" and pin 6 "AGND / Audio Ground"; the factory names supersede both (technical baseline). It also still expects CH-CON to be active-LOW, although Phase 1 measured active-HIGH. That question is still open (technical baseline).
  - (e) Rev B carries only some of the test additions recommended in DN-02 §8 and §17. These are missing:
    - the pull-down resistance check
    - pin 3 staying constant across source changes
    - a clock-direction watch
    - a capture that spans power-on (DN-02 §17, Phase 2 item 6). TP-01 §4.3.2 only starts capturing after power is applied.
  - (f) TP-03 still refers to "TP-KRC3006-01 Phase 2" without saying 2A or 2B.
- Action:
  - The architect writes the technical content of Rev C, as a diff on the Markdown baseline from CP-1.
  - You prepare the revision mechanics: the revision-history row, the header and the cross-references.
  - Build a trace table from DN-02 §8/§17 to TP steps. For each item that isn't adopted, give the reason.
  - Fix (c), (d) and (f) once the Rev C content lands.

## P2 — Propagate settled corrections

### DC-05 · E — Pin 2 / pin 6 naming conflicts across documents
- Update 2026-10-17: Factory names propagated in TP-01, DN-04 and breakout README; existing Phase 1 log labels retained with the historical record until DC-03 is dispositioned. New phase forms use factory names.
- Status: Open
- Finding: DN-02 §1 and the HAT README follow the factory names (2 GND, 6 D. GND). TP-01 and TL-01 call pin 2 "Digital Ground" and pin 6 "AGND / Audio Ground", and the breakout README describes pin 2 as "Audio ground".
- Action: standardize on the factory names with aliases ([rules/documents.md](../rules/documents.md), Naming). The TP/TL changes ride with Rev C (DC-04).

### DC-06 · P — DN-01 still gives the old reason for rejecting TXB/TXS
- Update 2026-10-17: Superseded 100 kΩ-series rationale removed; correct DN-02 resistances propagated. TI approximately 50 Ω guidance could not be verified from a primary document; marked source-needed, decision unchanged. Remains open for architect citation/rationale.
- Status: Open
- Finding: in "Level Shifting: SN74LVC8T245PWR", line 89 says the bus has 100K series resistors "on CLK (R146) and DATA H (R145), creating ~200K total impedance with very slow signal edges". Line 91 repeats "slow, rounded edges from the 100K resistors". DN-02 Rev C supersedes both.
- Action:
  - The decision stands. Rewrite both paragraphs on the corrected basis: the head unit's inline series resistance on the data, clock and request lines is 100 Ω–2.2 K. That's above TI's ~50 Ω source-impedance guidance for the TXB/TXS one-shot edge accelerators.
  - Cite the TI document number, or mark it `[TBD]`.
  - Add a revision-history row.

### DC-07 · P + T — DN-04 still describes 100K series impedance
- Update 2026-10-17: R-2 applied to DN-04 Rev D with dated owner risk acceptance, corrected per-pin values and FIX-01 section (R-1.5). Prepared for review.
- Status: Open
- Findings, passage by passage:

  | Passage | Line | What it says |
  |---|---|---|
  | §5 pin 1 | 55 | REQ H "100K series… changer-side R34 100K" |
  | §5 pin 11 | 85 | "R145 (100K)… R24 (100K)… ~200K… rounded edges" |
  | §5 pin 13 | 91 | "R146 (100K)… R25 (100K)… τ ≈ 6µs" |
  | §7 | 118 | "100K+ on CLK, DATA H, and REQ H" |
  | §9 "No series resistors on J3" | 171 | The rationale relies on that impedance. |

  §5 pin 2 still says to confirm 2↔6 continuity in Phase 1. That has now been confirmed.
- Action:
  - Correct the facts in §5 and §7 against DN-02 §3.1 and §12 (P). The KDC-CX85's changer-side resistors are R10, R13 and R16 at 100 Ω, not R34, R24 and R25 at 100K.
  - §9's rationale is now inverted: REQ H and DATA H are the lowest-impedance lines on the bus. The power-down reconfiguration procedure is the only protection left, and that risk has to be explicitly accepted again. This part is T and goes to the architect and the owner.

### DC-08 · P + T — DN-01 still describes the old platform and stack
- Update 2026-10-17: Software stack names and current platform propagated; original Pi 4-derived values remain visibly historical for architect review. Header standardization still awaits D-2/D-3. Pi 5 UART mapping conflict tracked in DC-26.
- Status: Open
- Finding:
  - DN-01 names the Pi 4, Flask and MPD/mplayer, and defines UART `READY` as "Flask app running". The package list at line 603 includes `flask`. The passages are at lines 19, 126, 361, 470, 491, 601–611, 625, 695–696, 711 and 717.
  - §9 item 3 (line 706) still says Phase 1 "will confirm" whether pins 2 and 6 are isolated. The Phase 1 record answers it: they're continuous.
  - The header's Date and Author are blank.
- Action:
  - Update the name and stack references to Pi 5, FastAPI and python-mpv (P, per DN-05 and the README).
  - Close §9 item 3, citing the Phase 1 record (P).
  - Values derived from the Pi 4's current draw need re-deriving: the parasitic-drain budget (§4.7) and §9 items 8 and 14. These are T and go to the architect. Don't change the numbers.

### DC-09 · T (architect) + E — DN-02 Rev C leftovers
- Update 2026-10-17: Ground-continuity observation recorded; retired-CX85/Arduino recommendations marked historical; revision history added. CLK idle claims remain untouched pending first Phase 2A capture, and the obsolete Phase 5 reference still needs architect mapping.
- Status: Open
- Reverified 2026-10-16: the root README's Completed section also repeats the CLK idle-LOW claim. DN-02 §1 repeats the obsolete Phase 1 ground-continuity question. DN-02 §10.1/§16.1 and DN-04 §5 pin 4 need the ON-polarity conflict carried forward from the Phase 1 record; do not choose a polarity. DN-02 §16.2's “Clock Is Bidirectional” heading states an open question as settled; the architect must review it against the technical baseline.
- Findings:
  - §3.1 and the HAT README say R145/R146 "define the idle LOW state" on CLK, but Phase 1 read 5.15 V on CLK (technical baseline, Open).
  - The pull-down claim hasn't been verified on the bench (DN-02 §8 item 3).
  - §10.4 and §17 still give bench actions for the KDC-CX85 (the COMMSW check) and firmware steps written for an "Arduino".
  - Line 218 says pin 6 "may be tied to Pin 2 (GND) internally", for Phase 1 to confirm. Phase 1 confirmed it.
  - §4 (line 164) refers to "Phase 5 testing", but no current test plan has a Phase 5.
  - DN-02 has no revision-history table.
- Action:
  - Hold the CLK wording until after the first 2A capture (architect).
  - Mark the CX85 and Arduino actions as historical, or move them to open items (E/P).
  - Close the pin 2/6 question, citing the Phase 1 record (P).
  - Ask the architect which phase the line 164 reference is meant to point to.
  - Add a revision-history table.

### DC-10 · P — "Arduino" is still named as the protocol controller
- Status: Closed ([#3](https://github.com/akreager/cd_changer_emulator/pull/3))
- Finding: DN-03 (lines 35, 98 and 107, e.g. "Arduino Nano firmware extension") and DN-04 §2 (line 23: "Arduino/Raspberry Pi integration architecture") name an Arduino. The protocol controller is now the ATtiny1616 (DN-01, README). The README's references to the Arduino IDE and megaTinyCore are correct; they describe the toolchain.
- Action: replace the controller name with ATtiny1616 (P), and add revision-history rows. If a passage depends on an Arduino-specific capability, flag it as T instead of rewording it.
- Resolution (2026-10-15): replaced all five controller references in [DN-03 Rev 0.2](../../docs/DN-KRC3006-03.md) and [DN-04 Rev D](../../docs/DN-KRC3006-04.md), citing DN-01 §§1–2. Added revision-history entries and updated the document register.

## P3 — Register and README hygiene

### DC-11 · E — The README tree lists directories that don't exist
- Status: Closed ([#4](https://github.com/akreager/cd_changer_emulator/pull/4))
- Finding: the root README's repository tree shows `firmware/src/`, `software/flask-app/`, `mpd-config/`, `power-mgmt/`, `wifi-manager/`, `hardware/gerbers/` and `hardware/bom/`. These paths have no tracked files, and some have legacy names.
- Action: show what exists, plus planned directories explicitly marked "(planned)". Don't invent new names; ask the owner.
- Verification (2026-10-15): all seven directories exist locally but are empty; `git ls-files` lists no files under them.
- Resolution (2026-10-15): the [README tree](../../README.md#repository-structure) marks those directories as planned, identifies the legacy software names, and distinguishes tracked documentation from future implementation content.

### DC-12 · E — A non-PDF file sits in `docs/records/`
- Status: Open
- Finding: `docs/records/TL-KRC3006-02-01-20260401.odt` breaks the PDF-only rule, and neither records table lists it. It appears to be TL-02's snapshot after its Phase 1.
- Action: decision D-7.

### DC-13 · E — TL-02 dates and a missing result
- Update 2026-10-17: Breakout README completion date corrected to record date 2026-04-10 and work order updated. DN-04 schedule labeled original targets. Missing TL-02 step 1.1 disposition remains for owner.
- Status: Open
- Reverified 2026-10-16: the breakout README's “Next Steps” calls TP-01 Phase 1 passive capture and still describes head-unit-only capture, unlike the current master register and root README. DN-04 §13 retains TBD build milestones; establish whether these are historical targets before changing them. Include this status text in the later editorial package.
- Finding: the breakout README says S/N 1 was "completed 4/5". The TL-02 record shows phase results dated 2026-04-01, 04-08 and 04-10. TL-02 step 1.1 (board outline 22 × 80 mm ±0.2) has no result in the published record.
- Action: fix the README date. Put the step 1.1 gap to the owner; he can choose a supplement under decision D-1.

### DC-14 · E — Reference register gaps
- Update 2026-10-17: REF-005 public CX85 service manual linked; REF-006 SparkFun limits and REF-007/008 C717 manuals added; root references synchronized. KRC-3006 SM public source and C717 OM edition match remain unverified.
- Status: Open
- Finding: REF-004 (KRC-3006 SM) and REF-005 (KDC-CX85 SM) are listed with "Source TBD", although DN-06 cites ManualsLib for the CX85 SM. The KDC-C717 manuals have no entries; DN-06 cites the OM as B64-1652-00, and the SM is B51-7731-00.
- Action: add public links (archive.org preferred) where they exist, and never host the PDFs. Take document numbers only from the documents themselves.

### DC-15 · E (wording needs the owner's approval) — No disclaimer
- Update 2026-10-17: One-paragraph footer drafted in the local review package; awaiting owner wording approval. Not inserted as approved text.
- Status: Open
- Finding: the repo has no non-affiliation or trademark disclaimer.
- Action: draft one paragraph for the README footer.

### DC-16 · E — Inconsistent headers and revision schemes
- Update 2026-10-17: Added histories where files changed, retained existing header/revision schemes pending D-2/D-3. DN-04 already had Rev D; retained that label as requested and added a dated row. No retrospective authorship rewrite.
- Status: Open
- Finding: see the revision-state table in the handoff (§8). DN-04's author line lists AI model names.
- Action: standardize after decisions D-2 and D-3. Until then, only add revision-history tables.

### DC-17 · E — Tester and author names vary
- Update 2026-10-17: New history rows use A. Kreager; future tester fields remain blank for AK at execution. Historical authors/testers retained pending D-3.
- Status: Open
- Finding: the names appear as "A. KREAGER", "Allen Kreager", "AK" and "Allen".
- Action: standardize going forward (decision D-3). Published records stay as they are.

### DC-20 · E — Convert the remaining test logs to flat ODF
- Update 2026-10-17: Converted TL-03 to .fods and TL-02 to .fodt in LibreOffice. TL-03 cell values identical before R-5/R-6 edits; TL-02 original 652 paragraphs/table texts identical, then conversion history added. README and TP references updated; architect-owned read-odf example needs follow-up.
- Status: Open (added 2026-10-15)
- Finding: decision D-10 makes flat ODF the log format. TL-01 is converted (DC-01). The rest isn't done yet:
  - TL-03 is `.ods`, and TL-02 is `.odt`.
  - TP-01 (§1, §6) and TP-03 refer to their logs as `.ods` files.
  - `docs/README.md` (File Format) and the root README (repository tree, Documentation table, Prerequisites) cover TL-01's `.fods`, but still list TL-02 and TL-03 in their old formats.
- Action:
  - In LibreOffice, save TL-03 as `.fods` and TL-02 as `.fodt` ("Flat XML ODF" in Save As). The cell dump from the [read-odf](../skills/read-odf/SKILL.md) skill must be identical before and after.
  - Update the README links, the tree and the format notes in the same commit.
  - Fix the TP references in their next revisions (TP-01 Rev C).

### DC-21 · P — Remove the UART baud rate from the design notes
- Update 2026-10-17: D-12 propagated in DN-01/DN-05; R-6 procedure/table drafted in TP-03/TL-03. Baud remains unspecified; candidate measurements, architect bit-time margin and owner latency limit are pending. 8N1 retained from DN-01 §4.8.
- Status: Open (added 2026-10-15)
- Reverified 2026-10-16: TP-03 §4.3.2 step 2 also specifies 9600 baud, with 38400 or 115200 as alternatives. Preserve this text in CP-1; apply D-12 in a separate revision. The accompanying rationale is technical and needs the architect's review.
- Finding: decision D-12 leaves the Pi ↔ ATtiny baud rate unspecified until hardware testing. Two design notes still state a rate:
  - DN-01 line 451: "UART (115200 baud, 8N1)"
  - DN-05 line 269: "pyserial, 115200 baud, 8N1"
- Action: replace the rate with "baud rate set during hardware testing (D-12)" and keep 8N1 only if the source supports it. Add revision-history rows. Search for any other mention with `grep -rn -i baud docs/`.

### DC-22 · T review + E — Breakout README audio-channel conflict
- Update 2026-10-17: R-4 applied to both J4/J5 tables: Tip = pin 8 R ch, Ring = pin 12 L ch, Sleeve = pin 2 GND; contact names replace fictitious numbers.
- Status: Open (added 2026-10-16)
- Finding: the [breakout README](../../hardware/kicad/changer%20cable%20breakout/README.md), J4/J5 Pinout tables, labels DIN pin 8 L CH and pin 12 R CH. Its J1/J2 table and Audio Interception section give pin 8 R CH and pin 12 L CH, as does [TP-02 §6.2](../../docs/TP-KRC3006-02.md#62-bare-board-electrical-tests), steps 1.12–1.13.
- Action: ask the architect to confirm the table correction against the hardware. Preserve both sides of the conflict until reviewed; no hardware inspection was performed in the CP-1 audit.

### DC-23 · T — Elapsed-time display requirements conflict
- Update 2026-10-17: R-5 applied to TP-03 and specified TL-03 cells; protocol time data is conditional on TP-01 Phase 2B capture, and display criteria check track/disc only.
- Status: Open (added 2026-10-16)
- Finding: [TP-03](../../docs/TP-KRC3006-03.md) §4.2.2 step 4 and §4.3.3 steps 3/4e require elapsed time on the head-unit display. [TL-03](../../docs/TL-KRC3006-03.fods), “Phase 3 — Integration” B37, expects “Time display correct”. [DN-05 §2.2](../../docs/DN-KRC3006-05.md#22-display-capabilities) says the head unit cannot display elapsed track time.
- Action: the architect reconciles the capability claim, procedures and log criteria. Preserve the source text during CP-1; document control does not change acceptance criteria.

### DC-24 · P + T — DN-02 assigns the ATtiny to a different supply rail
- Update 2026-10-17: R-3 applied in DN-02 Rev D; historical ATtiny 5 V/direct-drive recommendations marked superseded and divider struck. Existing DN-01 A/B supply assignments conflict with R-3; see DC-26 before hardware work.
- Status: Open (added 2026-10-16)
- Finding: [DN-02 §16.6](../../docs/DN-KRC3006-02.md#166-kenwood-used-five-separate-5v-rails-for-audio-quality) says “5V for Pi/ATtiny”. The [HAT README](../../hardware/kicad/emulator%20hat/README.md#design-overview) specifies the ATtiny1616 at 3.3 V.
- Action: propagate the settled controller supply voltage in a later revision. The architect reviews the surrounding rail-count and audio-quality rationale before it changes.

### DC-25 · E/P — DN-05 open questions use stale test references
- Update 2026-10-17: DN-05 capture references now point to TP-01 (Phase 2B time field / Phase 3 command mapping) and the C717; board verification remains TP-02.
- Status: Open (added 2026-10-16)
- Finding: [DN-05 §12](../../docs/DN-KRC3006-05.md#12-open-questions), item 1, points protocol capture to TP-02, whose scope is breakout-board verification ([TP-02 §2](../../docs/TP-KRC3006-02.md#2-scope)). Item 3 proposes live testing with the retired CX85; [DN-06](../../docs/DN-KRC3006-06.md) identifies the C717 as its replacement.
- Action: correct the plan reference and changer name in a later editorial/propagation revision, citing the plan scopes and DN-06.

### DC-26 · T — Hardware interface claims conflict with the propagated baseline
- Status: Open (2026-10-17)
- Evidence: DN-01 §2 assigns VCCA = 5 V / VCCB = 3.3 V, while approved R-3 specifies the bus on B at 5 V. DN-01's UART3/GPIO4/5 and device-node assignments come from its Pi 4 analysis; the target is Pi 5 and the current schematic has not been reviewed.
- Action: architect reconciles shifter A/B orientation, DIR/channel mapping and Pi 5 UART mapping against the actual design. No KiCad changes or silent wiring swaps by document control.

### DC-27 · T — DN-01's cranking-voltage measurement proposal conflicts with analyzer limits
- Status: Open (2026-10-17)
- Evidence: DN-01 §9 item 9 proposes a logic analyzer or scope on the 12 V changer supply; R-1.1 limits LA-01 input to 5.25 V and R-2 prohibits B.U. on the analyzer. DN-01 §9 item 6 also has a thermal-budget expression whose stated arithmetic needs architect review.
- Action: architect specifies appropriately rated voltage measurement equipment/probing and reviews the calculation. The old proposals are not executable approved procedures. No new probing circuit or corrected budget is invented here.

### DC-28 · T — R-1.4 lacks an ignition timing reference
- Status: Open (2026-10-17)
- Evidence: R-1.1 occupies all eight analyzer channels; R-1.4 requires time from ignition ON to first CLK edge but assigns no ignition marker.
- Action: architect supplies a safe timing-reference method. TP-01 §4.3.2 and the TL-01 power-on table mark it TBD. This does not block Phase 2A form preparation.

## P4 — Presentation

### DC-18 · E — The TL-01 record clips text
- Update 2026-10-17: Adjusted future TL-01 form widths, wrapping and print areas; exported review PDF. April published record unchanged. Original Phase 1 cells unchanged.
- Status: Open
- Finding: on pages 3–6 of the TL-01 record PDF, column A is too narrow, so titles, section labels and headers are cut off.
- Action: fix the column widths in the TL-01 template for future snapshots. Don't re-issue the April record for this alone.

### DC-19 · decision — `assets/changer_pins.png`
- Status: Open
- Finding: the image is a crop of the factory pin table.
- Action: check it against the IP posture (decision D-8).

## Already resolved (don't re-raise)

- TL-03 was added as `TL-KRC3006-03.ods` (now `.fods` under D-10). It was added on 2026-04-12 in `679f26a`; an earlier audit said it was missing.
- The format policy in both READMEs now reads "no mandated format, Markdown preferred" (`6be9221`, 2026-07-29).
- Every relative link in the Markdown files resolved at `11bc992`.
