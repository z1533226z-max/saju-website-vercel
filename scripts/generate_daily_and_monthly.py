#!/usr/bin/env python3
"""
사주 사이트 대량 SEO 페이지 생성기
- 12개 daily/{animal}/index.html (개별 띠 오늘의 운세)
- 144개 zodiac/{animal}/2026-{MM}/index.html (월별 운세)
총 156개 신규 페이지 생성
"""
import os
import hashlib
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
TODAY = date.today().isoformat()

# ──────────────────────────────────────────
# 12간지 기본 데이터
# ──────────────────────────────────────────
ZODIAC = [
    {"id": "rat",     "ko": "쥐띠",     "emoji": "🐀", "hanja": "子", "element": "수(水)", "el_short": "수"},
    {"id": "ox",      "ko": "소띠",     "emoji": "🐂", "hanja": "丑", "element": "토(土)", "el_short": "토"},
    {"id": "tiger",   "ko": "호랑이띠", "emoji": "🐅", "hanja": "寅", "element": "목(木)", "el_short": "목"},
    {"id": "rabbit",  "ko": "토끼띠",   "emoji": "🐇", "hanja": "卯", "element": "목(木)", "el_short": "목"},
    {"id": "dragon",  "ko": "용띠",     "emoji": "🐉", "hanja": "辰", "element": "토(土)", "el_short": "토"},
    {"id": "snake",   "ko": "뱀띠",     "emoji": "🐍", "hanja": "巳", "element": "화(火)", "el_short": "화"},
    {"id": "horse",   "ko": "말띠",     "emoji": "🐴", "hanja": "午", "element": "화(火)", "el_short": "화"},
    {"id": "goat",    "ko": "양띠",     "emoji": "🐑", "hanja": "未", "element": "토(土)", "el_short": "토"},
    {"id": "monkey",  "ko": "원숭이띠", "emoji": "🐒", "hanja": "申", "element": "금(金)", "el_short": "금"},
    {"id": "rooster", "ko": "닭띠",     "emoji": "🐓", "hanja": "酉", "element": "금(金)", "el_short": "금"},
    {"id": "dog",     "ko": "개띠",     "emoji": "🐕", "hanja": "戌", "element": "토(土)", "el_short": "토"},
    {"id": "pig",     "ko": "돼지띠",   "emoji": "🐷", "hanja": "亥", "element": "수(水)", "el_short": "수"},
]

MONTHS_KO = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]

# ──────────────────────────────────────────
# 월별 운세 콘텐츠 데이터
# ──────────────────────────────────────────
OVERALL_TEMPLATES = [
    "새로운 시작의 에너지가 충만한 시기입니다. 미루던 일이 있다면 과감히 도전해보세요. {el_short}의 기운이 당신을 밀어줍니다.",
    "인내와 끈기가 필요한 시기입니다. 당장 결과가 보이지 않더라도 묵묵히 전진하면 큰 수확을 얻을 수 있습니다.",
    "주변 사람들과의 관계에서 행운이 찾아옵니다. 소통에 적극적으로 나서면 뜻밖의 기회를 만날 수 있습니다.",
    "자기 자신을 돌아보는 시간이 필요합니다. 내면의 목소리에 귀 기울이면 올바른 방향을 찾을 수 있습니다.",
    "변화의 바람이 불어옵니다. 익숙한 것에 안주하기보다 새로운 환경을 받아들이면 성장할 수 있습니다.",
    "안정적인 시기입니다. 기존의 기반을 탄탄히 다지는 데 집중하세요. 큰 모험보다는 내실을 기하는 것이 좋습니다.",
    "창의적인 영감이 솟아나는 시기입니다. 예술적 활동이나 새로운 아이디어를 실행에 옮겨보세요.",
    "협력과 팀워크가 중요한 시기입니다. 혼자 해결하려 하기보다 함께하면 더 큰 성과를 거둘 수 있습니다.",
    "결실을 맺는 시기입니다. 그동안 쌓아온 노력이 결과로 나타나기 시작합니다. 자신감을 가지세요.",
    "학습과 성장의 시기입니다. 새로운 기술이나 지식을 습득하면 미래에 큰 도움이 될 것입니다.",
    "직감이 예리해지는 시기입니다. 중요한 결정을 내릴 때 이성과 직관의 균형을 맞추세요.",
    "마무리와 정리의 시기입니다. 한 해를 돌아보며 다음을 준비하는 시간으로 활용하세요.",
]

MONEY_TEMPLATES = [
    "재물 흐름이 원활합니다. 적극적인 재테크를 시작하기 좋은 시기입니다. 단, 과도한 욕심은 금물입니다.",
    "지출이 늘어날 수 있는 시기입니다. 계획적인 소비 습관을 유지하고, 충동구매를 자제하세요.",
    "뜻밖의 수입이 발생할 수 있습니다. 부업이나 투잡의 기회가 열릴 수 있으니 눈여겨보세요.",
    "저축에 집중하면 좋은 시기입니다. 큰 투자보다는 안정적인 적금이나 펀드가 적합합니다.",
    "사업적 기회가 열릴 수 있습니다. 네트워크를 활용한 비즈니스 제안에 귀를 기울이세요.",
    "금전 거래에 주의가 필요합니다. 보증이나 대출은 신중하게 결정하세요.",
    "투자 수익이 기대되는 시기입니다. 분산 투자로 리스크를 관리하면서 수익을 추구하세요.",
    "부동산이나 고가 자산에 관심을 가져볼 시기입니다. 장기적인 관점에서 접근하세요.",
    "절약 정신이 빛을 발하는 시기입니다. 작은 절약이 모여 큰 부를 만들어갑니다.",
    "동업이나 파트너십에서 재물이 올 수 있습니다. 신뢰할 수 있는 파트너를 만나세요.",
    "정기적인 수입이 안정되는 시기입니다. 이 안정을 기반으로 미래를 계획하세요.",
    "연말 정산이나 보너스 등 추가 수입이 기대됩니다. 현명하게 운용하세요.",
]

LOVE_TEMPLATES = [
    "연애 운이 상승합니다. 싱글이라면 새로운 만남의 기회가 찾아올 수 있습니다. 적극적으로 나서보세요.",
    "기존 관계가 깊어지는 시기입니다. 상대방에게 진심을 표현하면 관계가 한 단계 발전합니다.",
    "가족과의 시간이 중요한 시기입니다. 함께하는 활동을 통해 유대감을 강화하세요.",
    "소통이 핵심인 시기입니다. 오해가 생기기 쉬우니 솔직하고 명확하게 마음을 전하세요.",
    "로맨틱한 분위기가 감도는 시기입니다. 특별한 이벤트나 데이트를 계획해보세요.",
    "인간관계를 정리할 필요가 있는 시기입니다. 독이 되는 관계는 과감히 거리를 두세요.",
    "오래된 친구나 지인과의 재회가 기쁨을 가져다줍니다. 연락이 뜸했던 사람에게 먼저 손을 내밀어보세요.",
    "상대방의 장점에 집중하면 관계가 좋아집니다. 불만보다는 감사를 표현하세요.",
    "새로운 사교 모임에서 좋은 인연을 만날 수 있습니다. 취미 활동이나 동호회에 참여해보세요.",
    "혼자만의 시간도 소중합니다. 자기 자신을 사랑하는 것이 좋은 관계의 시작입니다.",
    "연인이나 배우자와 함께 여행을 떠나면 관계가 회복됩니다. 일상 탈출이 필요한 시기입니다.",
    "신뢰가 쌓이는 시기입니다. 진실된 마음이 상대방에게 전달되어 관계가 안정됩니다.",
]

HEALTH_TEMPLATES = [
    "활력이 넘치는 시기입니다. 새로운 운동을 시작하기에 좋습니다. 꾸준함이 핵심입니다.",
    "과로에 주의하세요. 적절한 휴식과 수면이 건강 유지의 핵심입니다.",
    "호흡기 건강에 신경 쓰세요. 환절기에는 특히 면역력 관리가 중요합니다.",
    "스트레스 관리가 필요한 시기입니다. 명상이나 요가로 마음의 안정을 찾으세요.",
    "소화기 건강에 주의하세요. 규칙적인 식사와 균형 잡힌 영양 섭취가 중요합니다.",
    "야외 활동이 건강에 도움이 됩니다. 자연 속에서 시간을 보내면 에너지가 충전됩니다.",
    "근골격계 건강을 체크하세요. 바른 자세와 스트레칭으로 몸을 관리하세요.",
    "수분 섭취를 충분히 하세요. 하루 8잔 이상의 물을 마시는 습관을 들이세요.",
    "정기 건강검진을 받아보세요. 예방이 최고의 치료입니다.",
    "심혈관 건강에 관심을 기울이세요. 유산소 운동과 저염식이 도움이 됩니다.",
    "눈 건강에 주의하세요. 장시간 전자기기 사용 후에는 반드시 눈을 쉬게 하세요.",
    "전반적으로 건강한 시기입니다. 이 건강을 유지하기 위해 생활습관을 점검하세요.",
]

WORK_TEMPLATES = [
    "직장에서 인정받을 수 있는 시기입니다. 맡은 일에 최선을 다하면 좋은 평가로 이어집니다.",
    "이직이나 전직을 고려하고 있다면 적극적으로 알아보세요. 좋은 기회가 있을 수 있습니다.",
    "팀 프로젝트에서 리더십을 발휘할 기회가 옵니다. 자신감 있게 의견을 제시하세요.",
    "업무 효율을 높이는 데 집중하세요. 새로운 툴이나 방법론을 배우면 성과가 올라갑니다.",
    "상사나 선배와의 관계가 좋아지는 시기입니다. 조언을 구하면 귀한 가르침을 얻을 수 있습니다.",
    "창업이나 사이드 프로젝트에 좋은 시기입니다. 아이디어를 실행에 옮겨보세요.",
    "업무 중 갈등이 생길 수 있습니다. 감정적 대응보다는 논리적으로 접근하세요.",
    "스킬 업그레이드에 투자하세요. 자격증이나 교육 과정이 커리어에 도움이 됩니다.",
    "안정적인 업무 환경이 유지됩니다. 꾸준히 성과를 쌓아가는 것이 중요합니다.",
    "네트워킹이 중요한 시기입니다. 업계 모임이나 컨퍼런스에 참여해보세요.",
    "프리랜서나 자영업자라면 새로운 클라이언트를 만날 기회가 있습니다.",
    "한 해를 마무리하며 커리어 방향을 재점검하세요. 내년 계획을 세우기 좋은 시기입니다.",
]

LUCKY_COLORS = ["빨강", "주황", "노랑", "초록", "파랑", "남색", "보라", "분홍", "하늘색", "금색", "은색", "갈색"]
LUCKY_DIRS = ["동쪽", "서쪽", "남쪽", "북쪽", "동남쪽", "동북쪽", "서남쪽", "서북쪽"]

def seed_hash(s):
    """Deterministic integer from string"""
    return int(hashlib.md5(s.encode()).hexdigest()[:8], 16)

def pick(lst, seed_val):
    return lst[seed_val % len(lst)]

def score(seed_val, lo=55, hi=95):
    return lo + (seed_val % (hi - lo + 1))

# ──────────────────────────────────────────
# Common HTML parts
# ──────────────────────────────────────────
def head_common():
    return """    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=Cormorant+Garamond:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">"""

def adsense_ga():
    return """    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-BNRL6FRMMM');</script>"""

def nav_html(active=""):
    items = [
        ("/", "사주풀이"), ("/zodiac/", "띠별 운세"), ("/daily/", "오늘의 운세"),
        ("/compatibility/", "궁합"), ("/palm/", "손금 분석"), ("/guide/", "사주 가이드"),
    ]
    links = []
    for href, label in items:
        cls = ' class="active"' if active == href else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    return f"""    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;">
                    <span class="gold-text">사주명리</span>
                </h1>
            </a>
            <nav class="nav-links">{''.join(links)}</nav>
        </nav>
    </header>"""

def footer_html():
    return """    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/compatibility/">궁합</a>
                <a href="/guide/">사주 가이드</a>
            </div>
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>"""


# ══════════════════════════════════════════
# PART 1: Daily individual pages (12개)
# ══════════════════════════════════════════
DAILY_JS_TEMPLATE = """
    <script>
    // Daily fortune - static generation, JS renders today's fortune
    var ZODIAC_DATA = {
        rat:{name:'쥐띠',emoji:'🐀',hanja:'子',element:'수(水)',branch:0},
        ox:{name:'소띠',emoji:'🐂',hanja:'丑',element:'토(土)',branch:1},
        tiger:{name:'호랑이띠',emoji:'🐅',hanja:'寅',element:'목(木)',branch:2},
        rabbit:{name:'토끼띠',emoji:'🐇',hanja:'卯',element:'목(木)',branch:3},
        dragon:{name:'용띠',emoji:'🐉',hanja:'辰',element:'토(土)',branch:4},
        snake:{name:'뱀띠',emoji:'🐍',hanja:'巳',element:'화(火)',branch:5},
        horse:{name:'말띠',emoji:'🐴',hanja:'午',element:'화(火)',branch:6},
        goat:{name:'양띠',emoji:'🐑',hanja:'未',element:'토(土)',branch:7},
        monkey:{name:'원숭이띠',emoji:'🐒',hanja:'申',element:'금(金)',branch:8},
        rooster:{name:'닭띠',emoji:'🐓',hanja:'酉',element:'금(金)',branch:9},
        dog:{name:'개띠',emoji:'🐕',hanja:'戌',element:'토(土)',branch:10},
        pig:{name:'돼지띠',emoji:'🐷',hanja:'亥',element:'수(水)',branch:11}
    };
    var MSGS={
        overall:['모든 일이 순조롭게 풀리는 날입니다.','차분하게 준비하면 좋은 결과를 얻습니다.','예상치 못한 기회가 찾아올 수 있습니다.','인내심이 필요한 날입니다.','주변 사람들과의 소통이 행운을 가져옵니다.','자기 자신에게 집중하면 좋은 하루가 됩니다.','새로운 시작에 좋은 날입니다.','감사하는 마음이 행복을 가져옵니다.','작은 변화가 큰 결과를 만듭니다.','직감을 믿고 행동하세요.','배움과 성장의 기회가 있습니다.','내면을 돌아보는 시간이 필요합니다.'],
        money:['재물운이 좋습니다. 투자에 좋은 시기입니다.','지출을 줄이고 절약하세요.','뜻밖의 수입이 있을 수 있습니다.','금전 결정은 신중하게.','저축에 집중하세요.','사업 기회가 올 수 있습니다.','안정적인 운용이 좋습니다.','협력에서 재물이 옵니다.','부수입 기회가 생깁니다.','서류를 꼼꼼히 확인하세요.','절약 습관이 부를 가져옵니다.','기다리면 더 좋은 조건이 옵니다.'],
        love:['로맨틱한 만남의 기회가 있습니다.','진심을 표현하면 좋은 반응을 얻습니다.','가족과의 시간이 마음을 편안하게 합니다.','갈등은 대화로 풀어보세요.','새로운 인연이 다가옵니다.','기존 관계가 깊어집니다.','사소한 배려가 큰 감동을 줍니다.','자기 자신을 사랑하세요.','오래된 친구와의 연락이 기쁨을 줍니다.','솔직한 마음이 좋은 관계를 만듭니다.','상대방 말에 귀 기울이세요.','만남의 자리에서 좋은 인연을 만납니다.'],
        health:['활력이 넘칩니다. 운동을 시작하세요.','충분한 수면이 중요합니다.','스트레스 관리에 신경 쓰세요.','산책이 기분 전환에 좋습니다.','수분 섭취를 충분히 하세요.','스트레칭으로 몸을 풀어주세요.','균형 잡힌 식사가 중요합니다.','자연 속에서 에너지를 충전하세요.','건강검진을 미루지 마세요.','허리와 눈에 주의하세요.','따뜻한 차가 마음과 몸을 녹입니다.','일과 휴식의 균형을 맞추세요.']
    };
    var COLORS=['빨강','주황','노랑','초록','파랑','남색','보라','분홍','하늘색','금색','은색','갈색'];
    var DIRS=['동쪽','서쪽','남쪽','북쪽','동남쪽','동북쪽','서남쪽','서북쪽'];

    function sRng(seed){var s=seed;return function(){s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff;};}
    function getDaySeed(){var d=new Date();return d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate();}
    function getGrade(s){if(s>=90)return{t:'대길',c:'grade-best'};if(s>=80)return{t:'길',c:'grade-good'};if(s>=70)return{t:'소길',c:'grade-ok'};if(s>=60)return{t:'평',c:'grade-normal'};return{t:'주의',c:'grade-caution'};}
    function stars(n){return String.fromCharCode(9733).repeat(n)+String.fromCharCode(9734).repeat(5-n);}

    (function(){
        var d=new Date();
        document.getElementById('today-date-badge').textContent=d.getFullYear()+String.fromCharCode(45765)+' '+(d.getMonth()+1)+String.fromCharCode(50900)+' '+d.getDate()+String.fromCharCode(51068)+' '+['일','월','화','수','목','금','토'][d.getDay()]+String.fromCharCode(50836)+String.fromCharCode(51068);

        var z=ZODIAC_DATA['__ZID__'];
        var seed=getDaySeed()*13+z.branch*7919;
        var r=sRng(seed);
        var os=Math.floor(r()*40+55),ms=Math.floor(r()*40+50),ls=Math.floor(r()*40+50),hs=Math.floor(r()*40+55);
        var om=MSGS.overall[Math.floor(r()*MSGS.overall.length)];
        var mm=MSGS.money[Math.floor(r()*MSGS.money.length)];
        var lm=MSGS.love[Math.floor(r()*MSGS.love.length)];
        var hm=MSGS.health[Math.floor(r()*MSGS.health.length)];
        var ln1=Math.floor(r()*45)+1,ln2=Math.floor(r()*45)+1;
        var lc=COLORS[Math.floor(r()*COLORS.length)];
        var ld=DIRS[Math.floor(r()*DIRS.length)];
        var lt=Math.floor(r()*12+1)+'시';
        var sr=Math.min(5,Math.max(1,Math.round(os/20)));
        var g=getGrade(os);

        var el=document.getElementById('daily-result');
        var h='<div class="result-header">';
        h+='<div class="result-emoji">'+z.emoji+'</div>';
        h+='<div class="result-info"><h3>'+z.name+' <span class="result-hanja">'+z.hanja+'('+z.element+')</span></h3><div class="result-stars">'+stars(sr)+'</div></div>';
        h+='<div class="result-grade '+g.c+'">'+g.t+'</div></div>';
        h+='<div class="result-scores-grid">';
        h+='<div class="result-score-card"><div class="rsc-icon">🔮</div><div class="rsc-label">총운</div><div class="rsc-score">'+os+'<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:'+os+'%;background:var(--color-gold);transition:width 0.8s;"></div></div></div>';
        h+='<div class="result-score-card"><div class="rsc-icon">💰</div><div class="rsc-label">재물운</div><div class="rsc-score">'+ms+'<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:'+ms+'%;background:#D4AF37;transition:width 0.8s;"></div></div></div>';
        h+='<div class="result-score-card"><div class="rsc-icon">💕</div><div class="rsc-label">연애운</div><div class="rsc-score">'+ls+'<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:'+ls+'%;background:#F87171;transition:width 0.8s;"></div></div></div>';
        h+='<div class="result-score-card"><div class="rsc-icon">💪</div><div class="rsc-label">건강운</div><div class="rsc-score">'+hs+'<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:'+hs+'%;background:#4ADE80;transition:width 0.8s;"></div></div></div>';
        h+='</div>';
        h+='<div class="result-messages">';
        h+='<div class="result-msg-card"><h4>🔮 오늘의 총운</h4><p>'+om+'</p></div>';
        h+='<div class="result-msg-card"><h4>💰 재물운</h4><p>'+mm+'</p></div>';
        h+='<div class="result-msg-card"><h4>💕 연애운</h4><p>'+lm+'</p></div>';
        h+='<div class="result-msg-card"><h4>💪 건강운</h4><p>'+hm+'</p></div>';
        h+='</div>';
        h+='<div class="result-lucky">';
        h+='<div class="lucky-chip"><span class="lucky-icon">🔢</span> 행운의 숫자: <strong>'+Math.min(ln1,ln2)+', '+Math.max(ln1,ln2)+'</strong></div>';
        h+='<div class="lucky-chip"><span class="lucky-icon">🎨</span> 행운의 색: <strong>'+lc+'</strong></div>';
        h+='<div class="lucky-chip"><span class="lucky-icon">🧭</span> 행운의 방향: <strong>'+ld+'</strong></div>';
        h+='<div class="lucky-chip"><span class="lucky-icon">⏰</span> 행운의 시간: <strong>'+lt+'</strong></div>';
        h+='</div>';
        h+='<div class="result-cta"><p>더 정확한 운세를 원하시면 생년월일시로 사주풀이를 해보세요!</p><a href="/" class="cta-btn-sm">무료 사주풀이 바로가기</a></div>';
        el.textContent='';
        el.insertAdjacentHTML('beforeend',h);
    })();
    </script>"""

def generate_daily_page(z):
    """daily/{animal}/index.html"""
    zid, ko, emoji, hanja, element = z["id"], z["ko"], z["emoji"], z["hanja"], z["element"]
    canon = f"https://saju.gon.ai.kr/daily/{zid}/"
    title = f"{ko} 오늘의 운세 | 매일 업데이트 {ko} 일일운세 - 사주명리"
    desc = f"오늘의 {ko}({hanja}) 운세를 확인하세요. 총운, 재물운, 연애운, 건강운 점수와 행운의 숫자, 색상, 방향까지 매일 새롭게 업데이트됩니다."
    keywords = f"{ko} 오늘의운세, {ko} 운세, {ko} 일일운세, 오늘 {ko}, {ko} 매일운세, 띠별 오늘운세"

    other_links = "\n".join(
        f'                <a href="/daily/{oz["id"]}/">{oz["emoji"]} {oz["ko"]}</a>'
        for oz in ZODIAC if oz["id"] != zid
    )

    faq_items = [
        (f"오늘 {ko} 총운은 어떤가요?", f"오늘의 {ko}({hanja}, {element}) 총운은 매일 자동으로 계산됩니다. 이 페이지에서 오늘의 총운 점수, 재물운, 연애운, 건강운을 실시간으로 확인하실 수 있습니다."),
        (f"{ko}의 행운의 숫자와 색상은?", f"오늘의 {ko} 행운의 숫자, 행운의 색상, 행운의 방향이 매일 업데이트됩니다. 하루를 시작하기 전에 확인하고 참고해보세요."),
        (f"{ko}는 어떤 해에 태어난 사람인가요?", f"{ko}({hanja})는 12간지 중 하나로, 출생연도의 마지막 자리에 따라 결정됩니다. 이 페이지에서 출생연도를 입력하면 자동으로 확인할 수 있습니다."),
    ]
    faq_json = ",\n        ".join(
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faq_items
    )

    js_block = DAILY_JS_TEMPLATE.replace("__ZID__", zid)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <title>{title}</title>
    <link rel="canonical" href="{canon}">
{head_common()}
    <link rel="stylesheet" href="/css/zodiac.css?v=1">
    <link rel="stylesheet" href="/css/daily.css?v=1">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{ko} 오늘의 운세 | 매일 업데이트">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canon}">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{ko} 오늘의 운세">
    <meta name="twitter:description" content="{desc}">
{adsense_ga()}
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"Article",
        "headline":"{ko} 오늘의 운세 - 매일 업데이트 총운, 재물운, 연애운, 건강운",
        "description":"{desc}",
        "url":"{canon}",
        "datePublished":"2026-01-01","dateModified":"{TODAY}",
        "publisher":{{"@type":"Organization","name":"사주명리","url":"https://saju.gon.ai.kr/"}},
        "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
            {{"@type":"ListItem","position":1,"name":"홈","item":"https://saju.gon.ai.kr/"}},
            {{"@type":"ListItem","position":2,"name":"오늘의 운세","item":"https://saju.gon.ai.kr/daily/"}},
            {{"@type":"ListItem","position":3,"name":"{ko} 오늘의 운세","item":"{canon}"}}
        ]}}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{faq_json}]
    }}
    </script>
</head>
<body>
{nav_html("/daily/")}

    <section class="daily-hero">
        <div class="container">
            <div class="hero-badge" id="today-date-badge"></div>
            <h1 class="hero-title"><span class="gold-text">{emoji} {ko} 오늘의 운세</span></h1>
            <p class="hero-subtitle">{ko}({hanja}, {element})의 오늘 운세를 확인하세요.<br>총운, 재물운, 연애운, 건강운이 매일 새롭게 업데이트됩니다.</p>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <div id="daily-result" class="daily-result"></div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">{ko} 월별 운세</span></h2>
            <div class="zodiac-links-grid">
{"".join(f'                <a href="/zodiac/{zid}/2026-{m:02d}/">{m}월 운세</a>' + chr(10) for m in range(1, 13))}            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">다른 띠 오늘의 운세</span></h2>
            <div class="zodiac-links-grid">
{other_links}
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/zodiac/{zid}/" class="cta-btn" style="background:transparent;border:1px solid var(--color-gold);color:var(--color-gold);">2026년 {ko} 운세</a>
            </div>
        </div>
    </section>

{footer_html()}
{js_block}
</body>
</html>"""


# ══════════════════════════════════════════
# PART 2: Monthly pages (144개)
# ══════════════════════════════════════════
def generate_monthly_page(z, month):
    """zodiac/{animal}/2026-{MM}/index.html"""
    zid, ko, emoji, hanja, element = z["id"], z["ko"], z["emoji"], z["hanja"], z["element"]
    el_short = z["el_short"]
    mm = f"{month:02d}"
    mko = MONTHS_KO[month - 1]
    canon = f"https://saju.gon.ai.kr/zodiac/{zid}/2026-{mm}/"
    title = f"2026년 {mko} {ko} 운세 | {ko} {mko} 총운, 재물운, 연애운 - 사주명리"
    desc = f"2026년 {mko} {ko}({hanja}) 운세 상세 분석. 총운, 재물운, 연애운, 건강운, 직장운 점수와 행운의 날, 색상, 숫자까지 확인하세요."
    keywords = f"{ko} {mko} 운세, 2026년 {mko} {ko}, {ko} {month}월, {mko} 띠별운세, {ko} 월별운세"

    s = seed_hash(f"{zid}-2026-{mm}")
    overall_score = score(s, 60, 92)
    money_score = score(s >> 3, 55, 90)
    love_score = score(s >> 5, 55, 90)
    health_score = score(s >> 7, 58, 92)
    work_score = score(s >> 9, 55, 90)

    overall_text = pick(OVERALL_TEMPLATES, s).replace("{el_short}", el_short)
    money_text = pick(MONEY_TEMPLATES, s >> 2)
    love_text = pick(LOVE_TEMPLATES, s >> 4)
    health_text = pick(HEALTH_TEMPLATES, s >> 6)
    work_text = pick(WORK_TEMPLATES, s >> 8)

    lucky_color = pick(LUCKY_COLORS, s >> 10)
    lucky_dir = pick(LUCKY_DIRS, s >> 11)
    lucky_num1 = (s % 45) + 1
    lucky_num2 = ((s >> 12) % 45) + 1
    lucky_day = (s % 28) + 1

    def grade(sc):
        if sc >= 85: return "대길"
        if sc >= 75: return "길"
        if sc >= 65: return "소길"
        return "평"

    def grade_css(sc):
        if sc >= 85: return "grade-best"
        if sc >= 75: return "grade-good"
        if sc >= 65: return "grade-ok"
        return "grade-normal"

    prev_m = month - 1 if month > 1 else 12
    next_m = month + 1 if month < 12 else 1
    month_nav = f"""            <div style="display:flex;justify-content:space-between;margin:2rem 0;">
                <a href="/zodiac/{zid}/2026-{prev_m:02d}/" style="color:var(--color-gold);">&larr; {MONTHS_KO[prev_m-1]}</a>
                <a href="/zodiac/{zid}/" style="color:var(--color-gold);">연간 운세</a>
                <a href="/zodiac/{zid}/2026-{next_m:02d}/" style="color:var(--color-gold);">{MONTHS_KO[next_m-1]} &rarr;</a>
            </div>"""

    months_grid = "\n".join(
        f'                <a href="/zodiac/{zid}/2026-{m:02d}/"{" style=background:var(--color-gold);color:#111;" if m==month else ""}>{MONTHS_KO[m-1]}</a>'
        for m in range(1, 13)
    )

    animals_grid = "\n".join(
        f'                <a href="/zodiac/{oz["id"]}/2026-{mm}/">{oz["emoji"]} {oz["ko"]}</a>'
        for oz in ZODIAC if oz["id"] != zid
    )

    faq_items = [
        (f"2026년 {mko} {ko} 총운은?", f"2026년 {mko} {ko}({hanja})의 총운 점수는 {overall_score}점({grade(overall_score)})입니다. {overall_text[:80]}"),
        (f"2026년 {mko} {ko} 재물운은?", f"{mko} {ko}의 재물운은 {money_score}점입니다. {money_text[:80]}"),
        (f"2026년 {mko} {ko} 행운의 날은?", f"{mko} {ko}의 행운의 날은 {lucky_day}일이며, 행운의 색상은 {lucky_color}, 행운의 방향은 {lucky_dir}입니다."),
    ]
    faq_json = ",\n        ".join(
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in faq_items
    )

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{desc}">
    <meta name="keywords" content="{keywords}">
    <title>{title}</title>
    <link rel="canonical" href="{canon}">
{head_common()}
    <link rel="stylesheet" href="/css/zodiac.css?v=1">
    <link rel="stylesheet" href="/css/daily.css?v=1">
    <meta property="og:type" content="article">
    <meta property="og:title" content="2026년 {mko} {ko} 운세">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canon}">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="2026년 {mko} {ko} 운세">
    <meta name="twitter:description" content="{desc}">
{adsense_ga()}
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"Article",
        "headline":"2026년 {mko} {ko} 운세 - 총운, 재물운, 연애운, 건강운, 직장운",
        "description":"{desc}",
        "url":"{canon}",
        "datePublished":"2026-01-01","dateModified":"{TODAY}",
        "publisher":{{"@type":"Organization","name":"사주명리","url":"https://saju.gon.ai.kr/"}},
        "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
            {{"@type":"ListItem","position":1,"name":"홈","item":"https://saju.gon.ai.kr/"}},
            {{"@type":"ListItem","position":2,"name":"띠별 운세","item":"https://saju.gon.ai.kr/zodiac/"}},
            {{"@type":"ListItem","position":3,"name":"{ko} 운세","item":"https://saju.gon.ai.kr/zodiac/{zid}/"}},
            {{"@type":"ListItem","position":4,"name":"{mko} 운세","item":"{canon}"}}
        ]}}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{faq_json}]
    }}
    </script>
</head>
<body>
{nav_html("/zodiac/")}

    <section class="daily-hero">
        <div class="container">
            <p style="font-size:0.9rem;color:var(--color-gold);margin-bottom:0.5rem;">2026년 {mko}</p>
            <h1 class="hero-title"><span class="gold-text">{emoji} {ko} {mko} 운세</span></h1>
            <p class="hero-subtitle">{ko}({hanja}, {element})의 2026년 {mko} 운세를 확인하세요.</p>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
{month_nav}

            <div class="result-header" style="margin-bottom:2rem;">
                <div class="result-emoji">{emoji}</div>
                <div class="result-info">
                    <h2 style="margin:0;font-size:1.3rem;">{ko} {mko} 운세</h2>
                    <p style="margin:0.3rem 0 0;color:var(--text-muted);font-size:0.9rem;">{hanja} | {element}</p>
                </div>
                <div class="result-grade {grade_css(overall_score)}">{grade(overall_score)}</div>
            </div>

            <div class="result-scores-grid">
                <div class="result-score-card"><div class="rsc-icon">🔮</div><div class="rsc-label">총운</div><div class="rsc-score">{overall_score}<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:{overall_score}%;background:var(--color-gold);transition:width 0.8s;"></div></div></div>
                <div class="result-score-card"><div class="rsc-icon">💰</div><div class="rsc-label">재물운</div><div class="rsc-score">{money_score}<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:{money_score}%;background:#D4AF37;transition:width 0.8s;"></div></div></div>
                <div class="result-score-card"><div class="rsc-icon">💕</div><div class="rsc-label">연애운</div><div class="rsc-score">{love_score}<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:{love_score}%;background:#F87171;transition:width 0.8s;"></div></div></div>
                <div class="result-score-card"><div class="rsc-icon">💪</div><div class="rsc-label">건강운</div><div class="rsc-score">{health_score}<small>점</small></div><div class="rsc-bar"><div class="rsc-fill" style="width:{health_score}%;background:#4ADE80;transition:width 0.8s;"></div></div></div>
            </div>

            <div class="result-messages">
                <div class="result-msg-card"><h3>🔮 {mko} 총운</h3><p>{overall_text}</p></div>
                <div class="result-msg-card"><h3>💰 재물운</h3><p>{money_text}</p></div>
                <div class="result-msg-card"><h3>💕 연애운</h3><p>{love_text}</p></div>
                <div class="result-msg-card"><h3>💪 건강운</h3><p>{health_text}</p></div>
                <div class="result-msg-card"><h3>💼 직장운</h3><p>{work_text}</p></div>
            </div>

            <div class="result-lucky">
                <div class="lucky-chip"><span class="lucky-icon">📅</span> 행운의 날: <strong>{lucky_day}일</strong></div>
                <div class="lucky-chip"><span class="lucky-icon">🔢</span> 행운의 숫자: <strong>{min(lucky_num1,lucky_num2)}, {max(lucky_num1,lucky_num2)}</strong></div>
                <div class="lucky-chip"><span class="lucky-icon">🎨</span> 행운의 색: <strong>{lucky_color}</strong></div>
                <div class="lucky-chip"><span class="lucky-icon">🧭</span> 행운의 방향: <strong>{lucky_dir}</strong></div>
            </div>

{month_nav}
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">{ko} 월별 운세</span></h2>
            <div class="zodiac-links-grid">
{months_grid}
            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">{mko} 다른 띠 운세</span></h2>
            <div class="zodiac-links-grid">
{animals_grid}
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/daily/{zid}/" class="cta-btn" style="background:transparent;border:1px solid var(--color-gold);color:var(--color-gold);">{ko} 오늘의 운세</a>
            </div>
        </div>
    </section>

{footer_html()}
</body>
</html>"""


# ══════════════════════════════════════════
# Sitemap generation
# ══════════════════════════════════════════
def generate_sitemap():
    urls = []
    def add(loc, freq="monthly", prio="0.7"):
        urls.append(f"""    <url>
        <loc>{loc}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>{freq}</changefreq>
        <priority>{prio}</priority>
    </url>""")

    add("https://saju.gon.ai.kr/", "weekly", "1.0")
    add("https://saju.gon.ai.kr/zodiac/", "weekly", "0.9")
    for z in ZODIAC:
        add(f"https://saju.gon.ai.kr/zodiac/{z['id']}/", "yearly", "0.8")
    for z in ZODIAC:
        for m in range(1, 13):
            add(f"https://saju.gon.ai.kr/zodiac/{z['id']}/2026-{m:02d}/", "monthly", "0.6")
    add("https://saju.gon.ai.kr/daily/", "daily", "0.9")
    for z in ZODIAC:
        add(f"https://saju.gon.ai.kr/daily/{z['id']}/", "daily", "0.7")
    add("https://saju.gon.ai.kr/palm/", "monthly", "0.7")
    add("https://saju.gon.ai.kr/additional-features.html", "monthly", "0.5")
    add("https://saju.gon.ai.kr/compatibility/", "monthly", "0.8")
    for z in ZODIAC:
        add(f"https://saju.gon.ai.kr/compatibility/{z['id']}/", "monthly", "0.7")
    add("https://saju.gon.ai.kr/guide/", "monthly", "0.8")
    for t in ["basics","five-elements","heavenly-stems","earthly-branches","yin-yang","ten-gods","how-to-read","day-master","fortune-cycle","shinshal","compatibility-theory","yongshin","elements-interaction"]:
        add(f"https://saju.gon.ai.kr/guide/{t}/", "monthly", "0.7")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""


# ══════════════════════════════════════════
# Main
# ══════════════════════════════════════════
def main():
    created = 0

    print("=== Generating daily/{animal}/ pages ===")
    for z in ZODIAC:
        d = os.path.join(PUBLIC_DIR, "daily", z["id"])
        os.makedirs(d, exist_ok=True)
        fpath = os.path.join(d, "index.html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(generate_daily_page(z))
        created += 1
        print(f"  Created daily/{z['id']}/index.html")

    print("\n=== Generating zodiac/{animal}/2026-{MM}/ pages ===")
    for z in ZODIAC:
        for month in range(1, 13):
            mm = f"{month:02d}"
            d = os.path.join(PUBLIC_DIR, "zodiac", z["id"], f"2026-{mm}")
            os.makedirs(d, exist_ok=True)
            fpath = os.path.join(d, "index.html")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(generate_monthly_page(z, month))
            created += 1
        print(f"  Created zodiac/{z['id']}/2026-01~12 (12 pages)")

    print("\n=== Updating sitemap.xml ===")
    sitemap_path = os.path.join(PUBLIC_DIR, "sitemap.xml")
    sitemap_content = generate_sitemap()
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    url_count = sitemap_content.count("<url>")
    print(f"  sitemap.xml updated ({url_count} URLs)")

    print(f"\nDone! Created {created} pages, sitemap has {url_count} URLs")


if __name__ == "__main__":
    main()
