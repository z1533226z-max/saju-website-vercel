"""
Saju Compatibility Analysis Module
Analyzes compatibility between two people based on their Saju
"""

from typing import Dict, Tuple, Optional


class CompatibilityAnalyzer:
    """
    Analyzes compatibility between two Saju calculations
    """
    
    def __init__(self):
        """Initialize the compatibility analyzer"""
        self.element_compatibility = self._init_element_compatibility()
        self.stem_compatibility = self._init_stem_compatibility()
        self.branch_compatibility = self._init_branch_compatibility()
        self.zodiac_compatibility = self._init_zodiac_compatibility()
    
    def _init_zodiac_compatibility(self) -> Dict:
        """Initialize zodiac (띠) compatibility"""
        return {
            # 삼합 (최고의 궁합)
            ('자', '진', '신'): 95,  # 쥐, 용, 원숭이
            ('축', '사', '유'): 95,  # 소, 뱀, 닭
            ('인', '오', '술'): 95,  # 호랑이, 말, 개
            ('묘', '미', '해'): 95,  # 토끼, 양, 돼지
            
            # 육합 (좋은 궁합)
            ('자', '축'): 90,  # 쥐-소
            ('인', '해'): 90,  # 호랑이-돼지
            ('묘', '술'): 90,  # 토끼-개
            ('진', '유'): 90,  # 용-닭
            ('사', '신'): 90,  # 뱀-원숭이
            ('오', '미'): 90,  # 말-양
            
            # 상충 (피해야 할 궁합)
            ('자', '오'): 30,  # 쥐-말
            ('축', '미'): 30,  # 소-양
            ('인', '신'): 30,  # 호랑이-원숭이
            ('묘', '유'): 30,  # 토끼-닭
            ('진', '술'): 30,  # 용-개
            ('사', '해'): 30,  # 뱀-돼지
        }
    
    def _init_element_compatibility(self) -> Dict:
        """Initialize element compatibility matrix"""
        return {
            ('wood', 'fire'): 90,      # Wood generates Fire
            ('fire', 'earth'): 90,      # Fire generates Earth
            ('earth', 'metal'): 90,     # Earth generates Metal
            ('metal', 'water'): 90,     # Metal generates Water
            ('water', 'wood'): 90,      # Water generates Wood
            
            ('wood', 'earth'): 30,      # Wood overcomes Earth
            ('earth', 'water'): 30,     # Earth overcomes Water
            ('water', 'fire'): 30,      # Water overcomes Fire
            ('fire', 'metal'): 30,      # Fire overcomes Metal
            ('metal', 'wood'): 30,      # Metal overcomes Wood
            
            ('wood', 'wood'): 70,       # Same element
            ('fire', 'fire'): 70,
            ('earth', 'earth'): 70,
            ('metal', 'metal'): 70,
            ('water', 'water'): 70,
            
            # Neutral relationships
            ('wood', 'water'): 80,      # Water nourishes Wood
            ('wood', 'metal'): 40,      # Metal cuts Wood
            ('fire', 'wood'): 80,       # Wood feeds Fire
            ('fire', 'water'): 40,      # Water extinguishes Fire
            ('earth', 'fire'): 80,      # Fire creates Earth
            ('earth', 'wood'): 40,      # Wood breaks Earth
            ('metal', 'earth'): 80,     # Earth produces Metal
            ('metal', 'fire'): 40,      # Fire melts Metal
            ('water', 'metal'): 80,     # Metal enriches Water
            ('water', 'earth'): 40      # Earth absorbs Water
        }
    
    def _init_stem_compatibility(self) -> Dict:
        """Initialize heavenly stem compatibility"""
        return {
            ('갑', '을'): 85,  # Wood pair
            ('병', '정'): 85,  # Fire pair
            ('무', '기'): 85,  # Earth pair
            ('경', '신'): 85,  # Metal pair
            ('임', '계'): 85,  # Water pair
            
            ('갑', '기'): 95,  # Special combination
            ('을', '경'): 95,
            ('병', '신'): 95,
            ('정', '임'): 95,
            ('무', '계'): 95
        }
    
    def _init_branch_compatibility(self) -> Dict:
        """Initialize earthly branch compatibility"""
        return {
            # Three harmonies (삼합)
            ('신', '자', '진'): 95,  # Water harmony
            ('해', '묘', '미'): 95,  # Wood harmony
            ('인', '오', '술'): 95,  # Fire harmony
            ('사', '유', '축'): 95,  # Metal harmony
            
            # Six harmonies (육합)
            ('자', '축'): 90,
            ('인', '해'): 90,
            ('묘', '술'): 90,
            ('진', '유'): 90,
            ('사', '신'): 90,
            ('오', '미'): 90,
            
            # Clashes (충)
            ('자', '오'): 20,
            ('축', '미'): 20,
            ('인', '신'): 20,
            ('묘', '유'): 20,
            ('진', '술'): 20,
            ('사', '해'): 20
        }
    
    def analyze_compatibility(self, saju1: Dict, saju2: Dict, 
                            elements1: Dict, elements2: Dict,
                            gender1: str = 'neutral', gender2: str = 'neutral',
                            is_lunar1: bool = False, is_lunar2: bool = False) -> Dict:
        """
        Analyze compatibility between two people
        
        Args:
            saju1: First person's Saju
            saju2: Second person's Saju
            elements1: First person's element distribution
            elements2: Second person's element distribution
            gender1: First person's gender
            gender2: Second person's gender
            is_lunar1: First person uses lunar calendar
            is_lunar2: Second person uses lunar calendar
            
        Returns:
            Compatibility analysis result
        """
        # Calculate element compatibility
        element_score = self._calculate_element_compatibility(elements1, elements2)
        
        # Calculate heavenly stem compatibility
        stem_score = self._calculate_stem_compatibility(saju1, saju2)
        
        # Calculate earthly branch compatibility
        branch_score = self._calculate_branch_compatibility(saju1, saju2)
        
        # 성별 조합에 따른 보정
        gender_adjustment = 0
        if gender1 == 'male' and gender2 == 'female':
            # 전통적인 남녀 조합 - 천간 점수 가중치 증가
            stem_score += 5
            gender_adjustment = 3
        elif gender1 == 'female' and gender2 == 'male':
            # 여성 주도형 조합 - 오행 점수 가중치 증가
            element_score += 5
            gender_adjustment = 2
        elif gender1 == gender2:
            # 동성 조합 - 지지(현실적) 점수 가중치 증가
            branch_score += 8
            gender_adjustment = -2  # 전통적 관점에서는 감점
        
        # 음력 사용자 보정 (음력은 더 정확한 사주로 간주)
        lunar_adjustment = 0
        if is_lunar1 and is_lunar2:
            # 둘 다 음력 - 더 정확한 궁합
            lunar_adjustment = 5
        elif is_lunar1 or is_lunar2:
            # 한 명만 음력
            lunar_adjustment = 2
        
        # Calculate overall score (weighted average) with adjustments
        overall_score = (
            element_score * 0.35 +
            stem_score * 0.35 +
            branch_score * 0.3 +
            gender_adjustment +
            lunar_adjustment
        )
        
        # 최종 점수 조정 (0-100 범위)
        overall_score = max(0, min(100, overall_score))
        
        # Generate advice with all context
        advice = self._generate_compatibility_advice(
            overall_score, element_score, stem_score, branch_score,
            gender1, gender2, elements1, elements2, is_lunar1, is_lunar2
        )
        
        # 오행 한글 변환
        element_korean = {
            'wood': '목(木)',
            'fire': '화(火)',
            'earth': '토(土)',
            'metal': '금(金)',
            'water': '수(水)'
        }
        
        dominant1 = max(elements1.items(), key=lambda x: x[1])[0]
        dominant2 = max(elements2.items(), key=lambda x: x[1])[0]
        
        return {
            'overall_score': round(overall_score, 1),
            'element_compatibility': round(element_score, 1),
            'heavenly_stem_compatibility': round(stem_score, 1),
            'earthly_branch_compatibility': round(branch_score, 1),
            'compatibility_level': self._get_compatibility_level(overall_score),
            'advice': advice,
            'details': {
                'dominant_element1': element_korean.get(dominant1, dominant1),
                'dominant_element2': element_korean.get(dominant2, dominant2),
                'dominant_element1_raw': dominant1,
                'dominant_element2_raw': dominant2,
                'day_master1': saju1.get('day', {}).get('heavenly', ''),
                'day_master2': saju2.get('day', {}).get('heavenly', ''),
                'gender1': gender1,
                'gender2': gender2
            }
        }
    
    def _calculate_element_compatibility(self, elements1: Dict, elements2: Dict) -> float:
        """Calculate compatibility based on element distribution"""
        # Find dominant elements
        dominant1 = max(elements1.items(), key=lambda x: x[1])[0]
        dominant2 = max(elements2.items(), key=lambda x: x[1])[0]
        
        # Get base compatibility score
        key = (dominant1, dominant2)
        reverse_key = (dominant2, dominant1)
        
        if key in self.element_compatibility:
            base_score = self.element_compatibility[key]
        elif reverse_key in self.element_compatibility:
            base_score = self.element_compatibility[reverse_key]
        else:
            base_score = 50  # Neutral
        
        # Adjust based on element balance
        balance_bonus = 0
        for element in ['wood', 'fire', 'earth', 'metal', 'water']:
            diff = abs(elements1.get(element, 0) - elements2.get(element, 0))
            if diff < 10:
                balance_bonus += 2
        
        return min(100, base_score + balance_bonus)
    
    def _calculate_stem_compatibility(self, saju1: Dict, saju2: Dict) -> float:
        """Calculate compatibility based on heavenly stems"""
        score = 60  # Base score
        matches = 0
        total = 0
        
        pillars = ['year', 'month', 'day', 'hour']
        
        for pillar in pillars:
            stem1 = saju1.get(pillar, {}).get('heavenly', '')
            stem2 = saju2.get(pillar, {}).get('heavenly', '')
            
            if stem1 and stem2:
                total += 1
                key = (stem1, stem2)
                reverse_key = (stem2, stem1)
                
                if key in self.stem_compatibility:
                    score += self.stem_compatibility[key] / 4
                    matches += 1
                elif reverse_key in self.stem_compatibility:
                    score += self.stem_compatibility[reverse_key] / 4
                    matches += 1
        
        # Special bonus for day master compatibility
        day1 = saju1.get('day', {}).get('heavenly', '')
        day2 = saju2.get('day', {}).get('heavenly', '')
        
        if day1 and day2:
            key = (day1, day2)
            reverse_key = (day2, day1)
            if key in self.stem_compatibility or reverse_key in self.stem_compatibility:
                score += 10
        
        return min(100, score)
    
    def _calculate_branch_compatibility(self, saju1: Dict, saju2: Dict) -> float:
        """Calculate compatibility based on earthly branches"""
        score = 60  # Base score
        
        pillars = ['year', 'month', 'day', 'hour']
        branches1 = [saju1.get(p, {}).get('earthly', '') for p in pillars]
        branches2 = [saju2.get(p, {}).get('earthly', '') for p in pillars]
        
        # Check for harmonies and clashes
        for b1 in branches1:
            for b2 in branches2:
                if b1 and b2:
                    key = (b1, b2)
                    reverse_key = (b2, b1)
                    
                    # Check two-branch relationships
                    if key in self.branch_compatibility:
                        score += (self.branch_compatibility[key] - 50) / 8
                    elif reverse_key in self.branch_compatibility:
                        score += (self.branch_compatibility[reverse_key] - 50) / 8
        
        return min(100, max(0, score))
    
    def _get_compatibility_level(self, score: float) -> str:
        """Get compatibility level description"""
        if score >= 90:
            return '천생연분 (Perfect Match)'
        elif score >= 80:
            return '매우 좋음 (Excellent)'
        elif score >= 70:
            return '좋음 (Good)'
        elif score >= 60:
            return '보통 (Average)'
        elif score >= 50:
            return '노력 필요 (Needs Effort)'
        else:
            return '어려움 (Challenging)'
    
    def _generate_compatibility_advice(self, overall: float, 
                                      element: float, stem: float, branch: float,
                                      gender1: str = 'neutral', gender2: str = 'neutral',
                                      elements1: Dict = None, elements2: Dict = None,
                                      is_lunar1: bool = False, is_lunar2: bool = False) -> str:
        """Generate detailed compatibility advice based on scores and characteristics"""
        advice = []
        
        # 기본 궁합 평가
        if overall >= 90:
            advice.append('💝 천생연분! 두 사람은 서로를 완벽하게 이해하고 보완하는 관계입니다.')
        elif overall >= 80:
            advice.append('💕 매우 좋은 궁합! 자연스럽게 서로에게 끌리고 편안함을 느끼는 관계입니다.')
        elif overall >= 70:
            advice.append('💖 좋은 궁합! 서로를 존중하고 배려한다면 행복한 관계를 유지할 수 있습니다.')
        elif overall >= 60:
            advice.append('💗 보통 궁합. 서로의 차이를 인정하고 노력한다면 좋은 관계로 발전할 수 있습니다.')
        else:
            advice.append('💔 도전적인 관계. 많은 이해와 인내가 필요하지만, 그만큼 성장할 수 있는 관계입니다.')
        
        # 오행 조화 특별 조언
        if element >= 85:
            advice.append('🌟 오행의 조화가 완벽합니다! 서로가 부족한 기운을 채워주는 이상적인 관계입니다.')
        elif element >= 70:
            advice.append('✨ 오행이 서로 상생하는 관계로, 함께 있으면 시너지 효과가 큽니다.')
        elif element < 50:
            advice.append('⚡ 오행의 충돌이 있어 가끔 의견 차이가 있을 수 있지만, 이는 서로를 성장시키는 계기가 됩니다.')
        
        # 천간 조화 (정신적/성격적 궁합)
        if stem >= 85:
            advice.append('🧠 정신적 교감이 뛰어나 대화만으로도 행복을 느낄 수 있는 관계입니다.')
        elif stem >= 70:
            advice.append('💭 가치관과 생각이 비슷해 깊은 대화가 가능한 관계입니다.')
        elif stem < 60:
            advice.append('🤔 서로 다른 관점을 가지고 있어, 새로운 시각을 배울 수 있는 관계입니다.')
        
        # 지지 조화 (현실적/물질적 궁합)
        if branch >= 85:
            advice.append('💰 현실적인 면에서 매우 잘 맞아, 함께 목표를 이루기 좋은 파트너입니다.')
        elif branch >= 70:
            advice.append('🏠 일상생활의 리듬이 잘 맞아 편안한 관계를 유지할 수 있습니다.')
        elif branch < 50:
            advice.append('🔄 생활 패턴이 달라 조율이 필요하지만, 서로의 영역을 존중하면 문제없습니다.')
        
        # 성별에 따른 특별 조언 (더 상세하게)
        if gender1 == 'female' and gender2 == 'male':
            advice.append('👩‍❤️‍👨 여성이 주도적이고 남성이 수용적인 현대적 관계입니다.')
            if stem >= 70:
                advice.append('여성의 직관과 남성의 논리가 조화를 이루는 관계입니다.')
            if element >= 70:
                advice.append('여성의 감성과 남성의 이성이 균형을 맞추는 이상적인 조합입니다.')
        elif gender1 == 'male' and gender2 == 'female':
            advice.append('👨‍❤️‍👩 남성이 리드하고 여성이 서포트하는 전통적이면서도 안정적인 관계입니다.')
            if stem >= 70:
                advice.append('남성의 추진력과 여성의 세심함이 시너지를 만드는 관계입니다.')
            if branch >= 70:
                advice.append('현실적인 면에서 남녀의 역할 분담이 자연스럽게 이루어집니다.')
        elif gender1 == 'male' and gender2 == 'male':
            advice.append('👨‍❤️‍👨 동성 커플로서 서로를 깊이 이해할 수 있는 관계입니다.')
            advice.append('전통적 성역할에 얽매이지 않고 자유로운 관계를 만들 수 있습니다.')
        elif gender1 == 'female' and gender2 == 'female':
            advice.append('👩‍❤️‍👩 동성 커플로서 감정적 교류가 깊은 관계입니다.')
            advice.append('서로의 섬세함을 이해하고 공감대가 높은 관계입니다.')
        
        # 음력/양력 사용에 따른 조언
        if is_lunar1 and is_lunar2:
            advice.append('🌙 두 분 모두 음력 기준으로 더욱 정확한 사주 궁합이 계산되었습니다.')
        elif is_lunar1:
            advice.append('🌗 첫 번째 분은 음력, 두 번째 분은 양력 기준입니다. 전통과 현대의 조화로운 만남입니다.')
        elif is_lunar2:
            advice.append('🌓 첫 번째 분은 양력, 두 번째 분은 음력 기준입니다. 서로 다른 관점이 관계를 풍부하게 만듭니다.')
        else:
            advice.append('☀️ 두 분 모두 양력 기준으로 현대적인 궁합이 계산되었습니다.')
        
        # 특별한 인연 표시
        if overall >= 85 and element >= 80 and stem >= 80:
            advice.append('🌈 특별한 인연! 전생에서 이어진 깊은 연으로 보입니다.')
        
        # 주의사항 (낮은 점수일 때)
        if overall < 60:
            advice.append('💡 팁: 서로의 기념일을 챙기고, 작은 선물과 편지로 마음을 표현하면 관계가 개선됩니다.')
        
        return ' '.join(advice)