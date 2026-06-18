#!/usr/bin/env python3
"""Batch 2: add 10 high-search-volume dream (꿈해몽) pages.

Targets Naver top-volume dream keywords missing from the existing 57 pages:
똥/귀신/시체/조상/전 애인/알몸/죽는/싸우는/지진/보석.

Idempotent. Does NOT touch the existing 57 pages — uses the *standardized*
nav/footer (with /yearly/ and /palm/) so new pages match the live site,
and patches the hub + sitemap in place.
"""

import os
import json
import hashlib

SITE_URL = "https://saju.gon.ai.kr"
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "dream")
SITEMAP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "public", "sitemap.xml")
TODAY = "2026-06-18"

# Standardized header nav (matches live, includes /yearly/ and /palm/)
NAV_LINKS = '<a href="/">사주풀이</a><a href="/zodiac/">띠별 운세</a><a href="/daily/">오늘의 운세</a><a href="/yearly/">2026년 운세</a><a href="/compatibility/">궁합</a><a href="/dream/" class="active">꿈해몽</a><a href="/palm/">손금 분석</a><a href="/guide/">사주 가이드</a>'

FOOTER = """    <footer class="site-footer">
        <div class="container">
                        <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/yearly/">2026년 운세</a>
                <a href="/compatibility/">궁합</a>
                <a href="/dream/">꿈해몽</a>
                <a href="/palm/">손금 분석</a>
                <a href="/guide/">사주 가이드</a>
            </div>
            <p class="footer-copy">&copy; 2026 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 꿈해몽은 전통 해몽학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>"""

DREAMS = [
    {
        "slug": "poop", "emoji": "💩", "title": "똥꿈",
        "keywords": "똥꿈 해몽, 똥꿈 의미, 똥꿈 로또, 대변꿈 해몽, 똥밟는꿈, 똥꿈 재물운",
        "desc": "똥꿈 해몽 총정리. 똥을 밟는 꿈, 똥을 뒤집어쓰는 꿈, 화장실 가득 찬 똥꿈 등 재물운과 연결된 똥꿈의 상황별 의미와 행운의 숫자.",
        "meanings": [
            ("똥을 밟는 꿈", "전통적으로 재물운이 들어오는 대표적 길몽입니다. 뜻밖의 수입이나 횡재가 따를 수 있습니다."),
            ("똥을 온몸에 뒤집어쓰는 꿈", "더러울수록 좋다는 똥꿈의 정수로, 막대한 재물이 들어올 최고의 길몽입니다. 사업 성공이나 큰 횡재를 의미합니다."),
            ("화장실에 똥이 가득 찬 꿈", "재물이 쌓이고 사업이 번창할 징조입니다. 금전운이 크게 상승합니다."),
            ("똥을 만지는 꿈", "손에 재물이 들어옵니다. 돈과 관련된 좋은 소식이 있을 수 있습니다."),
            ("똥을 치우거나 퍼내는 꿈", "오래된 빚이나 골칫거리를 정리하게 됩니다. 다만 아까워하며 버리면 손실에 주의하세요."),
            ("똥 냄새가 진하게 나는 꿈", "냄새가 강할수록 재물운이 강한 것으로 봅니다. 금전적 행운이 가까이 있습니다."),
        ],
        "faq": [
            ("똥꿈을 꾸면 로또를 사야 하나요?", "똥꿈은 뱀꿈, 돼지꿈과 함께 대표적인 재물꿈으로, 특히 똥을 뒤집어쓰는 꿈은 횡재의 징조로 해석됩니다."),
            ("똥꿈은 왜 더러울수록 좋은가요?", "해몽학에서 똥은 거름, 즉 재물의 상징입니다. 현실의 불쾌함과 반대로 풍요와 금전운을 뜻하기 때문입니다."),
            ("아기가 똥을 싸는 꿈은?", "아기 똥꿈 역시 재물운 상승의 길몽으로 봅니다. 집안에 경사나 금전적 이득이 따를 수 있습니다."),
        ],
        "related": ["money", "gold", "pig", "snake"],
    },
    {
        "slug": "ghost", "emoji": "👻", "title": "귀신꿈",
        "keywords": "귀신꿈 해몽, 귀신꿈 의미, 귀신한테쫓기는꿈, 귀신쫓는꿈, 가위눌리는꿈, 귀신꿈 길몽",
        "desc": "귀신꿈 해몽 총정리. 귀신에게 쫓기는 꿈, 귀신을 이기는 꿈, 귀신이 집에 들어오는 꿈 등 무서운 꿈 속에 숨은 길흉의 의미와 해석.",
        "meanings": [
            ("귀신에게 쫓기는 꿈", "현실의 스트레스나 건강에 대한 압박을 반영합니다. 충분한 휴식과 마음의 안정이 필요합니다."),
            ("귀신을 물리치거나 쫓아내는 꿈", "병마나 장애물을 이긴다는 최고의 길몽입니다. 건강 회복이나 경쟁에서의 승리를 의미합니다."),
            ("귀신이 집에 들어오는 꿈", "예상치 못한 변화나 손님이 찾아올 징조입니다. 주변 상황을 점검하세요."),
            ("귀신과 대화하는 꿈", "무의식의 메시지에 귀 기울일 때입니다. 직감이 중요한 답을 줄 수 있습니다."),
            ("귀신이 물건을 주는 꿈", "의외의 길몽으로, 뜻밖의 재물이나 좋은 기회가 들어올 수 있습니다."),
            ("귀신을 보고도 무섭지 않은 꿈", "두려움을 극복하고 어려운 문제를 해결할 힘이 생긴다는 의미입니다."),
        ],
        "faq": [
            ("귀신꿈은 왜 자주 꾸나요?", "주로 심리적 불안과 스트레스, 해결되지 않은 걱정이 원인입니다. 잠시 휴식을 취하고 마음을 편안히 하는 것이 좋습니다."),
            ("귀신꿈이 길몽일 수도 있나요?", "네, 귀신을 이기거나 귀신이 물건을 주는 꿈은 건강 회복과 재물운을 의미하는 길몽으로 해석합니다."),
            ("가위에 눌리는 꿈은?", "수면 중 몸과 의식이 분리되며 생기는 현상으로, 과로와 스트레스가 누적되었다는 신호일 수 있습니다."),
        ],
        "related": ["deceased", "ancestor", "corpse", "war"],
    },
    {
        "slug": "corpse", "emoji": "⚰️", "title": "시체꿈",
        "keywords": "시체꿈 해몽, 시체꿈 의미, 시체보는꿈, 시체태우는꿈, 죽은사람시체꿈, 시체꿈 재물운",
        "desc": "시체꿈 해몽 총정리. 시체를 보는 꿈, 방 안의 시체꿈, 시체를 태우는 꿈 등 무섭지만 재물·명예 길몽으로 풀이되는 시체꿈의 상황별 의미.",
        "meanings": [
            ("시체를 보는 꿈", "공포와 달리 업적, 재물, 새로운 시작을 상징하는 대표적 길몽입니다. 공들인 일이 결실을 맺습니다."),
            ("방 안에 시체가 있는 꿈", "집안에 경사가 생기거나 큰 재물이 들어와 가세가 일어설 징조입니다."),
            ("시체를 태우는 꿈", "묵은 고민을 깨끗이 태워 없애고, 적은 자본으로 큰 일을 일으킬 수 있는 최상의 길몽입니다."),
            ("시체를 닦아주는 꿈", "예상치 못한 횡재수가 생기며 재산이 불어납니다."),
            ("시체를 보고 도망가는 꿈", "다 잡은 기회를 놓치거나 불안으로 이득을 보지 못할 수 있습니다. 침착함이 필요합니다."),
            ("시체가 여럿 쌓여 있는 꿈", "가업의 번창과 큰 성취를 의미하는 강한 재물 길몽입니다."),
        ],
        "faq": [
            ("시체꿈은 무서운데 좋은 꿈인가요?", "죽음은 과거의 끝과 새로운 탄생을 의미해, 시체꿈은 재물·명예·문제 해결을 뜻하는 길몽으로 풀이됩니다."),
            ("시체가 흉측할수록 좋다는 게 사실인가요?", "전통 해몽에서 시체가 썩거나 흉측할수록 현실의 행운이 더 강해지는 경향이 있다고 봅니다."),
            ("시체꿈을 꾸면 로또를 사도 되나요?", "재물 길몽에 해당하므로 소액 복권을 시도해볼 만하지만, 맹신보다는 긍정적 에너지로 삼는 것이 좋습니다."),
        ],
        "related": ["ghost", "ancestor", "money", "deceased"],
    },
    {
        "slug": "ancestor", "emoji": "🙏", "title": "조상꿈",
        "keywords": "조상꿈 해몽, 조상님꿈 의미, 조상이돈주는꿈, 조상님화내는꿈, 제사꿈, 조상꿈 로또",
        "desc": "조상꿈 해몽 총정리. 조상님이 웃는 꿈, 조상이 돈을 주는 꿈, 조상님이 화내는 꿈 등 운이 열리는 신호로 풀이되는 조상꿈의 상황별 의미.",
        "meanings": [
            ("조상님이 웃으며 나타나는 꿈", "막혔던 운이 열리는 길몽입니다. 좋은 일이 다가오고 조상의 보살핌을 받고 있다는 의미입니다."),
            ("조상이 돈이나 물건을 주는 꿈", "재물운과 귀인운이 크게 상승합니다. 대표적인 복권·재물 관련 길몽으로 꼽힙니다."),
            ("조상님이 화를 내는 꿈", "현재 방향이 잘못되었다는 경고일 수 있습니다. 행동을 돌아보고 성묘나 기도를 올려보세요."),
            ("조상과 함께 식사하는 꿈", "재물운과 가정의 화목을 의미합니다. 집안에 좋은 기운이 깃듭니다."),
            ("조상이 길을 알려주는 꿈", "중요한 결정에 대한 지혜를 얻게 됩니다. 직감을 믿고 나아가세요."),
            ("조상님께 절을 올리는 꿈", "마음의 평안과 안정을 찾고, 가정사가 순조롭게 풀릴 징조입니다."),
        ],
        "faq": [
            ("조상님 꿈을 꾸면 제사를 지내야 하나요?", "전통적으로 조상이 꿈에 나오면 성묘하거나 기도를 올리는 것이 좋다고 합니다. 추모하는 마음이 가장 중요합니다."),
            ("조상이 돈을 주는 꿈은 로또 신호인가요?", "조상이 무언가를 주는 꿈은 재물운과 귀인운 상승의 길몽으로, 횡재의 신호로 자주 언급됩니다."),
            ("조상꿈을 자주 꾸는 이유는?", "그리움이나 미해결 감정, 또는 어려운 상황에서 지혜를 구하고 싶은 무의식의 반영일 수 있습니다."),
        ],
        "related": ["deceased", "ghost", "money", "corpse"],
    },
    {
        "slug": "ex", "emoji": "💔", "title": "전 애인꿈",
        "keywords": "전애인꿈 해몽, 전남친꿈, 전여친꿈, 옛애인꿈 의미, 헤어진사람꿈, 전애인재회꿈",
        "desc": "전 애인꿈 해몽 총정리. 옛 애인이 나오는 꿈, 전 애인과 재회하는 꿈, 전 애인과 싸우는 꿈 등 미해결 감정과 관계 심리를 비추는 꿈의 의미.",
        "meanings": [
            ("전 애인이 그냥 나오는 꿈", "아직 정리되지 않은 감정이나 그 시절의 미련을 반영합니다. 반드시 재회를 뜻하지는 않습니다."),
            ("전 애인과 재회하는 꿈", "과거를 매듭짓고 새로운 인연을 맞을 준비가 되었다는 신호일 수 있습니다."),
            ("전 애인과 싸우는 꿈", "남은 분노나 아쉬움을 정리하는 과정입니다. 마음을 비우면 한결 가벼워집니다."),
            ("전 애인이 행복해 보이는 꿈", "이제 그 관계를 놓아주라는 무의식의 메시지입니다. 현재의 나에게 집중하세요."),
            ("전 애인이 우는 꿈", "지난 관계에 대한 죄책감이나 연민이 남아 있음을 의미합니다."),
            ("전 애인을 떠나보내는 꿈", "감정 정리가 마무리되고 새로운 시작을 맞이할 시기입니다."),
        ],
        "faq": [
            ("전 애인 꿈은 무슨 의미인가요?", "대부분 실제 재회보다는 미해결 감정, 그 시절의 자신, 현재 관계에 대한 심리를 비추는 경우가 많습니다."),
            ("전 애인 꿈을 자주 꾸면?", "마음 한편에 정리되지 않은 감정이 남아 있다는 신호입니다. 충분히 애도하고 흘려보내는 것이 좋습니다."),
            ("전 애인 꿈이 재회의 신호인가요?", "꿈은 현실의 예언이 아니라 내면의 반영입니다. 재회 여부는 현실의 선택에 달려 있습니다."),
        ],
        "related": ["wedding", "ring", "flower", "naked"],
    },
    {
        "slug": "naked", "emoji": "🙈", "title": "알몸꿈",
        "keywords": "알몸꿈 해몽, 알몸꿈 의미, 벌거벗은꿈, 옷벗는꿈, 사람들앞에서알몸꿈, 알몸으로다니는꿈",
        "desc": "알몸꿈 해몽 총정리. 사람들 앞에서 알몸이 되는 꿈, 알몸으로 당당한 꿈, 알몸을 들키는 꿈 등 불안과 자아를 비추는 꿈의 상황별 의미.",
        "meanings": [
            ("사람들 앞에서 알몸이 되는 꿈", "취약함이 드러나는 것에 대한 불안과 타인의 평가에 대한 두려움을 반영합니다."),
            ("알몸인데도 당당한 꿈", "있는 그대로의 자신을 받아들이는 자신감을 의미합니다. 솔직함이 좋은 결과를 가져옵니다."),
            ("알몸을 들키는 꿈", "감추고 싶은 비밀이나 약점이 드러날까 하는 걱정을 나타냅니다."),
            ("알몸으로 목욕하는 꿈", "묵은 감정을 씻어내는 정화와 새로운 시작을 의미합니다."),
            ("알몸으로 거리를 걷는 꿈", "현실에서 보호막 없이 노출된 듯한 압박감을 느끼고 있음을 반영합니다."),
            ("타인의 알몸을 보는 꿈", "그 사람의 본모습이나 숨겨진 면을 알게 될 수 있음을 의미합니다."),
        ],
        "faq": [
            ("알몸꿈은 왜 꾸나요?", "주로 타인의 시선과 평가에 대한 불안, 또는 솔직하게 드러내고 싶은 마음이 반영된 심리몽입니다."),
            ("알몸인데 부끄럽지 않은 꿈은?", "자기 수용과 자신감의 표현으로, 어려운 상황도 당당히 헤쳐 나갈 수 있다는 긍정적 신호입니다."),
            ("알몸꿈도 길몽이 될 수 있나요?", "정화와 새 출발을 의미하는 경우 길몽이 됩니다. 꿈에서 느낀 감정이 해석의 핵심입니다."),
        ],
        "related": ["chased", "falling", "exam", "water"],
    },
    {
        "slug": "death", "emoji": "💀", "title": "죽는 꿈",
        "keywords": "죽는꿈 해몽, 내가죽는꿈, 가족이죽는꿈, 죽었다살아나는꿈, 죽는꿈 의미, 죽음꿈 길몽",
        "desc": "죽는 꿈 해몽 총정리. 내가 죽는 꿈, 가족이 죽는 꿈, 죽었다 살아나는 꿈 등 끝과 재탄생을 뜻하는 죽음꿈의 상황별 의미와 해석.",
        "meanings": [
            ("자신이 죽는 꿈", "실제 죽음이 아니라 한 시기의 끝과 재탄생을 의미하는 길몽입니다. 큰 변화와 새로운 출발이 찾아옵니다."),
            ("가족이 죽는 꿈", "역설적으로 그 사람의 장수나 관계의 개선을 의미하는 경우가 많습니다. 너무 불안해하지 마세요."),
            ("죽었다가 다시 살아나는 꿈", "기사회생, 회복, 재기를 의미합니다. 막혔던 일이 다시 풀리기 시작합니다."),
            ("편안하게 죽음을 맞이하는 꿈", "한 단계를 잘 마무리하고 다음 단계로 나아갈 준비가 되었음을 뜻합니다."),
            ("남이 죽는 꿈", "그 사람과의 관계에 변화가 생기거나, 자신의 어떤 면이 마무리됨을 의미합니다."),
            ("죽을 뻔하다 살아나는 꿈", "위기를 잘 넘기고 안전해진다는 신호입니다. 걱정은 기우로 끝납니다."),
        ],
        "faq": [
            ("죽는 꿈은 불길한 꿈인가요?", "아닙니다. 해몽에서 죽음은 끝과 새로운 시작을 상징해, 변화와 재탄생을 뜻하는 길몽으로 풀이됩니다."),
            ("가족이 죽는 꿈을 꾸면 어떡하나요?", "현실의 불행이 아니라 그 사람의 장수나 관계 회복을 의미하는 경우가 많으니 안심하셔도 됩니다."),
            ("죽는 꿈도 재물운과 관련이 있나요?", "죽음 뒤 새 출발은 재물과 성취로 이어지기도 합니다. 특히 죽었다 살아나는 꿈은 재기의 길몽입니다."),
        ],
        "related": ["deceased", "corpse", "ghost", "falling"],
    },
    {
        "slug": "fight", "emoji": "🥊", "title": "싸우는 꿈",
        "keywords": "싸우는꿈 해몽, 싸우는꿈 의미, 싸워서이기는꿈, 주먹다짐꿈, 말다툼꿈, 싸우는꿈 길몽",
        "desc": "싸우는 꿈 해몽 총정리. 싸워서 이기는 꿈, 싸워서 지는 꿈, 가족과 다투는 꿈 등 갈등과 승부를 비추는 꿈의 상황별 의미와 해석.",
        "meanings": [
            ("싸워서 이기는 꿈", "경쟁이나 어려운 문제에서 승리한다는 길몽입니다. 성취와 자신감이 따릅니다."),
            ("싸워서 지는 꿈", "현실의 부담이나 열세를 반영합니다. 전략을 다시 세우면 만회할 수 있습니다."),
            ("가족과 싸우는 꿈", "역설적으로 관계가 더 가까워지고 오해가 풀릴 징조로 봅니다."),
            ("주먹다짐을 하는 꿈", "억눌렀던 분노나 스트레스가 표출되는 과정입니다. 건강한 해소가 필요합니다."),
            ("말다툼을 하는 꿈", "현실에서 소통이 막혀 있음을 의미합니다. 대화로 풀어야 할 일이 있습니다."),
            ("칼이나 무기를 들고 싸우는 꿈", "강한 승부수를 던질 시기이거나, 단호한 결단이 필요한 상황을 나타냅니다."),
        ],
        "faq": [
            ("싸우는 꿈은 나쁜 꿈인가요?", "꼭 그렇지 않습니다. 싸워서 이기는 꿈은 승리와 성취의 길몽이며, 갈등의 해소를 의미하기도 합니다."),
            ("싸워서 이기면 길몽인가요?", "네, 경쟁에서의 승리, 문제 해결, 목표 달성을 뜻하는 대표적 길몽으로 풀이됩니다."),
            ("싸우는 꿈을 자주 꾸면?", "현실에서 풀리지 않은 갈등이나 억압된 감정이 있다는 신호입니다. 원인을 살펴보세요."),
        ],
        "related": ["war", "tiger", "chased", "ghost"],
    },
    {
        "slug": "earthquake", "emoji": "🏚️", "title": "지진꿈",
        "keywords": "지진꿈 해몽, 지진꿈 의미, 지진나는꿈, 건물무너지는꿈, 지진살아남는꿈, 땅흔들리는꿈",
        "desc": "지진꿈 해몽 총정리. 지진이 나는 꿈, 건물이 무너지는 꿈, 지진에서 살아남는 꿈 등 큰 변화와 기반의 흔들림을 뜻하는 꿈의 상황별 의미.",
        "meanings": [
            ("지진이 나는 꿈", "삶에 큰 변화나 전환점이 다가오고 있음을 의미합니다. 미리 대비하면 기회가 됩니다."),
            ("건물이 무너지는 지진꿈", "현재의 기반이나 환경이 흔들린다는 신호입니다. 기초를 다시 점검할 때입니다."),
            ("지진에서 살아남는 꿈", "큰 위기를 무사히 극복하고 더 단단해진다는 길몽입니다."),
            ("지진을 미리 예감하는 꿈", "직감이 예민해진 시기입니다. 변화의 신호를 잘 읽고 준비하세요."),
            ("작은 흔들림을 느끼는 꿈", "소소한 변화나 불안정이 있지만 곧 안정을 되찾습니다."),
            ("지진 후 다시 일어서는 꿈", "역경 뒤의 재건과 성장을 의미합니다. 무너진 자리에서 새로 시작합니다."),
        ],
        "faq": [
            ("지진꿈은 흉몽인가요?", "꼭 그렇지 않습니다. 지진은 큰 변화를 상징해, 위기를 넘기면 오히려 도약의 기회가 되는 경우가 많습니다."),
            ("지진꿈은 어떤 변화의 신호인가요?", "직장, 관계, 거주지 등 삶의 기반에 변화가 다가온다는 신호로 자주 해석됩니다."),
            ("지진에서 살아남으면 좋은 꿈인가요?", "네, 위기 극복과 회복력을 의미하는 길몽으로, 어려움을 이겨낸다는 긍정적 신호입니다."),
        ],
        "related": ["flood", "fire", "mountain", "war"],
    },
    {
        "slug": "jewel", "emoji": "💎", "title": "보석꿈",
        "keywords": "보석꿈 해몽, 보석꿈 의미, 다이아몬드꿈, 보석줍는꿈, 보석선물받는꿈, 보석꿈 재물운",
        "desc": "보석꿈 해몽 총정리. 보석을 줍는 꿈, 다이아몬드 꿈, 보석을 선물받는 꿈 등 재물운과 귀인운을 상징하는 보석꿈의 상황별 의미와 행운의 숫자.",
        "meanings": [
            ("보석을 줍는 꿈", "재물운이 들어오고 귀한 인연을 만날 길몽입니다. 뜻밖의 이득이 생길 수 있습니다."),
            ("다이아몬드가 나오는 꿈", "큰 행운과 변치 않는 사랑, 명예를 의미합니다. 소중한 결실을 얻게 됩니다."),
            ("보석을 선물받는 꿈", "귀인의 도움이나 인정을 받게 됩니다. 좋은 기회가 주어집니다."),
            ("보석이 환하게 빛나는 꿈", "명예와 성취가 따르는 길몽입니다. 능력을 인정받을 시기입니다."),
            ("보석을 잃어버리는 꿈", "소중한 것을 놓치지 않도록 주의하라는 메시지입니다. 관계나 기회를 점검하세요."),
            ("보석을 사는 꿈", "좋은 투자나 선택을 하게 됩니다. 가치 있는 곳에 자원을 쓰는 시기입니다."),
        ],
        "faq": [
            ("보석꿈은 재물운인가요?", "네, 보석은 부와 가치의 상징으로, 보석을 얻는 꿈은 재물운과 귀인운 상승을 뜻하는 길몽입니다."),
            ("보석꿈이 태몽이면?", "귀하고 빛나는 인물이 될 아이를 의미합니다. 재능과 복이 많은 아이로 풀이됩니다."),
            ("보석을 잃어버리는 꿈은 나쁜 꿈인가요?", "소중한 것에 대한 주의를 환기하는 꿈입니다. 관계나 기회를 소홀히 하지 말라는 신호입니다."),
        ],
        "related": ["gold", "money", "ring", "dragon"],
    },
]

# Titles for related-link resolution (existing + new dreams).
TITLE_MAP = {
    "money": "돈꿈", "gold": "금꿈 (황금꿈)", "pig": "돼지꿈", "snake": "뱀꿈",
    "deceased": "돌아가신 분 꿈", "war": "전쟁꿈", "wedding": "결혼꿈", "ring": "반지꿈",
    "flower": "꽃꿈", "chased": "쫓기는 꿈", "falling": "떨어지는 꿈", "exam": "시험꿈",
    "water": "물꿈", "tiger": "호랑이꿈", "flood": "홍수꿈", "fire": "불꿈",
    "mountain": "산꿈", "dragon": "용꿈",
}
TITLE_MAP.update({d["slug"]: d["title"] for d in DREAMS})


def lucky_numbers(slug):
    h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
    return sorted(set([(h >> i * 5) % 45 + 1 for i in range(6)]))[:3]


def generate_page(dream):
    slug = dream["slug"]

    meanings_html = ""
    for title, text in dream["meanings"]:
        meanings_html += f"""
            <div class="dream-meaning-card">
                <h3>{title}</h3>
                <p>{text}</p>
            </div>"""

    faq_html = ""
    faq_schema = []
    for q, a in dream["faq"]:
        faq_html += f"""
            <div class="dream-faq-item">
                <h3 class="dream-faq-q">{q}</h3>
                <p class="dream-faq-a">{a}</p>
            </div>"""
        faq_schema.append(
            f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        )
    faq_json = ",\n        ".join(faq_schema)

    related_html = ""
    for r in dream.get("related", []):
        if r in TITLE_MAP:
            related_html += f'<a href="/dream/{r}/" class="dream-related-link">{TITLE_MAP[r]}</a>\n                '

    nums = lucky_numbers(slug)
    balls = "".join(f'<span class="lucky-ball">{n}</span>' for n in nums)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{dream['desc']}">
    <meta name="keywords" content="{dream['keywords']}">
    <title>{dream['title']} 해몽 | 꿈의 의미와 행운의 숫자 - 사주명리</title>
    <link rel="canonical" href="{SITE_URL}/dream/{slug}/">
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=Cormorant+Garamond:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/dream.css">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{dream['title']} 해몽 | 꿈의 의미와 행운의 숫자">
    <meta property="og:description" content="{dream['desc']}">
    <meta property="og:url" content="{SITE_URL}/dream/{slug}/">
    <meta property="og:image" content="{SITE_URL}/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{dream['title']} 해몽">
    <meta name="twitter:description" content="{dream['desc']}">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-BNRL6FRMMM');</script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"Article",
        "headline":"{dream['title']} 해몽 - 꿈의 의미와 상황별 해석",
        "description":"{dream['desc']}",
        "url":"{SITE_URL}/dream/{slug}/",
        "datePublished":"{TODAY}","dateModified":"{TODAY}",
        "publisher":{{"@type":"Organization","name":"사주명리","url":"{SITE_URL}/"}},
        "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
            {{"@type":"ListItem","position":1,"name":"홈","item":"{SITE_URL}/"}},
            {{"@type":"ListItem","position":2,"name":"꿈해몽","item":"{SITE_URL}/dream/"}},
            {{"@type":"ListItem","position":3,"name":"{dream['title']} 해몽","item":"{SITE_URL}/dream/{slug}/"}}
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
    <header id="site-header">
        <nav class="container" style="display:flex;align-items:center;justify-content:space-between;padding:1rem 1.5rem;">
            <a href="/" class="logo-link" style="text-decoration:none;">
                <h1 style="font-family:var(--font-heading);font-size:var(--text-xl);margin:0;">
                    <span class="gold-text">사주명리</span>
                </h1>
            </a>
            <nav class="nav-links">{NAV_LINKS}</nav>
        </nav>
    </header>

    <section class="dream-hero">
        <div class="container">
            <div class="hero-badge">꿈해몽</div>
            <h1 class="hero-title"><span class="gold-text">{dream['emoji']} {dream['title']} 해몽</span></h1>
            <p class="hero-subtitle">{dream['desc'][:80]}...</p>
        </div>
    </section>

    <section class="dream-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">상황별 {dream['title']} 해석</span></h2>
            <div class="dream-meanings-grid">{meanings_html}
            </div>
        </div>
    </section>

    <section class="dream-section dream-lucky">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">행운의 숫자</span></h2>
            <div class="dream-lucky-card">
                <p>{dream['title']}을 꾸셨다면 오늘의 행운의 숫자를 참고하세요.</p>
                <div class="dream-lucky-numbers">
                    {balls}
                </div>
                <p class="dream-lucky-tip">로또 번호 선택에 참고해보세요! <a href="https://lotto.gon.ai.kr/" target="_blank">AI 로또킹에서 번호 추천 받기</a></p>
            </div>
        </div>
    </section>

    <section class="dream-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">자주 묻는 질문</span></h2>
            <div class="dream-faq-list">{faq_html}
            </div>
        </div>
    </section>

    <section class="dream-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">관련 꿈해몽</span></h2>
            <div class="dream-related-grid">
                {related_html}
            </div>
        </div>
    </section>

    <section class="dream-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">다른 꿈 찾아보기</span></h2>
            <div class="dream-all-links">
                <a href="/dream/">전체 꿈해몽 목록 보기</a>
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/dream/" class="cta-btn" style="background:transparent;border:1px solid var(--color-gold);color:var(--color-gold);">꿈해몽 전체 보기</a>
            </div>
        </div>
    </section>

{FOOTER}
</body>
</html>"""
    return html


# Hub placement: which category grid each new slug joins.
# A new "영적·길흉 꿈" category is created for ghost/corpse/ancestor/death.
SPIRITUAL_SLUGS = ["ghost", "corpse", "ancestor", "death"]
NATURE_ADD = ["earthquake"]
PERSON_ADD = ["ex", "naked", "fight"]
OBJECT_ADD = ["poop", "jewel"]


def _link(slug):
    d = next(x for x in DREAMS if x["slug"] == slug)
    return f'<a href="/dream/{slug}/" class="dream-hub-link">{d["emoji"]} {d["title"]}</a>'


def patch_hub():
    hub_path = os.path.join(BASE_DIR, "index.html")
    with open(hub_path, "r", encoding="utf-8") as f:
        html = f.read()

    if "/dream/poop/" in html:
        print("Hub already patched, skipping.")
        return

    # 1) bump counts
    html = html.replace("57가지", "67가지")
    html = html.replace('"numberOfItems":57', '"numberOfItems":67')

    # 2) append schema ItemList entries after the last (meat, position 57)
    meat_item = '{"@type":"ListItem","position":57,"url":"https://saju.gon.ai.kr/dream/meat/","name":"고기꿈 해몽"}'
    extra_items = []
    for i, d in enumerate(DREAMS, start=58):
        extra_items.append(
            f'{{"@type":"ListItem","position":{i},"url":"{SITE_URL}/dream/{d["slug"]}/","name":"{d["title"]} 해몽"}}'
        )
    html = html.replace(meat_item, meat_item + "," + ",".join(extra_items))

    # 3) 자연 꿈 grid: add after cloud
    cloud_link = '<a href="/dream/cloud/" class="dream-hub-link">☁️ 구름꿈</a>'
    add = "".join("\n                " + _link(s) for s in NATURE_ADD)
    html = html.replace(cloud_link, cloud_link + add)

    # 4) 사람/행동 꿈 grid: add after elevator
    elevator_link = '<a href="/dream/elevator/" class="dream-hub-link">🛗 엘리베이터꿈</a>'
    add = "".join("\n                " + _link(s) for s in PERSON_ADD)
    html = html.replace(elevator_link, elevator_link + add)

    # 5) 사물/기타 꿈 grid: add after meat
    meat_link = '<a href="/dream/meat/" class="dream-hub-link">🥩 고기꿈</a>'
    add = "".join("\n                " + _link(s) for s in OBJECT_ADD)
    html = html.replace(meat_link, meat_link + add)

    # 6) insert a new "영적·길흉 꿈" category before the 사물/기타 꿈 category
    obj_header = '        <div class="dream-hub-category">\n            <h2 class="section-title"><span class="gold-text">사물/기타 꿈</span></h2>'
    spiritual_links = "".join("\n                " + _link(s) for s in SPIRITUAL_SLUGS)
    new_cat = (
        '        <div class="dream-hub-category">\n'
        '            <h2 class="section-title"><span class="gold-text">영적·길흉 꿈</span></h2>\n'
        '            <div class="dream-hub-grid">' + spiritual_links + "\n"
        '                \n'
        '            </div>\n'
        '        </div>\n'
    )
    html = html.replace(obj_header, new_cat + obj_header)

    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Hub patched: +10 links, +1 category, counts 57->67.")


def patch_sitemap():
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_urls = ""
    added = 0
    for d in DREAMS:
        loc = f"{SITE_URL}/dream/{d['slug']}/"
        if loc in content:
            continue
        new_urls += f"""    <url>
        <loc>{loc}</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
"""
        added += 1

    if added == 0:
        print("Sitemap already has all new dream URLs, skipping.")
        return

    content = content.replace("</urlset>", new_urls + "</urlset>")
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sitemap: added {added} dream URLs.")


def main():
    for dream in DREAMS:
        slug_dir = os.path.join(BASE_DIR, dream["slug"])
        os.makedirs(slug_dir, exist_ok=True)
        page_html = generate_page(dream)
        with open(os.path.join(slug_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"Generated: /dream/{dream['slug']}/")

    patch_hub()
    patch_sitemap()
    print(f"\nDone. {len(DREAMS)} new dream pages.")


if __name__ == "__main__":
    main()
