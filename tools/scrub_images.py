#!/usr/bin/env python3
"""Strip location and other metadata from images, and give them web-safe names.

Usage:
    python3 tools/scrub_images.py PATH...            # dry run: report what would change
    python3 tools/scrub_images.py --apply PATH...    # scrub and rename in place
    python3 tools/scrub_images.py --check PATH...    # exit 1 if anything needs scrubbing (for hooks)

PATH can be files or directories (searched recursively).

What it does
- JPEG: removes every metadata segment (EXIF incl. GPS, XMP, IPTC/Photoshop,
  comments). Pixels are not re-encoded, so there's no quality loss. The EXIF
  orientation tag is kept (in a fresh, minimal EXIF block) so photos don't
  turn sideways.
- PNG: removes eXIf, tEXt, zTXt, iTXt and tIME chunks. Pixels are untouched.
- Names: lowercase, spaces and punctuation become "_" or "-", only
  [a-z0-9._-] remain, and the extension is normalised (".jpeg" -> ".jpg").
  "2026-03-31 21.24.15.jpg" becomes "2026-03-31_21-24-15.jpg".
- Inside a git work tree, renames use "git mv", and references to the old name
  in tracked Markdown files are updated (plain and %20-encoded forms).

Standard library only. Other formats (HEIC, TIFF, WebP) are reported, not
changed: convert them to JPEG or PNG first.
"""
import argparse
import os
import re
import struct
import subprocess
import sys
import urllib.parse

JPEG_EXT = {".jpg", ".jpeg"}
PNG_EXT = {".png"}
OTHER_IMG_EXT = {".heic", ".heif", ".tif", ".tiff", ".webp", ".gif", ".bmp"}
PNG_DROP = {b"eXIf", b"tEXt", b"zTXt", b"iTXt", b"tIME"}
PNG_SIG = b"\x89PNG\r\n\x1a\n"


# ---------- JPEG ----------

def _jpeg_segments(data):
    """Yield (marker, segment_bytes) up to and including SOS; then ("rest", tail)."""
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG")
    yield 0xD8, b"\xff\xd8"
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            raise ValueError(f"bad marker at byte {i}")
        while data[i] == 0xFF:      # fill bytes
            i += 1
        marker = data[i]
        i += 1
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            yield marker, bytes([0xFF, marker])
            continue
        length = struct.unpack(">H", data[i:i + 2])[0]
        seg = bytes([0xFF, marker]) + data[i:i + length]
        i += length
        yield marker, seg
        if marker == 0xDA:          # start of scan: the rest is image data
            yield "rest", data[i:]
            return


def _exif_orientation(app1_payload):
    """Return the Orientation value (1-8) from an EXIF APP1 payload, or None."""
    if not app1_payload.startswith(b"Exif\x00\x00"):
        return None
    t = app1_payload[6:]
    if t[:2] == b"II":
        e = "<"
    elif t[:2] == b"MM":
        e = ">"
    else:
        return None
    try:
        ifd = struct.unpack(e + "I", t[4:8])[0]
        count = struct.unpack(e + "H", t[ifd:ifd + 2])[0]
        for n in range(count):
            off = ifd + 2 + 12 * n
            tag, typ = struct.unpack(e + "HH", t[off:off + 4])
            if tag == 0x0112 and typ == 3:
                v = struct.unpack(e + "H", t[off + 8:off + 10])[0]
                return v if 1 <= v <= 8 else None
    except struct.error:
        return None
    return None


def _minimal_exif(orientation):
    """An APP1 segment holding only the Orientation tag."""
    tiff = (b"MM\x00\x2a" + struct.pack(">I", 8) + struct.pack(">H", 1)
            + struct.pack(">HHIHH", 0x0112, 3, 1, orientation, 0) + struct.pack(">I", 0))
    payload = b"Exif\x00\x00" + tiff
    return b"\xff\xe1" + struct.pack(">H", len(payload) + 2) + payload


def scrub_jpeg(data):
    """Return (new_bytes, list_of_removed_descriptions)."""
    out, removed, orientation = [], [], None
    for marker, seg in _jpeg_segments(data):
        if marker == "rest":
            out.append(seg)
            break
        if marker == 0xE1:
            payload = seg[4:]
            if payload.startswith(b"Exif\x00\x00"):
                orientation = _exif_orientation(payload) or orientation
                gps = b"\x88\x25" in payload[:4096] or b"\x25\x88" in payload[:4096]
                removed.append("EXIF" + (" (incl. GPS)" if gps else ""))
            elif b"ns.adobe.com/xap" in payload[:64]:
                removed.append("XMP")
            else:
                removed.append("APP1")
            continue
        if marker == 0xED:
            removed.append("IPTC/Photoshop")
            continue
        if marker == 0xFE:
            removed.append("comment")
            continue
        if isinstance(marker, int) and 0xE2 <= marker <= 0xEF and marker != 0xEE:
            # APP2 (ICC colour profile) is kept; other APPn are maker/vendor data.
            if marker == 0xE2 and seg[4:16] == b"ICC_PROFILE\x00":
                out.append(seg)
                continue
            removed.append(f"APP{marker - 0xE0}")
            continue
        out.append(seg)
    if orientation and orientation != 1:
        out.insert(1, _minimal_exif(orientation))   # right after SOI
    return b"".join(out), removed


# ---------- PNG ----------

def scrub_png(data):
    if not data.startswith(PNG_SIG):
        raise ValueError("not a PNG")
    out, removed, i = [PNG_SIG], [], 8
    while i < len(data):
        length = struct.unpack(">I", data[i:i + 4])[0]
        ctype = data[i + 4:i + 8]
        chunk = data[i:i + 12 + length]
        i += 12 + length
        if ctype in PNG_DROP:
            removed.append(ctype.decode())
            continue
        out.append(chunk)
        if ctype == b"IEND":
            break
    return b"".join(out), removed


# ---------- names ----------

def web_name(name):
    stem, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext == ".jpeg":
        ext = ".jpg"
    s = stem.lower()
    s = re.sub(r"(\d{4}-\d{2}-\d{2})[ _](\d{2})\.(\d{2})\.(\d{2})", r"\1_\2-\3-\4", s)  # phone timestamps
    s = s.replace("&", "and")
    s = re.sub(r"[\s]+", "_", s)
    s = re.sub(r"[^a-z0-9._-]+", "-", s)
    s = s.replace(".", "-")
    s = re.sub(r"([_-])[_-]+", r"\1", s).strip("._-")
    return (s or "image") + ext


# ---------- git helpers ----------

def git_root(path):
    try:
        r = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(path)) or ".",
                            "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    except FileNotFoundError:
        return None


def is_tracked(root, path):
    r = subprocess.run(["git", "-C", root, "ls-files", "--error-unmatch", os.path.relpath(path, root)],
                       capture_output=True)
    return r.returncode == 0


def update_refs(root, old_path, new_path):
    """Replace links to old_path in tracked Markdown files.

    Links are matched by their path relative to each Markdown file, so two
    images with the same name in different folders aren't confused.
    """
    old_abs, new_abs = os.path.abspath(old_path), os.path.abspath(new_path)
    out = subprocess.run(["git", "-C", root, "ls-files", "-z", "*.md"], capture_output=True, text=True).stdout
    changed = []
    for rel in filter(None, out.split("\0")):
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            continue
        here = os.path.dirname(p)
        old_rel = os.path.relpath(old_abs, here).replace(os.sep, "/")
        new_rel = os.path.relpath(new_abs, here).replace(os.sep, "/")
        text = open(p, encoding="utf-8").read()
        new_text = text
        old_root = os.path.relpath(old_abs, root).replace(os.sep, "/")
        new_root = os.path.relpath(new_abs, root).replace(os.sep, "/")
        # Relative links ("../assets/x.jpg") and repo-root links ("/../main/assets/x.jpg").
        for a_old, a_new, lead in ((old_rel, new_rel, r"(?<=[(<\"'\s])"), (old_root, new_root, r"(?<=/)")):
            for a in {a_old, a_old.replace(" ", "%20"), urllib.parse.quote(a_old)}:
                new_text = re.sub(lead + r"(\./)?" + re.escape(a) + r"(?=[)>\"'\s#?])",
                                  lambda m, n=a_new: (m.group(1) or "") + n, new_text)
        if new_text != text:
            open(p, "w", encoding="utf-8").write(new_text)
            changed.append(rel)
    return changed


# ---------- main ----------

def collect(paths):
    for p in paths:
        if os.path.isdir(p):
            for d, dirs, files in os.walk(p):
                dirs[:] = [x for x in dirs if x != ".git"]
                for f in sorted(files):
                    yield os.path.join(d, f)
        else:
            yield p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="scrub and rename in place")
    mode.add_argument("--check", action="store_true", help="exit 1 if anything needs changing")
    ap.add_argument("--no-rename", action="store_true", help="scrub metadata only")
    a = ap.parse_args()

    pending = 0
    for path in collect(a.paths):
        ext = os.path.splitext(path)[1].lower()
        if ext in OTHER_IMG_EXT:
            print(f"SKIP  {path}: {ext} isn't handled; convert to JPEG or PNG first")
            pending += 1
            continue
        if ext not in JPEG_EXT | PNG_EXT:
            continue
        data = open(path, "rb").read()
        try:
            new, removed = (scrub_jpeg if ext in JPEG_EXT else scrub_png)(data)
        except ValueError as e:
            print(f"ERROR {path}: {e}")
            pending += 1
            continue
        target = path if a.no_rename else os.path.join(os.path.dirname(path), web_name(os.path.basename(path)))
        rename = target != path
        if not removed and not rename:
            continue
        pending += 1
        what = []
        if removed:
            what.append("strip " + ", ".join(dict.fromkeys(removed)))
        if rename:
            what.append(f"rename -> {os.path.basename(target)}")
        print(f"{'DONE ' if a.apply else 'TODO '} {path}: " + "; ".join(what))
        if not a.apply:
            continue
        if removed:
            with open(path, "wb") as fh:
                fh.write(new)
        if rename:
            if os.path.exists(target):
                print(f"ERROR {target} already exists; not renaming {path}")
                continue
            root = git_root(path)
            if root and is_tracked(root, path):
                subprocess.run(["git", "-C", root, "mv", os.path.relpath(path, root),
                                os.path.relpath(target, root)], check=True)
                for rel in update_refs(root, path, target):
                    print(f"      updated reference in {rel}")
            else:
                os.rename(path, target)

    if a.check and pending:
        print(f"{pending} file(s) need scrubbing: run tools/scrub_images.py --apply")
        return 1
    if not a.apply and not a.check:
        print(f"{pending} file(s) would change. Re-run with --apply to change them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
