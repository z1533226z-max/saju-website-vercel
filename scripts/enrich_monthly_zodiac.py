#!/usr/bin/env python3
"""
월별 띠운세 페이지 심화 보강 (멱등 add-on)
- 대상: public/zodiac/{animal}/2026-{MM}/index.html (기본 MM=07, 현재월)
- 원본 generator(generate_daily_and_monthly.py) 재실행 금지 원칙에 따라,
  기존 페이지에 '월간 상세 해설 + 주차별 흐름 + 이달의 조언 + 확장 FAQ'를 삽입한다.
- 점수/행운값은 generator와 동일한 seed 로직으로 재현하여 화면 표시값과 100% 일치시킨다.
- ENRICH_MONTHLY_V1 마커로 재실행 시 중복 삽입을 방지(멱등).

사용법: python scripts/enrich_monthly_zodiac.py [MM]   (예: 07)
"""
import os
import re
import sys

# generator 모듈에서 데이터/헬퍼 재사용
import generate_daily_and_monthly as G

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
MARKER = "<!-- ENRICH_MONTHLY_V1 -->"

# 오행별 7월(여름=화 기운) 상호작용 해설
ELEMENT_JULY = {
    "수": "여름의 화(火) 기운이 강한 7월, 수(水) 기운의 {ko}는 상반된 에너지 사이에서 균형이 관건입니다. 서두르기보다 흐름을 먼저 읽으면 오히려 남들이 못 보는 기회가 열립니다.",
    "목": "성장의 목(木) 기운을 지닌 {ko}는 7월의 뜨거운 화(火) 기운과 만나 추진력이 배가됩니다. 이미 벌여둔 일을 확장하고 결실로 밀어붙이기 좋은 달입니다.",
    "화": "본연의 화(火) 기운이 7월 여름과 공명하여 에너지가 한 해 중 정점에 이릅니다. 다만 과열되어 성급해지지 않도록 완급 조절이 성패를 가릅니다.",
    "토": "안정의 토(土) 기운을 지닌 {ko}는 7월의 변화 속에서 중심을 잡아주는 자리에 서게 됩니다. 흔들리지 않는 꾸준함이 이달 최대의 무기입니다.",
    "금": "결단의 금(金) 기운을 지닌 {ko}에게 7월의 화(火) 기운은 자신을 단련하는 시험대입니다. 감정보다 원칙으로 대응할 때 유리한 고지를 점합니다.",
}


def band(sc):
    return "high" if sc >= 78 else ("mid" if sc >= 66 else "low")


WEEK_ADVICE = {
    "overall": {
        "high": "전반적으로 상승 흐름이 뚜렷합니다. 중요한 일을 앞당겨 시도해도 좋습니다.",
        "mid": "무난한 출발입니다. 큰 승부보다 계획을 점검하며 페이스를 잡으세요.",
        "low": "초반에는 무리하지 말고 컨디션과 일정 관리에 집중하는 것이 좋습니다.",
    },
    "money": {
        "high": "재물 흐름이 원활한 주간입니다. 투자·재테크 기회를 적극적으로 살펴보세요.",
        "mid": "수입과 지출의 균형을 맞추기 좋은 시기입니다. 무리한 확장은 다음으로 미루세요.",
        "low": "지출 관리와 충동구매 자제가 필요한 주간입니다. 보증·대출은 신중히 결정하세요.",
    },
    "love": {
        "high": "인간관계와 연애운이 밝습니다. 먼저 다가서면 좋은 인연·화해의 기회가 옵니다.",
        "mid": "소통에 조금만 더 신경 쓰면 관계가 부드러워집니다. 표현을 아끼지 마세요.",
        "low": "오해가 생기기 쉬운 주간입니다. 감정적 대응을 피하고 경청하는 자세가 중요합니다.",
    },
    "health": {
        "high": "활력이 넘칩니다. 새 운동을 시작하거나 활동량을 늘리기 좋은 마무리입니다.",
        "mid": "적당한 휴식으로 리듬을 유지하세요. 규칙적인 수면이 컨디션을 지킵니다.",
        "low": "과로와 여름철 냉방병에 주의하세요. 수분 섭취와 휴식을 우선하세요.",
    },
}


def build_section(z, month):
    zid, ko, hanja, el_short = z["id"], z["ko"], z["hanja"], z["el_short"]
    mko = G.MONTHS_KO[month - 1]

    # generator와 동일한 seed 재현 → 화면 표시값과 일치
    s = G.seed_hash(f"{zid}-2026-{month:02d}")
    overall = G.score(s, 60, 92)
    money = G.score(s >> 3, 55, 90)
    love = G.score(s >> 5, 55, 90)
    health = G.score(s >> 7, 58, 92)
    work = G.score(s >> 9, 55, 90)
    overall_text = G.pick(G.OVERALL_TEMPLATES, s).replace("{el_short}", el_short)
    money_text = G.pick(G.MONEY_TEMPLATES, s >> 2)
    love_text = G.pick(G.LOVE_TEMPLATES, s >> 4)
    health_text = G.pick(G.HEALTH_TEMPLATES, s >> 6)
    work_text = G.pick(G.WORK_TEMPLATES, s >> 8)
    lucky_color = G.pick(G.LUCKY_COLORS, s >> 10)
    lucky_dir = G.pick(G.LUCKY_DIRS, s >> 11)
    n1 = (s % 45) + 1
    n2 = ((s >> 12) % 45) + 1
    lucky_day = (s % 28) + 1

    def grade(sc):
        return "대길" if sc >= 85 else "길" if sc >= 75 else "소길" if sc >= 65 else "평"

    el_intro = ELEMENT_JULY[el_short].format(ko=ko)

    # 최저 카테고리 → 주의점
    cats = {"재물": money, "연애·인간관계": love, "건강": health, "직장": work}
    weak = min(cats, key=cats.get)
    weak_advice = {
        "재물": "지출 계획을 세우고 큰 금전 결정은 신중히 하세요.",
        "연애·인간관계": "말보다 경청, 지적보다 인정으로 관계의 균열을 예방하세요.",
        "건강": "여름철 과로와 냉방병을 경계하고 휴식을 우선하세요.",
        "직장": "성급한 판단을 피하고 논리적으로 접근해 갈등을 줄이세요.",
    }[weak]

    # 유리한 유형
    if overall >= 78:
        favor = "새로운 도전을 준비 중인 분, 미뤄둔 계획을 실행에 옮기려는 분에게 특히 유리한 달입니다."
    elif overall >= 66:
        favor = "기존의 일을 안정적으로 다지고 내실을 기하려는 분에게 잘 맞는 달입니다."
    else:
        favor = "무리한 확장보다 재정비와 휴식으로 다음을 준비하려는 분에게 어울리는 달입니다."

    weeks = [
        ("1주차 (7/1~7/6)", "overall", overall, "총운"),
        ("2주차 (7/7~7/13)", "money", money, "재물운"),
        ("3주차 (7/14~7/20)", "love", love, "연애·인간관계운"),
        ("4주차 (7/21~7/31)", "health", health, "건강·마무리"),
    ]
    week_rows = "\n".join(
        f'                <div class="result-msg-card"><h3>📆 {label} · {cat} {sc}점</h3>'
        f'<p>{WEEK_ADVICE[key][band(sc)]}</p></div>'
        for (label, key, sc, cat) in weeks
    )

    faq_items = [
        (f"2026년 {mko} {ko} 총운은 어떤가요?",
         f"2026년 {mko} {ko}({hanja})의 총운 점수는 {overall}점({grade(overall)})입니다. {overall_text}"),
        (f"2026년 {mko} {ko} 재물운은 어떤가요?",
         f"{mko} {ko}의 재물운은 {money}점입니다. {money_text}"),
        (f"2026년 {mko} {ko} 연애운은 어떤가요?",
         f"{mko} {ko}의 연애운은 {love}점입니다. {love_text}"),
        (f"2026년 {mko} {ko} 직장운과 건강운은 어떤가요?",
         f"직장운 {work}점, 건강운 {health}점입니다. {work_text} 건강 면에서는 {health_text}"),
        (f"2026년 {mko} {ko} 행운의 날과 색상은?",
         f"행운의 날은 {lucky_day}일, 행운의 색은 {lucky_color}, 행운의 방향은 {lucky_dir}, 행운의 숫자는 {n1}과 {n2}입니다."),
        (f"2026년 {mko} {ko}가 특히 주의할 점은?",
         f"이달 가장 낮은 흐름은 {weak}운입니다. {weak_advice}"),
    ]

    faq_visible = "\n".join(
        f'                <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in faq_items
    )

    section = f"""    {MARKER}
    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">2026년 {mko} {ko} 운세 총정리</span></h2>
            <div class="result-msg-card" style="margin-bottom:1.5rem;">
                <p style="line-height:1.9;">{el_intro}</p>
                <p style="line-height:1.9;margin-top:1rem;">종합적으로 {mko} {ko}의 총운은 <strong>{overall}점({grade(overall)})</strong>입니다. {overall_text} {favor}</p>
            </div>

            <h3 style="margin:1.5rem 0 0.8rem;">📅 {mko} 주차별 흐름</h3>
            <div class="result-messages">
{week_rows}
            </div>

            <h3 style="margin:1.5rem 0 0.8rem;">💡 이달의 조언</h3>
            <div class="result-msg-card">
                <p style="line-height:1.9;">이달 {ko}가 가장 신경 써야 할 부분은 <strong>{weak}운</strong>입니다. {weak_advice} 반대로 강점을 살리려면 총운 흐름이 좋은 초·중순에 중요한 일을 배치하는 것이 유리합니다. 행운의 날인 <strong>{lucky_day}일</strong>과 행운의 색 <strong>{lucky_color}</strong>을 일상에 활용해 보세요.</p>
            </div>

            <h3 style="margin:1.5rem 0 0.8rem;">❓ {mko} {ko} 운세 자주 묻는 질문</h3>
            <div class="faq-list">
{faq_visible}
            </div>
        </div>
    </section>

"""

    # FAQPage JSON-LD 항목 (동일 6개)
    faq_json = ",\n        ".join(
        '{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'.format(
            q=q, a=a) for q, a in faq_items
    )
    return section, faq_json


def enrich(path, z, month):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if MARKER in html:
        return "skip"

    ko = z["ko"]
    section, faq_json = build_section(z, month)

    # 1) 월별 운세 그리드 섹션 바로 앞에 상세 섹션 삽입
    anchor = f'<span class="gold-text">{ko} 월별 운세</span>'
    if anchor not in html:
        return "no-anchor"
    idx = html.index(anchor)
    sec_start = html.rindex("<section", 0, idx)
    html = html[:sec_start] + section + html[sec_start:]

    # 2) FAQPage JSON-LD mainEntity 3개 → 6개 교체
    html = re.sub(
        r'("@type":"FAQPage",\s*"mainEntity":\[).*?(\]\s*\}\s*</script>)',
        lambda m: m.group(1) + "\n        " + faq_json + "\n        " + m.group(2),
        html, count=1, flags=re.S,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return "ok"


def main():
    month = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    mm = f"{month:02d}"
    done = skipped = missing = 0
    for z in G.ZODIAC:
        path = os.path.join(PUBLIC_DIR, "zodiac", z["id"], f"2026-{mm}", "index.html")
        if not os.path.exists(path):
            print(f"  MISSING {path}")
            missing += 1
            continue
        r = enrich(path, z, month)
        print(f"  [{r}] zodiac/{z['id']}/2026-{mm}/")
        if r == "ok":
            done += 1
        elif r == "skip":
            skipped += 1
    print(f"\nDone: enriched={done}, skipped={skipped}, missing={missing} (month={mm})")


if __name__ == "__main__":
    main()
