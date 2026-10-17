# Tools

Helper scripts for the repository. Each one documents its own usage in its header.

| Script | What it does |
|---|---|
| [scrub_images.py](scrub_images.py) | Strips location and other metadata from JPEG and PNG files without re-encoding, and renames them web-safe. Dry run by default; `--apply` changes files; `--check` exits 1 if anything needs scrubbing. Standard library only. |

Run `python3 tools/scrub_images.py --apply <files or folders>` on every photo before you commit it.
