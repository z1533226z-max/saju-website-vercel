# -*- coding: utf-8 -*-
"""
오늘의 운세(/daily/) 공용 로직

- 오늘의 일진(日辰): SajuCalculator.calculate_day_pillar 로 계산
- 띠별 점수: 내 띠의 지지와 오늘 일지(日支)의 관계
  (육합·삼합·충·형·해·파·원진, 없으면 평)가 총운 점수 범위를 정하고,
  그 범위 안에서만 날짜별 시드로 변동한다.

- 전체 운세 지수(day_energy): 오늘 일진과 이번 달 월주의 관계
  (일간 왕상휴수 + 일지·월지 합충)로만 정한다. 12띠 평균이 아니다.

/daily/ (api/daily/index.py) 와 /daily/<띠>/ (api/daily/fortune.py) 가
같은 함수를 써서 목록과 상세 페이지 점수가 항상 일치한다.
"""
from datetime import datetime, timedelta, timezone

from _core.saju_calculator import SajuCalculator

KST = timezone(timedelta(hours=9))

_calc = SajuCalculator()

ZODIAC_DATA = {
    "rat":     {"name": "쥐띠",     "emoji": "🐀", "hanja": "子", "element": "수(水)", "branch": 0},
    "ox":      {"name": "소띠",     "emoji": "🐂", "hanja": "丑", "element": "토(土)", "branch": 1},
    "tiger":   {"name": "호랑이띠", "emoji": "🐅", "hanja": "寅", "element": "목(木)", "branch": 2},
    "rabbit":  {"name": "토끼띠",   "emoji": "🐇", "hanja": "卯", "element": "목(木)", "branch": 3},
    "dragon":  {"name": "용띠",     "emoji": "🐉", "hanja": "辰", "element": "토(土)", "branch": 4},
    "snake":   {"name": "뱀띠",     "emoji": "🐍", "hanja": "巳", "element": "화(火)", "branch": 5},
    "horse":   {"name": "말띠",     "emoji": "🐴", "hanja": "午", "element": "화(火)", "branch": 6},
    "goat":    {"name": "양띠",     "emoji": "🐑", "hanja": "未", "element": "토(土)", "branch": 7},
    "monkey":  {"name": "원숭이띠", "emoji": "🐒", "hanja": "申", "element": "금(金)", "branch": 8},
    "rooster": {"name": "닭띠",     "emoji": "🐓", "hanja": "酉", "element": "금(金)", "branch": 9},
    "dog":     {"name": "개띠",     "emoji": "🐕", "hanja": "戌", "element": "토(土)", "branch": 10},
    "pig":     {"name": "돼지띠",   "emoji": "🐷", "hanja": "亥", "element": "수(水)", "branch": 11},
}

ZODIAC_ORDER = ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
                "horse", "goat", "monkey", "rooster", "dog", "pig"]

# ── 지지 관계표 (子0 丑1 寅2 卯3 辰4 巳5 午6 未7 申8 酉9 戌10 亥11) ──────────
_pairs = lambda *ps: {frozenset(p) for p in ps}  # noqa: E731
YUKHAP = _pairs((0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7))          # 육합
SAMHAP = [{8, 0, 4}, {2, 6, 10}, {5, 9, 1}, {11, 3, 7}]                   # 삼합
HYEONG = _pairs((2, 5), (5, 8), (8, 2), (1, 10), (10, 7), (7, 1), (0, 3))  # 형
JAHYEONG = {4, 6, 9, 11}                                                  # 자형 (辰午酉亥)
WONJIN = _pairs((0, 7), (1, 6), (2, 9), (3, 8), (4, 11), (5, 10))          # 원진
HAE = _pairs((0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10))             # 해
PA = _pairs((0, 9), (3, 6), (4, 1), (7, 10), (2, 11), (5, 8))              # 파

# 관계별 표기·성격·총운 점수 범위·한 줄 풀이 (우선순위 순)
RELATIONS = {
    "yukhap": {"label": "육합(六合)", "tone": "good", "band": (85, 97),
               "explain": "서로 짝을 이루는 육합이라 사람과 일이 자연스럽게 맞물리는 날입니다. 부탁이나 협업을 시도해 보세요."},
    "samhap": {"label": "삼합(三合)", "tone": "good", "band": (80, 93),
               "explain": "같은 삼합 무리라 뜻이 맞는 사람과 힘을 모으기 좋은 날입니다."},
    "chung":  {"label": "충(沖)", "tone": "caution", "band": (46, 60),
               "explain": "정면으로 부딪히는 충이라 변동이 많은 날입니다. 큰 결정이나 먼 이동은 한 번 더 점검하세요."},
    "hyeong": {"label": "형(刑)", "tone": "caution", "band": (52, 65),
               "explain": "형이 걸려 마찰이나 실수가 생기기 쉽습니다. 서류와 말은 꼼꼼히 확인하세요."},
    "wonjin": {"label": "원진(怨嗔)", "tone": "caution", "band": (54, 67),
               "explain": "원진이라 괜한 서운함이 쌓이기 쉬운 날입니다. 감정 표현은 부드럽게 하세요."},
    "hae":    {"label": "해(害)", "tone": "caution", "band": (56, 69),
               "explain": "해가 되는 관계라 가까운 사이에서 오해가 생기기 쉽습니다. 한발 물러서 상대의 말을 먼저 들어 보세요."},
    "pa":     {"label": "파(破)", "tone": "caution", "band": (58, 71),
               "explain": "파가 걸려 계획이 조금씩 어긋날 수 있습니다. 일정에 여유를 두고 움직이세요."},
    "pyeong": {"label": "평(平)", "tone": "neutral", "band": (64, 79),
               "explain": "특별한 합이나 충이 없어 무난한 날입니다. 평소 페이스를 지키면 충분합니다."},
}
_SAME_BRANCH_EXPLAIN = "오늘 일지가 내 띠와 같은 지지라 익숙한 흐름입니다. 새 일보다 하던 일을 이어가기 좋습니다."
_JAHYEONG_EXPLAIN = "같은 지지가 겹치는 자형(自刑)이라 스스로를 몰아붙이기 쉽습니다. 무리한 일정은 줄이세요."

FORTUNE_MESSAGES = {
    "overall": {
        "good": [
            "모든 일이 순조롭게 풀리는 날입니다. 적극적으로 행동하세요.",
            "예상치 못한 기회가 찾아올 수 있습니다. 열린 마음을 가지세요.",
            "주변 사람들과의 소통이 행운을 가져다줍니다.",
            "새로운 시작에 좋은 날입니다. 미루던 일을 시작해보세요.",
            "직감을 믿고 행동하면 좋은 결과를 얻을 수 있습니다.",
        ],
        "neutral": [
            "차분하게 준비하면 좋은 결과를 얻을 수 있는 날입니다.",
            "자기 자신에게 집중하면 좋은 하루가 됩니다.",
            "감사하는 마음이 더 큰 행복을 가져다줍니다.",
            "작은 변화가 큰 결과를 만들어내는 날입니다.",
            "배움과 성장의 기회가 있는 날입니다. 새로운 것을 배워보세요.",
        ],
        "caution": [
            "인내심이 필요한 날입니다. 서두르지 마세요.",
            "조용히 내면을 돌아보는 시간이 필요한 날입니다.",
            "말과 행동을 한 번 더 점검하면 실수를 줄일 수 있는 날입니다.",
            "무리하게 밀어붙이기보다 한 걸음 물러서 흐름을 지켜보세요.",
        ],
    },
    "money": [
        "재물운이 좋습니다. 투자나 저축에 좋은 시기입니다.",
        "지출을 줄이고 절약하는 것이 좋은 날입니다.",
        "뜻밖의 수입이 있을 수 있습니다.",
        "금전적인 결정은 신중하게 내리세요.",
        "소비보다는 저축에 집중하면 좋겠습니다.",
        "사업적 기회가 올 수 있으니 준비하세요.",
        "과감한 투자보다는 안정적인 운용이 좋습니다.",
        "동업이나 협력에서 재물이 올 수 있습니다.",
        "부수입의 기회가 생길 수 있습니다.",
        "금전 거래는 서류를 꼼꼼히 확인하세요.",
        "절약의 습관이 큰 부를 가져다줍니다.",
        "기다리면 더 좋은 조건이 올 수 있습니다.",
    ],
    "love": [
        "로맨틱한 만남의 기회가 있습니다.",
        "상대방에게 진심을 표현하면 좋은 반응을 얻을 수 있습니다.",
        "가족과의 시간을 가지면 마음이 편안해집니다.",
        "갈등이 있다면 대화로 풀어보세요.",
        "새로운 인연이 다가올 수 있는 날입니다.",
        "기존 관계가 더욱 깊어지는 날입니다.",
        "사소한 배려가 큰 감동을 줍니다.",
        "혼자만의 시간도 중요합니다. 자기 자신을 사랑하세요.",
        "오래된 친구와의 연락이 기쁨을 가져다줍니다.",
        "솔직한 마음이 좋은 관계를 만듭니다.",
        "상대방의 말에 귀 기울이면 관계가 좋아집니다.",
        "만남의 자리에서 좋은 인연을 만날 수 있습니다.",
    ],
    "health": [
        "활력이 넘치는 날입니다. 운동을 시작해보세요.",
        "충분한 수면이 건강의 기본입니다. 일찍 잠자리에 드세요.",
        "스트레스 관리에 신경 쓰세요. 명상이 도움이 됩니다.",
        "가벼운 산책이 기분 전환에 좋은 날입니다.",
        "수분 섭취를 충분히 하세요.",
        "무리한 운동보다는 스트레칭으로 몸을 풀어주세요.",
        "균형 잡힌 식사가 중요한 날입니다.",
        "자연 속에서 시간을 보내면 에너지가 충전됩니다.",
        "정기 건강검진을 미루지 마세요.",
        "눈과 허리에 주의하세요. 자세를 바로 하세요.",
        "따뜻한 차 한 잔이 마음과 몸을 녹여줍니다.",
        "일과 휴식의 균형을 잘 맞추세요.",
    ],
}
# 점수가 낮은 날에는 고르지 않는 '강한 긍정' 문구 (점수와 문구가 엇갈리지 않도록)
_STRONG_POSITIVE = {"money": {0, 2}, "love": {0, 4, 11}, "health": {0}}
_STRONG_MIN_SCORE = 75

LUCKY_COLORS = ["빨강", "주황", "노랑", "초록", "파랑", "남색", "보라", "분홍", "하늘색", "금색", "은색", "갈색"]
LUCKY_DIRECTIONS = ["동쪽", "서쪽", "남쪽", "북쪽", "동남쪽", "동북쪽", "서남쪽", "서북쪽"]


def seeded_random(seed):
    """JS seededRandom 과 같은 LCG (float 연산으로 JS double 정밀도 재현)."""
    s = seed

    def next_val():
        nonlocal s
        s = int(float(s) * 1103515245.0 + 12345.0) & 0x7FFFFFFF
        return s / 0x7FFFFFFF
    return next_val


def _pick(rng, n):
    """0..n-1 균등 선택 (rng()가 1.0을 내도 범위를 넘지 않음)."""
    return min(n - 1, int(rng() * n))


def _to_kst(now=None):
    if now is None:
        return datetime.now(KST)
    if now.tzinfo is not None:
        return now.astimezone(KST)
    return now


def get_day_seed(now=None):
    now = _to_kst(now)
    return now.year * 10000 + now.month * 100 + now.day


_BRANCH_INDEX = {b["name_ko"]: i for i, b in enumerate(_calc.earthly_branches)}


def _pillar_info(p):
    """SajuCalculator 의 기둥(일주·월주) dict → 화면 표기용 dict."""
    branch_index = _BRANCH_INDEX[p["earthly"]]
    return {
        "name_ko": p["heavenly"] + p["earthly"],
        "hanja": p["heavenly_hanja"] + p["earthly_hanja"],
        "display": f"{p['heavenly']}{p['earthly']}({p['heavenly_hanja']}{p['earthly_hanja']})",
        "stem_ko": p["heavenly"], "stem_hanja": p["heavenly_hanja"],
        "branch_ko": p["earthly"], "branch_hanja": p["earthly_hanja"],
        "branch_index": branch_index,
        "element": p["element"],                                         # 천간 오행
        "branch_element": _calc.earthly_branches[branch_index]["element"],  # 지지 오행
    }


def get_day_ilji(now=None):
    """오늘(KST)의 일진. 예: 2026-10-03 → 경술(庚戌), 일간 오행 금."""
    now = _to_kst(now)
    return _pillar_info(_calc.calculate_day_pillar(datetime(now.year, now.month, now.day)))


def get_month_pillar(now=None):
    """오늘(KST)이 속한 절기월의 월주. 예: 2026-10-03 → 정유(丁酉), 월지 오행 금."""
    now = _to_kst(now)
    return _pillar_info(_calc.calculate_month_pillar(now.year, now.month, now.day))


def branch_relation(mine, day):
    """내 띠 지지(mine)와 오늘 일지(day)의 관계. 여러 관계가 겹치면 우선순위가 높은 것을 대표로."""
    pair = frozenset((mine, day))
    found = []
    if mine == day:
        if mine in JAHYEONG:
            found.append("hyeong")
    else:
        if pair in YUKHAP:
            found.append("yukhap")
        if any(pair <= g for g in SAMHAP):
            found.append("samhap")
        if (mine - day) % 12 == 6:
            found.append("chung")
        if pair in HYEONG:
            found.append("hyeong")
        if pair in WONJIN:
            found.append("wonjin")
        if pair in HAE:
            found.append("hae")
        if pair in PA:
            found.append("pa")

    key = found[0] if found else "pyeong"
    info = RELATIONS[key]
    explain = info["explain"]
    if mine == day:
        explain = _JAHYEONG_EXPLAIN if key == "hyeong" else _SAME_BRANCH_EXPLAIN
    return {
        "key": key,
        "label": info["label"],
        "tone": info["tone"],
        "explain": explain,
        "also": found[1:],
        "also_labels": [RELATIONS[k]["label"] for k in found[1:]],
    }


# ── 전체 운세 지수: 오늘 일진이 이번 달 월주와 얼마나 맞물리는가 ──────────────
# ① 일간 오행이 월령(월지 오행)에서 받는 힘: 왕상휴수사(旺相休囚死)
_GENERATES = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}   # 상생
_CONTROLS = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}    # 상극
SEASON_STRENGTH = {   # key: (표기, 점수)
    "wang": ("왕(旺)", 10),   # 달과 같은 오행
    "sang": ("상(相)", 6),    # 달이 일간을 생함
    "hyu":  ("휴(休)", 0),    # 일간이 달을 생함
    "su":   ("수(囚)", -4),   # 일간이 달을 극함
    "sa":   ("사(死)", -8),   # 달이 일간을 극함
}
# ② 일지 ↔ 월지 관계 (일지가 월지를 충하면 택일에서 꺼리는 월파일)
MONTH_RELATION_POINTS = {"yukhap": 14, "samhap": 10, "pyeong": 0, "pa": -5, "hae": -5,
                         "wonjin": -7, "hyeong": -8, "chung": -15}
DAY_ENERGY_BASE = 68
DAY_ENERGY_TIERS = [(85, "기운이 잘 맞물리는 날"), (72, "흐름이 순한 날"),
                    (60, "무난한 날"), (0, "신중하게 움직일 날")]


def season_strength(day_element, month_element):
    """일간 오행이 월령 오행 속에서 왕·상·휴·수·사 중 무엇인지."""
    if day_element == month_element:
        return "wang"
    if _GENERATES[month_element] == day_element:
        return "sang"
    if _GENERATES[day_element] == month_element:
        return "hyu"
    if _CONTROLS[day_element] == month_element:
        return "su"
    return "sa"


def _signed(n):
    return f"+{n}" if n > 0 else (f"−{-n}" if n < 0 else "±0")


def day_energy(now=None):
    """오늘의 전체 운세 지수 = 기본 68 + ① 일간 왕상휴수 + ② 일지·월지 관계.

    12띠 점수와 무관하게 오늘 일진과 이번 달 월주만으로 정해지므로
    날마다 실제로 달라지고, 화면에 근거(reason)를 그대로 보여 줄 수 있다.
    """
    now = _to_kst(now)
    day = get_day_ilji(now)
    month = get_month_pillar(now)
    s_key = season_strength(day["element"], month["branch_element"])
    s_label, s_pts = SEASON_STRENGTH[s_key]
    rel = branch_relation(month["branch_index"], day["branch_index"])
    r_pts = MONTH_RELATION_POINTS[rel["key"]]
    r_label = rel["label"] + ("·월파" if rel["key"] == "chung" else "")
    score = DAY_ENERGY_BASE + s_pts + r_pts
    desc = next(text for floor, text in DAY_ENERGY_TIERS if score >= floor)
    reason = (f"절기상 이번 달 {month['display']}월 기준: 기본 {DAY_ENERGY_BASE}"
              f" · 일간 {day['stem_hanja']}({day['element']}) {s_label} {_signed(s_pts)}"
              f" · 일지 {day['branch_hanja']}↔월지 {month['branch_hanja']} {r_label} {_signed(r_pts)}")
    return {"score": score, "desc": desc, "reason": reason, "strength": s_key, "relation": rel["key"]}


def _pick_message(category, score, rng):
    msgs = FORTUNE_MESSAGES[category]
    strong = _STRONG_POSITIVE.get(category, set())
    pool = [m for i, m in enumerate(msgs) if score >= _STRONG_MIN_SCORE or i not in strong]
    return pool[_pick(rng, len(pool))]


def _grade(score):
    if score >= 90: return "대길", "grade-best"
    if score >= 80: return "길", "grade-good"
    if score >= 70: return "소길", "grade-ok"
    if score >= 60: return "평", "grade-normal"
    return "주의", "grade-caution"


def generate_fortune(zodiac_key, now=None):
    now = _to_kst(now)
    zodiac = ZODIAC_DATA[zodiac_key]
    ilji = get_day_ilji(now)
    relation = branch_relation(zodiac["branch"], ilji["branch_index"])
    rng = seeded_random(get_day_seed(now) * 13 + zodiac["branch"] * 7919)

    # 총운: 지지 관계가 정한 범위 안에서만 변동
    lo, hi = RELATIONS[relation["key"]]["band"]
    overall = lo + _pick(rng, hi - lo + 1)

    def around_overall():
        return max(40, min(99, overall - 10 + _pick(rng, 21)))

    money, love, health = around_overall(), around_overall(), around_overall()

    overall_pool = FORTUNE_MESSAGES["overall"][relation["tone"]]
    overall_msg = overall_pool[_pick(rng, len(overall_pool))]
    money_msg = _pick_message("money", money, rng)
    love_msg = _pick_message("love", love, rng)
    health_msg = _pick_message("health", health, rng)

    # 행운의 숫자 2개 (1~45, 서로 다름)
    ln1 = _pick(rng, 45) + 1
    ln2 = _pick(rng, 44) + 1
    if ln2 >= ln1:
        ln2 += 1
    lucky_color = LUCKY_COLORS[_pick(rng, len(LUCKY_COLORS))]
    lucky_dir = LUCKY_DIRECTIONS[_pick(rng, len(LUCKY_DIRECTIONS))]
    lucky_time = f"{_pick(rng, 12) + 1}시"

    star = min(5, max(1, round(overall / 20)))
    g_text, g_class = _grade(overall)

    return {
        "zodiac": zodiac, "overall": overall, "money": money, "love": love, "health": health,
        "overall_msg": overall_msg, "money_msg": money_msg, "love_msg": love_msg, "health_msg": health_msg,
        "lucky_number": f"{min(ln1, ln2)}, {max(ln1, ln2)}",
        "lucky_color": lucky_color, "lucky_dir": lucky_dir, "lucky_time": lucky_time,
        "stars": "★" * star + "☆" * (5 - star), "grade_text": g_text, "grade_class": g_class,
        "ilji": ilji, "relation": relation,
    }
