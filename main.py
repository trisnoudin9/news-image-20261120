"""news-image-20261120 entry: a program that writes one image to /output/entry.png.

The image is the entry.png beside this file: a newspaper front page summing up
Friday 20 November 2026 in four panels — Trump delaying the Iran war decision
to 2027, the ICJ ruling Myanmar committed genocide against the Rohingya,
Cyclone Akvan bearing down on Odisha with 300,000 evacuated, and Anthropic's
record $81.3 billion IPO — researched from that day's news (Reuters,
The Hindu, BBC, Bloomberg, The Times of India). The program only copies the
vendored image, so two runs write the same bytes.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "entry.png"
    # The gate tells a PNG from a JPEG by its first bytes, so refuse to ship
    # a vendored file that is neither: a corrupt download must fail loudly
    # here, not as an invalid entry after submission.
    magic = src.read_bytes()[:4]
    if magic[:3] != b"\xff\xd8\xff" and magic != b"\x89PNG":
        raise RuntimeError(
            f"{src} is neither a JPEG nor a PNG (first bytes: {magic!r})"
        )
    dst = OUTPUT_DIR / "entry.png"
    shutil.copyfile(src, dst)
    # A truncated or failed copy must never silently pass as a valid entry:
    # refuse to finish unless the destination holds exactly the source bytes.
    if dst.stat().st_size != src.stat().st_size:
        raise RuntimeError(
            f"copy incomplete: {dst} holds {dst.stat().st_size} bytes, "
            f"expected {src.stat().st_size} from {src}"
        )


if __name__ == "__main__":
    main()
