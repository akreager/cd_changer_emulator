#!/usr/bin/env python3
"""Check that the document registers agree with the files in docs/.

Usage:
    python3 check_registers.py [REPO_ROOT]

Checks:
  1. Every TP/TL/DN file in docs/ has a table row in docs/README.md (the master
     register) and in the root README.md (the Documentation table).
  2. Every TP has a TL with the same number, and every TL has a TP.
  3. docs/records/ holds only PDFs (plus README.md), and every record appears
     in a table row of both records tables.
  4. Every record named in either records table exists in docs/records/.

Exit status: 0 if everything agrees, 1 if anything doesn't.
Uses only the Python 3 standard library.
"""
import os
import re
import sys

DOC_FILE = re.compile(r"^((TP|TL|DN)-KRC3006-(\d{2}))\.(md|odt|ods)$")
RECORD_NAME = re.compile(r"TL-KRC3006-\d{2}-[A-Za-z0-9]+-\d{8}(?:-S\d+)?")


def table_rows(path):
    with open(path, encoding="utf-8") as handle:
        return [line for line in handle if line.lstrip().startswith("|")]


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    docs = os.path.join(root, "docs")
    records = os.path.join(docs, "records")
    registers = {
        "docs/README.md": table_rows(os.path.join(docs, "README.md")),
        "README.md": table_rows(os.path.join(root, "README.md")),
    }
    problems = []

    ids = {}
    for name in sorted(os.listdir(docs)):
        match = DOC_FILE.match(name)
        if match:
            ids.setdefault(match.group(1), []).append(name)
    for doc_id, files in ids.items():
        if len(files) > 1:
            problems.append(f"{doc_id} exists in more than one format: {', '.join(files)}")
        for register, rows in registers.items():
            if not any(doc_id in row for row in rows):
                problems.append(f"{doc_id} has no table row in {register}")

    numbers = lambda kind: {i.split("-")[-1] for i in ids if i.startswith(kind)}
    for missing in sorted(numbers("TP") - numbers("TL")):
        problems.append(f"TP-KRC3006-{missing} has no paired TL-KRC3006-{missing}")
    for missing in sorted(numbers("TL") - numbers("TP")):
        problems.append(f"TL-KRC3006-{missing} has no paired TP-KRC3006-{missing}")

    record_stems = set()
    for name in sorted(os.listdir(records)):
        if name == "README.md":
            continue
        stem, extension = os.path.splitext(name)
        if extension.lower() != ".pdf":
            problems.append(f"docs/records/{name} is not a PDF (records are PDF only)")
        record_stems.add(stem)
        for register, rows in registers.items():
            if not any(stem in row for row in rows):
                problems.append(f"record {name} has no table row in {register}")
    for register, rows in registers.items():
        for row in rows:
            for named in RECORD_NAME.findall(row):
                if named not in record_stems:
                    problems.append(f"{register} lists record {named}, which isn't in docs/records/")

    for problem in problems:
        print(f"PROBLEM {problem}")
    print(f"checked {len(ids)} documents and {len(record_stems)} records, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
