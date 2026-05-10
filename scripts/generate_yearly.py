#!/usr/bin/env python3
"""2026년 띠별 연간 운세 페이지 생성 스크립트"""
import os

BASE = os.path.join(os.path.dirname(__file__), '..', 'public')
YEAR = 2026
TODAY = '2026-05-10'

ANIMALS = [
    {'key': 'rat', 'name': '쥐띠', 'emoji': '🐀', 'hanja': '子', 'element': '수(水)',
     'years': '1960, 1972, 1984, 1996, 2008, 2020',
     'personality': '영리하고 재치 있으며, 적응력이 뛰어납니다.',
     'yearly_overview': f'{YEAR}년은 쥐띠에게 새로운 도약의 해입니다. 상반기에는 기존 관계와 사업에서 안정적인 성과를 거두며, 하반기에는 예상치 못한 기회가 찾아옵니다. 특히 가을 이후 재물운이 크게 상승하여 투자나 사업 확장에 유리합니다.',
     'money': f'{YEAR}년 재물운은 전반적으로 양호합니다. 봄철에는 절약하는 습관이 중요하며, 여름 이후부터 수입이 증가합니다. 가을에 들어서면 뜻밖의 재물 기회가 생기니 준비를 잘 해두세요. 겨울에는 안정적인 자산 관리에 집중하는 것이 좋습니다.',
     'love': f'{YEAR}년 연애운은 봄에 새로운 만남이 있을 수 있습니다. 기존 커플은 여름에 관계가 더욱 깊어지며, 결혼을 고려하는 시기가 될 수 있습니다. 가을에는 소통이 중요하고, 겨울에는 따뜻한 시간을 함께 보내세요.',
     'health': f'{YEAR}년 건강운은 전반적으로 좋지만, 봄철 환절기 건강에 주의하세요. 여름에는 규칙적인 운동을 시작하기 좋은 시기입니다. 가을에는 소화기 관리에 신경 쓰고, 겨울에는 충분한 휴식을 취하세요.',
     'career': f'{YEAR}년 직업운은 상반기에 기존 업무에서 인정받는 시기이며, 하반기에는 이직이나 승진의 기회가 옵니다. 대인관계를 잘 관리하면 도움을 받을 수 있습니다.',
     'best_months': '4월, 8월, 11월', 'caution_months': '2월, 6월'},
    {'key': 'ox', 'name': '소띠', 'emoji': '🐂', 'hanja': '丑', 'element': '토(土)',
     'years': '1961, 1973, 1985, 1997, 2009, 2021',
     'personality': '성실하고 근면하며, 책임감이 강합니다.',
     'yearly_overview': f'{YEAR}년은 소띠에게 꾸준한 노력이 결실을 맺는 해입니다. 인내심을 갖고 추진해온 일들이 드디어 성과를 보이기 시작합니다. 다만 급격한 변화보다는 현재의 기반을 단단히 하는 데 집중하는 것이 좋습니다.',
     'money': f'{YEAR}년 재물운은 안정적입니다. 봄에는 예상 외의 지출이 있을 수 있으나, 여름부터 꾸준한 수입이 유지됩니다. 가을에는 부동산이나 장기 투자에 좋은 시기이며, 겨울에는 저축에 집중하세요.',
     'love': f'{YEAR}년 연애운은 여름에 좋은 인연을 만날 수 있습니다. 기존 관계에서는 서로의 신뢰를 더욱 단단히 할 시기입니다. 가을에는 가족과의 관계에서 행복을 느끼며, 겨울에는 편안한 시간을 보내세요.',
     'health': f'{YEAR}년 건강운은 체력 관리가 핵심입니다. 봄에 운동 습관을 만들어두면 1년 내내 도움이 됩니다. 여름에는 무리하지 않도록 주의하고, 겨울에는 관절 건강에 신경 쓰세요.',
     'career': f'{YEAR}년 직업운은 꾸준한 성장이 기대됩니다. 상반기에 시작한 프로젝트가 하반기에 좋은 결과를 가져옵니다. 동료들과의 협력이 성공의 열쇠입니다.',
     'best_months': '3월, 7월, 10월', 'caution_months': '1월, 9월'},
    {'key': 'tiger', 'name': '호랑이띠', 'emoji': '🐅', 'hanja': '寅', 'element': '목(木)',
     'years': '1962, 1974, 1986, 1998, 2010, 2022',
     'personality': '용감하고 자신감이 넘치며, 리더십이 뛰어납니다.',
     'yearly_overview': f'{YEAR}년은 호랑이띠에게 리더십을 발휘할 기회가 많은 해입니다. 도전적인 과제를 맡게 되지만, 자신감을 갖고 추진하면 크게 성공할 수 있습니다. 봄부터 가을까지 운세가 강하게 작용합니다.',
     'money': f'{YEAR}년 재물운은 상반기에 좋은 투자 기회가 있습니다. 여름에는 지출 관리가 필요하며, 가을부터 재물이 들어옵니다. 연말에는 보너스나 성과급을 기대할 수 있습니다.',
     'love': f'{YEAR}년 연애운은 봄에 활발합니다. 적극적으로 다가가면 좋은 인연을 만날 수 있습니다. 여름에는 기존 관계에서 작은 갈등이 있을 수 있으나 대화로 해결됩니다.',
     'health': f'{YEAR}년 건강운은 에너지가 넘치는 한 해입니다. 다만 과로에 주의하세요. 봄과 가을에 건강검진을 받아두면 좋습니다. 스트레스 관리에 명상이 도움됩니다.',
     'career': f'{YEAR}년 직업운은 새로운 직책이나 역할을 맡게 됩니다. 리더로서의 능력을 인정받는 시기이며, 9월 이후 중요한 프로젝트를 주도하게 됩니다.',
     'best_months': '3월, 6월, 9월', 'caution_months': '5월, 12월'},
    {'key': 'rabbit', 'name': '토끼띠', 'emoji': '🐇', 'hanja': '卯', 'element': '목(木)',
     'years': '1963, 1975, 1987, 1999, 2011, 2023',
     'personality': '온화하고 세심하며, 예술적 감각이 뛰어납니다.',
     'yearly_overview': f'{YEAR}년은 토끼띠에게 평화롭고 안정적인 해입니다. 내면의 성장과 자기 계발에 좋은 시기이며, 주변 사람들과의 관계에서 행복을 느끼게 됩니다. 여름 이후 기회의 폭이 넓어집니다.',
     'money': f'{YEAR}년 재물운은 안정적인 흐름을 보입니다. 큰 수익보다는 꾸준한 저축이 중요합니다. 여름에 예상치 못한 수입이 있을 수 있으며, 가을에는 부업이나 사이드 프로젝트에서 수익을 얻을 수 있습니다.',
     'love': f'{YEAR}년 연애운은 가을에 절정에 달합니다. 차분하고 진심 어린 만남이 이루어지며, 기존 커플은 결혼이나 동거를 시작하기 좋은 시기입니다.',
     'health': f'{YEAR}년 건강운은 정신 건강에 더 신경 써야 합니다. 요가나 명상이 도움이 되며, 봄에는 알레르기에 주의하세요. 여름에는 충분한 수면을 취하는 것이 중요합니다.',
     'career': f'{YEAR}년 직업운은 창의적인 분야에서 두각을 나타냅니다. 상반기에 아이디어를 정리하고, 하반기에 실행에 옮기면 좋은 결과를 얻습니다.',
     'best_months': '4월, 8월, 10월', 'caution_months': '1월, 7월'},
    {'key': 'dragon', 'name': '용띠', 'emoji': '🐉', 'hanja': '辰', 'element': '토(土)',
     'years': '1964, 1976, 1988, 2000, 2012, 2024',
     'personality': '야망이 크고 카리스마가 있으며, 운이 따르는 편입니다.',
     'yearly_overview': f'{YEAR}년은 용띠에게 운이 크게 따르는 해입니다. 큰 프로젝트나 사업에서 성공을 거둘 수 있으며, 주변의 지지를 받습니다. 특히 여름에 중요한 전환점이 찾아옵니다.',
     'money': f'{YEAR}년 재물운은 매우 좋습니다. 상반기부터 재물이 들어오며, 투자에도 좋은 시기입니다. 다만 과욕을 부리지 않도록 주의하세요. 가을에 큰 수익을 기대할 수 있습니다.',
     'love': f'{YEAR}년 연애운은 봄에 매력이 넘칩니다. 많은 사람의 관심을 받으며, 인연이 될 사람을 만날 확률이 높습니다. 여름 이후에는 진지한 관계로 발전합니다.',
     'health': f'{YEAR}년 건강운은 활동적인 한 해가 됩니다. 체력이 넘치지만 무리하지 않도록 주의하세요. 소화기와 간 건강에 신경 쓰고, 음주를 줄이는 것이 좋습니다.',
     'career': f'{YEAR}년 직업운은 승승장구하는 시기입니다. 새로운 사업을 시작하거나 기존 사업을 확장하기에 최적의 해입니다. 가을에 중요한 계약이 성사됩니다.',
     'best_months': '5월, 8월, 11월', 'caution_months': '3월, 10월'},
    {'key': 'snake', 'name': '뱀띠', 'emoji': '🐍', 'hanja': '巳', 'element': '화(火)',
     'years': '1965, 1977, 1989, 2001, 2013, 2025',
     'personality': '지혜롭고 신중하며, 직관력이 뛰어납니다.',
     'yearly_overview': f'{YEAR}년은 뱀띠에게 지혜를 발휘할 기회가 많은 해입니다. 복잡한 상황에서 현명한 판단으로 위기를 기회로 바꿀 수 있습니다. 하반기에 운세가 더욱 좋아집니다.',
     'money': f'{YEAR}년 재물운은 하반기에 집중됩니다. 상반기에는 절약 모드로 지내되, 여름 이후 투자 기회를 잡으세요. 연말에 큰 수익이 기대됩니다.',
     'love': f'{YEAR}년 연애운은 깊이 있는 만남이 이루어집니다. 표면적인 관계보다 진정성 있는 소통이 사랑을 키웁니다. 가을에 프로포즈나 고백의 기회가 옵니다.',
     'health': f'{YEAR}년 건강운은 정기적인 운동이 핵심입니다. 봄에 건강검진을 받아두세요. 여름에는 열 관리에 주의하고, 가을에는 호흡기 건강에 신경 쓰세요.',
     'career': f'{YEAR}년 직업운은 전문성을 높이는 데 집중하면 좋습니다. 자격증이나 교육 이수가 커리어 발전에 큰 도움이 됩니다. 10월 이후 승진 기회가 옵니다.',
     'best_months': '6월, 9월, 12월', 'caution_months': '2월, 4월'},
    {'key': 'horse', 'name': '말띠', 'emoji': '🐴', 'hanja': '午', 'element': '화(火)',
     'years': '1966, 1978, 1990, 2002, 2014, 2026',
     'personality': '활동적이고 열정적이며, 자유를 사랑합니다.',
     'yearly_overview': f'{YEAR}년은 말띠에게 특별한 해입니다. 자신의 띠 해(본명년)로 변화가 많지만 큰 성장을 이룰 수 있습니다. 신중하게 행동하되, 기회가 왔을 때 과감하게 결단하세요.',
     'money': f'{YEAR}년 재물운은 변동이 있습니다. 봄에는 지출이 많을 수 있으나, 여름 이후 안정됩니다. 투기성 투자는 피하고 안정적인 자산 관리에 집중하세요.',
     'love': f'{YEAR}년 연애운은 여름에 로맨틱한 만남이 기대됩니다. 자유로운 만남 속에서 운명적인 인연을 찾을 수 있습니다. 기존 관계에서는 서로의 공간을 존중하세요.',
     'health': f'{YEAR}년 건강운은 체력 관리가 중요합니다. 본명년이라 에너지 소모가 클 수 있으니, 규칙적인 생활과 충분한 수면이 필요합니다. 봄에 건강검진을 받으세요.',
     'career': f'{YEAR}년 직업운은 새로운 도전의 시기입니다. 이직이나 전직을 고려할 수 있으며, 하반기에 좋은 기회가 옵니다. 네트워킹이 중요한 해입니다.',
     'best_months': '2월, 7월, 10월', 'caution_months': '4월, 8월'},
    {'key': 'goat', 'name': '양띠', 'emoji': '🐑', 'hanja': '未', 'element': '토(土)',
     'years': '1967, 1979, 1991, 2003, 2015',
     'personality': '온순하고 예술적이며, 감성이 풍부합니다.',
     'yearly_overview': f'{YEAR}년은 양띠에게 내면의 평화와 성장을 이루는 해입니다. 예술적 감각을 활용한 활동에서 큰 만족감을 얻으며, 가을 이후 좋은 기회가 찾아옵니다.',
     'money': f'{YEAR}년 재물운은 봄에 안정적이며, 여름에 약간의 변동이 있습니다. 가을부터 재물운이 상승하며, 창작 활동이나 예술 관련 수입이 기대됩니다.',
     'love': f'{YEAR}년 연애운은 감성적인 만남이 이루어집니다. 봄에 새로운 인연이 시작되며, 가을에는 깊은 유대감을 느끼는 관계로 발전합니다.',
     'health': f'{YEAR}년 건강운은 정서적 안정이 중요합니다. 스트레스를 예술 활동으로 해소하면 좋습니다. 봄과 가을 환절기에 호흡기 건강에 주의하세요.',
     'career': f'{YEAR}년 직업운은 창의적인 분야에서 인정받습니다. 팀워크가 중요한 해이며, 동료들과의 협업에서 좋은 성과를 거둡니다.',
     'best_months': '3월, 9월, 11월', 'caution_months': '5월, 8월'},
    {'key': 'monkey', 'name': '원숭이띠', 'emoji': '🐒', 'hanja': '申', 'element': '금(金)',
     'years': '1968, 1980, 1992, 2004, 2016',
     'personality': '재치 있고 호기심이 많으며, 다재다능합니다.',
     'yearly_overview': f'{YEAR}년은 원숭이띠에게 다양한 기회가 쏟아지는 해입니다. 재치와 적응력을 발휘하여 여러 분야에서 성과를 거둘 수 있습니다. 봄과 여름에 특히 운이 좋습니다.',
     'money': f'{YEAR}년 재물운은 다양한 수입원에서 이익을 얻습니다. 봄에 사이드 프로젝트로 추가 수입이 생기며, 여름에는 투자 수익이 기대됩니다. 겨울에는 지출 관리에 주의하세요.',
     'love': f'{YEAR}년 연애운은 활발합니다. 다양한 만남 속에서 특별한 인연을 찾게 됩니다. 여름에 진지한 관계가 시작되며, 겨울에는 따뜻한 사랑이 꽃핍니다.',
     'health': f'{YEAR}년 건강운은 활동적인 한 해이지만 과로에 주의하세요. 다양한 활동 사이에서 휴식 시간을 확보하는 것이 중요합니다. 눈 건강에 특히 신경 쓰세요.',
     'career': f'{YEAR}년 직업운은 다재다능함이 빛나는 시기입니다. 새로운 기술을 배우거나 역할을 확장하기 좋습니다. 여름에 중요한 프로젝트를 맡게 됩니다.',
     'best_months': '2월, 6월, 10월', 'caution_months': '4월, 12월'},
    {'key': 'rooster', 'name': '닭띠', 'emoji': '🐓', 'hanja': '酉', 'element': '금(金)',
     'years': '1969, 1981, 1993, 2005, 2017',
     'personality': '근면하고 정직하며, 관찰력이 뛰어납니다.',
     'yearly_overview': f'{YEAR}년은 닭띠에게 근면함이 빛을 발하는 해입니다. 꼼꼼한 준비와 계획이 큰 성과로 이어지며, 여름 이후 인정받는 시기가 옵니다.',
     'money': f'{YEAR}년 재물운은 착실한 노력이 보상받습니다. 봄에 시작한 저축이 연말에 큰 목돈이 되며, 가을에 투자 기회가 찾아옵니다. 충동 구매를 자제하세요.',
     'love': f'{YEAR}년 연애운은 진실한 만남이 이루어집니다. 겉모습보다 내면의 아름다움을 중시하는 인연을 만나게 됩니다. 가을에 결혼 운이 좋습니다.',
     'health': f'{YEAR}년 건강운은 규칙적인 생활이 핵심입니다. 아침 일찍 일어나는 습관이 건강에 도움이 되며, 소화기 건강에 주의하세요.',
     'career': f'{YEAR}년 직업운은 전문성이 인정받는 시기입니다. 디테일에 강한 능력이 빛나며, 상반기에 중요한 업무를 맡게 됩니다.',
     'best_months': '1월, 7월, 11월', 'caution_months': '3월, 9월'},
    {'key': 'dog', 'name': '개띠', 'emoji': '🐕', 'hanja': '戌', 'element': '토(土)',
     'years': '1970, 1982, 1994, 2006, 2018',
     'personality': '충직하고 정의감이 강하며, 의리를 중시합니다.',
     'yearly_overview': f'{YEAR}년은 개띠에게 인간관계에서 행복을 찾는 해입니다. 충직한 성격이 주변의 신뢰를 얻어 많은 도움을 받게 됩니다. 봄과 가을에 중요한 전환점이 있습니다.',
     'money': f'{YEAR}년 재물운은 주변 사람을 통해 기회가 옵니다. 네트워킹이 재물운의 열쇠이며, 여름에 좋은 제안을 받을 수 있습니다. 가을에는 안정적인 수입이 유지됩니다.',
     'love': f'{YEAR}년 연애운은 의리 있는 만남이 특징입니다. 오래 알고 지낸 사람과 사랑이 싹틀 수 있으며, 여름에 관계가 한 단계 발전합니다.',
     'health': f'{YEAR}년 건강운은 전반적으로 양호하지만, 스트레스 관리가 중요합니다. 반려동물과 함께하는 산책이 정신 건강에 큰 도움이 됩니다.',
     'career': f'{YEAR}년 직업운은 팀 내에서 신뢰를 쌓는 시기입니다. 리더보다는 조력자 역할에서 빛나며, 하반기에 승진이나 인정받는 기회가 옵니다.',
     'best_months': '4월, 8월, 12월', 'caution_months': '2월, 6월'},
    {'key': 'pig', 'name': '돼지띠', 'emoji': '🐷', 'hanja': '亥', 'element': '수(水)',
     'years': '1971, 1983, 1995, 2007, 2019',
     'personality': '너그럽고 낙천적이며, 복이 많은 편입니다.',
     'yearly_overview': f'{YEAR}년은 돼지띠에게 풍요로운 해입니다. 타고난 복이 빛을 발하며, 여러 방면에서 좋은 일이 생깁니다. 특히 봄과 여름에 행운이 따르며, 재물운과 인간관계 모두 좋습니다.',
     'money': f'{YEAR}년 재물운은 매우 좋습니다. 봄부터 재물이 들어오며, 여름에 큰 수익을 기대할 수 있습니다. 다만 가을에는 관대한 성격으로 인한 과소비에 주의하세요.',
     'love': f'{YEAR}년 연애운은 따뜻한 사랑이 가득합니다. 너그러운 성격이 좋은 인연을 끌어당기며, 봄에 운명적인 만남이 있을 수 있습니다. 가을에는 가족과의 유대가 깊어집니다.',
     'health': f'{YEAR}년 건강운은 식이 조절이 핵심입니다. 맛있는 것을 좋아하는 성격상 체중 관리에 신경 쓰세요. 규칙적인 운동과 균형 잡힌 식단이 건강의 비결입니다.',
     'career': f'{YEAR}년 직업운은 안정적이고 풍요로운 시기입니다. 기존 업무에서 좋은 성과를 거두며, 동료들과의 관계가 원만합니다. 연말에 특별 보너스나 인센티브가 기대됩니다.',
     'best_months': '3월, 7월, 10월', 'caution_months': '5월, 9월'},
]

def gen_animal_page(a):
    """Generate individual yearly fortune page for an animal."""
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{YEAR}년 {a['name']}({a['hanja']}) 운세 총정리. 총운, 재물운, 연애운, 건강운, 직업운과 행운의 달, 주의할 달까지 한눈에 확인하세요.">
    <meta name="keywords" content="{YEAR}년 {a['name']} 운세, {a['name']} {YEAR}년 운세, {a['name']} 연간운세, {a['name']} 총운, {a['name']} 재물운, {a['name']} 연애운, 띠별 {YEAR} 운세">
    <title>{a['name']} {YEAR}년 운세 | {a['name']} 연간 총운, 재물운, 연애운 - 사주명리</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/yearly/{a['key']}/">
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=Cormorant+Garamond:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/zodiac.css?v=1">
    <link rel="stylesheet" href="/css/daily.css?v=1">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{a['name']} {YEAR}년 운세 | 연간 총운 정리">
    <meta property="og:description" content="{YEAR}년 {a['name']}({a['hanja']}) 운세를 확인하세요. 총운, 재물운, 연애운, 건강운, 직업운까지 한눈에.">
    <meta property="og:url" content="https://saju.gon.ai.kr/yearly/{a['key']}/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{a['name']} {YEAR}년 운세">
    <meta name="twitter:description" content="{YEAR}년 {a['name']}({a['hanja']}) 운세 총정리. 총운, 재물운, 연애운, 건강운, 직업운.">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-BNRL6FRMMM');</script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"Article",
        "headline":"{a['name']} {YEAR}년 운세 - 연간 총운, 재물운, 연애운, 건강운, 직업운",
        "description":"{YEAR}년 {a['name']}({a['hanja']}) 운세를 확인하세요. 총운, 재물운, 연애운, 건강운, 직업운과 행운의 달까지.",
        "url":"https://saju.gon.ai.kr/yearly/{a['key']}/",
        "datePublished":"{YEAR}-01-01","dateModified":"{TODAY}",
        "publisher":{{"@type":"Organization","name":"사주명리","url":"https://saju.gon.ai.kr/"}},
        "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
            {{"@type":"ListItem","position":1,"name":"홈","item":"https://saju.gon.ai.kr/"}},
            {{"@type":"ListItem","position":2,"name":"{YEAR}년 띠별 운세","item":"https://saju.gon.ai.kr/yearly/"}},
            {{"@type":"ListItem","position":3,"name":"{a['name']} {YEAR}년 운세","item":"https://saju.gon.ai.kr/yearly/{a['key']}/"}}
        ]}}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[
            {{"@type":"Question","name":"{YEAR}년 {a['name']} 총운은 어떤가요?","acceptedAnswer":{{"@type":"Answer","text":"{a['yearly_overview'][:150]}"}}}},
            {{"@type":"Question","name":"{YEAR}년 {a['name']} 재물운은?","acceptedAnswer":{{"@type":"Answer","text":"{a['money'][:150]}"}}}},
            {{"@type":"Question","name":"{a['name']}는 어떤 해에 태어난 사람인가요?","acceptedAnswer":{{"@type":"Answer","text":"{a['name']}({a['hanja']})는 12간지 중 하나로, 해당 출생연도: {a['years']}."}}}}
        ]
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
            <nav class="nav-links"><a href="/">사주풀이</a><a href="/zodiac/">띠별 운세</a><a href="/daily/">오늘의 운세</a><a href="/yearly/" class="active">{YEAR}년 운세</a><a href="/compatibility/">궁합</a><a href="/guide/">사주 가이드</a></nav>
        </nav>
    </header>

    <section class="daily-hero">
        <div class="container">
            <div class="hero-badge">{YEAR}년 연간 운세</div>
            <h1 class="hero-title"><span class="gold-text">{a['emoji']} {a['name']} {YEAR}년 운세</span></h1>
            <p class="hero-subtitle">{a['name']}({a['hanja']}, {a['element']}) | 출생연도: {a['years']}<br>{a['personality']}</p>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <div class="daily-result">
                <div class="result-messages">
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">🔮 {YEAR}년 총운</h2>
                        <p>{a['yearly_overview']}</p>
                    </div>
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">💰 재물운</h2>
                        <p>{a['money']}</p>
                    </div>
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">💕 연애운</h2>
                        <p>{a['love']}</p>
                    </div>
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">💪 건강운</h2>
                        <p>{a['health']}</p>
                    </div>
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">💼 직업운</h2>
                        <p>{a['career']}</p>
                    </div>
                </div>
                <div class="result-lucky">
                    <div class="lucky-chip"><span class="lucky-icon">🌟</span> 행운의 달: <strong>{a['best_months']}</strong></div>
                    <div class="lucky-chip"><span class="lucky-icon">⚠️</span> 주의할 달: <strong>{a['caution_months']}</strong></div>
                </div>
            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">{a['name']} 월별 운세</span></h2>
            <div class="zodiac-links-grid">
                <a href="/zodiac/{a['key']}/{YEAR}-01/">1월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-02/">2월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-03/">3월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-04/">4월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-05/">5월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-06/">6월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-07/">7월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-08/">8월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-09/">9월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-10/">10월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-11/">11월 운세</a>
                <a href="/zodiac/{a['key']}/{YEAR}-12/">12월 운세</a>
            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">다른 띠 {YEAR}년 운세</span></h2>
            <div class="zodiac-links-grid">
''' + '\n'.join(f'                <a href="/yearly/{o["key"]}/">{o["emoji"]} {o["name"]}</a>' for o in ANIMALS if o['key'] != a['key']) + f'''
            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">관련 운세</span></h2>
            <div class="zodiac-links-grid">
                <a href="/daily/{a['key']}/">오늘의 {a['name']} 운세</a>
                <a href="/zodiac/{a['key']}/">{a['name']} 상세 분석</a>
                <a href="/compatibility/{a['key']}/">{a['name']} 궁합</a>
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 {YEAR}년 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/daily/{a['key']}/" class="cta-btn" style="background:transparent;border:1px solid var(--color-gold);color:var(--color-gold);">오늘의 {a['name']} 운세</a>
            </div>
        </div>
    </section>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/yearly/">{YEAR}년 운세</a>
                <a href="/compatibility/">궁합</a>
                <a href="/guide/">사주 가이드</a>
            </div>
            <p class="footer-copy">&copy; {YEAR} 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>
</body>
</html>'''


def gen_index_page():
    """Generate the yearly fortune index page."""
    animal_cards = '\n'.join(f'''                <a href="/yearly/{a['key']}/" class="zodiac-card-link" style="text-decoration:none;">
                    <div class="zodiac-card" style="text-align:center;padding:1.5rem;">
                        <div style="font-size:2.5rem;margin-bottom:0.5rem;">{a['emoji']}</div>
                        <h3 style="margin:0;font-size:1.1rem;">{a['name']}</h3>
                        <p style="margin:0.3rem 0 0;font-size:0.85rem;opacity:0.8;">{a['hanja']} | {a['element']}</p>
                        <p style="margin:0.5rem 0 0;font-size:0.8rem;opacity:0.7;">{a['years']}</p>
                    </div>
                </a>''' for a in ANIMALS)

    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="description" content="{YEAR}년 띠별 운세 총정리. 쥐띠부터 돼지띠까지 12간지별 {YEAR}년 총운, 재물운, 연애운, 건강운, 직업운을 무료로 확인하세요.">
    <meta name="keywords" content="{YEAR}년 띠별운세, {YEAR}년 운세, {YEAR} 띠별 총운, 올해 띠별 운세, 12간지 {YEAR}년 운세, 연간 운세 무료, 띠별 연간운세">
    <title>{YEAR}년 띠별 운세 | 12간지 연간 총운 정리 - 사주명리</title>
    <link rel="canonical" href="https://saju.gon.ai.kr/yearly/">
    <meta name="naver-site-verification" content="0e1c05903546c204ebb9e52263162fe36a32fb28" />
    <meta name="google-adsense-account" content="ca-pub-7479840445702290">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;500;700&family=Cormorant+Garamond:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/reset.css">
    <link rel="stylesheet" href="/css/variables.css">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/zodiac.css?v=1">
    <link rel="stylesheet" href="/css/daily.css?v=1">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{YEAR}년 띠별 운세 | 12간지 연간 총운 정리">
    <meta property="og:description" content="{YEAR}년 띠별 운세를 확인하세요. 12간지별 총운, 재물운, 연애운, 건강운.">
    <meta property="og:url" content="https://saju.gon.ai.kr/yearly/">
    <meta property="og:image" content="https://saju.gon.ai.kr/assets/images/og-image.jpg">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:site_name" content="사주명리">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{YEAR}년 띠별 운세 | 12간지 연간 총운">
    <meta name="twitter:description" content="{YEAR}년 띠별 운세 총정리. 무료로 확인하세요.">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7479840445702290" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-BNRL6FRMMM"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-BNRL6FRMMM');</script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"CollectionPage",
        "name":"{YEAR}년 띠별 운세",
        "description":"{YEAR}년 12간지별 연간 운세 총정리",
        "url":"https://saju.gon.ai.kr/yearly/",
        "isPartOf":{{"@type":"WebSite","name":"사주명리","url":"https://saju.gon.ai.kr/"}},
        "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
            {{"@type":"ListItem","position":1,"name":"홈","item":"https://saju.gon.ai.kr/"}},
            {{"@type":"ListItem","position":2,"name":"{YEAR}년 띠별 운세","item":"https://saju.gon.ai.kr/yearly/"}}
        ]}}
    }}
    </script>
    <script type="application/ld+json">
    {{
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[
            {{"@type":"Question","name":"{YEAR}년 가장 운이 좋은 띠는?","acceptedAnswer":{{"@type":"Answer","text":"{YEAR}년에는 용띠와 돼지띠에게 특히 좋은 운이 따릅니다. 용띠는 사업과 재물운이 강하고, 돼지띠는 타고난 복이 빛을 발하는 해입니다."}}}},
            {{"@type":"Question","name":"{YEAR}년 띠별 운세는 어떻게 보나요?","acceptedAnswer":{{"@type":"Answer","text":"자신의 출생연도에 해당하는 띠를 선택하면 {YEAR}년 총운, 재물운, 연애운, 건강운, 직업운을 확인할 수 있습니다."}}}}
        ]
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
            <nav class="nav-links"><a href="/">사주풀이</a><a href="/zodiac/">띠별 운세</a><a href="/daily/">오늘의 운세</a><a href="/yearly/" class="active">{YEAR}년 운세</a><a href="/compatibility/">궁합</a><a href="/guide/">사주 가이드</a></nav>
        </nav>
    </header>

    <section class="daily-hero">
        <div class="container">
            <div class="hero-badge">{YEAR}년 연간 운세</div>
            <h1 class="hero-title"><span class="gold-text">🐲 {YEAR}년 띠별 운세</span></h1>
            <p class="hero-subtitle">12간지별 {YEAR}년 총운, 재물운, 연애운, 건강운, 직업운을<br>무료로 확인하세요.</p>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">내 띠 선택하기</span></h2>
            <div class="zodiac-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:1rem;">
{animal_cards}
            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <div class="daily-result">
                <div class="result-messages">
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">📅 {YEAR}년 운세 총평</h2>
                        <p>{YEAR}년은 병오(丙午)년으로, 활기차고 변화가 많은 해입니다. 12간지 중 말띠의 해이며, 불의 기운이 강하게 작용합니다. 새로운 시작과 도전에 유리하며, 적극적으로 행동하는 사람에게 기회가 찾아옵니다.</p>
                    </div>
                    <div class="result-msg-card">
                        <h2 style="font-size:1.3rem;margin-bottom:0.8rem;">🌟 {YEAR}년 행운의 띠 TOP 3</h2>
                        <p><strong>1위 용띠</strong> - 사업과 재물운이 크게 상승합니다.<br>
                        <strong>2위 돼지띠</strong> - 타고난 복이 빛을 발하는 해입니다.<br>
                        <strong>3위 호랑이띠</strong> - 리더십을 발휘할 기회가 많습니다.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="daily-section">
        <div class="container">
            <h2 class="section-title"><span class="gold-text">관련 운세</span></h2>
            <div class="zodiac-links-grid">
                <a href="/daily/">오늘의 띠별 운세</a>
                <a href="/zodiac/">띠별 상세 분석</a>
                <a href="/compatibility/">궁합 보기</a>
                <a href="/dream/">꿈해몽</a>
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 class="gold-text">더 정확한 {YEAR}년 운세가 궁금하신가요?</h2>
            <p>생년월일시를 입력하면 사주팔자 기반의 정밀한 운세를 확인할 수 있습니다.</p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <a href="/" class="cta-btn">무료 사주풀이</a>
                <a href="/daily/" class="cta-btn" style="background:transparent;border:1px solid var(--color-gold);color:var(--color-gold);">오늘의 운세</a>
            </div>
        </div>
    </section>

    <footer class="site-footer">
        <div class="container">
            <div class="footer-links">
                <a href="/">사주풀이</a>
                <a href="/zodiac/">띠별 운세</a>
                <a href="/daily/">오늘의 운세</a>
                <a href="/yearly/">{YEAR}년 운세</a>
                <a href="/compatibility/">궁합</a>
                <a href="/guide/">사주 가이드</a>
            </div>
            <p class="footer-copy">&copy; {YEAR} 사주명리. 전통 명리학 기반 운세 서비스.</p>
            <p class="footer-disclaimer">본 서비스의 운세 결과는 전통 명리학에 기반한 참고용 정보이며, 중요한 결정은 전문가와 상담하시기 바랍니다.</p>
        </div>
    </footer>
</body>
</html>'''


def main():
    # Create yearly directory
    yearly_dir = os.path.join(BASE, 'yearly')
    os.makedirs(yearly_dir, exist_ok=True)

    # Generate index page
    idx_path = os.path.join(yearly_dir, 'index.html')
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(gen_index_page())
    print(f'Created: {idx_path}')

    # Generate individual animal pages
    for a in ANIMALS:
        a_dir = os.path.join(yearly_dir, a['key'])
        os.makedirs(a_dir, exist_ok=True)
        a_path = os.path.join(a_dir, 'index.html')
        with open(a_path, 'w', encoding='utf-8') as f:
            f.write(gen_animal_page(a))
        print(f'Created: {a_path}')

    print(f'\nTotal: 13 pages created (1 index + 12 animals)')

    # Update sitemap
    sitemap_path = os.path.join(BASE, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build new sitemap entries
    new_entries = f'''    <url>
        <loc>https://saju.gon.ai.kr/yearly/</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.9</priority>
    </url>
'''
    for a in ANIMALS:
        new_entries += f'''    <url>
        <loc>https://saju.gon.ai.kr/yearly/{a['key']}/</loc>
        <lastmod>{TODAY}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.7</priority>
    </url>
'''

    # Insert before </urlset>
    content = content.replace('</urlset>', new_entries + '</urlset>')

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated: {sitemap_path} (+13 URLs)')


if __name__ == '__main__':
    main()
