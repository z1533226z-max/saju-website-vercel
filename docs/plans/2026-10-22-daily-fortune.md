# 띠별 오늘·내일 운세 구현 계획

**Goal:** 한국 시간 자정에 서버 HTML과 열린 화면의 운세 날짜가 함께 바뀌고 각 띠에서 내일을 미리 본다.

**Architecture:** 기존 Python SSR과 명리 관계·날짜 시드 생성기를 재사용한다. 하나의 KST 요청 시각에서 표시 날짜와 다음 자정을 계산한다. Vercel의 만료 후 stale 응답을 피하려고 운세 HTML은 no-store로 제공하고, JS는 다음 자정·복귀 시 서버 HTML을 다시 요청하는 역할만 한다. 오늘/내일은 일반 링크로 전환하여 JS 없이도 작동한다.

**Tech Stack:** Python BaseHTTPRequestHandler, pytest, 기존 CSS, 바닐라 JS, Playwright.

설계 승인: Orca 코디네이터 응답(2026-10-22) — SSR 유지, 단일 KST, stale 제거, `?day=tomorrow`, 열린 화면 갱신, cron 없음. 추가 조건: 내일 noindex,follow, canonical 오늘 주소 유지, 쿼리 캐시 키 확인, 23:59:59/00:00:01 주입 검증.

대안 비교: 매일 정적 빌드/배포는 정시 실행과 빌드 완료 지연 및 별도 운영 필요. TTL만 줄인 SSR은 만료 시 stale 재검증이 남을 수 있다. no-store SSR은 기존 함수만 사용하여 가장 단순하며 실제 함수 사용량 증가 가능성은 보고한다.

## 1. 날짜·응답 회귀 시험

- `tests/test_daily_rollover.py`에 UTC/KST 경계, 같은 날 결정성, 내일=다음날 오늘, 월말·연말·윤일, HTTP GET/HEAD·입력 검증 시험을 먼저 추가한다.
- 기존 구현에서 필요한 시험이 실패하는 것을 확인한 뒤 `api/_core/daily_fortune.py`, `api/daily/fortune.py`, `api/daily/index.py`를 수정한다.
- 기존 풀이 풀·합충 관계와 점수 범위를 유지하고, dateModified는 미리보기의 미래 날짜로 쓰지 않는다.

## 2. 오늘·내일 UI와 열린 화면 갱신

- `api/daily/fortune.py`에 날짜를 보이는 오늘/내일 링크, 선택 상태, 미리보기 설명을 추가한다.
- `public/css/daily.css`에 기존 테마를 따르는 전환 링크 스타일을 추가한다.
- `public/js/components/daily-refresh.js`로 자정 타이머·탭 복귀·뒤로가기 갱신을 구현한다. 운세 자체를 브라우저에서 계산하거나 개인정보를 저장하지 않는다.

## 3. 실제 서버·브라우저 검증과 인계

- 로컬 전용 서버 어댑터로 vercel.json 라우팅을 흉내 내서 실제 핸들러를 HTTP 호출한다. 운영 서버·DB 접근은 하지 않는다.
- 변경 전후의 동일 띠 두 날짜 HTML을 저장하고 비교한다.
- pytest 전체, 변경 Python/JS lint, npm build, 기존 npm lint 결과를 정직하게 기록한다.
- 390px·1440px, JS 없음, 오늘/내일 전환, 시계 주입 자정·복귀를 Playwright로 확인하고 보고서 옆 증거 폴더에 저장한다.
- 코드를 자체 리뷰·단순화하고 로컬 서버 종료 후 feat/daily-fortune에 커밋한다. push·배포는 하지 않는다.

수정 금지: AdBanner.tsx, sitemap·robots·canonical·공용 layout 메타데이터·홈 HTML, .env 및 secrets, docs/local. 정적 잔존 daily 파일은 실제 Vercel 라우트가 아니므로 이번에 재생성하지 않는다.
