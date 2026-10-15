#!/usr/bin/env python3
"""Check that a Markdown conversion has the same words as its source document.

Usage:
    python3 compare_words.py SOURCE.odt CONVERTED.md [--show N]

Both files are rendered to plain text with pandoc. Markup and table-drawing
characters are stripped, quotes and dashes are normalized, and the two word
sequences are compared. Formatting changes (headings, tables, lists, emphasis)
don't show up as differences; changed, added or missing words do.

Exit status: 0 if the word sequences match, 1 if they differ, 2 on error.
Requires pandoc on PATH.
"""
import argparse
import difflib
import re
import shutil
import subprocess
import sys

QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'",
                        " ": " ", "…": "..."})
MARKUP = re.compile(r"[|*_`#>+=\\\-–—]+")


def plain_text(path):
    source_format = "odt" if path.lower().endswith(".odt") else "gfm"
    result = subprocess.run(
        ["pandoc", "-f", source_format, "-t", "plain", "--wrap=none", path],
        capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed on {path}: {result.stderr.strip()}")
    return result.stdout


def words(text):
    return MARKUP.sub(" ", text.translate(QUOTES)).split()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("source", help="original document (.odt)")
    parser.add_argument("converted", help="Markdown conversion (.md)")
    parser.add_argument("--show", type=int, default=20, help="differences to print (default 20)")
    args = parser.parse_args()

    if shutil.which("pandoc") is None:
        print("error: pandoc is not installed", file=sys.stderr)
        return 2
    try:
        a = words(plain_text(args.source))
        b = words(plain_text(args.converted))
    except (RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    diffs = [op for op in matcher.get_opcodes() if op[0] != "equal"]
    print(f"source words: {len(a)}  converted words: {len(b)}  differing blocks: {len(diffs)}")
    for tag, i1, i2, j1, j2 in diffs[:args.show]:
        context = " ".join(a[max(0, i1 - 6):i1])
        print(f"\n[{tag}] after: ...{context}")
        print(f"  source:    {' '.join(a[i1:i2])[:300] or '(nothing)'}")
        print(f"  converted: {' '.join(b[j1:j2])[:300] or '(nothing)'}")
    if len(diffs) > args.show:
        print(f"\n... {len(diffs) - args.show} more")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
