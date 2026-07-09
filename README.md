# instaEco — 경제 뉴스 인스타그램 자동화

2030 직장인 대상 경제 뉴스 큐레이션 카드뉴스를 **소재 선정 → 리서치 → 작성 → 검수 → 이미지 생성 → 게시**까지 자동화한다.

## 파이프라인 전체 흐름

```
[콘텐츠 생성 — Claude Code 에이전트]        [게시 — Python]
01_topics.md  소주제 선정                    generate_images.py  → card_01~06.png
02_research.md 팩트 시트·구성                upload_instagram.py → 인스타 캐러셀 게시
03_draft.md    초안
04_final.md    검수·완성본  ───────────────▶ (04_final.md 를 이미지·캡션으로 변환)
```

콘텐츠 4단계는 `.claude/agents/` 의 에이전트가, 오케스트레이션은 `.claude/skills/insta-pipeline` 이 담당한다.
게시 2단계는 `src/` 의 파이썬 스크립트가 담당한다.

## 폴더 구조

```
src/
  parse_post.py         04_final.md 파서 (이미지·업로드 공유)
  generate_images.py    최종본 → 1080x1080 PNG 카드
  upload_instagram.py   PNG → 인스타그램 캐러셀 게시 (Graph API)
posts/YYYY-MM-DD/
  01~04_*.md            콘텐츠 산출물
  images/card_*.png     생성된 카드 이미지
```

## 1. 설치

```bash
pip install -r requirements.txt
```

## 2. 이미지 생성

```bash
python src/generate_images.py posts/2026-07-09
```

`posts/2026-07-09/images/` 에 `card_01.png ~ card_06.png` 생성. 폰트는 Windows 맑은고딕 사용.
이모지는 이미지에서 제거되고 캡션(텍스트)에는 유지된다.

## 3. 인스타그램 게시 준비 (최초 1회)

Graph API는 로컬 파일을 직접 올릴 수 없고 **공개 이미지 URL**이 필요하다. 이 repo 자체를 이미지 호스팅으로 쓴다.

**필요 조건**
1. 인스타그램 계정을 **프로페셔널(비즈니스/크리에이터)** 로 전환
2. 페이스북 페이지 생성 후 인스타그램 계정과 연결
3. [Meta for Developers](https://developers.facebook.com) 앱 생성 → `instagram_basic`, `instagram_content_publish`, `pages_read_engagement` 권한
4. 장기 액세스 토큰 발급, IG User ID 확인

**설정**
```bash
cp .env.example .env
# .env 에 IG_USER_ID, IG_ACCESS_TOKEN 입력
```

## 4. 게시

```bash
# 1) 이미지를 GitHub에 push (raw URL 호스팅용)
git add posts/2026-07-09/images && git commit -m "images 2026-07-09" && git push

# 2) IMAGE_BASE_URL 이 해당 날짜 폴더를 가리키는지 확인 후 게시
python src/upload_instagram.py posts/2026-07-09
```

`.env` 의 `IMAGE_BASE_URL` 은 게시할 날짜에 맞춰 갱신한다.

## 불변 규칙 (콘텐츠)

- 팩트 시트에 없는 수치·사실 게시 금지
- 투자 권유 표현 금지
- 기사 문장 복사 금지 (재서술 필수)

## 주의

- 액세스 토큰·`.env` 는 절대 커밋하지 않는다 (`.gitignore` 처리됨).
- 비공식 자동화 라이브러리(instagrapi 등, 아이디·비밀번호 로그인)는 계정 정지 위험이 있어 공식 Graph API를 사용한다.
