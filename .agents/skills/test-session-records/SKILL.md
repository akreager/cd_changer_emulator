---
name: test-session-records
description: Prepare the documents for a bench session, and close one out afterwards. Use before a session to check that the test plan and log match and the entry criteria are met. Use after a session to check the filled log and captures, publish the PDF record, and update the registers.
---

# Bench session records

The owner runs the bench. This skill keeps the documents in step with it.

## Before a session

Start this when the owner says a session is coming.

1. **The TP and the TL match.** The TP revision for the phase is released, and it matches its TL tab: the tab name, the step numbers and the columns. Use the [read-odf](../read-odf/SKILL.md) skill to read the tab.
2. **The entry criteria are met on paper.** The previous phase has an overall result, and its incidents are logged. If they aren't, say so before the session, not after it.
3. **Pre-fill the TL header:**
   - the TL revision
   - the equipment register, with models and serials (MOD-03 S/N 1, the logic analyzer, the DMM, the PSU)
   - the PulseView version
4. **Give the owner a short session sheet:**
   - the capture file names to use (`P[phase]_[description]_[NNN].sr` with a matching `.png`, TP-01 §6)
   - what each step must record
5. If the TP's technical content looks wrong, route it to the architect. Don't edit it.

## After a session

1. **Collect from the owner:** the filled TL (`.ods`), every capture (`.sr` and `.png`), and any photos.
2. **Check that the log is complete.** Report each gap with its sheet and cell reference.
   - Every row has a result, a P/F and a date.
   - The phase has an overall result.
   - Every deviation from "Expected" has an incident (Critical, Major, Minor or Observation).
   - Units are present and correct.
   - The Capture File Log, the files and the naming all agree.
3. **Send the gaps back to the owner as questions.** Don't fill them yourself ([rules/evidence.md](../../rules/evidence.md)).
4. **Once the log is complete:**
   - Commit the live TL to `docs/`.
   - Export a PDF snapshot of the whole TL to `docs/records/`, named `{TL-ID}-{phase}-{YYYYMMDD}` with the completion date.
   - Render the snapshot's pages and check for clipped cells before you commit it.
   - Commit the captures to `captures/`.
   - Update every register ([rules/documents.md](../../rules/documents.md)): the records tables, the phase progress, and the README status sections.
   - Under "For the architect", list the design-note statements that the results settle or contradict.
5. **Deliver it as one change package,** then run the [doc-audit](../doc-audit/SKILL.md) skill.
