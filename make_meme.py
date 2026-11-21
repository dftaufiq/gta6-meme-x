#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 entry: a WANTED poster for Jason & Lucia.

A Vice City sunset mugshot panel, six GTA wanted stars, and the make.fun
ghost paying the $500 reward. Pure Pillow, no network, deterministic.
Run:  python3 make_meme.py            -> writes meme.png (1200x1200)
      python3 make_meme.py --preview  -> also writes meme-480.png
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
W = H = 1200

INK = (42, 26, 14)          # dark brown poster ink
PAPER = (243, 228, 189)     # aged parchment
GOLD = (245, 179, 1)        # wanted-star gold
BAND = (25, 20, 25)         # reward band
PINK = (255, 136, 196)      # make.fun magenta ink (light)
WHITE = (255, 255, 255)
SIL = (22, 8, 31)           # silhouette purple-black

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, cx, y, text, fnt, fill, tracking):
    """Draw text centred on cx with letter tracking (px between chars)."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def star_points(cx, cy, r_outer, r_inner, rot=-90):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sky_color(t):
    """Vice City sunset gradient, t=0 top -> t=1 bottom."""
    stops = [
        (0.00, (43, 10, 61)),
        (0.35, (122, 30, 109)),
        (0.62, (214, 58, 118)),
        (0.85, (255, 122, 61)),
        (1.00, (255, 196, 77)),
    ]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple(round(c0[i] + (c1[i] - c0[i]) * f) for i in range(3))
    return stops[-1][1]


def draw_palm(draw, x, y, h, lean, flip=False):
    """Stylised palm silhouette: curved trunk + drooping fronds."""
    s = -1 if flip else 1
    # trunk: curved polyline
    pts = []
    for i in range(9):
        f = i / 8
        pts.append((x + s * lean * f * f, y - h * f))
    draw.line(pts, fill=SIL, width=14, joint="curve")
    cx, cy = pts[-1]
    # fronds
    for k in range(7):
        ang = math.radians(-160 + k * 26) if not flip else math.radians(-20 - k * 26)
        length = h * (0.42 + 0.1 * math.sin(k * 2.1))
        fpts = []
        for i in range(7):
            f = i / 6
            fx = cx + math.cos(ang) * length * f
            fy = cy + math.sin(ang) * length * f + 46 * f * f
            fpts.append((fx, fy))
        draw.line(fpts, fill=SIL, width=8, joint="curve")
    # coconuts
    draw.ellipse([cx - 12, cy - 2, cx + 2, cy + 12], fill=SIL)
    draw.ellipse([cx + 2, cy - 2, cx + 16, cy + 12], fill=SIL)


def draw_person(draw, cx, base_y, scale, long_hair=False):
    """Bust silhouette: head + shoulders, cut off at the panel bottom."""
    hr = 34 * scale            # head radius
    hy = base_y - 205 * scale  # head centre
    if long_hair:
        # one hair mass behind the head, down past the shoulders
        draw.ellipse([cx - hr - 10, hy - hr - 8,
                      cx + hr + 10, hy + 125 * scale], fill=SIL)
    draw.ellipse([cx - hr, hy - hr, cx + hr, hy + hr], fill=SIL)
    # neck, so the head joins the shoulders
    draw.rectangle([cx - 18 * scale, hy + 10,
                    cx + 18 * scale, hy + 78 * scale], fill=SIL)
    # shoulders / torso down past the panel edge
    sw = 100 * scale
    draw.polygon([
        (cx - sw, base_y + 40),
        (cx - sw, hy + 95 * scale),
        (cx - sw * 0.7, hy + 70 * scale),
        (cx - hr * 0.5, hy + 62 * scale),
        (cx + hr * 0.5, hy + 62 * scale),
        (cx + sw * 0.7, hy + 70 * scale),
        (cx + sw, hy + 95 * scale),
        (cx + sw, base_y + 40),
    ], fill=SIL)


def sunset_panel():
    px0, py0, px1, py1 = 90, 325, 1110, 685
    pw, ph = px1 - px0, py1 - py0
    panel = Image.new("RGB", (pw, ph))
    pd = ImageDraw.Draw(panel)
    for y in range(ph):
        pd.line([(0, y), (pw, y)], fill=sky_color(y / ph))
    # synthwave sun with slats
    sun_cx, sun_cy, sun_r = pw // 2, 175, 92
    pd.ellipse([sun_cx - sun_r, sun_cy - sun_r,
                sun_cx + sun_r, sun_cy + sun_r], fill=(255, 224, 138))
    for i, gap in enumerate([5, 7, 10, 13, 16]):
        y = sun_cy + 10 + i * 20
        pd.rectangle([sun_cx - sun_r - 2, y, sun_cx + sun_r + 2, y + gap],
                     fill=sky_color(y / ph))
    # thin ground strip along the bottom; the busts stand on it
    pd.rectangle([0, ph - 26, pw, ph], fill=(28, 11, 38))
    # palms left and right
    draw_palm(pd, 95, ph - 6, 190, 26)
    draw_palm(pd, pw - 95, ph - 6, 210, 30, flip=True)
    # Jason and Lucia, flanking the sun
    draw_person(pd, pw // 2 - 150, ph - 26, 1.15)
    draw_person(pd, pw // 2 + 150, ph - 26, 1.15, long_hair=True)
    # rounded corners + border
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=18, fill=255)
    panel.putalpha(mask)
    frame = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    ImageDraw.Draw(frame).rounded_rectangle(
        [0, 0, pw - 1, ph - 1], radius=18, outline=INK + (255,), width=6)
    panel = Image.alpha_composite(panel.convert("RGBA"), frame)
    return panel, (px0, py0)


def parchment():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(13)
    # soft stains
    stain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stain)
    for _ in range(7):
        x, y = rng.randint(0, W), rng.randint(0, H)
        r = rng.randint(90, 260)
        sd.ellipse([x - r, y - r // 2, x + r, y + r // 2],
                   fill=(190, 150, 90, 14))
    img = Image.alpha_composite(img.convert("RGBA"),
                                stain.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(img, "RGBA")
    # grain
    for _ in range(2600):
        x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
        d.point((x, y), fill=(120, 90, 50, rng.randint(8, 26)))
    # vignette: darkened edges
    for i in range(70):
        a = int(1.6 * (70 - i) ** 0.5)
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(90, 60, 25, a))
    # double border
    d.rectangle([26, 26, W - 27, H - 27], outline=INK + (255,), width=5)
    d.rectangle([44, 44, W - 45, H - 45], outline=INK + (255,), width=2)
    return img


def build():
    img = parchment()
    d = ImageDraw.Draw(img)

    tracked(d, W // 2, 62, "WANTED", font(SERIF, 148), INK, 14)
    tracked(d, W // 2, 232, "DEAD OR ALIVE", font(SANS, 46), INK, 16)
    # divider: line - diamond - line
    d.line([(250, 306), (560, 306)], fill=INK, width=3)
    d.line([(640, 306), (950, 306)], fill=INK, width=3)
    d.polygon([(600, 294), (614, 306), (600, 318), (586, 306)], fill=INK)

    panel, (px, py) = sunset_panel()
    img.paste(panel, (px, py), panel)
    d = ImageDraw.Draw(img)

    tracked(d, W // 2, 700, "JASON & LUCIA", font(SERIF, 62), INK, 4)

    # six wanted stars
    for i in range(6):
        cx = W // 2 + (i - 2.5) * 96
        cy = 826
        d.polygon(star_points(cx, cy, 34, 14), fill=GOLD, outline=INK)
        d.polygon(star_points(cx, cy, 34, 14), outline=INK, width=3)

    tracked(d, W // 2, 872, "CRIME: MAKING US WAIT 13 YEARS",
            font(SANS, 37), INK, 1)
    tracked(d, W // 2, 920, "LAST SEEN: LOS SANTOS, 2013",
            font(SANS, 37), INK, 1)

    # reward band with the make.fun ghost
    d.rounded_rectangle([70, 978, 1130, 1118], radius=22, fill=BAND)
    ghost = Image.open(HERE / "assets" / "mark-1024.png").convert("RGBA")
    ghost = ghost.resize((118, 118), Image.LANCZOS)
    img.paste(ghost, (96, 988), ghost)
    d = ImageDraw.Draw(img)
    d.text((238, 988), "REWARD $500", font=font(SANS, 56), fill=WHITE)
    d.text((240, 1058), "paid by my AI agent on make.fun",
           font=font(SANS, 32), fill=PINK)

    return img


def main():
    img = build().convert("RGB")
    img.save(HERE / "meme.png", "PNG")
    print("wrote", HERE / "meme.png", img.size)
    if "--preview" in sys.argv:
        img.resize((480, 480), Image.LANCZOS).save(HERE / "meme-480.png", "PNG")
        print("wrote", HERE / "meme-480.png")


if __name__ == "__main__":
    main()
