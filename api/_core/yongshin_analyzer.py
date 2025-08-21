# -*- coding: utf-8 -*-
"""
Yongshin (용신) Analyzer for Saju System
Analyzes day master strength and identifies useful/harmful gods
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class YongshinAnalysis:
    """Complete Yongshin analysis result"""
    day_master: str
    day_master_element: str
    strength: str  # 'very_strong', 'strong', 'balanced', 'weak', 'very_weak'
    strength_score: float
    useful_gods: List[str]
    harmful_gods: List[str]
    pattern_type: str  # 격국 type
    seasonal_influence: Dict[str, any]
    recommendations: List[str]
    element_balance: Dict[str, any]


class YongshinAnalyzer:
    """
    Analyzes Yongshin (용신) - useful and harmful gods in Saju
    Based on day master strength and element balance
    """
    
    def __init__(self):
        """Initialize the Yongshin analyzer"""
        self._initialize_element_relations()
        self._initialize_seasonal_strengths()
        self._initialize_pattern_rules()
        
    def _initialize_element_relations(self):
        """Initialize five element relationships"""
        # Five elements
        self.elements = ['목', '화', '토', '금', '수']
        
        # Element mapping for heavenly stems
        self.stem_elements = {
            '갑': '목', '을': '목',
            '병': '화', '정': '화',
            '무': '토', '기': '토',
            '경': '금', '신': '금',
            '임': '수', '계': '수'
        }
        
        # Element mapping for earthly branches
        self.branch_elements = {
            '자': '수', '축': '토', '인': '목', '묘': '목',
            '진': '토', '사': '화', '오': '화', '미': '토',
            '신': '금', '유': '금', '술': '토', '해': '수'
        }
        
        # Hidden stems in branches (지장간)
        self.hidden_stems = {
            '자': ['계'],           # 水
            '축': ['기', '신', '계'],  # 土, 金, 水
            '인': ['갑', '병', '무'],  # 木, 火, 土
            '묘': ['을'],           # 木
            '진': ['무', '을', '계'],  # 土, 木, 水
            '사': ['병', '무', '경'],  # 火, 土, 金
            '오': ['정', '기'],      # 火, 土
            '미': ['기', '정', '을'],  # 土, 火, 木
            '신': ['경', '임', '무'],  # 金, 水, 土
            '유': ['신'],           # 金
            '술': ['무', '신', '정'],  # 土, 金, 火
            '해': ['임', '갑']       # 水, 木
        }
        
        # Element generation cycle (상생)
        self.generating = {
            '목': '화',  # Wood generates Fire
            '화': '토',  # Fire generates Earth
            '토': '금',  # Earth generates Metal
            '금': '수',  # Metal generates Water
            '수': '목'   # Water generates Wood
        }
        
        # Element controlling cycle (상극)
        self.controlling = {
            '목': '토',  # Wood controls Earth
            '토': '수',  # Earth controls Water
            '수': '화',  # Water controls Fire
            '화': '금',  # Fire controls Metal
            '금': '목'   # Metal controls Wood
        }
        
        # Reverse relationships
        self.generated_by = {v: k for k, v in self.generating.items()}
        self.controlled_by = {v: k for k, v in self.controlling.items()}
        
    def _initialize_seasonal_strengths(self):
        """Initialize seasonal element strength modifiers"""
        # Season by month (lunar calendar)
        self.seasons = {
            '인': 'spring', '묘': 'spring',  # 1-2월
            '진': 'spring_earth',            # 3월 (transitional)
            '사': 'summer', '오': 'summer',  # 4-5월
            '미': 'summer_earth',            # 6월 (transitional)
            '신': 'autumn', '유': 'autumn',  # 7-8월
            '술': 'autumn_earth',            # 9월 (transitional)
            '해': 'winter', '자': 'winter',  # 10-11월
            '축': 'winter_earth'             # 12월 (transitional)
        }
        
        # Seasonal strength modifiers for each element
        self.seasonal_strength = {
            'spring': {
                '목': 1.5,   # Wood is strongest in spring
                '화': 1.2,   # Fire is growing
                '토': 0.8,   # Earth is weak
                '금': 0.6,   # Metal is weakest
                '수': 0.9    # Water is declining
            },
            'summer': {
                '목': 0.9,   # Wood is declining
                '화': 1.5,   # Fire is strongest in summer
                '토': 1.2,   # Earth is growing
                '금': 0.6,   # Metal is weak
                '수': 0.5    # Water is weakest
            },
            'autumn': {
                '목': 0.6,   # Wood is weak
                '화': 0.8,   # Fire is declining
                '토': 0.9,   # Earth is moderate
                '금': 1.5,   # Metal is strongest in autumn
                '수': 1.2    # Water is growing
            },
            'winter': {
                '목': 1.2,   # Wood is growing
                '화': 0.5,   # Fire is weakest
                '토': 0.6,   # Earth is weak
                '금': 0.9,   # Metal is declining
                '수': 1.5    # Water is strongest in winter
            },
            'spring_earth': {
                '목': 1.3,
                '화': 1.1,
                '토': 1.0,   # Earth is moderate in transitional
                '금': 0.7,
                '수': 0.8
            },
            'summer_earth': {
                '목': 0.8,
                '화': 1.3,
                '토': 1.3,   # Earth is strong after summer
                '금': 0.7,
                '수': 0.6
            },
            'autumn_earth': {
                '목': 0.7,
                '화': 0.7,
                '토': 1.1,   # Earth is moderate-strong
                '금': 1.3,
                '수': 1.1
            },
            'winter_earth': {
                '목': 1.1,
                '화': 0.6,
                '토': 0.8,   # Earth is weak in winter transition
                '금': 0.8,
                '수': 1.3
            }
        }
        
    def _initialize_pattern_rules(self):
        """Initialize pattern-based (격국) yongshin rules"""
        self.pattern_rules = {
            # 정격 (Normal patterns)
            '정관격': {
                'description': '정관이 용신인 격',
                'useful': ['정관', '정인', '식신'],
                'harmful': ['상관', '편관', '겁재'],
                'conditions': 'day_master_weak'
            },
            '편관격': {
                'description': '편관이 용신인 격',
                'useful': ['편관', '식신', '정인'],
                'harmful': ['겁재', '상관'],
                'conditions': 'day_master_weak'
            },
            '정인격': {
                'description': '정인이 용신인 격',
                'useful': ['정인', '편인', '정관'],
                'harmful': ['정재', '편재'],
                'conditions': 'day_master_weak'
            },
            '편인격': {
                'description': '편인이 용신인 격',
                'useful': ['편인', '편관'],
                'harmful': ['식신', '정재'],
                'conditions': 'day_master_weak'
            },
            '식신격': {
                'description': '식신이 용신인 격',
                'useful': ['식신', '정재', '편재'],
                'harmful': ['편인', '정인'],
                'conditions': 'day_master_strong'
            },
            '상관격': {
                'description': '상관이 용신인 격',
                'useful': ['상관', '편재'],
                'harmful': ['정인', '정관'],
                'conditions': 'day_master_strong'
            },
            '정재격': {
                'description': '정재가 용신인 격',
                'useful': ['정재', '식신', '정관'],
                'harmful': ['비견', '겁재', '편인'],
                'conditions': 'day_master_strong'
            },
            '편재격': {
                'description': '편재가 용신인 격',
                'useful': ['편재', '상관', '편관'],
                'harmful': ['비견', '겁재'],
                'conditions': 'day_master_strong'
            },
            
            # 특수격 (Special patterns)
            '종왕격': {
                'description': '일간이 극도로 강한 격',
                'useful': ['비견', '겁재', '정인', '편인'],
                'harmful': ['정관', '편관', '정재', '편재'],
                'conditions': 'day_master_very_strong'
            },
            '종약격': {
                'description': '일간이 극도로 약한 격',
                'useful': ['정관', '편관', '정재', '편재', '식신', '상관'],
                'harmful': ['비견', '겁재', '정인', '편인'],
                'conditions': 'day_master_very_weak'
            }
        }
        
    def analyze_day_master_strength(self, saju: Dict) -> Dict[str, any]:
        """
        Analyze the strength of day master (일간)
        
        Args:
            saju: Complete Saju data
            
        Returns:
            Day master strength analysis
        """
        day_stem = saju.get('day', {}).get('heavenly', '')
        if not day_stem:
            return {'strength': 'unknown', 'score': 0}
            
        day_element = self.stem_elements.get(day_stem, '')
        if not day_element:
            return {'strength': 'unknown', 'score': 0}
            
        # Count supporting elements
        support_score = 0
        drain_score = 0
        total_elements = 0
        
        # Analyze all pillars
        pillars = ['year', 'month', 'day', 'hour']
        for pillar in pillars:
            if pillar not in saju:
                continue
                
            # Check heavenly stem
            stem = saju[pillar].get('heavenly', '')
            if stem and stem != day_stem:  # Don't count day stem itself
                stem_element = self.stem_elements.get(stem, '')
                if stem_element:
                    total_elements += 1
                    score = self._calculate_element_support(day_element, stem_element)
                    if score > 0:
                        support_score += score
                    else:
                        drain_score += abs(score)
                        
            # Check earthly branch
            branch = saju[pillar].get('earthly', '')
            if branch:
                branch_element = self.branch_elements.get(branch, '')
                if branch_element:
                    total_elements += 1
                    
                    # Apply seasonal modifier
                    seasonal_modifier = 1.0
                    if pillar == 'month':
                        season = self.seasons.get(branch, '')
                        if season and season in self.seasonal_strength:
                            seasonal_modifier = self.seasonal_strength[season].get(day_element, 1.0)
                    
                    score = self._calculate_element_support(day_element, branch_element) * seasonal_modifier
                    if score > 0:
                        support_score += score
                    else:
                        drain_score += abs(score)
                        
                # Check hidden stems
                hidden = self.hidden_stems.get(branch, [])
                for h_stem in hidden:
                    h_element = self.stem_elements.get(h_stem, '')
                    if h_element:
                        total_elements += 0.5  # Hidden stems have half weight
                        score = self._calculate_element_support(day_element, h_element) * 0.5
                        if score > 0:
                            support_score += score
                        else:
                            drain_score += abs(score)
        
        # Calculate final strength
        if total_elements > 0:
            strength_ratio = support_score / (support_score + drain_score) if (support_score + drain_score) > 0 else 0.5
        else:
            strength_ratio = 0.5
            
        # Determine strength category
        if strength_ratio >= 0.8:
            strength = 'very_strong'
        elif strength_ratio >= 0.6:
            strength = 'strong'
        elif strength_ratio >= 0.4:
            strength = 'balanced'
        elif strength_ratio >= 0.2:
            strength = 'weak'
        else:
            strength = 'very_weak'
            
        return {
            'day_master': day_stem,
            'day_element': day_element,
            'strength': strength,
            'strength_score': strength_ratio,
            'support_score': support_score,
            'drain_score': drain_score,
            'total_elements': total_elements
        }
        
    def _calculate_element_support(self, day_element: str, other_element: str) -> float:
        """
        Calculate how much an element supports or drains the day master
        
        Args:
            day_element: Day master element
            other_element: Other element to compare
            
        Returns:
            Support score (positive) or drain score (negative)
        """
        if day_element == other_element:
            return 2.0  # Same element provides strong support
            
        # Check generation relationships
        if self.generated_by.get(day_element) == other_element:
            return 1.5  # Being generated provides support
        if self.generating.get(day_element) == other_element:
            return -1.0  # Generating others drains energy
            
        # Check control relationships
        if self.controlled_by.get(day_element) == other_element:
            return -1.5  # Being controlled drains energy
        if self.controlling.get(day_element) == other_element:
            return -0.5  # Controlling others requires some energy
            
        return 0  # No direct relationship
        
    def find_useful_god(self, saju: Dict, elements: Dict) -> List[str]:
        """
        Find useful gods (용신) based on day master strength and element balance
        
        Args:
            saju: Complete Saju data
            elements: Element percentages
            
        Returns:
            List of useful god elements
        """
        strength_analysis = self.analyze_day_master_strength(saju)
        day_element = strength_analysis['day_element']
        strength = strength_analysis['strength']
        
        useful_gods = []
        
        # Determine useful gods based on strength
        if strength in ['very_weak', 'weak']:
            # Weak day master needs support
            useful_gods.append(day_element)  # Same element
            useful_gods.append(self.generated_by.get(day_element, ''))  # Supporting element
            
            # If extremely weak, also add controlling element (종약격 tendency)
            if strength == 'very_weak':
                useful_gods.append(self.controlled_by.get(day_element, ''))
                
        elif strength in ['very_strong', 'strong']:
            # Strong day master needs outlet or control
            useful_gods.append(self.generating.get(day_element, ''))  # Outlet element
            useful_gods.append(self.controlling.get(day_element, ''))  # Wealth element
            
            # If extremely strong, embrace strength (종왕격 tendency)
            if strength == 'very_strong':
                useful_gods.append(day_element)  # Same element
                useful_gods.append(self.generated_by.get(day_element, ''))  # Supporting element
                
        else:  # balanced
            # Balanced day master - check what's lacking
            min_element = min(elements.items(), key=lambda x: x[1])[0] if elements else None
            if min_element:
                element_map = {'wood': '목', 'fire': '화', 'earth': '토', 'metal': '금', 'water': '수'}
                useful_gods.append(element_map.get(min_element, ''))
                
        # Remove empty strings and duplicates
        useful_gods = list(filter(None, useful_gods))
        useful_gods = list(dict.fromkeys(useful_gods))  # Remove duplicates while preserving order
        
        return useful_gods
        
    def find_harmful_god(self, saju: Dict, elements: Dict) -> List[str]:
        """
        Find harmful gods (기신/忌神) based on day master strength
        
        Args:
            saju: Complete Saju data
            elements: Element percentages
            
        Returns:
            List of harmful god elements
        """
        strength_analysis = self.analyze_day_master_strength(saju)
        day_element = strength_analysis['day_element']
        strength = strength_analysis['strength']
        
        harmful_gods = []
        
        # Determine harmful gods based on strength
        if strength in ['very_weak', 'weak']:
            # Weak day master - controlling and draining elements are harmful
            harmful_gods.append(self.controlled_by.get(day_element, ''))  # Controlling element
            harmful_gods.append(self.generating.get(day_element, ''))  # Draining element
            
            # If not extremely weak, same element can be harmful if excessive
            if strength == 'weak' and elements:
                element_map = {'wood': '목', 'fire': '화', 'earth': '토', 'metal': '금', 'water': '수'}
                reverse_map = {v: k for k, v in element_map.items()}
                day_elem_eng = reverse_map.get(day_element, '')
                if day_elem_eng and elements.get(day_elem_eng, 0) > 40:
                    harmful_gods.append(day_element)
                    
        elif strength in ['very_strong', 'strong']:
            # Strong day master - supporting elements can be harmful
            harmful_gods.append(day_element)  # Same element (too much)
            harmful_gods.append(self.generated_by.get(day_element, ''))  # Supporting element
            
            # If extremely strong (종왕격), controlling elements become harmful
            if strength == 'very_strong':
                harmful_gods.append(self.controlled_by.get(day_element, ''))
                harmful_gods.append(self.controlling.get(day_element, ''))
                
        else:  # balanced
            # Balanced day master - check what's excessive
            max_element = max(elements.items(), key=lambda x: x[1])[0] if elements else None
            if max_element and elements.get(max_element, 0) > 35:
                element_map = {'wood': '목', 'fire': '화', 'earth': '토', 'metal': '금', 'water': '수'}
                harmful_gods.append(element_map.get(max_element, ''))
                
        # Remove empty strings and duplicates
        harmful_gods = list(filter(None, harmful_gods))
        harmful_gods = list(dict.fromkeys(harmful_gods))  # Remove duplicates while preserving order
        
        return harmful_gods
        
    def determine_pattern_type(self, saju: Dict, strength_analysis: Dict) -> str:
        """
        Determine the pattern type (격국) based on Saju structure
        
        Args:
            saju: Complete Saju data
            strength_analysis: Day master strength analysis
            
        Returns:
            Pattern type name
        """
        strength = strength_analysis['strength']
        
        # Check for special patterns first
        if strength == 'very_strong':
            return '종왕격'
        elif strength == 'very_weak':
            return '종약격'
            
        # Analyze ten gods distribution to determine normal pattern
        # This is simplified - full implementation would analyze all ten gods
        month_stem = saju.get('month', {}).get('heavenly', '')
        if not month_stem:
            return '보통격'
            
        # Simplified pattern determination based on month stem
        # In full implementation, this would check all ten gods relationships
        day_stem = saju.get('day', {}).get('heavenly', '')
        if day_stem == month_stem:
            return '비견격'
            
        # Default patterns based on strength
        if strength == 'weak':
            return '정인격'  # Weak day master often benefits from resource
        elif strength == 'strong':
            return '식신격'  # Strong day master benefits from expression
        else:
            return '정재격'  # Balanced day master can handle wealth
            
    def analyze_seasonal_influence(self, saju: Dict) -> Dict[str, any]:
        """
        Analyze seasonal influence on elements
        
        Args:
            saju: Complete Saju data
            
        Returns:
            Seasonal influence analysis
        """
        month_branch = saju.get('month', {}).get('earthly', '')
        if not month_branch:
            return {'season': 'unknown', 'modifiers': {}}
            
        season = self.seasons.get(month_branch, 'unknown')
        modifiers = self.seasonal_strength.get(season, {})
        
        # Determine which elements are strong/weak in this season
        strong_elements = [elem for elem, mod in modifiers.items() if mod > 1.2]
        weak_elements = [elem for elem, mod in modifiers.items() if mod < 0.7]
        
        return {
            'month_branch': month_branch,
            'season': season,
            'modifiers': modifiers,
            'strong_elements': strong_elements,
            'weak_elements': weak_elements,
            'description': self._get_season_description(season)
        }
        
    def _get_season_description(self, season: str) -> str:
        """Get description for season"""
        descriptions = {
            'spring': '봄 - 목(木)이 왕성하고 화(火)가 상승하는 시기',
            'summer': '여름 - 화(火)가 왕성하고 토(土)가 생성되는 시기',
            'autumn': '가을 - 금(金)이 왕성하고 수(水)가 상승하는 시기',
            'winter': '겨울 - 수(水)가 왕성하고 목(木)이 생성되는 시기',
            'spring_earth': '봄 환절기 - 토(土)가 조절 역할을 하는 시기',
            'summer_earth': '여름 환절기 - 토(土)가 강해지는 시기',
            'autumn_earth': '가을 환절기 - 토(土)가 수확을 돕는 시기',
            'winter_earth': '겨울 환절기 - 토(土)가 약해지는 시기'
        }
        return descriptions.get(season, '계절 정보 없음')
        
    def generate_recommendations(self, analysis: YongshinAnalysis) -> List[str]:
        """
        Generate practical recommendations based on yongshin analysis
        
        Args:
            analysis: Complete yongshin analysis
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Recommendations based on day master strength
        if analysis.strength == 'very_weak':
            recommendations.append('일간이 매우 약하니 무리한 도전보다는 협력과 지원을 구하세요.')
            recommendations.append('건강 관리에 특별히 신경쓰고 과로를 피하세요.')
        elif analysis.strength == 'weak':
            recommendations.append('자신감을 기르고 주변의 도움을 적극 활용하세요.')
            recommendations.append('꾸준한 자기계발로 부족한 부분을 보완하세요.')
        elif analysis.strength == 'strong':
            recommendations.append('리더십을 발휘하되 독단적이지 않도록 주의하세요.')
            recommendations.append('자신의 능력을 나누고 베푸는 것이 좋습니다.')
        elif analysis.strength == 'very_strong':
            recommendations.append('강한 의지와 추진력을 긍정적으로 활용하세요.')
            recommendations.append('타인의 의견을 경청하고 유연성을 기르세요.')
        else:  # balanced
            recommendations.append('균형잡힌 상태를 유지하며 안정적인 발전을 추구하세요.')
            recommendations.append('극단적인 선택보다는 중용의 도를 지키세요.')
            
        # Recommendations based on useful gods
        if analysis.useful_gods:
            element_colors = {
                '목': '녹색, 청색',
                '화': '빨강, 자주색',
                '토': '노랑, 갈색',
                '금': '흰색, 은색',
                '수': '검정, 남색'
            }
            
            element_directions = {
                '목': '동쪽',
                '화': '남쪽',
                '토': '중앙',
                '금': '서쪽',
                '수': '북쪽'
            }
            
            for god in analysis.useful_gods[:2]:  # Top 2 useful gods
                color = element_colors.get(god, '')
                direction = element_directions.get(god, '')
                if color and direction:
                    recommendations.append(f'{god} 기운이 용신이니 {color} 계열과 {direction} 방향이 유리합니다.')
                    
        # Pattern-specific recommendations
        if analysis.pattern_type == '종왕격':
            recommendations.append('자신의 강한 기운을 그대로 활용하는 것이 좋습니다.')
            recommendations.append('전문 분야에서 독보적인 위치를 추구하세요.')
        elif analysis.pattern_type == '종약격':
            recommendations.append('대세를 따르고 유연하게 적응하는 것이 유리합니다.')
            recommendations.append('강한 조직이나 파트너와 함께하면 성공할 수 있습니다.')
            
        return recommendations
        
    def analyze(self, saju: Dict, elements: Dict) -> YongshinAnalysis:
        """
        Perform complete yongshin analysis
        
        Args:
            saju: Complete Saju data
            elements: Element percentages from element analysis
            
        Returns:
            Complete yongshin analysis
        """
        # Analyze day master strength
        strength_analysis = self.analyze_day_master_strength(saju)
        
        # Find useful and harmful gods
        useful_gods = self.find_useful_god(saju, elements)
        harmful_gods = self.find_harmful_god(saju, elements)
        
        # Determine pattern type
        pattern_type = self.determine_pattern_type(saju, strength_analysis)
        
        # Analyze seasonal influence
        seasonal_influence = self.analyze_seasonal_influence(saju)
        
        # Create analysis object
        analysis = YongshinAnalysis(
            day_master=strength_analysis['day_master'],
            day_master_element=strength_analysis['day_element'],
            strength=strength_analysis['strength'],
            strength_score=strength_analysis['strength_score'],
            useful_gods=useful_gods,
            harmful_gods=harmful_gods,
            pattern_type=pattern_type,
            seasonal_influence=seasonal_influence,
            recommendations=[],
            element_balance={
                'support_score': strength_analysis.get('support_score', 0),
                'drain_score': strength_analysis.get('drain_score', 0),
                'total_elements': strength_analysis.get('total_elements', 0)
            }
        )
        
        # Generate recommendations
        analysis.recommendations = self.generate_recommendations(analysis)
        
        return analysis


# Helper functions
def analyze_yongshin(saju: Dict, elements: Dict) -> YongshinAnalysis:
    """
    Convenience function to analyze yongshin
    
    Args:
        saju: Complete Saju data
        elements: Element percentages
        
    Returns:
        Complete yongshin analysis
    """
    analyzer = YongshinAnalyzer()
    return analyzer.analyze(saju, elements)