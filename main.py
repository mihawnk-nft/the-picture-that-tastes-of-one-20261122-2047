#!/usr/bin/env python3
"""Entry point for the-picture-that-tastes-of-one-20261122-2047.

Copies the bundled entry.png to the output directory (``/output`` by
default, or ``$MAKEFUN_OUTPUT_DIR`` when set). Standard library only.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    if not SOURCE.is_file():
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    if data[:8] != PNG_MAGIC:
        print("error: entry.png is not a valid PNG (bad magic)", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)
    # Verify the copy landed intact before reporting success.
    written = target.read_bytes()
    if written != data:
        print(f"error: {target} differs from source after write",
              file=sys.stderr)
        return 1
    print(f"wrote {target}: {len(written)} bytes (verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
