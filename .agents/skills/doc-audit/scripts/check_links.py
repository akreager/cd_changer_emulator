#!/usr/bin/env python3
"""Check that every relative link and image in the repository's Markdown files resolves.

Usage:
    python3 check_links.py [REPO_ROOT]

Run from the repository root, or pass it as an argument. External links
(http, https, mailto) and pure #anchors are skipped, and so are links inside
fenced code blocks. Handles GitHub's '/../main/<path>' form and
root-relative '/<path>' links. Exit status: 0 if every link resolves,
1 if any is broken.
"""
import os
import re
import sys
import urllib.parse

LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "node_modules"}


def markdown_files(root):
    for directory, subdirs, files in os.walk(root):
        subdirs[:] = [d for d in subdirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(".md"):
                yield os.path.join(directory, name)


def resolve(root, md_path, link):
    path = urllib.parse.unquote(link.split("#", 1)[0])
    if not path:
        return None
    if path.startswith("/../main/"):
        return os.path.join(root, path[len("/../main/"):])
    if path.startswith("/"):
        return os.path.join(root, path.lstrip("/"))
    return os.path.normpath(os.path.join(os.path.dirname(md_path), path))


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    broken = 0
    checked = 0
    for md in sorted(markdown_files(root)):
        in_fence = False
        with open(md, encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                for match in LINK.finditer(line):
                    link = match.group(1).strip("<>")
                    if link.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    target = resolve(root, md, link)
                    if target is None:
                        continue
                    checked += 1
                    if not os.path.exists(target):
                        broken += 1
                        print(f"BROKEN {os.path.relpath(md, root)}:{number}: {link}")
    print(f"checked {checked} relative links, {broken} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
