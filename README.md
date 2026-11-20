# The World Today — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/trisnoudin9/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/trisnoudin9/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up Friday 20 November 2026's world news, as a newspaper
front page with four panels:

1. **Trump delays Iran decision to 2027** — President Trump says there is
   "no rush" on the Iran war decision and he will "see what happens" after
   1 January, pushing the call into next year.
2. **ICJ: Myanmar committed genocide** — the International Court of Justice,
   the UN's top court, rules Myanmar committed genocide against the Rohingya
   minority in its 2017 crackdown.
3. **Cyclone Akvan** — the severe cyclonic storm bears down on India's east
   coast, with 300,000 people evacuated in Odisha and 423 rescue teams
   deployed ahead of landfall.
4. **Anthropic IPO, biggest ever** — the AI company prices its IPO at $83 a
   share, raising $81.3 billion in the largest initial public offering on
   record, with a reported valuation around $1.5 trillion.

`main.py` copies the vendored `entry.png` (1024×1024, JPEG bytes, 302,178
bytes, under 1 MiB) to `/output/entry.png`. The image was composed and
captioned from that day's reporting (Reuters, The Hindu, BBC, Bloomberg,
The Times of India).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Verify

```sh
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
cmp entry.png out/entry.png && echo "byte-identical"
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=mq46yedx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
