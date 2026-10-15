---
name: odt-to-markdown
description: Convert a test plan (TP-KRC3006-NN) from .odt to Markdown with its content unchanged, prove the conversion is faithful with a word-sequence check, and update every reference to the file. Use for document control package CP-1, or for any later ODT-to-Markdown conversion.
---

# Convert a test plan from ODT to Markdown

The point of converting is that later technical revisions become reviewable diffs. That only works if the conversion itself changes no content, so keep the conversion and any fixes in separate commits.

## 1. Content stays identical

- Convert at the document's current revision.
- Make no wording, numbering or technical fixes. That includes known defects, such as backlog items DC-04 and DC-05. Those follow as separate commits.
- The one exception is a blank header field that the document's own revision history answers. List it in the pull request. Example: TP-02's header Revision field is blank, but its revision history shows Rev B.

## 2. Keep the revision letter

Add a revision-history row:

```
YYYY-MM-DD — Converted from ODT to Markdown. No content change.
```

## 3. Structure

- The header block becomes a two-column table with the same fields as the ODT.
- Headings keep their section numbers, so references like "TP-01 §4.2" still resolve.
- Procedure steps become ordered lists that keep their original step numbers.
- Tables become GFM pipe tables.
- CAUTION and NOTE callouts become blockquotes with a bold label, e.g. `> **CAUTION:** …`.
- Drop the footers. They only repeat the ID, the revision and the page number.

## 4. Starting point

```sh
pandoc -f odt -t gfm --wrap=none docs/TP-KRC3006-01.odt -o docs/TP-KRC3006-01.md
```

Then fix two pandoc quirks by hand:

- Every table comes out with an empty header row, and the real header lands in the first body row. Promote that row to the header.
- In TP-02, the §8.2 "Isolation Verification" table has cells with more than one paragraph, so pandoc emits it as raw HTML. Rebuild it as a pipe table, joining paragraphs within a cell with `<br>`.

## 5. Prove it's faithful

Run the check before you remove the `.odt`:

```sh
python3 .agents/skills/odt-to-markdown/scripts/compare_words.py docs/TP-KRC3006-01.odt docs/TP-KRC3006-01.md
```

- The script renders both files to plain text with pandoc, strips markup and table-drawing characters, and compares the word sequences.
- It exits 0 when they match, and otherwise prints every differing block.
- Every remaining difference must be formatting only. List any that aren't in the pull request.
- **Baseline at `11bc992`:** a raw pandoc conversion of TP-01 and TP-03 matches word for word. TP-02 differs only in the HTML table. A one-word content edit is caught.
- If the `.odt` is already gone, recover it from git first: `git show 11bc992:docs/TP-KRC3006-01.odt > /tmp/TP-01.odt`.

## 6. Same commit: remove the original and update the references

- Add the `.md`, and `git rm` the `.odt`. Git history keeps the original. Confirm the removal with the owner in the pull request's decisions list.
- Update every reference to the file:
  - the root `README.md`: the repository tree, the Documentation table, and the LibreOffice line under Prerequisites
  - `docs/README.md`: the register and the "File Format" section
- Then run the [doc-audit](../doc-audit/SKILL.md) skill.

## 7. Order

Convert TP-01 first, because it gates Rev C. Then do TP-03, then TP-02. Use one commit per test plan, all in one pull request.
