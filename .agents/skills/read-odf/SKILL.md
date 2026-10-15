---
name: read-odf
description: Read the project's ODF documents and records. Use it for the cells of a test log (.fods or .ods) with sheet and cell references, a cell-level diff between two versions of a log, the text of an .odt document, or the text and layout of a record PDF in docs/records/.
---

# Read and diff logs, documents and records

## Test logs (`.fods` or `.ods`)

```sh
python3 .agents/skills/read-odf/scripts/ods_cells.py docs/TL-KRC3006-01.fods
python3 .agents/skills/read-odf/scripts/ods_cells.py docs/TL-KRC3006-01.fods --sheet "Phase 1 — Static Verification"
```

- This prints every non-empty cell as `[sheet] E8: value`, plus the file's generator.
- It reads flat (`.fods`) and zipped (`.ods`) files, and detects which from the content.
- Use the cell references when you report a gap, e.g. "Phase 1 tab, E8 (P/F) blank".
- A blank cell prints nothing. To prove a cell is empty, check that its reference is missing from the output.
- Don't use pandas' odf reader. It returns empty sheets for these logs.
- A `.fods` file is plain XML, so you can grep it directly. Don't judge a change from its raw diff, though; see the next section.

## Diff two versions of a log

LibreOffice renumbers its internal cell styles on every save. On the TL-01 log, a save with no edits rewrites about 1,200 lines of XML, so a raw diff hides the real change. Diff the cell values instead.

**One-time setup per clone.** `.gitattributes` already routes `*.fods` through this driver:

```sh
git config diff.odscells.textconv "python3 .agents/skills/read-odf/scripts/ods_cells.py"
```

**Then use git as usual:**

```sh
git diff -- docs/TL-KRC3006-01.fods
git log -p -- docs/TL-KRC3006-01.fods
```

Each changed cell shows as one `-`/`+` line pair:

```
-[Phase 1 — Static Verification] F27: 5.15
+[Phase 1 — Static Verification] F27: 5.16
```

**Comparing two files outside git:**

```sh
diff <(python3 .agents/skills/read-odf/scripts/ods_cells.py old.ods) <(python3 .agents/skills/read-odf/scripts/ods_cells.py new.fods)
```

The first output line, `# generator:`, differs between LibreOffice and other writers. Ignore it.

## `.odt` documents

```sh
pandoc -f odt -t plain --wrap=none docs/TP-KRC3006-02.odt
```

- Pandoc drops headers and footers. In this project's test plans they only repeat the document ID, the revision and the page number.
- In Markdown output, pandoc writes an em dash in a field as `---`. Check the plain-text output for the real character.

## Record PDFs (`docs/records/`)

```sh
pdftotext -layout docs/records/TL-KRC3006-01-P1-20260419.pdf -
pdftoppm -r 80 -png docs/records/TL-KRC3006-01-P1-20260419.pdf /tmp/rec
```

- Use `pdftotext` for the words, and render the pages with `pdftoppm` to check the layout.
- Text extraction hides clipped cells and misaligned columns. For example, column A is cut off on pages 3–6 of the TL-01 Phase 1 record, which only shows in the rendered pages.
- When a record and its working log disagree, the record is what was published. Report the difference; don't resolve it ([rules/evidence.md](../../rules/evidence.md)).
