#!/usr/bin/env python3
"""
Specialized Compatibility Calculators
특화된 관계별 궁합 계산 시스템
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import math

from .compatibility_calculator import (
    CompatibilityCalculator, 
    CompatibilityResult,
    CompatibilityLevel
)


@dataclass
class LoverCompatibilityResult(CompatibilityResult):
    """연인 궁합 결과"""
    # 애정운 특화 점수
    romance_score: float  # 로맨스 점수
    passion_score: float  # 열정 점수
    emotional_bond_score: float  # 정서적 유대 점수
    communication_score: float  # 소통 점수
    
    # 애정운 분석
    love_language: str  # 사랑의 언어
    romantic_dynamics: List[str]  # 로맨틱한 역학
    passion_indicators: List[str]  # 열정 지표
    long_term_potential: str  # 장기적 잠재력


@dataclass
class MarriageCompatibilityResult(CompatibilityResult):
    """부부 궁합 결과"""
    # 결혼 생활 특화 점수
    stability_score: float  # 안정성 점수
    financial_harmony_score: float  # 재정 조화 점수
    family_building_score: float  # 가정 건설 점수
    conflict_resolution_score: float  # 갈등 해결 점수
    
    # 결혼 생활 분석
    marriage_type: str  # 결혼 유형
    household_dynamics: List[str]  # 가정 역학
    parenting_compatibility: str  # 육아 궁합
    longevity_factors: List[str]  # 지속 요인


@dataclass
class BusinessCompatibilityResult(CompatibilityResult):
    """사업 파트너 궁합 결과"""
    # 사업 특화 점수
    wealth_creation_score: float  # 재물 창출 점수
    cooperation_score: float  # 협력 점수
    risk_management_score: float  # 위험 관리 점수
    innovation_score: float  # 혁신 점수
    
    # 사업 분석
    business_synergy: str  # 사업 시너지
    role_distribution: Dict[str, str]  # 역할 분배
    success_factors: List[str]  # 성공 요인
    risk_areas: List[str]  # 위험 영역


@dataclass 
class FamilyCompatibilityResult(CompatibilityResult):
    """가족 궁합 결과"""
    # 가족 관계 특화 점수
    harmony_score: float  # 조화 점수
    support_score: float  # 지원 점수
    understanding_score: float  # 이해 점수
    generational_balance_score: float  # 세대 균형 점수
    
    # 가족 분석
    family_dynamics: str  # 가족 역학
    relationship_type: str  # 관계 유형 (부모-자녀, 형제 등)
    bonding_factors: List[str]  # 유대 요인
    healing_areas: List[str]  # 치유 영역


class LoverCompatibility(CompatibilityCalculator):
    """연인 궁합 계산기 - 애정운 중심"""
    
    def _get_clean_elements(self, saju: Dict) -> Dict:
        """오행 데이터를 안전하게 추출"""
        elements = saju.get('elements', {})
        if not isinstance(elements, dict):
            return {}
        if 'distribution' in elements:
            elements = elements['distribution']
        # 숫자 값만 필터링
        return {k: v for k, v in elements.items() if isinstance(v, (int, float))}
    
    def calculate_compatibility(self, saju1: Dict, saju2: Dict) -> LoverCompatibilityResult:
        """연인 궁합 계산"""
        # 기본 궁합 계산
        base_result = super().calculate_compatibility(saju1, saju2)
        
        # 애정운 특화 분석
        romance_score = self._calculate_romance_score(saju1, saju2)
        passion_score = self._calculate_passion_score(saju1, saju2)
        emotional_bond_score = self._calculate_emotional_bond(saju1, saju2)
        communication_score = self._calculate_communication_score(saju1, saju2)
        
        # 사랑의 언어 분석
        love_language = self._analyze_love_language(saju1, saju2)
        
        # 로맨틱 역학 분석
        romantic_dynamics = self._analyze_romantic_dynamics(
            saju1, saju2, base_result.pillar_analysis
        )
        
        # 열정 지표 확인
        passion_indicators = self._check_passion_indicators(saju1, saju2)
        
        # 장기적 잠재력 평가
        long_term_potential = self._evaluate_long_term_potential(
            base_result.total_score, 
            emotional_bond_score,
            communication_score
        )
        
        # 애정운 가중치 적용한 총점 재계산
        total_score = self._calculate_lover_total_score(
            base_result.element_balance_score,
            base_result.ten_gods_score,
            base_result.pillar_scores,
            romance_score,
            passion_score,
            emotional_bond_score,
            communication_score
        )
        
        # 연인 특화 조언 생성
        advice = self._generate_lover_advice(
            love_language,
            romantic_dynamics,
            passion_indicators,
            base_result.challenges
        )
        
        return LoverCompatibilityResult(
            total_score=total_score,
            level=self._determine_compatibility_level(total_score),
            element_balance_score=base_result.element_balance_score,
            ten_gods_score=base_result.ten_gods_score,
            pillar_scores=base_result.pillar_scores,
            element_analysis=base_result.element_analysis,
            ten_gods_analysis=base_result.ten_gods_analysis,
            pillar_analysis=base_result.pillar_analysis,
            strengths=base_result.strengths,
            challenges=base_result.challenges,
            advice=advice,
            special_combinations=base_result.special_combinations,
            warning_signs=base_result.warning_signs,
            romance_score=romance_score,
            passion_score=passion_score,
            emotional_bond_score=emotional_bond_score,
            communication_score=communication_score,
            love_language=love_language,
            romantic_dynamics=romantic_dynamics,
            passion_indicators=passion_indicators,
            long_term_potential=long_term_potential
        )
    
    def _calculate_romance_score(self, saju1: Dict, saju2: Dict) -> float:
        """로맨스 점수 계산"""
        score = 50
        
        # 일지 육합 확인 (로맨틱한 조합)
        day1_branch = saju1.get('day', {}).get('earthly', '')
        day2_branch = saju2.get('day', {}).get('earthly', '')
        
        if (day1_branch, day2_branch) in self.earthly_branch_relations['육합'] or \
           (day2_branch, day1_branch) in self.earthly_branch_relations['육합']:
            score += 30  # 육합은 로맨스에 매우 좋음
        
        # 홍염살, 도화살 등 애정 신살 확인
        if self._has_romance_shinshal(saju1) and self._has_romance_shinshal(saju2):
            score += 20  # 양쪽 모두 애정 신살이 있으면 열정적
        
        # 화(火) 오행이 있으면 열정 추가
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        fire_count1 = elements1.get('화', 0)
        fire_count2 = elements2.get('화', 0)
        if fire_count1 > 0 and fire_count2 > 0:
            score += 10
        
        return min(100, max(0, score))
    
    def _calculate_passion_score(self, saju1: Dict, saju2: Dict) -> float:
        """열정 점수 계산"""
        score = 50
        
        # 상관, 겁재 등 열정적인 십성 확인
        passionate_gods = ['상관', '겁재', '편관', '편재']
        
        # 일간 관계에서 열정적인 십성 찾기
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in passionate_gods:
            score += 20
        
        # 충이 있으면 열정적이지만 불안정
        conflict_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if (branch1, branch2) in self.earthly_branch_relations['충']:
                conflict_count += 1
        
        if conflict_count == 1:
            score += 15  # 적당한 충은 열정
        elif conflict_count >= 2:
            score -= 10  # 너무 많은 충은 문제
        
        return min(100, max(0, score))
    
    def _calculate_emotional_bond(self, saju1: Dict, saju2: Dict) -> float:
        """정서적 유대 점수 계산"""
        score = 50
        
        # 수(水) 오행이 있으면 정서적 교감
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        water_count1 = elements1.get('수', 0)
        water_count2 = elements2.get('수', 0)
        if water_count1 > 0 and water_count2 > 0:
            score += 15
        
        # 정인, 정관 등 안정적인 십성
        stable_gods = ['정인', '정관', '정재', '식신']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in stable_gods:
            score += 20
        
        # 월지가 같으면 정서적 공감
        month1_branch = saju1.get('month', {}).get('earthly', '')
        month2_branch = saju2.get('month', {}).get('earthly', '')
        if month1_branch == month2_branch:
            score += 15
        
        return min(100, max(0, score))
    
    def _calculate_communication_score(self, saju1: Dict, saju2: Dict) -> float:
        """소통 점수 계산"""
        score = 50
        
        # 목(木) 오행이 있으면 소통 원활
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        wood_count1 = elements1.get('목', 0)
        wood_count2 = elements2.get('목', 0)
        if wood_count1 > 0 and wood_count2 > 0:
            score += 15
        
        # 식신, 상관이 있으면 표현력 좋음
        expressive_gods = ['식신', '상관']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in expressive_gods:
            score += 20
        
        # 천간합이 많으면 소통 원활
        harmony_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            stem1 = saju1.get(pillar, {}).get('heavenly', '')
            stem2 = saju2.get(pillar, {}).get('heavenly', '')
            if (stem1, stem2) in self.heavenly_stem_relations['합']:
                harmony_count += 1
        
        score += harmony_count * 10
        
        return min(100, max(0, score))
    
    def _has_romance_shinshal(self, saju: Dict) -> bool:
        """애정 관련 신살 확인"""
        # 홍염살, 도화살 등의 지지 확인
        romance_branches = ['오', '자', '묘', '유']  # 도화살 지지
        
        for pillar in ['year', 'month', 'day', 'hour']:
            branch = saju.get(pillar, {}).get('earthly', '')
            if branch in romance_branches:
                return True
        return False
    
    def _analyze_love_language(self, saju1: Dict, saju2: Dict) -> str:
        """사랑의 언어 분석"""
        # 주요 오행 기반 사랑의 언어 판단
        elements1 = saju1.get('elements', {})
        elements2 = saju2.get('elements', {})
        
        # elements 구조 처리
        if not isinstance(elements1, dict):
            elements1 = {}
        if not isinstance(elements2, dict):
            elements2 = {}
        if 'distribution' in elements1:
            elements1 = elements1['distribution']
        if 'distribution' in elements2:
            elements2 = elements2['distribution']
        
        # 안전한 dominant element 계산
        clean_elements1 = {k: v for k, v in elements1.items() if isinstance(v, (int, float))}
        clean_elements2 = {k: v for k, v in elements2.items() if isinstance(v, (int, float))}
        
        # 가장 강한 오행 찾기
        dominant1 = max(clean_elements1.items(), key=lambda x: x[1])[0] if clean_elements1 else None
        dominant2 = max(clean_elements2.items(), key=lambda x: x[1])[0] if clean_elements2 else None
        
        love_languages = {
            '목': '봉사와 헌신의 사랑',
            '화': '열정과 표현의 사랑',
            '토': '안정과 신뢰의 사랑',
            '금': '품격과 존중의 사랑',
            '수': '지혜와 소통의 사랑'
        }
        
        if dominant1 and dominant2:
            if dominant1 == dominant2:
                return f"공통된 {love_languages.get(dominant1, '균형잡힌 사랑')}"
            else:
                return f"{love_languages.get(dominant1, '')}과 {love_languages.get(dominant2, '')}의 조화"
        
        return "다양한 사랑의 표현"
    
    def _analyze_romantic_dynamics(self, saju1: Dict, saju2: Dict, 
                                  pillar_analysis: Dict) -> List[str]:
        """로맨틱한 역학 분석"""
        dynamics = []
        
        # 일주 관계 확인
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('heavenly_relation') == '천간합':
            dynamics.append("천간합으로 자연스러운 끌림")
        if day_analysis.get('earthly_relation') == '육합':
            dynamics.append("육합으로 깊은 애정")
        
        # 월주 관계 확인
        month_analysis = pillar_analysis.get('month', {})
        if month_analysis.get('earthly_relation') == '육합':
            dynamics.append("감정적 교감이 깊음")
        
        # 시주 관계 확인
        hour_analysis = pillar_analysis.get('hour', {})
        if hour_analysis.get('heavenly_relation') == '천간합':
            dynamics.append("미래를 함께 꿈꾸는 관계")
        
        return dynamics[:5]
    
    def _check_passion_indicators(self, saju1: Dict, saju2: Dict) -> List[str]:
        """열정 지표 확인"""
        indicators = []
        
        # 화 오행 확인
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        fire1 = elements1.get('화', 0)
        fire2 = elements2.get('화', 0)
        if fire1 > 2 or fire2 > 2:
            indicators.append("강한 화 기운으로 열정적")
        
        # 도화살 확인
        if self._has_romance_shinshal(saju1) or self._has_romance_shinshal(saju2):
            indicators.append("도화살로 매력적인 관계")
        
        # 충 관계 확인
        for pillar in ['day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if (branch1, branch2) in self.earthly_branch_relations['충']:
                indicators.append(f"{pillar} 충으로 역동적인 관계")
                break
        
        return indicators[:4]
    
    def _evaluate_long_term_potential(self, total_score: float, 
                                     emotional_bond: float,
                                     communication: float) -> str:
        """장기적 잠재력 평가"""
        avg_score = (total_score + emotional_bond + communication) / 3
        
        if avg_score >= 75:
            return "매우 높음 - 결혼까지 이어질 가능성"
        elif avg_score >= 65:
            return "높음 - 진지한 관계로 발전 가능"
        elif avg_score >= 55:
            return "보통 - 노력하면 지속 가능"
        elif avg_score >= 45:
            return "도전적 - 상호 노력 필요"
        else:
            return "낮음 - 단기적 관계 가능성"
    
    def _calculate_lover_total_score(self, element_score: float, ten_gods_score: float,
                                    pillar_scores: Dict[str, float], romance: float,
                                    passion: float, emotional: float, 
                                    communication: float) -> float:
        """연인 궁합 총점 계산"""
        # 연인 관계 특화 가중치
        weights = {
            'element': 0.10,
            'ten_gods': 0.10,
            'year': 0.05,
            'month': 0.05,
            'day': 0.15,  # 일주 중요
            'hour': 0.05,
            'romance': 0.20,  # 로맨스 매우 중요
            'passion': 0.10,
            'emotional': 0.10,
            'communication': 0.10
        }
        
        total = (
            element_score * weights['element'] +
            ten_gods_score * weights['ten_gods'] +
            pillar_scores.get('year', 50) * weights['year'] +
            pillar_scores.get('month', 50) * weights['month'] +
            pillar_scores.get('day', 50) * weights['day'] +
            pillar_scores.get('hour', 50) * weights['hour'] +
            romance * weights['romance'] +
            passion * weights['passion'] +
            emotional * weights['emotional'] +
            communication * weights['communication']
        )
        
        return round(total, 2)
    
    def _generate_lover_advice(self, love_language: str, dynamics: List[str],
                              indicators: List[str], challenges: List[str]) -> List[str]:
        """연인 특화 조언 생성"""
        advice = []
        
        # 사랑의 언어 기반 조언
        advice.append(f"서로의 사랑 표현 방식 ({love_language})을 이해하고 존중하세요")
        
        # 로맨틱 역학 기반 조언
        if "천간합" in str(dynamics):
            advice.append("자연스러운 끌림을 즐기되 일상의 노력도 잊지 마세요")
        if "육합" in str(dynamics):
            advice.append("깊은 애정을 바탕으로 신뢰를 쌓아가세요")
        
        # 열정 지표 기반 조언
        if "화 기운" in str(indicators):
            advice.append("열정을 유지하되 서로를 태우지 않도록 조절하세요")
        if "도화살" in str(indicators):
            advice.append("매력적인 관계이니 서로에게만 집중하세요")
        
        # 도전 과제 기반 조언
        if "충" in str(challenges):
            advice.append("충돌 시 감정보다 이성적 대화로 해결하세요")
        
        # 일반 연인 조언
        advice.append("정기적인 데이트로 로맨스를 유지하세요")
        advice.append("서로의 개인 시간도 존중해주세요")
        advice.append("작은 서프라이즈로 일상에 활력을 더하세요")
        
        return advice[:7]


class MarriageCompatibility(CompatibilityCalculator):
    """부부 궁합 계산기 - 결혼 생활 안정성 중심"""
    
    def _get_clean_elements(self, saju: Dict) -> Dict:
        """오행 데이터를 안전하게 추출"""
        elements = saju.get('elements', {})
        if not isinstance(elements, dict):
            return {}
        if 'distribution' in elements:
            elements = elements['distribution']
        return {k: v for k, v in elements.items() if isinstance(v, (int, float))}
    
    def calculate_compatibility(self, saju1: Dict, saju2: Dict) -> MarriageCompatibilityResult:
        """부부 궁합 계산"""
        # 기본 궁합 계산
        base_result = super().calculate_compatibility(saju1, saju2)
        
        # 결혼 생활 특화 분석
        stability_score = self._calculate_stability_score(saju1, saju2)
        financial_harmony = self._calculate_financial_harmony(saju1, saju2)
        family_building = self._calculate_family_building_score(saju1, saju2)
        conflict_resolution = self._calculate_conflict_resolution(saju1, saju2)
        
        # 결혼 유형 분석
        marriage_type = self._analyze_marriage_type(saju1, saju2)
        
        # 가정 역학 분석
        household_dynamics = self._analyze_household_dynamics(
            saju1, saju2, base_result.pillar_analysis
        )
        
        # 육아 궁합 평가
        parenting_compatibility = self._evaluate_parenting_compatibility(saju1, saju2)
        
        # 지속 요인 확인
        longevity_factors = self._check_longevity_factors(
            base_result.element_analysis,
            base_result.pillar_analysis
        )
        
        # 부부 특화 총점 계산
        total_score = self._calculate_marriage_total_score(
            base_result.element_balance_score,
            base_result.ten_gods_score,
            base_result.pillar_scores,
            stability_score,
            financial_harmony,
            family_building,
            conflict_resolution
        )
        
        # 부부 특화 조언 생성
        advice = self._generate_marriage_advice(
            marriage_type,
            household_dynamics,
            parenting_compatibility,
            base_result.challenges
        )
        
        return MarriageCompatibilityResult(
            total_score=total_score,
            level=self._determine_compatibility_level(total_score),
            element_balance_score=base_result.element_balance_score,
            ten_gods_score=base_result.ten_gods_score,
            pillar_scores=base_result.pillar_scores,
            element_analysis=base_result.element_analysis,
            ten_gods_analysis=base_result.ten_gods_analysis,
            pillar_analysis=base_result.pillar_analysis,
            strengths=base_result.strengths,
            challenges=base_result.challenges,
            advice=advice,
            special_combinations=base_result.special_combinations,
            warning_signs=base_result.warning_signs,
            stability_score=stability_score,
            financial_harmony_score=financial_harmony,
            family_building_score=family_building,
            conflict_resolution_score=conflict_resolution,
            marriage_type=marriage_type,
            household_dynamics=household_dynamics,
            parenting_compatibility=parenting_compatibility,
            longevity_factors=longevity_factors
        )
    
    def _calculate_stability_score(self, saju1: Dict, saju2: Dict) -> float:
        """안정성 점수 계산"""
        score = 50
        
        # 토(土) 오행이 강하면 안정적
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        earth1 = elements1.get('토', 0)
        earth2 = elements2.get('토', 0)
        if earth1 > 0 and earth2 > 0:
            score += 20
        
        # 정관, 정재 등 안정적인 십성
        stable_gods = ['정관', '정재', '정인']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in stable_gods:
            score += 25
        
        # 충이 적으면 안정적
        conflict_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if (branch1, branch2) in self.earthly_branch_relations['충']:
                conflict_count += 1
        
        score -= conflict_count * 10
        
        return min(100, max(0, score))
    
    def _calculate_financial_harmony(self, saju1: Dict, saju2: Dict) -> float:
        """재정 조화 점수 계산"""
        score = 50
        
        # 금(金) 오행이 있으면 재물운
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        metal1 = elements1.get('금', 0)
        metal2 = elements2.get('금', 0)
        if metal1 > 0 and metal2 > 0:
            score += 15
        
        # 정재, 편재가 있으면 재물 관리
        wealth_gods = ['정재', '편재']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in wealth_gods:
            score += 20
        
        # 년주가 합하면 가문의 재산 조화
        year1_branch = saju1.get('year', {}).get('earthly', '')
        year2_branch = saju2.get('year', {}).get('earthly', '')
        if (year1_branch, year2_branch) in self.earthly_branch_relations['육합']:
            score += 15
        
        return min(100, max(0, score))
    
    def _calculate_family_building_score(self, saju1: Dict, saju2: Dict) -> float:
        """가정 건설 점수 계산"""
        score = 50
        
        # 시주가 합하면 자녀운 좋음
        hour1_branch = saju1.get('hour', {}).get('earthly', '')
        hour2_branch = saju2.get('hour', {}).get('earthly', '')
        if (hour1_branch, hour2_branch) in self.earthly_branch_relations['육합']:
            score += 25
        
        # 목(木) 오행이 있으면 성장과 발전
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        wood1 = elements1.get('목', 0)
        wood2 = elements2.get('목', 0)
        if wood1 > 0 and wood2 > 0:
            score += 15
        
        # 식신이 있으면 자녀 복
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation == '식신':
            score += 20
        
        return min(100, max(0, score))
    
    def _calculate_conflict_resolution(self, saju1: Dict, saju2: Dict) -> float:
        """갈등 해결 능력 점수"""
        score = 50
        
        # 수(水) 오행이 있으면 유연함
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        water1 = elements1.get('수', 0)
        water2 = elements2.get('수', 0)
        if water1 > 0 and water2 > 0:
            score += 15
        
        # 정인이 있으면 포용력
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in ['정인', '편인']:
            score += 20
        
        # 형, 해가 없으면 갈등 적음
        punishment_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if self._check_punishment(branch1, branch2):
                punishment_count += 1
        
        score -= punishment_count * 15
        
        return min(100, max(0, score))
    
    def _analyze_marriage_type(self, saju1: Dict, saju2: Dict) -> str:
        """결혼 유형 분석"""
        # 주요 십성 관계로 결혼 유형 판단
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        
        marriage_types = {
            '정관': '전통적이고 안정적인 결혼',
            '편관': '역동적이고 변화가 많은 결혼',
            '정재': '경제적으로 풍요로운 결혼',
            '편재': '자유롭고 독립적인 결혼',
            '정인': '정신적 교감이 깊은 결혼',
            '편인': '독특하고 개성있는 결혼',
            '비견': '동반자적 평등한 결혼',
            '겁재': '경쟁적이지만 성장하는 결혼',
            '식신': '화목하고 자녀 복이 있는 결혼',
            '상관': '창의적이고 표현적인 결혼'
        }
        
        return marriage_types.get(ten_god_relation, '균형잡힌 결혼')
    
    def _analyze_household_dynamics(self, saju1: Dict, saju2: Dict,
                                   pillar_analysis: Dict) -> List[str]:
        """가정 역학 분석"""
        dynamics = []
        
        # 년주 관계 - 시댁/처가 관계
        year_analysis = pillar_analysis.get('year', {})
        if year_analysis.get('earthly_relation') == '육합':
            dynamics.append("양가 부모님과 조화로운 관계")
        elif year_analysis.get('earthly_relation') == '충':
            dynamics.append("양가 관계에서 중재 역할 필요")
        
        # 월주 관계 - 형제/친척 관계
        month_analysis = pillar_analysis.get('month', {})
        if month_analysis.get('earthly_relation') == '육합':
            dynamics.append("형제/친척과 원만한 관계")
        
        # 일주 관계 - 부부 관계
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('earthly_relation') == '육합':
            dynamics.append("부부간 깊은 신뢰와 애정")
        
        # 시주 관계 - 자녀 관계
        hour_analysis = pillar_analysis.get('hour', {})
        if hour_analysis.get('earthly_relation') == '육합':
            dynamics.append("자녀와 좋은 관계 형성")
        
        return dynamics[:5]
    
    def _evaluate_parenting_compatibility(self, saju1: Dict, saju2: Dict) -> str:
        """육아 궁합 평가"""
        # 시주 관계 확인
        hour1_branch = saju1.get('hour', {}).get('earthly', '')
        hour2_branch = saju2.get('hour', {}).get('earthly', '')
        
        if (hour1_branch, hour2_branch) in self.earthly_branch_relations['육합']:
            return "매우 좋음 - 육아 방식이 조화로움"
        elif (hour1_branch, hour2_branch) in self.earthly_branch_relations['충']:
            return "도전적 - 육아관 차이 조율 필요"
        
        # 식신 확인
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation == '식신':
            return "좋음 - 자녀에게 좋은 부모"
        
        return "보통 - 서로 협력하면 좋은 부모 가능"
    
    def _check_longevity_factors(self, element_analysis: Dict,
                                pillar_analysis: Dict) -> List[str]:
        """결혼 지속 요인 확인"""
        factors = []
        
        # 오행 상생 관계
        if element_analysis.get('generating_score', 0) > 15:
            factors.append("오행 상생으로 서로를 도움")
        
        # 일주 육합
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('earthly_relation') == '육합':
            factors.append("일지 육합으로 변치 않는 애정")
        
        # 보완적 관계
        if element_analysis.get('complementary_score', 0) > 20:
            factors.append("서로의 부족함을 채워주는 관계")
        
        # 천간합
        if day_analysis.get('heavenly_relation') == '천간합':
            factors.append("천간합으로 자연스러운 조화")
        
        return factors[:4]
    
    def _calculate_marriage_total_score(self, element_score: float, ten_gods_score: float,
                                       pillar_scores: Dict[str, float], stability: float,
                                       financial: float, family: float,
                                       conflict: float) -> float:
        """부부 궁합 총점 계산"""
        # 결혼 생활 특화 가중치
        weights = {
            'element': 0.10,
            'ten_gods': 0.10,
            'year': 0.10,  # 가문 관계
            'month': 0.10,  # 형제 관계
            'day': 0.15,  # 부부 관계
            'hour': 0.10,  # 자녀 관계
            'stability': 0.15,  # 안정성 중요
            'financial': 0.10,
            'family': 0.05,
            'conflict': 0.05
        }
        
        total = (
            element_score * weights['element'] +
            ten_gods_score * weights['ten_gods'] +
            pillar_scores.get('year', 50) * weights['year'] +
            pillar_scores.get('month', 50) * weights['month'] +
            pillar_scores.get('day', 50) * weights['day'] +
            pillar_scores.get('hour', 50) * weights['hour'] +
            stability * weights['stability'] +
            financial * weights['financial'] +
            family * weights['family'] +
            conflict * weights['conflict']
        )
        
        return round(total, 2)
    
    def _generate_marriage_advice(self, marriage_type: str, dynamics: List[str],
                                 parenting: str, challenges: List[str]) -> List[str]:
        """부부 특화 조언 생성"""
        advice = []
        
        # 결혼 유형 기반 조언
        advice.append(f"{marriage_type}의 특성을 이해하고 장점을 살리세요")
        
        # 가정 역학 기반 조언
        if "양가 부모님" in str(dynamics):
            advice.append("양가 부모님께 균형있게 효도하세요")
        if "자녀와 좋은 관계" in str(dynamics):
            advice.append("자녀 교육에 일관된 방향을 유지하세요")
        
        # 육아 궁합 기반 조언
        if "도전적" in parenting:
            advice.append("육아관 차이는 대화로 조율하세요")
        
        # 도전 과제 기반 조언
        if "충" in str(challenges):
            advice.append("정기적인 부부 대화 시간을 가지세요")
        
        # 일반 부부 조언
        advice.append("가사 분담을 명확히 하여 갈등을 줄이세요")
        advice.append("경제적 계획을 함께 세우고 실행하세요")
        advice.append("부부만의 시간을 정기적으로 가지세요")
        
        return advice[:7]


class BusinessCompatibility(CompatibilityCalculator):
    """사업 파트너 궁합 계산기 - 재물운과 협력 중심"""
    
    def _get_clean_elements(self, saju: Dict) -> Dict:
        """오행 데이터를 안전하게 추출"""
        elements = saju.get('elements', {})
        if not isinstance(elements, dict):
            return {}
        if 'distribution' in elements:
            elements = elements['distribution']
        # 숫자 값만 필터링
        return {k: v for k, v in elements.items() if isinstance(v, (int, float))}
    
    def calculate_compatibility(self, saju1: Dict, saju2: Dict) -> BusinessCompatibilityResult:
        """사업 파트너 궁합 계산"""
        # 기본 궁합 계산
        base_result = super().calculate_compatibility(saju1, saju2)
        
        # 사업 특화 분석
        wealth_creation = self._calculate_wealth_creation(saju1, saju2)
        cooperation = self._calculate_cooperation_score(saju1, saju2)
        risk_management = self._calculate_risk_management(saju1, saju2)
        innovation = self._calculate_innovation_score(saju1, saju2)
        
        # 사업 시너지 분석
        business_synergy = self._analyze_business_synergy(saju1, saju2)
        
        # 역할 분배 제안
        role_distribution = self._suggest_role_distribution(saju1, saju2)
        
        # 성공 요인 확인
        success_factors = self._identify_success_factors(
            base_result.element_analysis,
            base_result.pillar_analysis
        )
        
        # 위험 영역 확인
        risk_areas = self._identify_risk_areas(base_result.warning_signs)
        
        # 사업 특화 총점 계산
        total_score = self._calculate_business_total_score(
            base_result.element_balance_score,
            base_result.ten_gods_score,
            base_result.pillar_scores,
            wealth_creation,
            cooperation,
            risk_management,
            innovation
        )
        
        # 사업 특화 조언 생성
        advice = self._generate_business_advice(
            business_synergy,
            role_distribution,
            success_factors,
            risk_areas
        )
        
        return BusinessCompatibilityResult(
            total_score=total_score,
            level=self._determine_compatibility_level(total_score),
            element_balance_score=base_result.element_balance_score,
            ten_gods_score=base_result.ten_gods_score,
            pillar_scores=base_result.pillar_scores,
            element_analysis=base_result.element_analysis,
            ten_gods_analysis=base_result.ten_gods_analysis,
            pillar_analysis=base_result.pillar_analysis,
            strengths=base_result.strengths,
            challenges=base_result.challenges,
            advice=advice,
            special_combinations=base_result.special_combinations,
            warning_signs=base_result.warning_signs,
            wealth_creation_score=wealth_creation,
            cooperation_score=cooperation,
            risk_management_score=risk_management,
            innovation_score=innovation,
            business_synergy=business_synergy,
            role_distribution=role_distribution,
            success_factors=success_factors,
            risk_areas=risk_areas
        )
    
    def _calculate_wealth_creation(self, saju1: Dict, saju2: Dict) -> float:
        """재물 창출 능력 점수"""
        score = 50
        
        # 금(金) 오행 - 재물
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        metal1 = elements1.get('금', 0)
        metal2 = elements2.get('금', 0)
        if metal1 > 0 and metal2 > 0:
            score += 20
        
        # 정재, 편재 십성
        wealth_gods = ['정재', '편재']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in wealth_gods:
            score += 25
        
        # 토(土) 오행 - 안정적 재물
        earth1 = elements1.get('토', 0)
        earth2 = elements2.get('토', 0)
        if earth1 > 0 and earth2 > 0:
            score += 10
        
        return min(100, max(0, score))
    
    def _calculate_cooperation_score(self, saju1: Dict, saju2: Dict) -> float:
        """협력 점수 계산"""
        score = 50
        
        # 천간합이 많으면 협력 좋음
        harmony_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            stem1 = saju1.get(pillar, {}).get('heavenly', '')
            stem2 = saju2.get(pillar, {}).get('heavenly', '')
            if (stem1, stem2) in self.heavenly_stem_relations['합']:
                harmony_count += 1
        
        score += harmony_count * 15
        
        # 비견, 겁재가 있으면 협력 관계
        cooperative_gods = ['비견', '겁재']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in cooperative_gods:
            score += 15
        
        return min(100, max(0, score))
    
    def _calculate_risk_management(self, saju1: Dict, saju2: Dict) -> float:
        """위험 관리 능력 점수"""
        score = 50
        
        # 수(水) 오행 - 유연성과 적응력
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        water1 = elements1.get('수', 0)
        water2 = elements2.get('수', 0)
        if water1 > 0 or water2 > 0:
            score += 15
        
        # 정관, 정인 - 신중함
        cautious_gods = ['정관', '정인']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in cautious_gods:
            score += 20
        
        # 충이 많으면 위험 증가
        conflict_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if (branch1, branch2) in self.earthly_branch_relations['충']:
                conflict_count += 1
        
        score -= conflict_count * 10
        
        return min(100, max(0, score))
    
    def _calculate_innovation_score(self, saju1: Dict, saju2: Dict) -> float:
        """혁신 능력 점수"""
        score = 50
        
        # 화(火) 오행 - 창의성과 열정
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        fire1 = elements1.get('화', 0)
        fire2 = elements2.get('화', 0)
        if fire1 > 0 or fire2 > 0:
            score += 15
        
        # 상관, 편인 - 창의성
        creative_gods = ['상관', '편인']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in creative_gods:
            score += 20
        
        # 목(木) 오행 - 성장과 발전
        wood1 = elements1.get('목', 0)
        wood2 = elements2.get('목', 0)
        if wood1 > 0 or wood2 > 0:
            score += 15
        
        return min(100, max(0, score))
    
    def _analyze_business_synergy(self, saju1: Dict, saju2: Dict) -> str:
        """사업 시너지 분석"""
        # 오행 보완 관계 확인
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        
        # 서로 부족한 오행을 보완하는지
        complementary = False
        for element in ['목', '화', '토', '금', '수']:
            if elements1.get(element, 0) == 0 and elements2.get(element, 0) > 0:
                complementary = True
                break
            elif elements2.get(element, 0) == 0 and elements1.get(element, 0) > 0:
                complementary = True
                break
        
        if complementary:
            return "상호 보완적 시너지 - 서로의 약점을 보완"
        
        # 십성 관계 확인
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        
        synergy_types = {
            '정재': '안정적 수익 창출 시너지',
            '편재': '모험적 사업 확장 시너지',
            '정관': '체계적 관리 시너지',
            '편관': '혁신적 돌파 시너지',
            '비견': '평등한 파트너십 시너지',
            '식신': '창의적 생산 시너지'
        }
        
        return synergy_types.get(ten_god_relation, '균형잡힌 협력 시너지')
    
    def _suggest_role_distribution(self, saju1: Dict, saju2: Dict) -> Dict[str, str]:
        """역할 분배 제안"""
        roles = {}
        
        # Person 1 역할 결정
        elements1 = self._get_clean_elements(saju1)
        dominant1 = max(elements1.items(), key=lambda x: x[1])[0] if elements1 else None
        
        role_by_element = {
            '목': 'CEO/전략기획',
            '화': '마케팅/홍보',
            '토': 'COO/운영관리',
            '금': 'CFO/재무관리',
            '수': 'CTO/기술개발'
        }
        
        roles['person1'] = role_by_element.get(dominant1, '종합관리')
        
        # Person 2 역할 결정
        elements2 = self._get_clean_elements(saju2)
        dominant2 = max(elements2.items(), key=lambda x: x[1])[0] if elements2 else None
        
        roles['person2'] = role_by_element.get(dominant2, '종합관리')
        
        # 역할 중복 시 조정
        if roles['person1'] == roles['person2']:
            roles['recommendation'] = '공동 대표 체제 권장'
        else:
            roles['recommendation'] = '역할 분담 명확화 권장'
        
        return roles
    
    def _identify_success_factors(self, element_analysis: Dict,
                                 pillar_analysis: Dict) -> List[str]:
        """성공 요인 확인"""
        factors = []
        
        # 오행 상생
        if element_analysis.get('generating_score', 0) > 15:
            factors.append("오행 상생으로 시너지 효과")
        
        # 보완적 관계
        if element_analysis.get('complementary_score', 0) > 20:
            factors.append("상호 보완적 역량")
        
        # 천간합
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('heavenly_relation') == '천간합':
            factors.append("자연스러운 협력 관계")
        
        # 육합
        if day_analysis.get('earthly_relation') == '육합':
            factors.append("신뢰 기반 파트너십")
        
        return factors[:4]
    
    def _identify_risk_areas(self, warning_signs: List[str]) -> List[str]:
        """위험 영역 확인"""
        risks = []
        
        for warning in warning_signs:
            if "충" in warning:
                risks.append("의견 충돌 위험")
            if "극함" in warning:
                risks.append("권력 불균형 위험")
            if "형" in warning:
                risks.append("법적 분쟁 위험")
        
        # 기본 사업 위험
        risks.append("시장 변화 대응력 점검 필요")
        
        return risks[:4]
    
    def _calculate_business_total_score(self, element_score: float, ten_gods_score: float,
                                       pillar_scores: Dict[str, float], wealth: float,
                                       cooperation: float, risk: float,
                                       innovation: float) -> float:
        """사업 파트너 궁합 총점 계산"""
        # 사업 특화 가중치
        weights = {
            'element': 0.10,
            'ten_gods': 0.10,
            'year': 0.05,
            'month': 0.05,
            'day': 0.10,
            'hour': 0.05,
            'wealth': 0.25,  # 재물 창출 매우 중요
            'cooperation': 0.15,
            'risk': 0.10,
            'innovation': 0.05
        }
        
        total = (
            element_score * weights['element'] +
            ten_gods_score * weights['ten_gods'] +
            pillar_scores.get('year', 50) * weights['year'] +
            pillar_scores.get('month', 50) * weights['month'] +
            pillar_scores.get('day', 50) * weights['day'] +
            pillar_scores.get('hour', 50) * weights['hour'] +
            wealth * weights['wealth'] +
            cooperation * weights['cooperation'] +
            risk * weights['risk'] +
            innovation * weights['innovation']
        )
        
        return round(total, 2)
    
    def _generate_business_advice(self, synergy: str, roles: Dict[str, str],
                                 success_factors: List[str], risks: List[str]) -> List[str]:
        """사업 파트너 특화 조언 생성"""
        advice = []
        
        # 시너지 기반 조언
        advice.append(f"{synergy}를 최대한 활용하세요")
        
        # 역할 분배 조언
        if roles.get('recommendation'):
            advice.append(f"{roles['recommendation']}으로 효율성을 높이세요")
        
        # 성공 요인 활용
        if success_factors:
            advice.append(f"강점인 '{success_factors[0]}'를 적극 활용하세요")
        
        # 위험 관리
        if risks:
            advice.append(f"'{risks[0]}' 대비책을 마련하세요")
        
        # 일반 사업 조언
        advice.append("명확한 계약서와 역할 분담 문서화")
        advice.append("정기적인 성과 리뷰와 전략 회의")
        advice.append("이익 분배 방식을 사전에 명확히 합의")
        
        return advice[:7]


class FamilyCompatibility(CompatibilityCalculator):
    """가족 궁합 계산기 - 가족 간 조화 중심"""
    
    def _get_clean_elements(self, saju: Dict) -> Dict:
        """오행 데이터를 안전하게 추출"""
        elements = saju.get('elements', {})
        if not isinstance(elements, dict):
            return {}
        if 'distribution' in elements:
            elements = elements['distribution']
        # 숫자 값만 필터링
        return {k: v for k, v in elements.items() if isinstance(v, (int, float))}
    
    def calculate_compatibility(self, saju1: Dict, saju2: Dict,
                               relationship_type: str = "부모자녀") -> FamilyCompatibilityResult:
        """가족 궁합 계산"""
        # 기본 궁합 계산
        base_result = super().calculate_compatibility(saju1, saju2)
        
        # 가족 관계 특화 분석
        harmony_score = self._calculate_family_harmony(saju1, saju2, relationship_type)
        support_score = self._calculate_support_score(saju1, saju2, relationship_type)
        understanding_score = self._calculate_understanding_score(saju1, saju2)
        generational_balance = self._calculate_generational_balance(saju1, saju2, relationship_type)
        
        # 가족 역학 분석
        family_dynamics = self._analyze_family_dynamics(saju1, saju2, relationship_type)
        
        # 유대 요인 확인
        bonding_factors = self._identify_bonding_factors(
            base_result.element_analysis,
            base_result.pillar_analysis,
            relationship_type
        )
        
        # 치유 영역 확인
        healing_areas = self._identify_healing_areas(
            base_result.challenges,
            relationship_type
        )
        
        # 가족 특화 총점 계산
        total_score = self._calculate_family_total_score(
            base_result.element_balance_score,
            base_result.ten_gods_score,
            base_result.pillar_scores,
            harmony_score,
            support_score,
            understanding_score,
            generational_balance,
            relationship_type
        )
        
        # 가족 특화 조언 생성
        advice = self._generate_family_advice(
            relationship_type,
            family_dynamics,
            bonding_factors,
            healing_areas
        )
        
        return FamilyCompatibilityResult(
            total_score=total_score,
            level=self._determine_compatibility_level(total_score),
            element_balance_score=base_result.element_balance_score,
            ten_gods_score=base_result.ten_gods_score,
            pillar_scores=base_result.pillar_scores,
            element_analysis=base_result.element_analysis,
            ten_gods_analysis=base_result.ten_gods_analysis,
            pillar_analysis=base_result.pillar_analysis,
            strengths=base_result.strengths,
            challenges=base_result.challenges,
            advice=advice,
            special_combinations=base_result.special_combinations,
            warning_signs=base_result.warning_signs,
            harmony_score=harmony_score,
            support_score=support_score,
            understanding_score=understanding_score,
            generational_balance_score=generational_balance,
            family_dynamics=family_dynamics,
            relationship_type=relationship_type,
            bonding_factors=bonding_factors,
            healing_areas=healing_areas
        )
    
    def _calculate_family_harmony(self, saju1: Dict, saju2: Dict,
                                 relationship_type: str) -> float:
        """가족 조화 점수 계산"""
        score = 50
        
        # 관계 유형별 중요 요소
        if relationship_type == "부모자녀":
            # 시주 관계가 중요 (부모의 시주 = 자녀)
            hour1_branch = saju1.get('hour', {}).get('earthly', '')
            day2_branch = saju2.get('day', {}).get('earthly', '')
            
            if (hour1_branch, day2_branch) in self.earthly_branch_relations['육합']:
                score += 30
        
        elif relationship_type == "형제자매":
            # 월주 관계가 중요 (같은 부모)
            month1_branch = saju1.get('month', {}).get('earthly', '')
            month2_branch = saju2.get('month', {}).get('earthly', '')
            
            if month1_branch == month2_branch:
                score += 20
        
        # 오행 조화
        elements1 = self._get_clean_elements(saju1)
        elements2 = self._get_clean_elements(saju2)
        
        # 상생 관계면 조화로움
        for element in ['목', '화', '토', '금', '수']:
            if elements1.get(element, 0) > 0 and elements2.get(element, 0) > 0:
                score += 5
        
        return min(100, max(0, score))
    
    def _calculate_support_score(self, saju1: Dict, saju2: Dict,
                                relationship_type: str) -> float:
        """지원 점수 계산"""
        score = 50
        
        # 정인이 있으면 지원적
        supportive_gods = ['정인', '편인', '정관']
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        if ten_god_relation in supportive_gods:
            score += 25
        
        # 부모자녀 관계에서 부모가 자녀를 생하는 오행
        if relationship_type == "부모자녀":
            elements1 = self._get_clean_elements(saju1)
            elements2 = self._get_clean_elements(saju2)
            
            dominant1 = max(elements1.items(), key=lambda x: x[1])[0] if elements1 else None
            dominant2 = max(elements2.items(), key=lambda x: x[1])[0] if elements2 else None
            
            if dominant1 and dominant2:
                if self.element_relations[dominant1]['generates'] == dominant2:
                    score += 20  # 부모가 자녀를 생함
        
        return min(100, max(0, score))
    
    def _calculate_understanding_score(self, saju1: Dict, saju2: Dict) -> float:
        """이해 점수 계산"""
        score = 50
        
        # 수(水) 오행 - 이해와 포용
        water1 = saju1.get('elements', {}).get('수', 0)
        water2 = saju2.get('elements', {}).get('수', 0)
        if water1 > 0 and water2 > 0:
            score += 20
        
        # 천간합이 있으면 이해 관계
        harmony_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            stem1 = saju1.get(pillar, {}).get('heavenly', '')
            stem2 = saju2.get(pillar, {}).get('heavenly', '')
            if (stem1, stem2) in self.heavenly_stem_relations['합']:
                harmony_count += 1
        
        score += harmony_count * 10
        
        return min(100, max(0, score))
    
    def _calculate_generational_balance(self, saju1: Dict, saju2: Dict,
                                       relationship_type: str) -> float:
        """세대 균형 점수 계산"""
        score = 50
        
        if relationship_type == "부모자녀":
            # 년주 차이 확인 (세대 차이)
            year1_branch = saju1.get('year', {}).get('earthly', '')
            year2_branch = saju2.get('year', {}).get('earthly', '')
            
            # 삼합이면 세대 조화
            for triple, element in self.earthly_branch_relations['삼합'].items():
                if year1_branch in triple and year2_branch in triple:
                    score += 25
                    break
        
        elif relationship_type == "형제자매":
            # 년주가 같거나 비슷하면 좋음
            year1_branch = saju1.get('year', {}).get('earthly', '')
            year2_branch = saju2.get('year', {}).get('earthly', '')
            
            if year1_branch == year2_branch:
                score += 30
        
        return min(100, max(0, score))
    
    def _analyze_family_dynamics(self, saju1: Dict, saju2: Dict,
                                relationship_type: str) -> str:
        """가족 역학 분석"""
        # 십성 관계로 가족 역학 판단
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        
        if relationship_type == "부모자녀":
            dynamics_map = {
                '정인': '자애로운 부모와 효성스러운 자녀',
                '편인': '독특한 교육 방식의 부모',
                '정관': '엄격하지만 사랑 깊은 관계',
                '편관': '자유로운 교육 스타일',
                '식신': '화목하고 즐거운 가족'
            }
        elif relationship_type == "형제자매":
            dynamics_map = {
                '비견': '평등하고 협력적인 형제',
                '겁재': '경쟁적이지만 성장하는 관계',
                '정인': '서로 돌보는 형제',
                '식신': '즐겁고 유쾌한 형제'
            }
        else:
            dynamics_map = {}
        
        return dynamics_map.get(ten_god_relation, f"일반적인 {relationship_type} 관계")
    
    def _identify_bonding_factors(self, element_analysis: Dict,
                                 pillar_analysis: Dict,
                                 relationship_type: str) -> List[str]:
        """유대 요인 확인"""
        factors = []
        
        # 오행 상생
        if element_analysis.get('generating_score', 0) > 15:
            factors.append("자연스러운 오행 상생 관계")
        
        # 관계별 특별 요인
        if relationship_type == "부모자녀":
            hour_analysis = pillar_analysis.get('hour', {})
            if hour_analysis.get('earthly_relation') == '육합':
                factors.append("부모의 시주와 자녀의 조화")
        
        elif relationship_type == "형제자매":
            month_analysis = pillar_analysis.get('month', {})
            if month_analysis.get('earthly_relation') == '육합':
                factors.append("형제간 깊은 정서적 유대")
        
        # 천간합
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('heavenly_relation') == '천간합':
            factors.append("자연스러운 친밀감")
        
        return factors[:4]
    
    def _identify_healing_areas(self, challenges: List[str],
                               relationship_type: str) -> List[str]:
        """치유 영역 확인"""
        areas = []
        
        for challenge in challenges:
            if "충" in challenge:
                areas.append("세대 갈등 치유 필요")
            if "형" in challenge:
                areas.append("과거 상처 치유 필요")
        
        # 관계별 치유 영역
        if relationship_type == "부모자녀":
            areas.append("세대 간 소통 개선")
        elif relationship_type == "형제자매":
            areas.append("경쟁심 해소와 협력")
        
        return areas[:4]
    
    def _calculate_family_total_score(self, element_score: float, ten_gods_score: float,
                                     pillar_scores: Dict[str, float], harmony: float,
                                     support: float, understanding: float,
                                     generational: float, relationship_type: str) -> float:
        """가족 궁합 총점 계산"""
        # 관계 유형별 가중치
        if relationship_type == "부모자녀":
            weights = {
                'element': 0.10,
                'ten_gods': 0.10,
                'year': 0.10,  # 세대
                'month': 0.05,
                'day': 0.10,
                'hour': 0.15,  # 부모 시주 중요
                'harmony': 0.15,
                'support': 0.10,
                'understanding': 0.10,
                'generational': 0.05
            }
        elif relationship_type == "형제자매":
            weights = {
                'element': 0.10,
                'ten_gods': 0.10,
                'year': 0.10,
                'month': 0.20,  # 형제는 월주 중요
                'day': 0.10,
                'hour': 0.05,
                'harmony': 0.15,
                'support': 0.05,
                'understanding': 0.10,
                'generational': 0.05
            }
        else:
            # 기본 가중치
            weights = {
                'element': 0.15,
                'ten_gods': 0.15,
                'year': 0.10,
                'month': 0.10,
                'day': 0.10,
                'hour': 0.10,
                'harmony': 0.10,
                'support': 0.10,
                'understanding': 0.05,
                'generational': 0.05
            }
        
        total = (
            element_score * weights['element'] +
            ten_gods_score * weights['ten_gods'] +
            pillar_scores.get('year', 50) * weights['year'] +
            pillar_scores.get('month', 50) * weights['month'] +
            pillar_scores.get('day', 50) * weights['day'] +
            pillar_scores.get('hour', 50) * weights['hour'] +
            harmony * weights['harmony'] +
            support * weights['support'] +
            understanding * weights['understanding'] +
            generational * weights['generational']
        )
        
        return round(total, 2)
    
    def _generate_family_advice(self, relationship_type: str, dynamics: str,
                               bonding_factors: List[str], healing_areas: List[str]) -> List[str]:
        """가족 특화 조언 생성"""
        advice = []
        
        # 관계 유형별 조언
        if relationship_type == "부모자녀":
            advice.append("자녀의 개성을 인정하고 지지해주세요")
            advice.append("세대 차이를 이해하고 소통하세요")
        elif relationship_type == "형제자매":
            advice.append("서로의 다름을 인정하고 존중하세요")
            advice.append("경쟁보다는 협력을 추구하세요")
        
        # 가족 역학 기반 조언
        advice.append(f"{dynamics}의 특성을 이해하세요")
        
        # 유대 요인 활용
        if bonding_factors:
            advice.append(f"'{bonding_factors[0]}'를 통해 관계를 강화하세요")
        
        # 치유 영역 대응
        if healing_areas:
            advice.append(f"'{healing_areas[0]}'에 집중하여 관계를 개선하세요")
        
        # 일반 가족 조언
        advice.append("정기적인 가족 시간을 가지세요")
        advice.append("서로에 대한 감사를 표현하세요")
        
        return advice[:7]