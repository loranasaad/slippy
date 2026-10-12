#!/usr/bin/env python3
"""Sets Slippy's version everywhere at once, so Illustrator and Photoshop
always ship the same one. VERSION at the repo's root drives both plug-ins'
builds; this also rewrites the copies that are typed out by hand (the
website's badge and the Photoshop panel's browser preview).

    python3 tools/set_version.py 1.3.2   # set it
    python3 tools/set_version.py --check # fail if any copy differs from VERSION
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each hand-typed copy: (file, pattern whose group 1 is the version).
COPIES = [
    ("docs/index.html", r'<span class="version" id="version">v(\d+\.\d+\.\d+)</span>'),
    ("photoshop/panel/main.js", r'listening: false, version: "(\d+\.\d+\.\d+)" \}'),
]


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as f:
        f.write(text)


def check():
    want = read("VERSION").strip()
    bad = []
    for rel, pattern in COPIES:
        found = re.findall(pattern, read(rel))
        if found != [want]:
            bad.append(f"{rel}: {found or 'no version found'}")
    if bad:
        sys.exit(f"Not at VERSION {want}:\n  " + "\n  ".join(bad)
                 + "\nRun: python3 tools/set_version.py " + want)
    print(f"Everything is at {want}.")


def set_version(version):
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"'{version}' isn't a version like 1.3.2.")
    write("VERSION", version + "\n")
    for rel, pattern in COPIES:
        text, n = re.subn(pattern, lambda m: m.group(0).replace(m.group(1), version), read(rel))
        if n != 1:
            sys.exit(f"{rel}: expected one version, found {n}.")
        write(rel, text)
    check()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--check":
        check()
    else:
        set_version(sys.argv[1])


if __name__ == "__main__":
    main()
