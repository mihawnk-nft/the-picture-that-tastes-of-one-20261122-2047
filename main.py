#!/usr/bin/env python3
"""the-picture-that-tastes-of-one-20261122-2047: write one picture of food
to /output/entry.png.

The image is a 1024x1024 PNG drawn at build time (see render.py in the
build directory): a stack of golden pancakes drowned in glossy maple
syrup with a melting pat of butter, on a cream plate over a warm dark
table -- one ingredient, maple syrup, you can taste at one look. Every
shape is drawn in code. This program only copies the PNG the repository
holds, so it needs no network and writes identical bytes on every run.
"""
import os
import shutil

MAX_BYTES = 1048576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        os.remove(dst)
        raise SystemExit("entry.png is not a PNG")
    size = os.path.getsize(dst)
    if size > MAX_BYTES:
        os.remove(dst)
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB cap")
    print(f"wrote {dst}: {size} bytes")


if __name__ == "__main__":
    main()
