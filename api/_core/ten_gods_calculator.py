# -*- coding: utf-8 -*-
"""
Ten Gods (십성) Calculator for Saju Analysis
Calculates the relationships between heavenly stems and analyzes their balance
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Element(Enum):
    """Five elements (오행)"""
    WOOD = "목"
    FIRE = "화"
    EARTH = "토"
    METAL = "금"
    WATER = "수"


class Polarity(Enum):
    """Yin/Yang polarity"""
    YANG = "양"
    YIN = "음"


class TenGodType(Enum):
    """Ten Gods (십성) types"""
    BI_JIAN = "비견"  # 比肩 - Companion
    JIE_CAI = "겁재"  # 劫財 - Rob Wealth
    SHI_SHEN = "식신"  # 食神 - Eating God
    SHANG_GUAN = "상관"  # 傷官 - Hurting Officer
    ZHENG_CAI = "정재"  # 正財 - Direct Wealth
    PIAN_CAI = "편재"  # 偏財 - Indirect Wealth
    ZHENG_GUAN = "정관"  # 正官 - Direct Officer
    PIAN_GUAN = "편관"  # 偏官 - Indirect Officer (Seven Killings)
    ZHENG_YIN = "정인"  # 正印 - Direct Resource
    PIAN_YIN = "편인"  # 偏印 - Indirect Resource


@dataclass
class StemInfo:
    """Information about a heavenly stem"""
    character: str
    element: Element
    polarity: Polarity


@dataclass
class TenGodRelation:
    """Represents a Ten God relationship"""
    god_type: TenGodType
    source_stem: str
    target_stem: str
    strength: float
    characteristics: List[str]


class TenGodsCalculator:
    """
    Calculator for Ten Gods (십성) relationships in Saju
    Analyzes the relationships between heavenly stems
    """
    
    def __init__(self):
        """Initialize the Ten Gods calculator with stem mappings"""
        self.stem_info = self._initialize_stem_info()
        self.element_cycle = self._initialize_element_cycle()
        self.ten_gods_characteristics = self._initialize_characteristics()
    
    def _initialize_stem_info(self) -> Dict[str, StemInfo]:
        """Initialize heavenly stem information"""
        return {
            '갑': StemInfo('갑', Element.WOOD, Polarity.YANG),
            '을': StemInfo('을', Element.WOOD, Polarity.YIN),
            '병': StemInfo('병', Element.FIRE, Polarity.YANG),
            '정': StemInfo('정', Element.FIRE, Polarity.YIN),
            '무': StemInfo('무', Element.EARTH, Polarity.YANG),
            '기': StemInfo('기', Element.EARTH, Polarity.YIN),
            '경': StemInfo('경', Element.METAL, Polarity.YANG),
            '신': StemInfo('신', Element.METAL, Polarity.YIN),
            '임': StemInfo('임', Element.WATER, Polarity.YANG),
            '계': StemInfo('계', Element.WATER, Polarity.YIN),
        }
    
    def _initialize_element_cycle(self) -> Dict[Element, Dict[str, Element]]:
        """Initialize the five element cycle relationships"""
        return {
            Element.WOOD: {
                'generates': Element.FIRE,
                'controls': Element.EARTH,
                'generated_by': Element.WATER,
                'controlled_by': Element.METAL
            },
            Element.FIRE: {
                'generates': Element.EARTH,
                'controls': Element.METAL,
                'generated_by': Element.WOOD,
                'controlled_by': Element.WATER
            },
            Element.EARTH: {
                'generates': Element.METAL,
                'controls': Element.WATER,
                'generated_by': Element.FIRE,
                'controlled_by': Element.WOOD
            },
            Element.METAL: {
                'generates': Element.WATER,
                'controls': Element.WOOD,
                'generated_by': Element.EARTH,
                'controlled_by': Element.FIRE
            },
            Element.WATER: {
                'generates': Element.WOOD,
                'controls': Element.FIRE,
                'generated_by': Element.METAL,
                'controlled_by': Element.EARTH
            }
        }
    
    def _initialize_characteristics(self) -> Dict[TenGodType, Dict[str, any]]:
        """Initialize Ten Gods characteristics and meanings"""
        return {
            TenGodType.BI_JIAN: {
                'category': 'self',
                'meaning': '동료, 형제, 경쟁자',
                'positive': '협력, 우정, 독립심',
                'negative': '경쟁, 고집, 분리',
                'strength_factor': 1.0
            },
            TenGodType.JIE_CAI: {
                'category': 'self',
                'meaning': '경쟁자, 라이벌',
                'positive': '진취성, 도전정신',
                'negative': '손재, 경쟁, 갈등',
                'strength_factor': 0.9
            },
            TenGodType.SHI_SHEN: {
                'category': 'output',
                'meaning': '재능, 창의성, 자녀',
                'positive': '예술성, 창조력, 표현력',
                'negative': '낭비, 산만함',
                'strength_factor': 0.8
            },
            TenGodType.SHANG_GUAN: {
                'category': 'output',
                'meaning': '도전, 혁신, 비판',
                'positive': '개혁, 창의성, 리더십',
                'negative': '반항, 비판적, 충돌',
                'strength_factor': 0.85
            },
            TenGodType.ZHENG_CAI: {
                'category': 'wealth',
                'meaning': '정당한 재물, 아내(남성)',
                'positive': '안정적 수입, 성실',
                'negative': '인색, 보수적',
                'strength_factor': 0.9
            },
            TenGodType.PIAN_CAI: {
                'category': 'wealth',
                'meaning': '의외의 재물, 애인',
                'positive': '사업수완, 투자',
                'negative': '투기, 불안정',
                'strength_factor': 0.85
            },
            TenGodType.ZHENG_GUAN: {
                'category': 'power',
                'meaning': '직위, 명예, 남편(여성)',
                'positive': '리더십, 책임감, 명예',
                'negative': '압박, 스트레스',
                'strength_factor': 1.0
            },
            TenGodType.PIAN_GUAN: {
                'category': 'power',
                'meaning': '권력, 도전, 위기',
                'positive': '추진력, 결단력',
                'negative': '폭력성, 극단적',
                'strength_factor': 0.95
            },
            TenGodType.ZHENG_YIN: {
                'category': 'resource',
                'meaning': '어머니, 교육, 지원',
                'positive': '학문, 지혜, 보호',
                'negative': '의존성, 나태',
                'strength_factor': 0.9
            },
            TenGodType.PIAN_YIN: {
                'category': 'resource',
                'meaning': '특수재능, 종교, 철학',
                'positive': '직관, 영성, 특수능력',
                'negative': '고독, 편협함',
                'strength_factor': 0.85
            }
        }
    
    def calculate_ten_gods(self, day_stem: str, target_stem: str) -> Optional[TenGodRelation]:
        """
        Calculate the Ten Gods relationship between day stem and target stem
        
        Args:
            day_stem: Day master heavenly stem (일간)
            target_stem: Target heavenly stem to compare
            
        Returns:
            TenGodRelation object or None if stems are invalid
        """
        if day_stem not in self.stem_info or target_stem not in self.stem_info:
            return None
        
        day_info = self.stem_info[day_stem]
        target_info = self.stem_info[target_stem]
        
        # Determine the element relationship
        relationship = self._get_element_relationship(day_info.element, target_info.element)
        
        # Determine the specific Ten God based on relationship and polarity
        ten_god_type = self._determine_ten_god_type(
            day_info, target_info, relationship
        )
        
        # Calculate strength based on various factors
        strength = self._calculate_strength(day_info, target_info, ten_god_type)
        
        # Get characteristics for this Ten God
        characteristics = self._get_characteristics(ten_god_type)
        
        return TenGodRelation(
            god_type=ten_god_type,
            source_stem=day_stem,
            target_stem=target_stem,
            strength=strength,
            characteristics=characteristics
        )
    
    def _get_element_relationship(self, source_element: Element, target_element: Element) -> str:
        """Determine the relationship between two elements"""
        if source_element == target_element:
            return 'same'
        elif self.element_cycle[source_element]['generates'] == target_element:
            return 'generates'  # I generate (output)
        elif self.element_cycle[source_element]['controls'] == target_element:
            return 'controls'  # I control (wealth)
        elif self.element_cycle[source_element]['generated_by'] == target_element:
            return 'generated_by'  # Generates me (resource)
        elif self.element_cycle[source_element]['controlled_by'] == target_element:
            return 'controlled_by'  # Controls me (power)
        else:
            return 'none'
    
    def _determine_ten_god_type(self, day_info: StemInfo, target_info: StemInfo, 
                                relationship: str) -> TenGodType:
        """Determine the specific Ten God type based on relationship and polarity"""
        same_polarity = (day_info.polarity == target_info.polarity)
        
        if relationship == 'same':
            # Same element - Companion or Rob Wealth
            if same_polarity:
                return TenGodType.BI_JIAN  # 비견
            else:
                return TenGodType.JIE_CAI  # 겁재
        
        elif relationship == 'generates':
            # I generate - Eating God or Hurting Officer
            if same_polarity:
                return TenGodType.SHI_SHEN  # 식신
            else:
                return TenGodType.SHANG_GUAN  # 상관
        
        elif relationship == 'controls':
            # I control - Direct or Indirect Wealth
            if same_polarity:
                return TenGodType.PIAN_CAI  # 편재
            else:
                return TenGodType.ZHENG_CAI  # 정재
        
        elif relationship == 'controlled_by':
            # Controls me - Direct or Indirect Officer
            if same_polarity:
                return TenGodType.PIAN_GUAN  # 편관 (칠살)
            else:
                return TenGodType.ZHENG_GUAN  # 정관
        
        elif relationship == 'generated_by':
            # Generates me - Direct or Indirect Resource
            if same_polarity:
                return TenGodType.PIAN_YIN  # 편인
            else:
                return TenGodType.ZHENG_YIN  # 정인
        
        # Default fallback (shouldn't normally reach here)
        return TenGodType.BI_JIAN
    
    def _calculate_strength(self, day_info: StemInfo, target_info: StemInfo, 
                           ten_god_type: TenGodType) -> float:
        """
        Calculate the strength of the Ten God relationship
        
        Returns:
            Strength value between 0.0 and 1.0
        """
        base_strength = self.ten_gods_characteristics[ten_god_type]['strength_factor']
        
        # Adjust based on element strength relationships
        element_modifier = 1.0
        
        # Same element relationships are stronger
        if day_info.element == target_info.element:
            element_modifier = 1.2
        # Supporting elements (generating cycle)
        elif self._is_supporting_element(day_info.element, target_info.element):
            element_modifier = 1.1
        # Conflicting elements
        elif self._is_conflicting_element(day_info.element, target_info.element):
            element_modifier = 0.9
        
        # Polarity harmony affects strength
        polarity_modifier = 1.0 if day_info.polarity != target_info.polarity else 0.95
        
        # Calculate final strength
        strength = base_strength * element_modifier * polarity_modifier
        
        # Normalize to 0.0-1.0 range
        return min(1.0, max(0.0, strength))
    
    def _is_supporting_element(self, elem1: Element, elem2: Element) -> bool:
        """Check if elements support each other in the generation cycle"""
        return (self.element_cycle[elem1]['generates'] == elem2 or 
                self.element_cycle[elem1]['generated_by'] == elem2)
    
    def _is_conflicting_element(self, elem1: Element, elem2: Element) -> bool:
        """Check if elements conflict in the control cycle"""
        return (self.element_cycle[elem1]['controls'] == elem2 or 
                self.element_cycle[elem1]['controlled_by'] == elem2)
    
    def _get_characteristics(self, ten_god_type: TenGodType) -> List[str]:
        """Get characteristics for a Ten God type"""
        info = self.ten_gods_characteristics[ten_god_type]
        return [
            info['meaning'],
            f"긍정: {info['positive']}",
            f"부정: {info['negative']}"
        ]
    
    def get_all_ten_gods(self, saju: Dict) -> Dict[str, any]:
        """
        Calculate all Ten Gods relationships in a Saju chart
        
        Args:
            saju: Dictionary containing four pillars with heavenly stems
            
        Returns:
            Dictionary with all Ten Gods relationships and analysis
        """
        if not saju or 'day' not in saju:
            return {}
        
        day_stem = saju.get('day', {}).get('heavenly', '')
        if not day_stem:
            return {}
        
        # Collect all heavenly stems from the four pillars
        stems = []
        positions = ['year', 'month', 'day', 'hour']
        
        for position in positions:
            if position in saju and 'heavenly' in saju[position]:
                stem = saju[position]['heavenly']
                if stem and position != 'day':  # Exclude day stem itself
                    stems.append((position, stem))
        
        # Calculate Ten Gods for each stem
        ten_gods_relations = {}
        for position, stem in stems:
            relation = self.calculate_ten_gods(day_stem, stem)
            if relation:
                ten_gods_relations[position] = {
                    'stem': stem,
                    'god_type': relation.god_type.value,
                    'strength': relation.strength,
                    'characteristics': relation.characteristics
                }
        
        # Analyze the balance of Ten Gods
        balance_analysis = self._analyze_ten_gods_balance(ten_gods_relations)
        
        # Calculate overall strength for each category
        category_strength = self._calculate_category_strength(ten_gods_relations)
        
        return {
            'day_master': day_stem,
            'relations': ten_gods_relations,
            'balance': balance_analysis,
            'category_strength': category_strength,
            'dominant_gods': self._get_dominant_gods(ten_gods_relations),
            'lacking_gods': self._get_lacking_gods(balance_analysis)
        }
    
    def _analyze_ten_gods_balance(self, relations: Dict) -> Dict[str, any]:
        """
        Analyze the balance of Ten Gods in the chart
        
        Returns:
            Dictionary with balance analysis
        """
        # Count occurrences of each Ten God type
        god_counts = {}
        total_strength = {}
        
        for position, info in relations.items():
            god_type = info['god_type']
            strength = info['strength']
            
            if god_type not in god_counts:
                god_counts[god_type] = 0
                total_strength[god_type] = 0.0
            
            god_counts[god_type] += 1
            total_strength[god_type] += strength
        
        # Analyze categories
        categories = {
            'self': 0,      # 비견, 겁재
            'output': 0,    # 식신, 상관
            'wealth': 0,    # 정재, 편재
            'power': 0,     # 정관, 편관
            'resource': 0   # 정인, 편인
        }
        
        for god_type, count in god_counts.items():
            for ten_god, info in self.ten_gods_characteristics.items():
                if ten_god.value == god_type:
                    category = info['category']
                    categories[category] += count
                    break
        
        # Determine balance status
        balance_status = self._determine_balance_status(categories)
        
        return {
            'god_counts': god_counts,
            'total_strength': total_strength,
            'categories': categories,
            'status': balance_status,
            'recommendations': self._generate_balance_recommendations(categories)
        }
    
    def _calculate_category_strength(self, relations: Dict) -> Dict[str, float]:
        """Calculate the total strength for each Ten God category"""
        category_strength = {
            'self': 0.0,
            'output': 0.0,
            'wealth': 0.0,
            'power': 0.0,
            'resource': 0.0
        }
        
        for position, info in relations.items():
            god_type = info['god_type']
            strength = info['strength']
            
            # Find the category for this god type
            for ten_god, characteristics in self.ten_gods_characteristics.items():
                if ten_god.value == god_type:
                    category = characteristics['category']
                    category_strength[category] += strength
                    break
        
        # Normalize strengths
        total = sum(category_strength.values())
        if total > 0:
            for category in category_strength:
                category_strength[category] = round(category_strength[category] / total * 100, 1)
        
        return category_strength
    
    def _get_dominant_gods(self, relations: Dict) -> List[str]:
        """Identify the dominant Ten Gods in the chart"""
        if not relations:
            return []
        
        # Sort by strength
        sorted_gods = sorted(
            relations.items(),
            key=lambda x: x[1]['strength'],
            reverse=True
        )
        
        # Return top 2 dominant gods
        dominant = []
        for position, info in sorted_gods[:2]:
            dominant.append(f"{info['god_type']} ({position})")
        
        return dominant
    
    def _get_lacking_gods(self, balance: Dict) -> List[str]:
        """Identify lacking Ten Gods categories"""
        categories = balance.get('categories', {})
        lacking = []
        
        # Categories with 0 occurrences are lacking
        for category, count in categories.items():
            if count == 0:
                lacking.append(self._get_category_korean_name(category))
        
        return lacking
    
    def _get_category_korean_name(self, category: str) -> str:
        """Get Korean name for Ten God category"""
        names = {
            'self': '비겁(자아)',
            'output': '식상(표현)',
            'wealth': '재성(재물)',
            'power': '관성(권력)',
            'resource': '인성(지원)'
        }
        return names.get(category, category)
    
    def _determine_balance_status(self, categories: Dict[str, int]) -> str:
        """Determine the overall balance status"""
        values = list(categories.values())
        max_val = max(values) if values else 0
        min_val = min(values) if values else 0
        
        # Check for extreme imbalance
        if max_val >= 3 and min_val == 0:
            return "극도로 불균형"
        elif max_val >= 2 and min_val == 0:
            return "불균형"
        elif max_val - min_val <= 1:
            return "균형"
        else:
            return "약간 불균형"
    
    def _generate_balance_recommendations(self, categories: Dict[str, int]) -> List[str]:
        """Generate recommendations based on Ten Gods balance"""
        recommendations = []
        
        # Check each category
        for category, count in categories.items():
            if count == 0:
                if category == 'self':
                    recommendations.append("자아/독립성 강화 필요 - 자신감과 주체성을 기르세요")
                elif category == 'output':
                    recommendations.append("표현력/창의성 개발 필요 - 예술이나 창작 활동을 시도하세요")
                elif category == 'wealth':
                    recommendations.append("재물운 보강 필요 - 재테크와 경제 관념을 기르세요")
                elif category == 'power':
                    recommendations.append("리더십/책임감 개발 필요 - 관리 능력을 향상시키세요")
                elif category == 'resource':
                    recommendations.append("학습/지원 체계 필요 - 멘토를 찾고 지식을 쌓으세요")
            elif count >= 3:
                if category == 'self':
                    recommendations.append("자아가 너무 강함 - 협력과 타협을 배우세요")
                elif category == 'output':
                    recommendations.append("표현 과다 - 절제와 집중이 필요합니다")
                elif category == 'wealth':
                    recommendations.append("재물욕 과다 - 정신적 가치도 중요시하세요")
                elif category == 'power':
                    recommendations.append("권력욕 과다 - 섬기는 리더십을 실천하세요")
                elif category == 'resource':
                    recommendations.append("의존성 과다 - 독립성과 자립심을 기르세요")
        
        # If balanced
        if not recommendations:
            recommendations.append("전체적으로 균형이 잘 잡혀 있습니다")
            recommendations.append("현재의 균형을 유지하면서 각 분야를 고르게 발전시키세요")
        
        return recommendations
    
    def get_ten_god_interpretation(self, ten_god_type: TenGodType) -> Dict[str, any]:
        """
        Get detailed interpretation for a specific Ten God
        
        Args:
            ten_god_type: The Ten God type to interpret
            
        Returns:
            Dictionary with detailed interpretation
        """
        if ten_god_type not in self.ten_gods_characteristics:
            return {}
        
        info = self.ten_gods_characteristics[ten_god_type]
        
        return {
            'name': ten_god_type.value,
            'category': info['category'],
            'meaning': info['meaning'],
            'positive_traits': info['positive'],
            'negative_traits': info['negative'],
            'life_areas': self._get_life_areas(ten_god_type),
            'career_implications': self._get_career_implications(ten_god_type),
            'relationship_implications': self._get_relationship_implications(ten_god_type)
        }
    
    def _get_life_areas(self, ten_god_type: TenGodType) -> List[str]:
        """Get life areas influenced by a Ten God"""
        life_areas = {
            TenGodType.BI_JIAN: ['독립성', '자아정체성', '형제관계', '동료관계'],
            TenGodType.JIE_CAI: ['경쟁', '도전', '사업 파트너', '재물 경쟁'],
            TenGodType.SHI_SHEN: ['창의성', '자녀운', '취미', '예술'],
            TenGodType.SHANG_GUAN: ['표현력', '비판력', '혁신', '리더십'],
            TenGodType.ZHENG_CAI: ['정규수입', '결혼(남성)', '안정', '저축'],
            TenGodType.PIAN_CAI: ['부수입', '투자', '사업', '이성관계'],
            TenGodType.ZHENG_GUAN: ['직장', '지위', '결혼(여성)', '명예'],
            TenGodType.PIAN_GUAN: ['권력', '도전', '경쟁', '스트레스'],
            TenGodType.ZHENG_YIN: ['교육', '어머니', '보호', '학문'],
            TenGodType.PIAN_YIN: ['특수재능', '종교', '철학', '직관']
        }
        return life_areas.get(ten_god_type, [])
    
    def _get_career_implications(self, ten_god_type: TenGodType) -> str:
        """Get career implications for a Ten God"""
        career_implications = {
            TenGodType.BI_JIAN: "독립적인 사업이나 프리랜서에 적합",
            TenGodType.JIE_CAI: "경쟁이 치열한 분야에서 성공 가능",
            TenGodType.SHI_SHEN: "예술, 요리, 교육 분야에 재능",
            TenGodType.SHANG_GUAN: "혁신적인 스타트업이나 개혁 분야",
            TenGodType.ZHENG_CAI: "안정적인 직장이나 공무원",
            TenGodType.PIAN_CAI: "사업, 투자, 영업 분야",
            TenGodType.ZHENG_GUAN: "관리직, 공직, 대기업",
            TenGodType.PIAN_GUAN: "군인, 경찰, 격투기, CEO",
            TenGodType.ZHENG_YIN: "교육, 연구, 의료 분야",
            TenGodType.PIAN_YIN: "종교, 철학, 대체의학, 상담"
        }
        return career_implications.get(ten_god_type, "다양한 분야에서 활동 가능")
    
    def _get_relationship_implications(self, ten_god_type: TenGodType) -> str:
        """Get relationship implications for a Ten God"""
        relationship_implications = {
            TenGodType.BI_JIAN: "독립적이지만 신뢰할 수 있는 관계",
            TenGodType.JIE_CAI: "경쟁적이지만 자극이 되는 관계",
            TenGodType.SHI_SHEN: "즐겁고 창의적인 관계",
            TenGodType.SHANG_GUAN: "도전적이고 성장하는 관계",
            TenGodType.ZHENG_CAI: "안정적이고 헌신적인 관계",
            TenGodType.PIAN_CAI: "자유롭고 다양한 관계",
            TenGodType.ZHENG_GUAN: "책임감 있고 신뢰하는 관계",
            TenGodType.PIAN_GUAN: "열정적이지만 갈등 가능한 관계",
            TenGodType.ZHENG_YIN: "보호받고 지원받는 관계",
            TenGodType.PIAN_YIN: "영적이고 특별한 관계"
        }
        return relationship_implications.get(ten_god_type, "조화로운 관계 가능")


# Helper functions for easy usage
def calculate_ten_gods(day_stem: str, target_stem: str) -> Optional[TenGodRelation]:
    """
    Calculate Ten Gods relationship between two stems
    
    Args:
        day_stem: Day master stem
        target_stem: Target stem to compare
        
    Returns:
        TenGodRelation object or None
    """
    calculator = TenGodsCalculator()
    return calculator.calculate_ten_gods(day_stem, target_stem)


def analyze_saju_ten_gods(saju: Dict) -> Dict:
    """
    Analyze all Ten Gods relationships in a Saju chart
    
    Args:
        saju: Saju chart dictionary
        
    Returns:
        Complete Ten Gods analysis
    """
    calculator = TenGodsCalculator()
    return calculator.get_all_ten_gods(saju)


def get_ten_god_meaning(ten_god_name: str) -> Dict:
    """
    Get the meaning and interpretation of a Ten God
    
    Args:
        ten_god_name: Korean name of the Ten God
        
    Returns:
        Interpretation dictionary
    """
    calculator = TenGodsCalculator()
    
    # Find the enum value
    for ten_god in TenGodType:
        if ten_god.value == ten_god_name:
            return calculator.get_ten_god_interpretation(ten_god)
    
    return {}