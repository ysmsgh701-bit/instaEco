"""생성된 카드 이미지를 인스타그램 캐러셀로 게시 (Instagram Graph API).

전제:
- 인스타그램 프로페셔널(비즈니스/크리에이터) 계정 + 페이스북 페이지 연결
- .env: IG_USER_ID, IG_ACCESS_TOKEN, IMAGE_BASE_URL
- Graph API는 로컬 파일 업로드 불가 → 이미지는 공개 URL이어야 함.
  이 repo(GitHub)에 이미지를 먼저 push하고 raw URL을 IMAGE_BASE_URL로 사용한다.

사용법: python src/upload_instagram.py posts/2026-07-09
"""
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from parse_post import parse, full_caption

GRAPH = "https://graph.facebook.com/v21.0"


def _post(path, data):
    r = requests.post(f"{GRAPH}/{path}", data=data, timeout=60)
    body = r.json()
    if r.status_code != 200 or "error" in body:
        raise RuntimeError(f"Graph API 오류 ({path}): {body}")
    return body


def _wait_ready(ig_id, token, creation_id, tries=10):
    """캐러셀 컨테이너가 게시 준비될 때까지 대기."""
    for _ in range(tries):
        r = requests.get(
            f"{GRAPH}/{creation_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=30,
        ).json()
        if r.get("status_code") == "FINISHED":
            return
        if r.get("status_code") == "ERROR":
            raise RuntimeError(f"컨테이너 처리 실패: {r}")
        time.sleep(3)
    raise RuntimeError("컨테이너 준비 시간 초과")


def upload(post_dir):
    load_dotenv()
    ig_id = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]
    base = os.environ["IMAGE_BASE_URL"].rstrip("/")  # 예: https://raw.githubusercontent.com/ysmsgh701-bit/instaEco/main/posts/2026-07-09/images

    post_dir = Path(post_dir)
    parsed = parse(post_dir / "04_final.md")
    caption = full_caption(parsed)
    images = sorted((post_dir / "images").glob("card_*.png"))
    if not images:
        raise RuntimeError("이미지 없음 — 먼저 generate_images.py 실행")

    # 1. 각 이미지 캐러셀 아이템 컨테이너 생성
    child_ids = []
    for img in images:
        url = f"{base}/{img.name}"
        res = _post(f"{ig_id}/media", {
            "image_url": url,
            "is_carousel_item": "true",
            "access_token": token,
        })
        child_ids.append(res["id"])
        print(f"  아이템 생성: {img.name}")

    # 2. 캐러셀 부모 컨테이너 생성
    parent = _post(f"{ig_id}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(child_ids),
        "caption": caption,
        "access_token": token,
    })
    _wait_ready(ig_id, token, parent["id"])

    # 3. 게시
    published = _post(f"{ig_id}/media_publish", {
        "creation_id": parent["id"],
        "access_token": token,
    })
    print(f"게시 완료 — media id: {published['id']}")
    return published["id"]


if __name__ == "__main__":
    upload(sys.argv[1] if len(sys.argv) > 1 else "posts/2026-07-09")
