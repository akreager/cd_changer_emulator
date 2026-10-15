#!/usr/bin/env python3
"""Print every non-empty cell of an .ods workbook, with its sheet and cell reference.

Usage:
    python3 ods_cells.py LOG.ods [--sheet NAME]

Reads content.xml directly, so it works where pandas' odf reader returns empty
sheets (as it does for the TL-KRC3006 logs). Repeated rows and columns are
expanded into the right coordinates. Output lines look like:

    [Phase 1 — Static Verification] E8: PASS

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
    parser.add_argument("path", help=".ods file")
    parser.add_argument("--sheet", help="only print this sheet")
    args = parser.parse_args()

    with zipfile.ZipFile(args.path) as archive:
        content = ET.fromstring(archive.read("content.xml"))
        meta = ET.fromstring(archive.read("meta.xml"))
    generator = meta.find(f".//{META}generator")
    print(f"# {args.path}  (generator: {generator.text if generator is not None else 'unknown'})")

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
