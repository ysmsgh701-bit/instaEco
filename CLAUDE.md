# 인스타그램 경제 뉴스 큐레이션 자동화

## 계정 컨셉
- 대주제: 경제 뉴스 큐레이션
- 타겟: 경제 뉴스 읽을 시간 없는 2030 직장인
- 포맷: 카드뉴스 (표지 + 본문 3~4장 + CTA), 존댓말 해요체
- 수익 모델: 팔로워 성장 → 광고·제휴

## 파이프라인
`/insta-pipeline` 실행 → 4개 에이전트 순차 호출:
1. `insta-topic-scout` → `posts/YYYY-MM-DD/01_topics.md` (소주제 선정)
2. `insta-content-researcher` → `02_research.md` (팩트 시트·카드 구성)
3. `insta-writer` → `03_draft.md` (초안)
4. `insta-reviewer` → `04_final.md` (검수·완성)

오케스트레이션은 메인 세션이 스킬로 수행 (`.claude/skills/insta-pipeline/SKILL.md`).

## 불변 규칙
- 팩트 시트에 없는 수치·사실 게시물 사용 금지
- 투자 권유 표현 금지
- 기사 문장 복사 금지 (재서술 필수)
