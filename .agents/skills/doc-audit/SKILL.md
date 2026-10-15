---
name: doc-audit
description: Check that the documentation agrees with itself. It covers broken links, registers out of step with the files, unpaired test plans and logs, misfiled records, and stale terms that contradict the technical baseline. Run it before every document change package and at every phase gate, and report the results in the pull request.
---

# Documentation audit

Run all three steps from the repository root, and paste the results into the pull request under "Checks run".

## 1. Links

```sh
python3 .agents/skills/doc-audit/scripts/check_links.py
```

This checks every relative link and image in every Markdown file, including GitHub's `/../main/<path>` form. It skips external links and fenced code blocks. It exits 1 if any link is broken.

## 2. Registers

```sh
python3 .agents/skills/doc-audit/scripts/check_registers.py
```

This checks the following:

- every TP, TL and DN file has a table row in `docs/README.md` and in the root `README.md`
- no document exists in two formats at once, e.g. half-way through a conversion
- every TP has a TL with the same number, and every TL has a TP
- `docs/records/` holds only PDFs
- every record is listed in both records tables, and every listed record exists

**Baseline at `11bc992`:** it reports the three known problems with `docs/records/TL-KRC3006-02-01-20260401.odt` (backlog DC-12, decision D-7).

The script checks that rows exist; it doesn't check that their content is right. Also read the register rows you touched against the files: status, revision, file extension and description. Then check the root README's status sections (Current Milestone, Immediate To-Do, Completed) against the latest records.

## 3. Stale terms

Each command below is followed by what its hits usually mean.

```sh
grep -rnE '100K(\+| series| on)|200K|slow[^.]{0,20}edges|rounded edges|τ ≈ 6' docs README.md hardware/kicad/*/README.md
```
Superseded bus-impedance claims (DN-02 Rev C). Expect one false positive: DN-02's 100K/(100K+10K) divider.

```sh
grep -rnE 'Flask|MPD|mplayer|Pi 4|Arduino' docs/*.md README.md
```
A legacy stack or controller. DN-05's FastAPI-versus-Flask comparison and the Arduino IDE toolchain are correct.

```sh
grep -rnE 'AGND|[Aa]udio [Gg]round' docs README.md hardware/kicad/*/README.md
```
Pin 6 called the audio ground. Its factory name is D. GND.

```sh
grep -rn 'CX85' docs/*.md
```
Forward-looking actions only. Historical analysis of the KDC-CX85 is fine.

```sh
grep -rn 'TBD' docs README.md reference/README.md
```
Gaps to track in the backlog.

- Zipped `.odt` and `.ods` files need text extraction before they can be searched. Flat `.fods` and `.fodt` files are XML, so grep reads them directly. See the [read-odf](../read-odf/SKILL.md) skill.
- Check every hit against [context/technical-baseline.md](../../context/technical-baseline.md). A hit that contradicts a settled item becomes a backlog item. A hit that states an open item as settled also becomes a backlog item.
