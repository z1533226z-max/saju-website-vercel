#!/usr/bin/env python3
"""
Saju Compatibility Calculator
두 사주 간의 궁합을 계산하는 시스템
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import math


class CompatibilityLevel(Enum):
    """궁합 수준 정의"""
    EXCELLENT = "천생연분"
    VERY_GOOD = "매우 좋음"
    GOOD = "좋음"
    AVERAGE = "보통"
    CHALLENGING = "노력 필요"
    DIFFICULT = "어려움"
    VERY_DIFFICULT = "매우 어려움"


@dataclass
class CompatibilityResult:
    """궁합 분석 결과"""
    total_score: float  # 0-100
    level: CompatibilityLevel
    
    # 세부 점수
    element_balance_score: float  # 오행 균형 점수
    ten_gods_score: float  # 십성 관계 점수
    pillar_scores: Dict[str, float]  # 각 주별 점수
    
    # 세부 분석
    element_analysis: Dict[str, any]
    ten_gods_analysis: Dict[str, any]
    pillar_analysis: Dict[str, any]
    
    # 조언
    strengths: List[str]
    challenges: List[str]
    advice: List[str]
    
    # 특별 궁합
    special_combinations: List[str]
    warning_signs: List[str]


class CompatibilityCalculator:
    """사주 궁합 계산기"""
    
    def __init__(self):
        """초기화"""
        # 오행 상생상극 관계
        self.element_relations = {
            '목': {'generates': '화', 'controls': '토', 'generated_by': '수', 'controlled_by': '금'},
            '화': {'generates': '토', 'controls': '금', 'generated_by': '목', 'controlled_by': '수'},
            '토': {'generates': '금', 'controls': '수', 'generated_by': '화', 'controlled_by': '목'},
            '금': {'generates': '수', 'controls': '목', 'generated_by': '토', 'controlled_by': '화'},
            '수': {'generates': '목', 'controls': '화', 'generated_by': '금', 'controlled_by': '토'}
        }
        
        # 천간 합충 관계
        self.heavenly_stem_relations = {
            '합': {
                ('갑', '기'): '토',  # 갑기합토
                ('을', '경'): '금',  # 을경합금
                ('병', '신'): '수',  # 병신합수
                ('정', '임'): '목',  # 정임합목
                ('무', '계'): '화'   # 무계합화
            },
            '충': {
                ('갑', '경'), ('을', '신'), ('병', '임'), ('정', '계'), ('무', '갑'),
                ('기', '을'), ('경', '병'), ('신', '정'), ('임', '무'), ('계', '기')
            }
        }
        
        # 지지 합충형해파 관계
        self.earthly_branch_relations = {
            '삼합': {
                ('인', '오', '술'): '화',  # 인오술 삼합화
                ('사', '유', '축'): '금',  # 사유축 삼합금
                ('신', '자', '진'): '수',  # 신자진 삼합수
                ('해', '묘', '미'): '목'   # 해묘미 삼합목
            },
            '육합': {
                ('자', '축'): '토', ('인', '해'): '목', ('묘', '술'): '화',
                ('진', '유'): '금', ('사', '신'): '수', ('오', '미'): '토'
            },
            '충': {
                ('자', '오'), ('축', '미'), ('인', '신'), 
                ('묘', '유'), ('진', '술'), ('사', '해')
            },
            '형': {
                ('인', '사', '신'),  # 무은지형
                ('축', '술', '미'),  # 무례지형
                ('자', '묘')         # 무례지형
            },
            '해': {
                ('자', '미'), ('축', '오'), ('인', '사'),
                ('묘', '진'), ('신', '해'), ('유', '술')
            },
            '파': {
                ('자', '유'), ('오', '묘'), ('사', '신'), ('해', '인')
            }
        }
        
        # 십성 궁합 관계 (일간 기준)
        self.ten_gods_compatibility = {
            '정관': {
                'good': ['정재', '정인', '식신'],
                'neutral': ['편재', '편인', '비견'],
                'challenging': ['편관', '상관', '겁재']
            },
            '편관': {
                'good': ['편재', '편인', '상관'],
                'neutral': ['정재', '정인', '식신'],
                'challenging': ['정관', '비견', '겁재']
            },
            '정인': {
                'good': ['정관', '편관', '비견'],
                'neutral': ['겁재', '식신', '상관'],
                'challenging': ['정재', '편재', '편인']
            },
            '편인': {
                'good': ['편관', '정관', '겁재'],
                'neutral': ['비견', '식신', '상관'],
                'challenging': ['편재', '정재', '정인']
            },
            '정재': {
                'good': ['식신', '정관', '비견'],
                'neutral': ['상관', '편관', '겁재'],
                'challenging': ['정인', '편인', '편재']
            },
            '편재': {
                'good': ['상관', '편관', '겁재'],
                'neutral': ['식신', '정관', '비견'],
                'challenging': ['편인', '정인', '정재']
            },
            '비견': {
                'good': ['정인', '편인', '식신'],
                'neutral': ['정관', '정재', '상관'],
                'challenging': ['편관', '편재', '겁재']
            },
            '겁재': {
                'good': ['편인', '정인', '상관'],
                'neutral': ['편관', '편재', '식신'],
                'challenging': ['정관', '정재', '비견']
            },
            '식신': {
                'good': ['정재', '비견', '정인'],
                'neutral': ['편재', '겁재', '편인'],
                'challenging': ['정관', '편관', '상관']
            },
            '상관': {
                'good': ['편재', '겁재', '편인'],
                'neutral': ['정재', '비견', '정인'],
                'challenging': ['편관', '정관', '식신']
            }
        }
    
    def calculate_compatibility(self, saju1: Dict, saju2: Dict) -> CompatibilityResult:
        """
        두 사주 간의 궁합 계산
        
        Args:
            saju1: 첫 번째 사람의 사주
            saju2: 두 번째 사람의 사주
            
        Returns:
            CompatibilityResult: 궁합 분석 결과
        """
        # 1. 오행 균형 궁합도 계산
        element_balance_score, element_analysis = self._calculate_element_balance(saju1, saju2)
        
        # 2. 십성 관계 궁합도 계산
        ten_gods_score, ten_gods_analysis = self._calculate_ten_gods_compatibility(saju1, saju2)
        
        # 3. 각 주별 궁합도 계산
        pillar_scores, pillar_analysis = self._calculate_pillar_compatibility(saju1, saju2)
        
        # 4. 특별 조합 확인
        special_combinations = self._check_special_combinations(saju1, saju2)
        
        # 5. 경고 신호 확인
        warning_signs = self._check_warning_signs(saju1, saju2)
        
        # 6. 종합 점수 계산 (가중 평균)
        total_score = self._calculate_total_score(
            element_balance_score,
            ten_gods_score,
            pillar_scores
        )
        
        # 7. 궁합 수준 결정
        level = self._determine_compatibility_level(total_score)
        
        # 8. 강점과 도전 과제 분석
        strengths = self._analyze_strengths(
            element_analysis, ten_gods_analysis, pillar_analysis, special_combinations
        )
        challenges = self._analyze_challenges(
            element_analysis, ten_gods_analysis, pillar_analysis, warning_signs
        )
        
        # 9. 조언 생성
        advice = self._generate_advice(
            level, strengths, challenges, element_analysis, ten_gods_analysis
        )
        
        return CompatibilityResult(
            total_score=total_score,
            level=level,
            element_balance_score=element_balance_score,
            ten_gods_score=ten_gods_score,
            pillar_scores=pillar_scores,
            element_analysis=element_analysis,
            ten_gods_analysis=ten_gods_analysis,
            pillar_analysis=pillar_analysis,
            strengths=strengths,
            challenges=challenges,
            advice=advice,
            special_combinations=special_combinations,
            warning_signs=warning_signs
        )
    
    def _calculate_element_balance(self, saju1: Dict, saju2: Dict) -> Tuple[float, Dict]:
        """오행 균형 궁합도 계산"""
        analysis = {}
        
        # 각자의 오행 분포 가져오기
        elements1 = saju1.get('elements', {})
        elements2 = saju2.get('elements', {})
        
        # elements가 dict가 아닌 경우 처리
        if not isinstance(elements1, dict):
            elements1 = {}
        if not isinstance(elements2, dict):
            elements2 = {}
        
        # elements에 'total'이나 'distribution' 키가 있는 경우 처리
        if 'distribution' in elements1:
            elements1 = elements1['distribution']
        if 'distribution' in elements2:
            elements2 = elements2['distribution']
        
        # 오행별 보완 관계 분석
        complementary_score = 0
        harmony_score = 0
        
        for element in ['목', '화', '토', '금', '수']:
            # 값이 dict인 경우 count 추출
            val1 = elements1.get(element, 0)
            val2 = elements2.get(element, 0)
            count1 = val1 if isinstance(val1, (int, float)) else 0
            count2 = val2 if isinstance(val2, (int, float)) else 0
            
            # 서로 부족한 오행을 보완하는지 확인
            if count1 == 0 and count2 > 0:
                complementary_score += 10
            elif count2 == 0 and count1 > 0:
                complementary_score += 10
            
            # 오행 균형 조화도
            diff = abs(count1 - count2)
            if diff == 0:
                harmony_score += 10
            elif diff == 1:
                harmony_score += 7
            elif diff == 2:
                harmony_score += 4
            else:
                harmony_score += 1
        
        # 상생 관계 확인
        generating_score = 0
        
        # 안전한 dominant element 계산
        clean_elements1 = {k: v for k, v in elements1.items() if isinstance(v, (int, float))}
        clean_elements2 = {k: v for k, v in elements2.items() if isinstance(v, (int, float))}
        
        dominant_element1 = max(clean_elements1.items(), key=lambda x: x[1])[0] if clean_elements1 else None
        dominant_element2 = max(clean_elements2.items(), key=lambda x: x[1])[0] if clean_elements2 else None
        
        if dominant_element1 and dominant_element2:
            if self.element_relations[dominant_element1]['generates'] == dominant_element2:
                generating_score = 20
                analysis['relationship'] = f"{dominant_element1}이(가) {dominant_element2}을(를) 생함"
            elif self.element_relations[dominant_element2]['generates'] == dominant_element1:
                generating_score = 20
                analysis['relationship'] = f"{dominant_element2}이(가) {dominant_element1}을(를) 생함"
            elif self.element_relations[dominant_element1]['controls'] == dominant_element2:
                generating_score = -10
                analysis['relationship'] = f"{dominant_element1}이(가) {dominant_element2}을(를) 극함"
            elif self.element_relations[dominant_element2]['controls'] == dominant_element1:
                generating_score = -10
                analysis['relationship'] = f"{dominant_element2}이(가) {dominant_element1}을(를) 극함"
            else:
                generating_score = 10
                analysis['relationship'] = "중립적 관계"
        
        # 최종 점수 계산
        total = min(100, max(0, complementary_score + harmony_score + generating_score))
        
        analysis['complementary_score'] = complementary_score
        analysis['harmony_score'] = harmony_score
        analysis['generating_score'] = generating_score
        analysis['elements1'] = elements1
        analysis['elements2'] = elements2
        
        return total, analysis
    
    def _calculate_ten_gods_compatibility(self, saju1: Dict, saju2: Dict) -> Tuple[float, Dict]:
        """십성 관계 궁합도 계산"""
        analysis = {}
        score = 50  # 기본 점수
        
        # 일간 가져오기
        day_stem1 = saju1.get('day', {}).get('heavenly', '')
        day_stem2 = saju2.get('day', {}).get('heavenly', '')
        
        if not day_stem1 or not day_stem2:
            return score, analysis
        
        # 일간 간의 십성 관계 계산
        ten_god_relation = self._get_ten_god_relation(day_stem1, day_stem2)
        analysis['main_relation'] = ten_god_relation
        
        # 십성 관계에 따른 점수 조정
        compatibility_adjustments = {
            '정관-정재': 20, '편관-편재': 15,
            '정인-정관': 15, '편인-편관': 12,
            '식신-정재': 18, '상관-편재': 10,
            '비견-비견': 8, '겁재-겁재': 5,
            '정관-편관': -10, '정재-편재': -5,
            '정인-편인': -5, '식신-상관': -8
        }
        
        # 관계 점수 조정
        for relation_pair, adjustment in compatibility_adjustments.items():
            if ten_god_relation in relation_pair:
                score += adjustment
                break
        
        # 각 주의 천간 간 합충 관계 확인
        pillars = ['year', 'month', 'day', 'hour']
        harmony_count = 0
        conflict_count = 0
        
        for pillar in pillars:
            stem1 = saju1.get(pillar, {}).get('heavenly', '')
            stem2 = saju2.get(pillar, {}).get('heavenly', '')
            
            if stem1 and stem2:
                # 천간합 확인
                if (stem1, stem2) in self.heavenly_stem_relations['합'] or \
                   (stem2, stem1) in self.heavenly_stem_relations['합']:
                    harmony_count += 1
                    score += 5
                
                # 천간충 확인
                if (stem1, stem2) in self.heavenly_stem_relations['충'] or \
                   (stem2, stem1) in self.heavenly_stem_relations['충']:
                    conflict_count += 1
                    score -= 5
        
        analysis['harmony_count'] = harmony_count
        analysis['conflict_count'] = conflict_count
        
        return min(100, max(0, score)), analysis
    
    def _calculate_pillar_compatibility(self, saju1: Dict, saju2: Dict) -> Tuple[Dict[str, float], Dict]:
        """각 주별 궁합도 계산"""
        pillar_scores = {}
        pillar_analysis = {}
        
        pillar_weights = {
            'year': 0.15,   # 연주 - 가문, 조상
            'month': 0.25,  # 월주 - 부모, 형제
            'day': 0.40,    # 일주 - 자신, 배우자
            'hour': 0.20    # 시주 - 자녀, 미래
        }
        
        for pillar_name in ['year', 'month', 'day', 'hour']:
            score = 50  # 기본 점수
            analysis = {}
            
            # 천간 비교
            stem1 = saju1.get(pillar_name, {}).get('heavenly', '')
            stem2 = saju2.get(pillar_name, {}).get('heavenly', '')
            
            if stem1 and stem2:
                # 천간합 확인
                if (stem1, stem2) in self.heavenly_stem_relations['합'] or \
                   (stem2, stem1) in self.heavenly_stem_relations['합']:
                    score += 25
                    analysis['heavenly_relation'] = '천간합'
                # 천간충 확인
                elif (stem1, stem2) in self.heavenly_stem_relations['충'] or \
                     (stem2, stem1) in self.heavenly_stem_relations['충']:
                    score -= 20
                    analysis['heavenly_relation'] = '천간충'
                else:
                    analysis['heavenly_relation'] = '평화'
            
            # 지지 비교
            branch1 = saju1.get(pillar_name, {}).get('earthly', '')
            branch2 = saju2.get(pillar_name, {}).get('earthly', '')
            
            if branch1 and branch2:
                # 육합 확인
                if (branch1, branch2) in self.earthly_branch_relations['육합'] or \
                   (branch2, branch1) in self.earthly_branch_relations['육합']:
                    score += 30
                    analysis['earthly_relation'] = '육합'
                # 충 확인
                elif (branch1, branch2) in self.earthly_branch_relations['충'] or \
                     (branch2, branch1) in self.earthly_branch_relations['충']:
                    score -= 25
                    analysis['earthly_relation'] = '충'
                # 형 확인
                elif self._check_punishment(branch1, branch2):
                    score -= 15
                    analysis['earthly_relation'] = '형'
                # 해 확인
                elif (branch1, branch2) in self.earthly_branch_relations['해'] or \
                     (branch2, branch1) in self.earthly_branch_relations['해']:
                    score -= 10
                    analysis['earthly_relation'] = '해'
                # 파 확인
                elif (branch1, branch2) in self.earthly_branch_relations['파'] or \
                     (branch2, branch1) in self.earthly_branch_relations['파']:
                    score -= 8
                    analysis['earthly_relation'] = '파'
                else:
                    analysis['earthly_relation'] = '평화'
            
            pillar_scores[pillar_name] = min(100, max(0, score))
            pillar_analysis[pillar_name] = analysis
        
        return pillar_scores, pillar_analysis
    
    def _check_punishment(self, branch1: str, branch2: str) -> bool:
        """형 관계 확인"""
        for punishment_group in self.earthly_branch_relations['형']:
            if branch1 in punishment_group and branch2 in punishment_group:
                return True
        return False
    
    def _check_special_combinations(self, saju1: Dict, saju2: Dict) -> List[str]:
        """특별한 궁합 조합 확인"""
        special = []
        
        # 일주 천간지지가 모두 합하는 경우
        day1_stem = saju1.get('day', {}).get('heavenly', '')
        day2_stem = saju2.get('day', {}).get('heavenly', '')
        day1_branch = saju1.get('day', {}).get('earthly', '')
        day2_branch = saju2.get('day', {}).get('earthly', '')
        
        if day1_stem and day2_stem and day1_branch and day2_branch:
            stem_harmony = (day1_stem, day2_stem) in self.heavenly_stem_relations['합'] or \
                          (day2_stem, day1_stem) in self.heavenly_stem_relations['합']
            branch_harmony = (day1_branch, day2_branch) in self.earthly_branch_relations['육합'] or \
                           (day2_branch, day1_branch) in self.earthly_branch_relations['육합']
            
            if stem_harmony and branch_harmony:
                special.append("천생연분 - 일주 천간지지 완전합")
        
        # 삼합 확인
        branches1 = [saju1.get(p, {}).get('earthly', '') for p in ['year', 'month', 'day', 'hour']]
        branches2 = [saju2.get(p, {}).get('earthly', '') for p in ['year', 'month', 'day', 'hour']]
        all_branches = set(branches1 + branches2)
        
        for triple, element in self.earthly_branch_relations['삼합'].items():
            if all(branch in all_branches for branch in triple):
                special.append(f"삼합 {element}국 형성")
        
        # 연월일시 모든 천간이 합하는 경우
        all_harmony = True
        for pillar in ['year', 'month', 'day', 'hour']:
            stem1 = saju1.get(pillar, {}).get('heavenly', '')
            stem2 = saju2.get(pillar, {}).get('heavenly', '')
            if stem1 and stem2:
                if not ((stem1, stem2) in self.heavenly_stem_relations['합'] or \
                        (stem2, stem1) in self.heavenly_stem_relations['합']):
                    all_harmony = False
                    break
        
        if all_harmony:
            special.append("사주 전체 천간합 - 매우 드문 인연")
        
        return special
    
    def _check_warning_signs(self, saju1: Dict, saju2: Dict) -> List[str]:
        """경고 신호 확인"""
        warnings = []
        
        # 일주 충 확인
        day1_branch = saju1.get('day', {}).get('earthly', '')
        day2_branch = saju2.get('day', {}).get('earthly', '')
        
        if day1_branch and day2_branch:
            if (day1_branch, day2_branch) in self.earthly_branch_relations['충'] or \
               (day2_branch, day1_branch) in self.earthly_branch_relations['충']:
                warnings.append("일지충 - 배우자궁 충돌")
        
        # 다중 충 확인
        conflict_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if branch1 and branch2:
                if (branch1, branch2) in self.earthly_branch_relations['충'] or \
                   (branch2, branch1) in self.earthly_branch_relations['충']:
                    conflict_count += 1
        
        if conflict_count >= 3:
            warnings.append(f"다중충 ({conflict_count}개) - 잦은 충돌 가능성")
        
        # 형살 확인
        punishment_count = 0
        for pillar in ['year', 'month', 'day', 'hour']:
            branch1 = saju1.get(pillar, {}).get('earthly', '')
            branch2 = saju2.get(pillar, {}).get('earthly', '')
            if branch1 and branch2:
                if self._check_punishment(branch1, branch2):
                    punishment_count += 1
        
        if punishment_count >= 2:
            warnings.append(f"다중형 ({punishment_count}개) - 갈등과 시련")
        
        # 오행 극 관계 확인
        elements1 = saju1.get('elements', {})
        elements2 = saju2.get('elements', {})
        
        # elements가 dict가 아닌 경우 처리
        if not isinstance(elements1, dict):
            elements1 = {}
        if not isinstance(elements2, dict):
            elements2 = {}
        
        # elements에 'distribution' 키가 있는 경우 처리
        if 'distribution' in elements1:
            elements1 = elements1['distribution']
        if 'distribution' in elements2:
            elements2 = elements2['distribution']
        
        if elements1 and elements2:
            # 안전한 dominant element 계산
            clean_elements1 = {k: v for k, v in elements1.items() if isinstance(v, (int, float))}
            clean_elements2 = {k: v for k, v in elements2.items() if isinstance(v, (int, float))}
            
            dominant1 = max(clean_elements1.items(), key=lambda x: x[1])[0] if clean_elements1 else None
            dominant2 = max(clean_elements2.items(), key=lambda x: x[1])[0] if clean_elements2 else None
            
            if dominant1 and dominant2:
                if self.element_relations[dominant1]['controls'] == dominant2:
                    warnings.append(f"{dominant1}이(가) {dominant2}을(를) 극함 - 일방적 관계 주의")
                elif self.element_relations[dominant2]['controls'] == dominant1:
                    warnings.append(f"{dominant2}이(가) {dominant1}을(를) 극함 - 일방적 관계 주의")
        
        return warnings
    
    def _calculate_total_score(self, element_score: float, ten_gods_score: float,
                               pillar_scores: Dict[str, float]) -> float:
        """종합 점수 계산"""
        # 가중치
        weights = {
            'element': 0.25,
            'ten_gods': 0.20,
            'year': 0.10,
            'month': 0.10,
            'day': 0.25,  # 일주가 가장 중요
            'hour': 0.10
        }
        
        total = (
            element_score * weights['element'] +
            ten_gods_score * weights['ten_gods'] +
            pillar_scores.get('year', 50) * weights['year'] +
            pillar_scores.get('month', 50) * weights['month'] +
            pillar_scores.get('day', 50) * weights['day'] +
            pillar_scores.get('hour', 50) * weights['hour']
        )
        
        return round(total, 2)
    
    def _determine_compatibility_level(self, score: float) -> CompatibilityLevel:
        """궁합 수준 결정"""
        if score >= 85:
            return CompatibilityLevel.EXCELLENT
        elif score >= 75:
            return CompatibilityLevel.VERY_GOOD
        elif score >= 65:
            return CompatibilityLevel.GOOD
        elif score >= 50:
            return CompatibilityLevel.AVERAGE
        elif score >= 40:
            return CompatibilityLevel.CHALLENGING
        elif score >= 30:
            return CompatibilityLevel.DIFFICULT
        else:
            return CompatibilityLevel.VERY_DIFFICULT
    
    def _get_ten_god_relation(self, stem1: str, stem2: str) -> str:
        """두 천간 사이의 십성 관계 계산"""
        # 간단한 구현 - 실제로는 더 복잡한 계산 필요
        stem_elements = {
            '갑': '목', '을': '목', '병': '화', '정': '화',
            '무': '토', '기': '토', '경': '금', '신': '금',
            '임': '수', '계': '수'
        }
        
        element1 = stem_elements.get(stem1, '')
        element2 = stem_elements.get(stem2, '')
        
        if not element1 or not element2:
            return "불명"
        
        # 관계 판단 (간단한 버전)
        if element1 == element2:
            return "비견"
        elif self.element_relations[element1]['generates'] == element2:
            return "식신"
        elif self.element_relations[element1]['controls'] == element2:
            return "정재"
        elif self.element_relations[element2]['generates'] == element1:
            return "정인"
        elif self.element_relations[element2]['controls'] == element1:
            return "정관"
        else:
            return "중립"
    
    def _analyze_strengths(self, element_analysis: Dict, ten_gods_analysis: Dict,
                          pillar_analysis: Dict, special_combinations: List[str]) -> List[str]:
        """강점 분석"""
        strengths = []
        
        # 오행 균형 강점
        if element_analysis.get('complementary_score', 0) >= 20:
            strengths.append("서로의 부족한 오행을 보완하는 관계")
        if element_analysis.get('generating_score', 0) >= 15:
            strengths.append("오행 상생 관계로 서로를 돕는 관계")
        
        # 십성 관계 강점
        if ten_gods_analysis.get('harmony_count', 0) >= 2:
            strengths.append("천간합이 많아 조화로운 관계")
        
        # 일주 궁합 강점
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('heavenly_relation') == '천간합':
            strengths.append("일간이 합하여 강한 인연")
        if day_analysis.get('earthly_relation') == '육합':
            strengths.append("일지가 합하여 안정적인 관계")
        
        # 특별 조합 강점
        strengths.extend(special_combinations)
        
        return strengths[:5]  # 상위 5개만
    
    def _analyze_challenges(self, element_analysis: Dict, ten_gods_analysis: Dict,
                           pillar_analysis: Dict, warning_signs: List[str]) -> List[str]:
        """도전 과제 분석"""
        challenges = []
        
        # 오행 불균형 도전
        if element_analysis.get('generating_score', 0) <= -10:
            challenges.append("오행 상극 관계로 갈등 가능성")
        
        # 십성 관계 도전
        if ten_gods_analysis.get('conflict_count', 0) >= 2:
            challenges.append("천간충이 많아 의견 충돌 가능")
        
        # 일주 궁합 도전
        day_analysis = pillar_analysis.get('day', {})
        if day_analysis.get('earthly_relation') == '충':
            challenges.append("일지충으로 인한 갈등 주의")
        
        # 경고 신호
        challenges.extend(warning_signs)
        
        return challenges[:5]  # 상위 5개만
    
    def _generate_advice(self, level: CompatibilityLevel, strengths: List[str],
                        challenges: List[str], element_analysis: Dict,
                        ten_gods_analysis: Dict) -> List[str]:
        """조언 생성"""
        advice = []
        
        # 수준별 기본 조언
        if level in [CompatibilityLevel.EXCELLENT, CompatibilityLevel.VERY_GOOD]:
            advice.append("천생연분에 가까운 관계입니다. 서로를 아끼고 존중하세요.")
        elif level in [CompatibilityLevel.GOOD, CompatibilityLevel.AVERAGE]:
            advice.append("좋은 인연입니다. 노력하면 더 좋은 관계가 될 수 있습니다.")
        else:
            advice.append("도전이 있는 관계입니다. 서로를 이해하려는 노력이 필요합니다.")
        
        # 오행 관련 조언
        if element_analysis.get('generating_score', 0) < 0:
            advice.append("상극 관계의 오행은 이해와 배려로 극복할 수 있습니다.")
        elif element_analysis.get('complementary_score', 0) >= 20:
            advice.append("서로 부족한 부분을 채워주는 관계로 발전시키세요.")
        
        # 충/합 관련 조언
        if ten_gods_analysis.get('conflict_count', 0) >= 2:
            advice.append("충돌이 있을 때는 대화와 타협으로 해결하세요.")
        if ten_gods_analysis.get('harmony_count', 0) >= 2:
            advice.append("좋은 합이 있으니 서로를 믿고 의지하세요.")
        
        # 도전 과제 극복 조언
        if "일지충" in str(challenges):
            advice.append("일지충은 서로 다른 가치관을 인정하면 극복됩니다.")
        if "다중충" in str(challenges):
            advice.append("잦은 충돌은 서로의 개성을 존중하면 줄어듭니다.")
        
        # 강점 활용 조언
        if "천생연분" in str(strengths):
            advice.append("매우 드문 좋은 인연이니 소중히 가꾸세요.")
        if "삼합" in str(strengths):
            advice.append("삼합의 에너지를 활용해 공동 목표를 세우세요.")
        
        return advice[:7]  # 상위 7개만