"""04_final.md를 카드/캡션/해시태그 구조로 파싱한다. 이미지 생성·업로드가 공유."""
import re
from pathlib import Path

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002190-\U000021FF"
    "\U00002B00-\U00002BFF\U0001F1E6-\U0001F1FF️❤✅⭐]+",
    flags=re.UNICODE,
)


def strip_emoji(text):
    return EMOJI.sub("", text).strip()


def parse(md_path):
    """반환: {"cards": [{"title": str|None, "lines": [str]}], "caption": str, "hashtags": str}"""
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    cards, caption, hashtags = [], [], ""
    section = None  # None | "card" | "caption" | "hashtag"
    cur = None

    for raw in lines:
        line = raw.rstrip()

        if line.startswith("### 카드"):
            if cur:
                cards.append(cur)
            cur = {"title": None, "lines": []}
            section = "card"
            continue
        if line.startswith("## 캡션"):
            if cur:
                cards.append(cur); cur = None
            section = "caption"; continue
        if line.startswith("## 해시태그"):
            section = "hashtag"; continue
        if line.startswith("## 사용한 팩트") or line.startswith("---") or line.startswith("## 검수"):
            if cur:
                cards.append(cur); cur = None
            section = None; continue

        if section == "card" and cur is not None:
            if line.startswith("**제목:**"):
                cur["title"] = line.replace("**제목:**", "").strip()
            elif line.strip():
                cur["lines"].append(line.strip())
        elif section == "caption" and line.strip():
            caption.append(line.strip())
        elif section == "hashtag" and line.strip():
            hashtags = line.strip()

    return {
        "cards": cards,
        "caption": "\n\n".join(caption),
        "hashtags": hashtags,
    }


def full_caption(parsed):
    """인스타 캡션 = 본문 + 해시태그."""
    return f"{parsed['caption']}\n\n{parsed['hashtags']}"
