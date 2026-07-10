"""04_final.md -> 1080x1080 카드뉴스 PNG. 사용법: python src/generate_images.py posts/2026-07-09"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from parse_post import parse, strip_emoji, full_caption

W = H = 1080
NAVY = (15, 37, 71)
WHITE = (255, 255, 255)
DARK = (26, 26, 26)
GRAY = (90, 100, 115)
ACCENT = (46, 134, 222)
HANDLE = "@instaeco · 경제 3분 브리핑"

FONT = "C:/Windows/Fonts/malgun.ttf"
FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BD if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, text, fnt, y, color, max_w):
    for ln in wrap(draw, text, fnt, max_w):
        w = draw.textlength(ln, font=fnt)
        draw.text(((W - w) / 2, y), ln, font=fnt, fill=color)
        y += fnt.size + 18
    return y


def render_cover(card, idx, total):
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.text((80, 90), "경제 3분 브리핑", font=font(38, True), fill=ACCENT)
    hook = strip_emoji(card["lines"][0] if card["lines"] else card.get("title", ""))
    d.rectangle([80, 470, 220, 482], fill=ACCENT)
    draw_center(d, hook, font(84, True), 300, WHITE, W - 160)
    d.text((80, H - 110), HANDLE, font=font(32), fill=(150, 170, 200))
    d.text((W - 200, H - 110), f"{idx}/{total}", font=font(32, True), fill=(150, 170, 200))
    return img


def render_body(card, idx, total):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 180], fill=NAVY)
    d.text((80, 68), strip_emoji(card["title"] or ""), font=font(52, True), fill=WHITE)
    y = 280
    for ln in card["lines"]:
        for wln in wrap(d, strip_emoji(ln), font(40), W - 160):
            d.text((80, y), wln, font=font(40), fill=DARK)
            y += 40 + 20
        y += 22  # 문장 간 간격
    d.line([80, H - 90, W - 80, H - 90], fill=(225, 228, 233), width=2)
    d.text((80, H - 70), HANDLE, font=font(28), fill=GRAY)
    d.text((W - 190, H - 70), f"{idx}/{total}", font=font(28, True), fill=ACCENT)
    return img


def main(post_dir):
    post_dir = Path(post_dir)
    parsed = parse(post_dir / "04_final.md")
    out = post_dir / "images"
    out.mkdir(exist_ok=True)
    cards = parsed["cards"]
    total = len(cards)
    paths = []
    for i, card in enumerate(cards, 1):
        img = render_cover(card, i, total) if i == 1 else render_body(card, i, total)
        p = out / f"card_{i:02d}.png"
        img.save(p, "PNG")
        paths.append(p)
    cap_path = post_dir / "caption.txt"
    cap_path.write_text(full_caption(parsed), encoding="utf-8")
    print(f"생성 완료: {total}장 -> {out}")
    for p in paths:
        print(f"  {p.name}")
    print(f"캡션(붙여넣기용): {cap_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "posts/2026-07-09")
