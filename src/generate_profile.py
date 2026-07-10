"""인스타 프로필 사진 생성 (원형 크롭 대응). 출력: assets/profile.png"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 1080
NAVY = (15, 37, 71)
ACCENT = (46, 134, 222)
WHITE = (255, 255, 255)
LIGHT = (150, 180, 225)
FONT_BD = "C:/Windows/Fonts/malgunbd.ttf"


def font(sz):
    return ImageFont.truetype(FONT_BD, sz)


def ctext(d, text, fnt, cy, fill):
    w = d.textlength(text, font=fnt)
    x = (S - w) / 2
    box = d.textbbox((x, 0), text, font=fnt)
    d.text((x, cy - (box[3] - box[1]) / 2 - box[1]), text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (S, S), NAVY)
    d = ImageDraw.Draw(img)
    c = S / 2

    # 배경 원 + 얇은 액센트 링 (원형 크롭 안쪽)
    d.ellipse([40, 40, S - 40, S - 40], fill=NAVY)
    d.ellipse([70, 70, S - 70, S - 70], outline=ACCENT, width=10)

    # 텍스트 (상단·중앙 영역)
    ctext(d, "경제", font(110), 330, LIGHT)
    ctext(d, "3분", font(200), 500, WHITE)

    # 상승 막대 (경제/성장 모티프) — 하단 영역, 텍스트와 분리
    heights = [80, 130, 180, 240]
    bw, gap = 66, 42
    total = len(heights) * bw + (len(heights) - 1) * gap
    x = (S - total) / 2
    base = 850
    for i, h in enumerate(heights):
        fill = WHITE if i == len(heights) - 1 else ACCENT
        d.rounded_rectangle([x, base - h, x + bw, base], radius=14, fill=fill)
        x += bw + gap

    out = Path("assets"); out.mkdir(exist_ok=True)
    p = out / "profile.png"
    img.save(p, "PNG")
    print(f"프로필 생성: {p}")


if __name__ == "__main__":
    main()
