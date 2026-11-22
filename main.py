#!/usr/bin/env python3
"""Entry point for "The picture that tastes of one ingredient".

Copies the pre-rendered entry image (entry.png, sitting next to this file)
to the output directory as entry.png.

Standard library only. Requires Python 3.13+.
"""

import os
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # 1 MiB size cap from the competition kit


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target = out_dir / "entry.png"

    data = source.read_bytes()

    # Validate before writing anything.
    if not data.startswith(PNG_MAGIC):
        print("error: entry.png is not a valid PNG (bad magic bytes)",
              file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes, over the "
              f"{MAX_BYTES}-byte cap", file=sys.stderr)
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)

    # Verify the written copy before reporting success.
    written = target.read_bytes()
    if written != data:
        print("error: written copy does not match the source image",
              file=sys.stderr)
        return 1

    print(f"copied {source} ({len(data)} bytes) -> "
          f"{target} ({len(written)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
