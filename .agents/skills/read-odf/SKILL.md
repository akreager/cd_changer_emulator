---
name: read-odf
description: Read the project's binary documents. Use it for the cells of an .ods test log (with sheet and cell references), the text of an .odt document, or the text and layout of a record PDF in docs/records/. Use it whenever you need to check what a log or record actually says.
---

# Read logs, documents and records

## `.ods` test logs (TL-KRC3006-NN)

```sh
python3 .agents/skills/read-odf/scripts/ods_cells.py docs/TL-KRC3006-01.ods
python3 .agents/skills/read-odf/scripts/ods_cells.py docs/TL-KRC3006-01.ods --sheet "Phase 1 — Static Verification"
```

- This prints every non-empty cell as `[sheet] E8: value`, plus the file's generator.
- Use the cell references when you report a gap, e.g. "Phase 1 tab, E8 (P/F) blank".
- Don't use pandas' odf reader. It returns empty sheets for these logs.
- A blank cell prints nothing. To prove a cell is empty, check that its reference is missing from the output.

## `.odt` documents

```sh
pandoc -f odt -t plain --wrap=none docs/TP-KRC3006-02.odt
```

- Pandoc drops headers and footers. In this project's test plans they only repeat the document ID, the revision and the page number.
- Pandoc prints an em dash in a field as `---` in Markdown output. Check the plain-text output for the real character.

## Record PDFs (`docs/records/`)

```sh
pdftotext -layout docs/records/TL-KRC3006-01-P1-20260419.pdf -
pdftoppm -r 80 -png docs/records/TL-KRC3006-01-P1-20260419.pdf /tmp/rec
```

- Use `pdftotext` for the words, and render the pages with `pdftoppm` to check the layout.
- Text extraction hides clipped cells and misaligned columns. For example, column A is cut off on pages 3–6 of the TL-01 Phase 1 record, which only shows in the rendered pages.
- When a record and its working log disagree, the record is what was published. Report the difference; don't resolve it ([rules/evidence.md](../../rules/evidence.md)).
