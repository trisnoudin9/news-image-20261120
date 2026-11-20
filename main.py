"""news-image-20261120 entry: write the entry image to the output directory.

The entry is a single newspaper-style front page summing up Friday
20 November 2026 in four panels:

* Trump pushing the Iran war decision into 2027 ("no rush", decide after
  1 January);
* the ICJ ruling that Myanmar committed genocide against the Rohingya in
  its 2017 crackdown;
* Cyclone Akvan bearing down on Odisha with 300,000 people evacuated;
* Anthropic pricing its IPO at $83 a share, raising $81.3 billion — the
  largest IPO on record.

The image itself is vendored next to this file as entry.png (JPEG bytes,
1024x1024). This program does nothing creative: it copies those bytes to
the output directory and refuses to finish unless the destination holds
exactly the same bytes. That makes the entry deterministic — every run
produces identical output.

Outside the grader's container, /output is replaced by
MAKEFUN_OUTPUT_DIR:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def _fail(message: str) -> "SystemExit":
    print(f"error: {message}", file=sys.stderr)
    return SystemExit(1)


def _check_magic(path: Path) -> None:
    """Refuse a vendored file that is neither JPEG nor PNG.

    A corrupt or mis-downloaded bundle must fail loudly here instead of
    shipping an invalid entry.
    """
    head = path.read_bytes()[:4]
    if head[:3] != b"\xff\xd8\xff" and head != b"\x89PNG":
        raise _fail(f"{path} is neither JPEG nor PNG (first bytes: {head!r})")


def _check_size(src: Path, dst: Path) -> None:
    """Refuse a truncated copy: the destination must hold every source byte."""
    got = dst.stat().st_size
    want = src.stat().st_size
    if got != want:
        raise _fail(
            f"copy incomplete: {dst} holds {got} bytes, expected {want} "
            f"from {src}"
        )


def _jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Read (width, height) from a JPEG by walking its segments to SOF0/SOF2.

    Every marker except the standalone ones (SOI, EOI, RSTn, TEM) is
    followed by a 2-byte big-endian length that includes the length bytes
    themselves. The frame header (SOF0 baseline, SOF2 progressive) holds
    precision (1 byte), height (2 bytes), width (2 bytes). Hitting SOS or
    the end of the file first means no frame header — not a valid JPEG.
    """
    if data[:2] != b"\xff\xd8":
        raise _fail("not a valid JPEG: missing SOI marker (\\xff\\xd8)")
    pos = 2
    while pos < len(data):
        if data[pos] != 0xFF:
            raise _fail(f"not a valid JPEG: expected marker at offset {pos}")
        while pos < len(data) and data[pos] == 0xFF:
            pos += 1
        if pos >= len(data):
            break
        marker = data[pos]
        pos += 1
        if marker in (0x01, 0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            continue
        if pos + 2 > len(data):
            raise _fail("not a valid JPEG: truncated segment length")
        seg_len = int.from_bytes(data[pos:pos + 2], "big")
        if seg_len < 2 or pos + seg_len > len(data):
            raise _fail("not a valid JPEG: truncated segment")
        if marker in (0xC0, 0xC2):
            body = data[pos + 2:pos + seg_len]
            if len(body) < 5:
                raise _fail("not a valid JPEG: truncated frame header")
            height = int.from_bytes(body[1:3], "big")
            width = int.from_bytes(body[3:5], "big")
            return width, height
        if marker == 0xDA:
            raise _fail("not a valid JPEG: no frame header (SOF) before scan data")
        pos += seg_len
    raise _fail("not a valid JPEG: no frame header (SOF) found")


def _png_dimensions(data: bytes) -> tuple[int, int]:
    """Read (width, height) from a PNG's IHDR chunk."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise _fail("not a valid PNG: missing IHDR chunk")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def _check_dimensions(path: Path) -> None:
    """Require the vendored image to be exactly 1024x1024.

    A resized or wrong-format bundle must fail here with a clear message,
    not as a rejected entry after submission.
    """
    data = path.read_bytes()
    if data[:3] == b"\xff\xd8\xff":
        width, height = _jpeg_dimensions(data)
        kind = "JPEG"
    elif data[:4] == b"\x89PNG":
        width, height = _png_dimensions(data)
        kind = "PNG"
    else:
        raise _fail(f"{path} is neither JPEG nor PNG")
    if (width, height) != (1024, 1024):
        raise _fail(
            f"{path} is {kind} {width}x{height}, expected 1024x1024"
        )


def main() -> None:
    src = Path(__file__).resolve().parent / "entry.png"
    _check_magic(src)
    _check_dimensions(src)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dst = OUTPUT_DIR / "entry.png"
    shutil.copyfile(src, dst)
    _check_size(src, dst)


if __name__ == "__main__":
    main()
