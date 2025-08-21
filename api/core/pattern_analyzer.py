# -*- coding: utf-8 -*-
"""
Pattern Analyzer for Saju System
Identifies pattern types (격국) and provides detailed interpretations
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PatternAnalysis:
    """Complete pattern analysis result"""
    pattern_type: str  # Main pattern type
    pattern_category: str  # 정격, 변격, 특수격
    pattern_name: str  # Korean name
    description: str  # Pattern description
    characteristics: List[str]  # Key characteristics
    career_guidance: str  # Career recommendations
    wealth_fortune: str  # Wealth prospects
    relationship_advice: str  # Relationship guidance
    cautions: List[str]  # Things to be careful about
    famous_examples: List[str]  # Historical figures with this pattern
    success_factors: List[str]  # Keys to success
    strength_score: float  # Pattern strength (0-1)


class PatternAnalyzer:
    """
    Analyzes Saju patterns (격국) for detailed personality and destiny interpretation
    """
    
    def __init__(self):
        """Initialize the pattern analyzer"""
        self._initialize_element_relations()
        self._initialize_ten_gods()
        self._initialize_patterns()
        
    def _initialize_element_relations(self):
        """Initialize element relationships for pattern analysis"""
        # Element mapping
        self.stem_elements = {
            '갑': '목', '을': '목',
            '병': '화', '정': '화',
            '무': '토', '기': '토',
            '경': '금', '신': '금',
            '임': '수', '계': '수'
        }
        
        self.branch_elements = {
            '자': '수', '축': '토', '인': '목', '묘': '목',
            '진': '토', '사': '화', '오': '화', '미': '토',
            '신': '금', '유': '금', '술': '토', '해': '수'
        }
        
        # Hidden stems in branches
        self.hidden_stems = {
            '자': ['계'],
            '축': ['기', '신', '계'],
            '인': ['갑', '병', '무'],
            '묘': ['을'],
            '진': ['무', '을', '계'],
            '사': ['병', '무', '경'],
            '오': ['정', '기'],
            '미': ['기', '정', '을'],
            '신': ['경', '임', '무'],
            '유': ['신'],
            '술': ['무', '신', '정'],
            '해': ['임', '갑']
        }
        
    def _initialize_ten_gods(self):
        """Initialize Ten Gods relationships for pattern identification"""
        # Ten Gods calculation rules
        self.ten_gods_map = {
            # From 갑 (Yang Wood) perspective
            ('갑', '갑'): '비견', ('갑', '을'): '겁재',
            ('갑', '병'): '식신', ('갑', '정'): '상관',
            ('갑', '무'): '편재', ('갑', '기'): '정재',
            ('갑', '경'): '편관', ('갑', '신'): '정관',
            ('갑', '임'): '편인', ('갑', '계'): '정인',
            
            # From 을 (Yin Wood) perspective
            ('을', '을'): '비견', ('을', '갑'): '겁재',
            ('을', '정'): '식신', ('을', '병'): '상관',
            ('을', '기'): '편재', ('을', '무'): '정재',
            ('을', '신'): '편관', ('을', '경'): '정관',
            ('을', '계'): '편인', ('을', '임'): '정인',
            
            # From 병 (Yang Fire) perspective
            ('병', '병'): '비견', ('병', '정'): '겁재',
            ('병', '무'): '식신', ('병', '기'): '상관',
            ('병', '경'): '편재', ('병', '신'): '정재',
            ('병', '임'): '편관', ('병', '계'): '정관',
            ('병', '갑'): '편인', ('병', '을'): '정인',
            
            # From 정 (Yin Fire) perspective
            ('정', '정'): '비견', ('정', '병'): '겁재',
            ('정', '기'): '식신', ('정', '무'): '상관',
            ('정', '신'): '편재', ('정', '경'): '정재',
            ('정', '계'): '편관', ('정', '임'): '정관',
            ('정', '을'): '편인', ('정', '갑'): '정인',
            
            # From 무 (Yang Earth) perspective
            ('무', '무'): '비견', ('무', '기'): '겁재',
            ('무', '경'): '식신', ('무', '신'): '상관',
            ('무', '임'): '편재', ('무', '계'): '정재',
            ('무', '갑'): '편관', ('무', '을'): '정관',
            ('무', '병'): '편인', ('무', '정'): '정인',
            
            # From 기 (Yin Earth) perspective
            ('기', '기'): '비견', ('기', '무'): '겁재',
            ('기', '신'): '식신', ('기', '경'): '상관',
            ('기', '계'): '편재', ('기', '임'): '정재',
            ('기', '을'): '편관', ('기', '갑'): '정관',
            ('기', '정'): '편인', ('기', '병'): '정인',
            
            # From 경 (Yang Metal) perspective
            ('경', '경'): '비견', ('경', '신'): '겁재',
            ('경', '임'): '식신', ('경', '계'): '상관',
            ('경', '갑'): '편재', ('경', '을'): '정재',
            ('경', '병'): '편관', ('경', '정'): '정관',
            ('경', '무'): '편인', ('경', '기'): '정인',
            
            # From 신 (Yin Metal) perspective
            ('신', '신'): '비견', ('신', '경'): '겁재',
            ('신', '계'): '식신', ('신', '임'): '상관',
            ('신', '을'): '편재', ('신', '갑'): '정재',
            ('신', '정'): '편관', ('신', '병'): '정관',
            ('신', '기'): '편인', ('신', '무'): '정인',
            
            # From 임 (Yang Water) perspective
            ('임', '임'): '비견', ('임', '계'): '겁재',
            ('임', '갑'): '식신', ('임', '을'): '상관',
            ('임', '병'): '편재', ('임', '정'): '정재',
            ('임', '무'): '편관', ('임', '기'): '정관',
            ('임', '경'): '편인', ('임', '신'): '정인',
            
            # From 계 (Yin Water) perspective
            ('계', '계'): '비견', ('계', '임'): '겁재',
            ('계', '을'): '식신', ('계', '갑'): '상관',
            ('계', '정'): '편재', ('계', '병'): '정재',
            ('계', '기'): '편관', ('계', '무'): '정관',
            ('계', '신'): '편인', ('계', '경'): '정인'
        }
        
    def _initialize_patterns(self):
        """Initialize all pattern definitions"""
        self.patterns = {
            # 정격 (Regular Patterns) - 8 types
            '정관격': {
                'category': '정격',
                'name': '정관격 (正官格)',
                'description': '정관이 월지에 있고 일간을 적절히 제어하는 격',
                'characteristics': [
                    '품위와 명예를 중시',
                    '정직하고 원칙적',
                    '책임감이 강함',
                    '리더십과 권위',
                    '안정적인 성향'
                ],
                'career': '공무원, 법조인, 교육자, 관리직, 정치인',
                'wealth': '안정적인 수입, 꾸준한 재산 증식, 명예와 함께 오는 부',
                'relationship': '전통적인 결혼관, 책임감 있는 배우자, 안정적인 가정생활',
                'cautions': ['지나친 원칙주의', '융통성 부족', '권위주의적 태도'],
                'famous': ['세종대왕', '이순신 장군'],
                'success_factors': ['정직과 신뢰', '꾸준한 노력', '원칙 준수']
            },
            
            '편관격': {
                'category': '정격',
                'name': '편관격 (偏官格)',
                'description': '편관(칠살)이 강하게 작용하는 격',
                'characteristics': [
                    '강한 추진력',
                    '결단력과 실행력',
                    '도전정신',
                    '카리스마',
                    '투쟁심'
                ],
                'career': '군인, 경찰, 운동선수, 외과의사, 검사, CEO',
                'wealth': '큰 성공 또는 실패, 투기적 성향, 벤처 사업 적합',
                'relationship': '열정적이지만 충돌 가능, 강한 개성의 배우자',
                'cautions': ['과도한 공격성', '인내심 부족', '극단적 선택'],
                'famous': ['나폴레옹', '징기스칸'],
                'success_factors': ['적절한 통제력', '인내심 기르기', '협력 중시']
            },
            
            '정재격': {
                'category': '정격',
                'name': '정재격 (正財格)',
                'description': '정재가 주도적인 역할을 하는 격',
                'characteristics': [
                    '성실하고 근면',
                    '경제관념 발달',
                    '현실적 사고',
                    '안정 추구',
                    '가족 중시'
                ],
                'career': '회계사, 은행원, 재무관리자, 부동산업, 자영업',
                'wealth': '착실한 재산 축적, 저축과 투자, 안정적 수입원',
                'relationship': '현실적 결혼관, 경제력 중시, 안정적 가정',
                'cautions': ['지나친 물질주의', '인색함', '모험심 부족'],
                'famous': ['정주영', '워런 버핏'],
                'success_factors': ['꾸준한 저축', '신중한 투자', '가족 화목']
            },
            
            '편재격': {
                'category': '정격',
                'name': '편재격 (偏財格)',
                'description': '편재가 강하게 나타나는 격',
                'characteristics': [
                    '사업 수완',
                    '기회 포착 능력',
                    '유연한 사고',
                    '사교적 성향',
                    '다재다능'
                ],
                'career': '사업가, 무역업, 영업직, 투자가, 프리랜서',
                'wealth': '변동성 큰 수입, 다양한 수입원, 투자 수익',
                'relationship': '자유로운 연애관, 다양한 인연, 변화 많은 관계',
                'cautions': ['산만함', '투기 성향', '책임감 부족'],
                'famous': ['빌 게이츠', '스티브 잡스'],
                'success_factors': ['집중력 향상', '리스크 관리', '장기 계획']
            },
            
            '정인격': {
                'category': '정격',
                'name': '정인격 (正印格)',
                'description': '정인이 일간을 생조하는 격',
                'characteristics': [
                    '학구적 성향',
                    '인자하고 온화',
                    '전통 중시',
                    '교육열',
                    '정신적 가치 추구'
                ],
                'career': '교수, 연구원, 작가, 종교인, 상담사, 교육자',
                'wealth': '명예와 함께 오는 부, 지적 재산, 안정적 수입',
                'relationship': '정신적 교감 중시, 온화한 가정, 자녀 교육 중시',
                'cautions': ['현실감 부족', '의존적 성향', '결단력 부족'],
                'famous': ['공자', '퇴계 이황'],
                'success_factors': ['지속적 학습', '인덕 쌓기', '후진 양성']
            },
            
            '편인격': {
                'category': '정격',
                'name': '편인격 (偏印格)',
                'description': '편인이 특별한 재능을 부여하는 격',
                'characteristics': [
                    '독특한 재능',
                    '직관력 발달',
                    '예술적 감각',
                    '종교적 성향',
                    '독립적 사고'
                ],
                'career': '예술가, 디자이너, 점술가, 심리상담사, 발명가',
                'wealth': '특수 재능으로 인한 수입, 불규칙적 수입',
                'relationship': '독특한 인연, 정신적 연결, 자유로운 관계',
                'cautions': ['고집', '비현실적 사고', '대인관계 어려움'],
                'famous': ['반 고흐', '아인슈타인'],
                'success_factors': ['재능 개발', '현실 감각', '소통 능력']
            },
            
            '식신격': {
                'category': '정격',
                'name': '식신격 (食神格)',
                'description': '식신이 일간의 기운을 표현하는 격',
                'characteristics': [
                    '낙천적 성격',
                    '표현력 풍부',
                    '먹는 것 좋아함',
                    '예술적 재능',
                    '유머 감각'
                ],
                'career': '요리사, 연예인, 작가, 교사, 서비스업',
                'wealth': '재능을 통한 수입, 꾸준한 수익, 즐기며 버는 돈',
                'relationship': '즐거운 연애, 화목한 가정, 자녀 복',
                'cautions': ['나태함', '과식', '책임감 부족'],
                'famous': ['백종원', '유재석'],
                'success_factors': ['재능 활용', '건강 관리', '꾸준함']
            },
            
            '상관격': {
                'category': '정격',
                'name': '상관격 (傷官格)',
                'description': '상관이 강하게 발현되는 격',
                'characteristics': [
                    '뛰어난 재능',
                    '비판적 사고',
                    '개혁 성향',
                    '독창성',
                    '반골 기질'
                ],
                'career': '비평가, 언론인, 개혁가, 예술가, 변호사',
                'wealth': '재능과 실력으로 큰 성공 가능, 변동성 있음',
                'relationship': '까다로운 연애관, 완벽주의, 충돌 가능성',
                'cautions': ['과도한 비판', '대인관계 문제', '오만함'],
                'famous': ['베토벤', '피카소'],
                'success_factors': ['겸손함', '협력 정신', '인내심']
            },
            
            # 변격 (Irregular Patterns) - 6 types
            '종격': {
                'category': '변격',
                'name': '종격 (從格)',
                'description': '일간이 극도로 약해 다른 오행을 따르는 격',
                'characteristics': [
                    '유연한 적응력',
                    '협조적 성향',
                    '상황 판단력',
                    '처세술',
                    '변화 수용'
                ],
                'career': '외교관, 중재자, 컨설턴트, 서비스업, 비서',
                'wealth': '타인과의 협력으로 성공, 인맥이 재산',
                'relationship': '조화로운 관계, 배우자 운 강함, 협력적',
                'cautions': ['주체성 부족', '의존적', '줏대 없음'],
                'famous': ['헨리 키신저'],
                'success_factors': ['협력 관계', '적응력', '인맥 관리']
            },
            
            '전왕격': {
                'category': '변격',
                'name': '전왕격 (專旺格)',
                'description': '일간이 극도로 강해 자기 오행만 왕성한 격',
                'characteristics': [
                    '강한 자아',
                    '독립심',
                    '추진력',
                    '자신감',
                    '리더십'
                ],
                'career': 'CEO, 창업가, 정치인, 독립 사업가, 예술가',
                'wealth': '자수성가, 독립 사업으로 큰 성공',
                'relationship': '독립적 관계, 강한 개성, 이해 필요',
                'cautions': ['독선적', '협력 부족', '고집'],
                'famous': ['이건희', '일론 머스크'],
                'success_factors': ['독창성', '추진력', '비전']
            },
            
            '일행득기격': {
                'category': '변격',
                'name': '일행득기격 (一行得氣格)',
                'description': '한 가지 오행이 극도로 강한 격',
                'characteristics': [
                    '전문성',
                    '집중력',
                    '완벽주의',
                    '깊이 있는 탐구',
                    '한 분야 최고'
                ],
                'career': '전문가, 장인, 연구원, 교수, 기술자',
                'wealth': '전문 분야에서 최고 대우, 안정적 고수입',
                'relationship': '깊고 진실한 관계, 소수 정예',
                'cautions': ['융통성 부족', '편협함', '사회성 부족'],
                'famous': ['장영실', '스티븐 호킹'],
                'success_factors': ['전문성 극대화', '꾸준한 연구', '깊이']
            },
            
            '양인격': {
                'category': '변격',
                'name': '양인격 (陽刃格)',
                'description': '양인(羊刃)이 강하게 작용하는 격',
                'characteristics': [
                    '강인한 의지',
                    '투쟁심',
                    '극단적 성향',
                    '돌파력',
                    '결단력'
                ],
                'career': '군인, 격투기 선수, 외과의사, 혁명가',
                'wealth': '극과 극의 재운, 대박 또는 대실패',
                'relationship': '열정적이지만 폭발적, 극단적 사랑',
                'cautions': ['폭력성', '극단주의', '자제력 부족'],
                'famous': ['관우', '나폴레옹'],
                'success_factors': ['자제력', '인내', '중용']
            },
            
            '건록격': {
                'category': '변격',
                'name': '건록격 (建祿格)',
                'description': '월지에 건록이 있는 격',
                'characteristics': [
                    '자수성가',
                    '독립심',
                    '실력 중시',
                    '자립심',
                    '노력형'
                ],
                'career': '창업가, 자영업, 프리랜서, 전문직',
                'wealth': '자신의 노력으로 축적, 실력이 곧 재산',
                'relationship': '독립적 관계, 실력 있는 배우자',
                'cautions': ['고독', '협력 부족', '완고함'],
                'famous': ['안철수', '마크 저커버그'],
                'success_factors': ['실력 향상', '독창성', '끈기']
            },
            
            '월겁격': {
                'category': '변격',
                'name': '월겁격 (月劫格)',
                'description': '월지에 겁재가 있는 격',
                'characteristics': [
                    '경쟁심',
                    '도전 정신',
                    '형제·친구 중시',
                    '협동심',
                    '활동적'
                ],
                'career': '스포츠, 영업, 경쟁 분야, 팀 리더',
                'wealth': '경쟁을 통한 성취, 공동 사업 성공',
                'relationship': '친구 같은 연인, 동료애, 경쟁적 관계',
                'cautions': ['과도한 경쟁', '시기심', '배신'],
                'famous': ['손흥민', '김연아'],
                'success_factors': ['팀워크', '정정당당', '우정']
            },
            
            # 특수격 (Special Patterns)
            '화기토양격': {
                'category': '특수격',
                'name': '화기토양격 (火氣土養格)',
                'description': '화와 토가 조화를 이루는 특수격',
                'characteristics': [
                    '따뜻한 성품',
                    '포용력',
                    '중재 능력',
                    '안정감',
                    '신뢰감'
                ],
                'career': '교육자, 상담사, 중재자, 사회사업가',
                'wealth': '안정적이고 지속적인 수입, 신뢰가 재산',
                'relationship': '따뜻하고 안정적인 관계, 가족 화목',
                'cautions': ['우유부단', '과도한 배려', '자기 희생'],
                'famous': ['테레사 수녀', '김구'],
                'success_factors': ['인덕', '신뢰', '포용']
            },
            
            '곡직격': {
                'category': '특수격',
                'name': '곡직격 (曲直格)',
                'description': '목이 왕성하여 곧게 뻗는 격',
                'characteristics': [
                    '정직함',
                    '성장 지향',
                    '생명력',
                    '창의성',
                    '발전 가능성'
                ],
                'career': '교육, 의료, 환경, 예술, 디자인',
                'wealth': '성장과 함께 증가하는 부, 장기 투자 성공',
                'relationship': '성장하는 사랑, 발전적 관계',
                'cautions': ['융통성 부족', '고집', '급성장 부작용'],
                'famous': ['세종대왕', '빌 게이츠'],
                'success_factors': ['지속 성장', '창의력', '정직']
            },
            
            '염상격': {
                'category': '특수격',
                'name': '염상격 (炎上格)',
                'description': '화가 왕성하여 타오르는 격',
                'characteristics': [
                    '열정',
                    '화려함',
                    '표현력',
                    '리더십',
                    '카리스마'
                ],
                'career': '연예인, 정치인, CEO, 예술가, 방송인',
                'wealth': '명성과 함께 오는 부, 대중적 성공',
                'relationship': '열정적 사랑, 화려한 로맨스',
                'cautions': ['허영', '과시욕', '번아웃'],
                'famous': ['마릴린 먼로', '엘비스 프레슬리'],
                'success_factors': ['열정 유지', '겸손', '지속력']
            },
            
            '종혁격': {
                'category': '특수격',
                'name': '종혁격 (從革格)',
                'description': '금이 왕성하여 개혁하는 격',
                'characteristics': [
                    '개혁 정신',
                    '결단력',
                    '정의감',
                    '단호함',
                    '변화 주도'
                ],
                'career': '법조인, 개혁가, 정치인, 군인, 경찰',
                'wealth': '정의로운 부, 개혁을 통한 성공',
                'relationship': '원칙적 사랑, 정의로운 관계',
                'cautions': ['융통성 부족', '극단주의', '독선'],
                'famous': ['링컨', '마틴 루터 킹'],
                'success_factors': ['정의', '용기', '신념']
            },
            
            '윤하격': {
                'category': '특수격',
                'name': '윤하격 (潤下格)',
                'description': '수가 왕성하여 흐르는 격',
                'characteristics': [
                    '유연함',
                    '적응력',
                    '지혜',
                    '통찰력',
                    '변화무쌍'
                ],
                'career': '철학자, 작가, 심리학자, 외교관, 컨설턴트',
                'wealth': '지혜를 통한 부, 유동적 자산',
                'relationship': '깊은 이해, 정신적 교감',
                'cautions': ['우유부단', '일관성 부족', '산만함'],
                'famous': ['노자', '공자'],
                'success_factors': ['지혜', '통찰', '유연성']
            }
        }
        
    def _calculate_ten_gods(self, day_stem: str, other_stem: str) -> str:
        """Calculate Ten Gods relationship between two stems"""
        return self.ten_gods_map.get((day_stem, other_stem), '')
        
    def _analyze_ten_gods_distribution(self, saju: Dict) -> Dict[str, int]:
        """Analyze distribution of Ten Gods in Saju"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        if not day_stem:
            return {}
            
        ten_gods_count = {
            '비견': 0, '겁재': 0,
            '식신': 0, '상관': 0,
            '정재': 0, '편재': 0,
            '정관': 0, '편관': 0,
            '정인': 0, '편인': 0
        }
        
        # Check all pillars
        for pillar in ['year', 'month', 'day', 'hour']:
            if pillar not in saju:
                continue
                
            # Check heavenly stem
            stem = saju[pillar].get('heavenly', '')
            if stem and not (pillar == 'day'):  # Don't count day stem against itself
                ten_god = self._calculate_ten_gods(day_stem, stem)
                if ten_god:
                    ten_gods_count[ten_god] += 1
                    
            # Check earthly branch hidden stems
            branch = saju[pillar].get('earthly', '')
            if branch:
                hidden = self.hidden_stems.get(branch, [])
                for h_stem in hidden:
                    ten_god = self._calculate_ten_gods(day_stem, h_stem)
                    if ten_god:
                        ten_gods_count[ten_god] += 0.5  # Hidden stems have half weight
                        
        return ten_gods_count
        
    def _check_regular_pattern(self, saju: Dict, ten_gods_dist: Dict) -> Optional[str]:
        """Check for regular patterns (정격)"""
        # Get month branch and its main element
        month_branch = saju.get('month', {}).get('earthly', '')
        month_stem = saju.get('month', {}).get('heavenly', '')
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not month_stem or not day_stem:
            return None
            
        # Calculate month pillar's ten god
        month_ten_god = self._calculate_ten_gods(day_stem, month_stem)
        
        # Check for dominant ten god in month pillar
        if month_ten_god == '정관' and ten_gods_dist.get('정관', 0) >= 1:
            return '정관격'
        elif month_ten_god == '편관' and ten_gods_dist.get('편관', 0) >= 1:
            return '편관격'
        elif month_ten_god == '정재' and ten_gods_dist.get('정재', 0) >= 1:
            return '정재격'
        elif month_ten_god == '편재' and ten_gods_dist.get('편재', 0) >= 1:
            return '편재격'
        elif month_ten_god == '정인' and ten_gods_dist.get('정인', 0) >= 1:
            return '정인격'
        elif month_ten_god == '편인' and ten_gods_dist.get('편인', 0) >= 1:
            return '편인격'
        elif month_ten_god == '식신' and ten_gods_dist.get('식신', 0) >= 1:
            return '식신격'
        elif month_ten_god == '상관' and ten_gods_dist.get('상관', 0) >= 1:
            return '상관격'
            
        # Check based on overall distribution
        max_god = max(ten_gods_dist.items(), key=lambda x: x[1])[0] if ten_gods_dist else None
        
        if max_god in ['정관', '편관', '정재', '편재', '정인', '편인', '식신', '상관']:
            return f'{max_god}격'
            
        return None
        
    def _check_irregular_pattern(self, saju: Dict, ten_gods_dist: Dict) -> Optional[str]:
        """Check for irregular patterns (변격)"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        month_branch = saju.get('month', {}).get('earthly', '')
        
        if not day_stem:
            return None
            
        # Check for extreme distributions
        total_self = ten_gods_dist.get('비견', 0) + ten_gods_dist.get('겁재', 0)
        total_resource = ten_gods_dist.get('정인', 0) + ten_gods_dist.get('편인', 0)
        total_output = ten_gods_dist.get('식신', 0) + ten_gods_dist.get('상관', 0)
        total_wealth = ten_gods_dist.get('정재', 0) + ten_gods_dist.get('편재', 0)
        total_power = ten_gods_dist.get('정관', 0) + ten_gods_dist.get('편관', 0)
        
        total_count = sum([total_self, total_resource, total_output, total_wealth, total_power])
        
        # 종격 - extremely weak day master
        if total_self < 1 and total_resource < 1:
            if total_wealth > 2 or total_power > 2:
                return '종격'
                
        # 전왕격 - extremely strong day master
        if total_self > 3 and total_resource > 1:
            if total_power < 1 and total_wealth < 1:
                return '전왕격'
                
        # 일행득기격 - one element dominates
        day_element = self.stem_elements.get(day_stem, '')
        element_count = self._count_elements(saju)
        max_element = max(element_count.items(), key=lambda x: x[1])[0] if element_count else None
        
        if max_element and element_count[max_element] > 5:
            return '일행득기격'
            
        # 양인격 - check for Yang Blade
        yang_blade_branches = {
            '갑': '묘', '을': '인',
            '병': '오', '정': '사',
            '무': '오', '기': '사',
            '경': '유', '신': '신',
            '임': '자', '계': '해'
        }
        
        blade_branch = yang_blade_branches.get(day_stem, '')
        if blade_branch and month_branch == blade_branch:
            return '양인격'
            
        # 건록격 - check for Lu position
        lu_branches = {
            '갑': '인', '을': '묘',
            '병': '사', '정': '오',
            '무': '사', '기': '오',
            '경': '신', '신': '유',
            '임': '해', '계': '자'
        }
        
        lu_branch = lu_branches.get(day_stem, '')
        if lu_branch and month_branch == lu_branch:
            return '건록격'
            
        # 월겁격 - Rob wealth in month
        if ten_gods_dist.get('겁재', 0) >= 2:
            return '월겁격'
            
        return None
        
    def _check_special_pattern(self, saju: Dict) -> Optional[str]:
        """Check for special patterns (특수격)"""
        element_count = self._count_elements(saju)
        
        # 화기토양격 - Fire and Earth harmony
        if element_count.get('화', 0) >= 2 and element_count.get('토', 0) >= 2:
            if element_count.get('화', 0) + element_count.get('토', 0) >= 5:
                return '화기토양격'
                
        # 곡직격 - Wood dominance
        if element_count.get('목', 0) >= 4:
            return '곡직격'
            
        # 염상격 - Fire dominance
        if element_count.get('화', 0) >= 4:
            return '염상격'
            
        # 종혁격 - Metal dominance
        if element_count.get('금', 0) >= 4:
            return '종혁격'
            
        # 윤하격 - Water dominance
        if element_count.get('수', 0) >= 4:
            return '윤하격'
            
        return None
        
    def _count_elements(self, saju: Dict) -> Dict[str, int]:
        """Count elements in Saju"""
        element_count = {'목': 0, '화': 0, '토': 0, '금': 0, '수': 0}
        
        for pillar in ['year', 'month', 'day', 'hour']:
            if pillar not in saju:
                continue
                
            # Count stem element
            stem = saju[pillar].get('heavenly', '')
            if stem:
                element = self.stem_elements.get(stem, '')
                if element:
                    element_count[element] += 1
                    
            # Count branch element
            branch = saju[pillar].get('earthly', '')
            if branch:
                element = self.branch_elements.get(branch, '')
                if element:
                    element_count[element] += 1
                    
        return element_count
        
    def identify_pattern(self, saju: Dict) -> str:
        """
        Identify the main pattern type in Saju
        
        Args:
            saju: Complete Saju data
            
        Returns:
            Pattern type name
        """
        # Analyze Ten Gods distribution
        ten_gods_dist = self._analyze_ten_gods_distribution(saju)
        
        # Check for special patterns first (highest priority)
        special_pattern = self._check_special_pattern(saju)
        if special_pattern:
            return special_pattern
            
        # Check for irregular patterns
        irregular_pattern = self._check_irregular_pattern(saju, ten_gods_dist)
        if irregular_pattern:
            return irregular_pattern
            
        # Check for regular patterns
        regular_pattern = self._check_regular_pattern(saju, ten_gods_dist)
        if regular_pattern:
            return regular_pattern
            
        # Default to most common pattern
        return '정재격'
        
    def analyze(self, saju: Dict) -> PatternAnalysis:
        """
        Perform complete pattern analysis
        
        Args:
            saju: Complete Saju data
            
        Returns:
            Complete pattern analysis
        """
        # Identify pattern
        pattern_type = self.identify_pattern(saju)
        
        # Get pattern details
        pattern_info = self.patterns.get(pattern_type, self.patterns['정재격'])
        
        # Calculate pattern strength
        strength_score = self._calculate_pattern_strength(saju, pattern_type)
        
        # Create analysis object
        analysis = PatternAnalysis(
            pattern_type=pattern_type,
            pattern_category=pattern_info['category'],
            pattern_name=pattern_info['name'],
            description=pattern_info['description'],
            characteristics=pattern_info['characteristics'],
            career_guidance=pattern_info['career'],
            wealth_fortune=pattern_info['wealth'],
            relationship_advice=pattern_info['relationship'],
            cautions=pattern_info['cautions'],
            famous_examples=pattern_info.get('famous', []),
            success_factors=pattern_info['success_factors'],
            strength_score=strength_score
        )
        
        return analysis
        
    def _calculate_pattern_strength(self, saju: Dict, pattern_type: str) -> float:
        """Calculate how strongly the pattern manifests"""
        # Simplified strength calculation
        # In real implementation, this would be more complex
        
        ten_gods_dist = self._analyze_ten_gods_distribution(saju)
        element_count = self._count_elements(saju)
        
        strength = 0.5  # Base strength
        
        # Adjust based on pattern type
        if '격' in pattern_type:
            # Check if the relevant ten god is strong
            god_name = pattern_type.replace('격', '')
            if god_name in ten_gods_dist:
                strength += min(ten_gods_dist[god_name] * 0.1, 0.3)
                
        # Adjust based on element balance
        max_element_count = max(element_count.values()) if element_count else 0
        if max_element_count >= 4:
            strength += 0.2
            
        return min(strength, 1.0)
        
    def get_pattern_summary(self, pattern_type: str) -> str:
        """Get a brief summary of a pattern"""
        pattern = self.patterns.get(pattern_type, {})
        if pattern:
            return f"{pattern['name']}: {pattern['description']}"
        return f"Unknown pattern: {pattern_type}"


# Helper function
def analyze_pattern(saju: Dict) -> PatternAnalysis:
    """
    Convenience function to analyze pattern
    
    Args:
        saju: Complete Saju data
        
    Returns:
        Complete pattern analysis
    """
    analyzer = PatternAnalyzer()
    return analyzer.analyze(saju)