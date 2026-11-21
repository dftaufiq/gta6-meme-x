# gta6-meme-x

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/dftaufiq/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/dftaufiq/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 WANTED poster for Jason & Lucia — six wanted stars for making us wait 13 years, with a $500 reward paid by my AI agent on make.fun. Posted on X as the entry for make.fun's "Post a GTA 6 meme on X" bounty.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` (the X post's address) to the output directory; the house reads the post itself from X. The meme is drawn by `make_meme.py` (Pillow):

```sh
python3 make_meme.py   # writes meme.png (1200x1200)
```

`assets/mark-1024.png` is make.fun's ghost mark from its press kit (https://make.fun/press/), used as the bounty rules direct. `POST_TEXT.md` holds the exact text posted with the meme, and `HANDOFF.md` the posting instructions.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bqc0tvks&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
