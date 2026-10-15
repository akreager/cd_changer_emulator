#!/usr/bin/env python3
"""Print every non-empty cell of an ODF spreadsheet, with its sheet and cell reference.

Usage:
    python3 ods_cells.py LOG.fods [--sheet NAME]
    python3 ods_cells.py LOG.ods  [--sheet NAME]

Reads both flat (.fods, a single XML file) and zipped (.ods) spreadsheets. It
detects the format from the file's content, not its name, so it also works as
a git textconv driver, which hands it temporary files. Repeated rows and
columns are expanded into the right coordinates. Output lines look like:

    [Phase 1 — Static Verification] E8: PASS

Automatic style names and view settings aren't printed, so two saves of the
same data produce identical output. That makes this the way to diff logs:
LibreOffice renumbers styles on every save, which floods a raw XML diff.

Uses only the Python 3 standard library.
"""
import argparse
import sys
import zipfile
from xml.etree import ElementTree as ET

TABLE = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
TEXT = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"
META = "{urn:oasis:names:tc:opendocument:xmlns:meta:1.0}"
OFFICE = "{urn:oasis:names:tc:opendocument:xmlns:office:1.0}"


def load(path):
    """Return (content root, meta root) for a flat or zipped ODF spreadsheet."""
    with open(path, "rb") as handle:
        zipped = handle.read(2) == b"PK"
    if zipped:
        with zipfile.ZipFile(path) as archive:
            content = ET.fromstring(archive.read("content.xml"))
            meta = ET.fromstring(archive.read("meta.xml"))
        return content, meta
    root = ET.parse(path).getroot()
    return root, root


def column_letters(index):
    letters = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def cell_text(cell):
    paragraphs = ["".join(p.itertext()) for p in cell.iter(TEXT + "p")]
    text = " / ".join(p for p in paragraphs if p.strip())
    return text or cell.get(OFFICE + "value") or ""


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("path", help=".fods or .ods file")
    parser.add_argument("--sheet", help="only print this sheet")
    args = parser.parse_args()

    content, meta = load(args.path)
    generator = meta.find(f".//{META}generator")
    print(f"# generator: {generator.text if generator is not None else 'unknown'}")

    for sheet in content.iter(TABLE + "table"):
        name = sheet.get(TABLE + "name")
        if args.sheet and name != args.sheet:
            continue
        print(f"\n## {name}")
        row_number = 1
        for row in sheet.iter(TABLE + "table-row"):
            rows_repeated = int(row.get(TABLE + "number-rows-repeated", "1"))
            column = 0
            for cell in row:
                if cell.tag not in (TABLE + "table-cell", TABLE + "covered-table-cell"):
                    continue
                columns_repeated = int(cell.get(TABLE + "number-columns-repeated", "1"))
                text = cell_text(cell)
                if text:
                    suffix = f" (repeated x{rows_repeated} rows)" if rows_repeated > 1 else ""
                    print(f"[{name}] {column_letters(column)}{row_number}: {text}{suffix}")
                column += columns_repeated
            row_number += rows_repeated
    return 0


if __name__ == "__main__":
    sys.exit(main())
