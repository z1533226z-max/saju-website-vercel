# -*- coding: utf-8 -*-
"""
Major Fortune (대운) Calculator for Saju Analysis
Calculates 10-year fortune periods based on birth information and gender
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import calendar


class ProgressionDirection(Enum):
    """Fortune progression direction"""
    FORWARD = "순행"  # 順行 - Forward progression
    REVERSE = "역행"  # 逆行 - Reverse progression


@dataclass
class MajorFortunePeriod:
    """Represents a 10-year major fortune period"""
    start_age: int
    end_age: int
    heavenly_stem: str
    earthly_branch: str
    combined_name: str
    element: str
    description: str
    fortune_themes: Dict[str, str]


class MajorFortuneCalculator:
    """
    Calculates Major Fortune (대운) periods for Saju analysis
    """
    
    def __init__(self):
        """Initialize the Major Fortune Calculator"""
        self.heavenly_stems = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
        self.earthly_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
        
        # 60 Jiazi cycle (60갑자)
        self.sixty_jiazi = self._generate_sixty_jiazi()
        
        # Branch relationships for harmony/conflict analysis
        self.branch_relations = self._initialize_branch_relations()
        
        # Element mapping for stems and branches
        self.stem_elements = {
            '갑': '목', '을': '목',
            '병': '화', '정': '화',
            '무': '토', '기': '토',
            '경': '금', '신': '금',
            '임': '수', '계': '수'
        }
        
        self.branch_elements = {
            '인': '목', '묘': '목',
            '사': '화', '오': '화',
            '진': '토', '술': '토', '축': '토', '미': '토',
            '신': '금', '유': '금',
            '해': '수', '자': '수'
        }
        
        # Yin/Yang polarity for stems
        self.stem_polarity = {
            '갑': 'yang', '병': 'yang', '무': 'yang', '경': 'yang', '임': 'yang',
            '을': 'yin', '정': 'yin', '기': 'yin', '신': 'yin', '계': 'yin'
        }
        
        # Fortune interpretation data
        self.fortune_interpretations = self._load_fortune_interpretations()
    
    def calculate_major_fortune_start(self, birth_date: datetime, birth_time: str, 
                                     month_pillar: Dict, year_stem: str, gender: str) -> Dict:
        """
        Calculate when major fortune periods start
        
        Args:
            birth_date: Birth date
            birth_time: Birth time as string (HH:MM)
            month_pillar: Month pillar from Saju
            year_stem: Year heavenly stem
            gender: 'male' or 'female'
            
        Returns:
            Dictionary with start age and progression direction
        """
        # Determine progression direction based on gender and year stem polarity
        direction = self._determine_progression_direction(year_stem, gender)
        
        # Calculate days to next/previous solar term
        days_to_term = self._calculate_days_to_solar_term(birth_date, direction)
        
        # Convert days to years (traditional formula: 3 days = 1 year)
        start_age = round(days_to_term / 3)
        
        # Minimum start age is 1
        if start_age < 1:
            start_age = 1
        
        return {
            'start_age': start_age,
            'direction': direction.value,
            'days_calculated': days_to_term,
            'calculation_method': '3일 = 1년 환산법'
        }
    
    def get_major_fortune_periods(self, saju: Dict, birth_date: datetime, 
                                 gender: str, current_age: Optional[int] = None) -> List[MajorFortunePeriod]:
        """
        Generate 10-year major fortune periods
        
        Args:
            saju: Complete Saju data
            birth_date: Birth date
            gender: 'male' or 'female'
            current_age: Current age (optional)
            
        Returns:
            List of MajorFortunePeriod objects
        """
        # Get month pillar and year stem
        month_pillar = saju.get('month', {})
        year_stem = saju.get('year', {}).get('heavenly', '')
        birth_time = saju.get('birth_info', {}).get('time', '00:00')
        
        # Calculate start age and direction
        fortune_info = self.calculate_major_fortune_start(
            birth_date, birth_time, month_pillar, year_stem, gender
        )
        
        start_age = fortune_info['start_age']
        direction = ProgressionDirection.FORWARD if fortune_info['direction'] == '순행' else ProgressionDirection.REVERSE
        
        # Get starting point from month pillar
        start_stem = month_pillar.get('heavenly', '갑')
        start_branch = month_pillar.get('earthly', '자')
        
        # Generate fortune periods
        periods = []
        for i in range(8):  # Generate 8 periods (80 years coverage)
            period_start_age = start_age + (i * 10)
            period_end_age = period_start_age + 9
            
            # Calculate stem and branch for this period
            if direction == ProgressionDirection.FORWARD:
                stem_idx = (self.heavenly_stems.index(start_stem) + i + 1) % 10
                branch_idx = (self.earthly_branches.index(start_branch) + i + 1) % 12
            else:
                stem_idx = (self.heavenly_stems.index(start_stem) - i - 1) % 10
                branch_idx = (self.earthly_branches.index(start_branch) - i - 1) % 12
            
            period_stem = self.heavenly_stems[stem_idx]
            period_branch = self.earthly_branches[branch_idx]
            
            # Create period object
            period = MajorFortunePeriod(
                start_age=period_start_age,
                end_age=period_end_age,
                heavenly_stem=period_stem,
                earthly_branch=period_branch,
                combined_name=f"{period_stem}{period_branch}",
                element=self._get_dominant_element(period_stem, period_branch),
                description=self._get_period_description(period_stem, period_branch),
                fortune_themes=self._get_fortune_themes(period_stem, period_branch)
            )
            
            periods.append(period)
        
        return periods
    
    def get_current_major_fortune(self, saju: Dict, birth_date: datetime, 
                                 gender: str, current_date: Optional[datetime] = None) -> Optional[MajorFortunePeriod]:
        """
        Get the current major fortune period
        
        Args:
            saju: Complete Saju data
            birth_date: Birth date
            gender: 'male' or 'female'
            current_date: Current date (defaults to today)
            
        Returns:
            Current MajorFortunePeriod or None
        """
        if current_date is None:
            current_date = datetime.now()
        
        # Calculate current age
        age = current_date.year - birth_date.year
        if current_date.month < birth_date.month or \
           (current_date.month == birth_date.month and current_date.day < birth_date.day):
            age -= 1
        
        # Get all periods
        periods = self.get_major_fortune_periods(saju, birth_date, gender, age)
        
        # Find current period
        for period in periods:
            if period.start_age <= age <= period.end_age:
                return period
        
        return None
    
    def _determine_progression_direction(self, year_stem: str, gender: str) -> ProgressionDirection:
        """
        Determine fortune progression direction based on gender and year stem polarity
        
        Rules:
        - Male + Yang year stem = Forward
        - Male + Yin year stem = Reverse
        - Female + Yang year stem = Reverse
        - Female + Yin year stem = Forward
        """
        year_polarity = self.stem_polarity.get(year_stem, 'yang')
        
        if gender == 'male':
            return ProgressionDirection.FORWARD if year_polarity == 'yang' else ProgressionDirection.REVERSE
        else:  # female
            return ProgressionDirection.REVERSE if year_polarity == 'yang' else ProgressionDirection.FORWARD
    
    def _calculate_days_to_solar_term(self, birth_date: datetime, direction: ProgressionDirection) -> int:
        """
        Calculate days to next or previous solar term
        
        Simplified calculation - in real implementation would need accurate solar term dates
        """
        # Solar terms occur approximately every 15 days
        # This is a simplified calculation
        day_of_month = birth_date.day
        
        if direction == ProgressionDirection.FORWARD:
            # Days to next solar term (around 5th or 20th of month)
            if day_of_month <= 5:
                days = 5 - day_of_month
            elif day_of_month <= 20:
                days = 20 - day_of_month
            else:
                days = 35 - day_of_month  # Next month's 5th
        else:
            # Days from previous solar term
            if day_of_month >= 20:
                days = day_of_month - 20
            elif day_of_month >= 5:
                days = day_of_month - 5
            else:
                days = day_of_month + 10  # From previous month's 20th
        
        return max(1, abs(days))
    
    def _get_dominant_element(self, stem: str, branch: str) -> str:
        """Get the dominant element of a stem-branch combination"""
        stem_elem = self.stem_elements.get(stem, '토')
        branch_elem = self.branch_elements.get(branch, '토')
        
        # If both are same, return that element
        if stem_elem == branch_elem:
            return stem_elem
        
        # Otherwise return stem element as dominant
        return stem_elem
    
    def _get_period_description(self, stem: str, branch: str) -> str:
        """Get description for a major fortune period"""
        element = self._get_dominant_element(stem, branch)
        
        descriptions = {
            '목': '성장과 발전의 시기, 새로운 시작과 확장',
            '화': '열정과 명예의 시기, 활발한 활동과 인정',
            '토': '안정과 축적의 시기, 기반 다지기와 실리 추구',
            '금': '결실과 정리의 시기, 성과 획득과 체계 정립',
            '수': '지혜와 유연함의 시기, 통찰력과 적응력 발휘'
        }
        
        return descriptions.get(element, '변화와 전환의 시기')
    
    def _get_fortune_themes(self, stem: str, branch: str) -> Dict[str, str]:
        """Get fortune themes for a period"""
        element = self._get_dominant_element(stem, branch)
        
        themes = {
            '목': {
                'career': '사업 확장, 승진, 새로운 도전',
                'wealth': '투자 수익, 사업 소득 증가',
                'health': '간과 눈 건강 주의, 스트레스 관리',
                'relationships': '새로운 만남, 인맥 확대',
                'overall': '진취적 기운, 성장 에너지'
            },
            '화': {
                'career': '명예 상승, 리더십 발휘, 공적 인정',
                'wealth': '명예를 통한 재물, 급격한 변동',
                'health': '심장과 혈액순환 주의, 과로 방지',
                'relationships': '열정적 만남, 활발한 교류',
                'overall': '화려한 성과, 주목받는 시기'
            },
            '토': {
                'career': '안정적 직장, 중재자 역할, 신뢰 구축',
                'wealth': '부동산 투자, 안정적 수입',
                'health': '소화기 건강, 체중 관리 필요',
                'relationships': '신뢰 기반 관계, 결혼 운',
                'overall': '안정과 균형, 실속 추구'
            },
            '금': {
                'career': '체계화, 전문성 강화, 권위 확립',
                'wealth': '저축과 절약, 계획적 재테크',
                'health': '호흡기와 피부 관리, 규칙적 생활',
                'relationships': '의리있는 관계, 장기적 유대',
                'overall': '결단력과 추진력, 원칙 중시'
            },
            '수': {
                'career': '창의적 활동, 유연한 대처, 소통 중시',
                'wealth': '유동적 자산, 다양한 수입원',
                'health': '신장과 방광 건강, 수분 섭취',
                'relationships': '지적 교류, 정신적 유대',
                'overall': '지혜와 통찰, 유연한 대응'
            }
        }
        
        return themes.get(element, {
            'career': '변화와 적응의 시기',
            'wealth': '신중한 관리 필요',
            'health': '건강 관리 중요',
            'relationships': '인간관계 재정립',
            'overall': '전환기적 흐름'
        })
    
    def _load_fortune_interpretations(self) -> Dict:
        """Load detailed fortune interpretation data"""
        return {
            '갑자': {
                'nature': '새로운 시작의 에너지',
                'positive': '창의력 발휘, 리더십 강화, 새로운 기회',
                'negative': '성급함, 인내심 부족, 충돌 가능성',
                'advice': '신중한 계획과 인내심을 가지고 추진하세요'
            },
            '을축': {
                'nature': '꾸준한 성장의 시기',
                'positive': '안정적 발전, 신뢰 구축, 실속 추구',
                'negative': '변화 저항, 고집, 융통성 부족',
                'advice': '유연성을 기르고 새로운 것을 받아들이세요'
            },
            # Add more combinations as needed
        }
    
    def analyze_fortune_transition(self, current_period: MajorFortunePeriod, 
                                  next_period: MajorFortunePeriod) -> Dict:
        """
        Analyze the transition between fortune periods
        
        Args:
            current_period: Current major fortune period
            next_period: Next major fortune period
            
        Returns:
            Analysis of the transition
        """
        current_elem = current_period.element
        next_elem = next_period.element
        
        # Check element relationship
        relationship = self._check_element_relationship(current_elem, next_elem)
        
        transition_analysis = {
            'current_period': f"{current_period.combined_name} ({current_period.start_age}-{current_period.end_age}세)",
            'next_period': f"{next_period.combined_name} ({next_period.start_age}-{next_period.end_age}세)",
            'element_transition': f"{current_elem} → {next_elem}",
            'relationship': relationship,
            'preparation_advice': self._get_transition_advice(current_elem, next_elem, relationship)
        }
        
        return transition_analysis
    
    def _check_element_relationship(self, elem1: str, elem2: str) -> str:
        """Check relationship between two elements"""
        generating = {
            '목': '화', '화': '토', '토': '금', '금': '수', '수': '목'
        }
        
        controlling = {
            '목': '토', '토': '수', '수': '화', '화': '금', '금': '목'
        }
        
        if elem1 == elem2:
            return '비화 (같은 오행)'
        elif generating.get(elem1) == elem2:
            return '상생 (생성하는 관계)'
        elif generating.get(elem2) == elem1:
            return '설기 (생성받는 관계)'
        elif controlling.get(elem1) == elem2:
            return '상극 (극하는 관계)'
        elif controlling.get(elem2) == elem1:
            return '상모 (극을 받는 관계)'
        else:
            return '무관 (직접 관계 없음)'
    
    def _get_transition_advice(self, current_elem: str, next_elem: str, relationship: str) -> str:
        """Get advice for transitioning between periods"""
        advice_map = {
            '상생': '자연스러운 발전이 예상됩니다. 현재의 성과가 다음 시기의 기반이 됩니다.',
            '설기': '에너지가 소모될 수 있습니다. 충분한 휴식과 재충전이 필요합니다.',
            '상극': '도전적인 전환기입니다. 변화에 대한 준비와 유연한 대응이 중요합니다.',
            '상모': '압박감을 느낄 수 있습니다. 스트레스 관리와 건강 관리에 신경쓰세요.',
            '비화': '비슷한 에너지가 지속됩니다. 매너리즘에 빠지지 않도록 주의하세요.',
            '무관': '새로운 국면으로의 전환입니다. 열린 마음으로 변화를 받아들이세요.'
        }
        
        return advice_map.get(relationship, '신중하게 다음 시기를 준비하세요.')
    
    def _generate_sixty_jiazi(self) -> List[Tuple[str, str]]:
        """Generate 60 Jiazi cycle combinations"""
        jiazi = []
        for i in range(60):
            stem_idx = i % 10
            branch_idx = i % 12
            jiazi.append((self.heavenly_stems[stem_idx], self.earthly_branches[branch_idx]))
        return jiazi
    
    def _initialize_branch_relations(self) -> Dict:
        """Initialize earthly branch relationships"""
        return {
            # 삼합 (Three Harmony)
            'harmony_three': [
                ['신', '자', '진'],  # 申子辰 - Water
                ['사', '유', '축'],  # 巳酉丑 - Metal
                ['인', '오', '술'],  # 寅午戌 - Fire
                ['해', '묘', '미']   # 亥卯未 - Wood
            ],
            # 육합 (Six Harmony)
            'harmony_six': {
                '자': '축', '축': '자',  # 子丑
                '인': '해', '해': '인',  # 寅亥
                '묘': '술', '술': '묘',  # 卯戌
                '진': '유', '유': '진',  # 辰酉
                '사': '신', '신': '사',  # 巳申
                '오': '미', '미': '오'   # 午未
            },
            # 충 (Conflict)
            'conflict': {
                '자': '오', '오': '자',  # 子午
                '축': '미', '미': '축',  # 丑未
                '인': '신', '신': '인',  # 寅申
                '묘': '유', '유': '묘',  # 卯酉
                '진': '술', '술': '진',  # 辰戌
                '사': '해', '해': '사'   # 巳亥
            },
            # 형 (Punishment)
            'punishment': {
                '자': '묘', '묘': '자',  # 子卯 - 무례지형
                '축': ['술', '미'], '술': ['축', '미'], '미': ['축', '술'],  # 丑戌未 - 무은지형
                '인': ['사', '신'], '사': ['인', '신'], '신': ['인', '사'],  # 寅巳申 - 무자비형
                '진': '진', '오': '오', '유': '유', '해': '해'  # 自刑
            },
            # 파 (Destruction)
            'destruction': {
                '자': '유', '유': '자',  # 子酉
                '오': '묘', '묘': '오',  # 午卯
                '신': '사', '사': '신',  # 申巳
                '해': '인', '인': '해',  # 亥寅
                '축': '진', '진': '축',  # 丑辰
                '술': '미', '미': '술'   # 戌未
            },
            # 해 (Harm)
            'harm': {
                '자': '미', '미': '자',  # 子未
                '축': '오', '오': '축',  # 丑午
                '인': '사', '사': '인',  # 寅巳
                '묘': '진', '진': '묘',  # 卯辰
                '신': '해', '해': '신',  # 申亥
                '유': '술', '술': '유'   # 酉戌
            }
        }
    
    def calculate_yearly_fortune(self, current_year: int, saju: Dict) -> Dict:
        """
        Calculate yearly fortune (세운) for a specific year
        
        Args:
            current_year: Year to calculate fortune for
            saju: Complete Saju data
            
        Returns:
            Yearly fortune analysis
        """
        # Calculate year's heavenly stem and earthly branch
        # Using 1984 (갑자년) as reference point
        reference_year = 1984  # 갑자년
        year_diff = current_year - reference_year
        
        # Get current year's stem and branch
        year_idx = year_diff % 60
        if year_idx < 0:
            year_idx += 60
        
        year_stem = self.sixty_jiazi[year_idx][0]
        year_branch = self.sixty_jiazi[year_idx][1]
        
        # Analyze relationships with personal Saju
        relationships = self._analyze_fortune_relationships(
            year_stem, year_branch, saju
        )
        
        # Get element and interpretation
        year_element = self._get_dominant_element(year_stem, year_branch)
        
        return {
            'year': current_year,
            'heavenly_stem': year_stem,
            'earthly_branch': year_branch,
            'combined_name': f"{year_stem}{year_branch}",
            'element': year_element,
            'relationships': relationships,
            'interpretation': self._interpret_yearly_fortune(
                year_stem, year_branch, year_element, relationships
            ),
            'advice': self._get_yearly_advice(relationships)
        }
    
    def calculate_monthly_fortune(self, year: int, month: int, saju: Dict) -> Dict:
        """
        Calculate monthly fortune (월운)
        
        Args:
            year: Year
            month: Month (1-12)
            saju: Complete Saju data
            
        Returns:
            Monthly fortune analysis
        """
        # Calculate month's stem and branch based on year stem
        year_stem_idx = self.heavenly_stems.index(
            self.calculate_yearly_fortune(year, saju)['heavenly_stem']
        )
        
        # Month stem calculation (based on year stem)
        # 갑기년: 병인월부터, 을경년: 무인월부터, etc.
        month_stem_start = {
            0: 2, 5: 2,  # 갑, 기
            1: 4, 6: 4,  # 을, 경
            2: 6, 7: 6,  # 병, 신
            3: 8, 8: 8,  # 정, 임
            4: 0, 9: 0   # 무, 계
        }
        
        stem_start_idx = month_stem_start.get(year_stem_idx % 5 * 2 + year_stem_idx // 5, 0)
        month_stem_idx = (stem_start_idx + month - 1) % 10
        month_stem = self.heavenly_stems[month_stem_idx]
        
        # Month branch (fixed by solar calendar)
        month_branches = ['인', '묘', '진', '사', '오', '미', '신', '유', '술', '해', '자', '축']
        month_branch = month_branches[month - 1] if 1 <= month <= 12 else '인'
        
        # Analyze relationships
        relationships = self._analyze_fortune_relationships(
            month_stem, month_branch, saju
        )
        
        month_element = self._get_dominant_element(month_stem, month_branch)
        
        return {
            'year': year,
            'month': month,
            'heavenly_stem': month_stem,
            'earthly_branch': month_branch,
            'combined_name': f"{month_stem}{month_branch}",
            'element': month_element,
            'relationships': relationships,
            'interpretation': self._interpret_monthly_fortune(
                month_stem, month_branch, month_element, relationships
            )
        }
    
    def calculate_daily_fortune(self, date: datetime, saju: Dict) -> Dict:
        """
        Calculate daily fortune (일운)
        
        Args:
            date: Date to calculate fortune for
            saju: Complete Saju data
            
        Returns:
            Daily fortune analysis
        """
        # Calculate day's stem and branch using 60-day cycle
        # Using a reference date for calculation
        reference_date = datetime(1984, 1, 1)  # 갑자일
        days_diff = (date - reference_date).days
        
        day_idx = days_diff % 60
        if day_idx < 0:
            day_idx += 60
        
        day_stem = self.sixty_jiazi[day_idx][0]
        day_branch = self.sixty_jiazi[day_idx][1]
        
        # Analyze relationships
        relationships = self._analyze_fortune_relationships(
            day_stem, day_branch, saju
        )
        
        day_element = self._get_dominant_element(day_stem, day_branch)
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'heavenly_stem': day_stem,
            'earthly_branch': day_branch,
            'combined_name': f"{day_stem}{day_branch}",
            'element': day_element,
            'relationships': relationships,
            'interpretation': self._interpret_daily_fortune(
                day_stem, day_branch, day_element, relationships
            ),
            'lucky_hours': self._calculate_lucky_hours(day_stem, day_branch, saju)
        }
    
    def _analyze_fortune_relationships(self, fortune_stem: str, fortune_branch: str, 
                                      saju: Dict) -> Dict:
        """
        Analyze relationships between fortune and personal Saju
        
        Args:
            fortune_stem: Fortune's heavenly stem
            fortune_branch: Fortune's earthly branch
            saju: Personal Saju data
            
        Returns:
            Relationship analysis including 합충형파해
        """
        relationships = {
            'harmonies': [],
            'conflicts': [],
            'punishments': [],
            'destructions': [],
            'harms': [],
            'overall_score': 0
        }
        
        # Get Saju branches
        saju_branches = [
            saju.get('year', {}).get('earthly', ''),
            saju.get('month', {}).get('earthly', ''),
            saju.get('day', {}).get('earthly', ''),
            saju.get('hour', {}).get('earthly', '')
        ]
        
        # Check each type of relationship
        for saju_branch in saju_branches:
            if not saju_branch:
                continue
            
            # Check harmony (육합)
            if self.branch_relations['harmony_six'].get(fortune_branch) == saju_branch:
                relationships['harmonies'].append({
                    'type': '육합',
                    'branches': f"{fortune_branch}-{saju_branch}",
                    'effect': 'positive'
                })
                relationships['overall_score'] += 2
            
            # Check conflict (충)
            if self.branch_relations['conflict'].get(fortune_branch) == saju_branch:
                relationships['conflicts'].append({
                    'type': '충',
                    'branches': f"{fortune_branch}-{saju_branch}",
                    'effect': 'negative'
                })
                relationships['overall_score'] -= 3
            
            # Check punishment (형)
            punishment = self.branch_relations['punishment'].get(fortune_branch, [])
            if isinstance(punishment, str) and punishment == saju_branch:
                relationships['punishments'].append({
                    'type': '형',
                    'branches': f"{fortune_branch}-{saju_branch}",
                    'effect': 'negative'
                })
                relationships['overall_score'] -= 2
            elif isinstance(punishment, list) and saju_branch in punishment:
                relationships['punishments'].append({
                    'type': '형',
                    'branches': f"{fortune_branch}-{saju_branch}",
                    'effect': 'negative'
                })
                relationships['overall_score'] -= 2
            
            # Check destruction (파)
            if self.branch_relations['destruction'].get(fortune_branch) == saju_branch:
                relationships['destructions'].append({
                    'type': '파',
                    'branches': f"{fortune_branch}-{saju_branch}",
                    'effect': 'negative'
                })
                relationships['overall_score'] -= 2
            
            # Check harm (해)
            if self.branch_relations['harm'].get(fortune_branch) == saju_branch:
                relationships['harms'].append({
                    'type': '해',
                    'branches': f"{fortune_branch}-{saju_branch}",
                    'effect': 'negative'
                })
                relationships['overall_score'] -= 1
        
        # Check three harmony (삼합)
        for harmony_group in self.branch_relations['harmony_three']:
            if fortune_branch in harmony_group:
                matching_branches = [b for b in saju_branches if b in harmony_group and b != fortune_branch]
                if len(matching_branches) >= 1:
                    relationships['harmonies'].append({
                        'type': '삼합',
                        'branches': f"{fortune_branch} with {', '.join(matching_branches)}",
                        'effect': 'very positive'
                    })
                    # 수정: 삼합 점수를 제한적으로 적용 (최대 +6점)
                    relationships['overall_score'] += min(6, 3 + len(matching_branches))
        
        # 점수 범위 제한 (-10 ~ +10)
        relationships['overall_score'] = max(-10, min(10, relationships['overall_score']))
        
        return relationships
    
    def _interpret_yearly_fortune(self, stem: str, branch: str, element: str, 
                                 relationships: Dict) -> str:
        """Generate interpretation for yearly fortune"""
        score = relationships['overall_score']
        
        if score >= 5:
            base = "매우 길한 한 해입니다. 모든 일이 순조롭게 풀릴 것입니다."
        elif score >= 2:
            base = "대체로 좋은 한 해가 될 것입니다. 기회를 잘 활용하세요."
        elif score >= -1:
            base = "평탄한 한 해가 예상됩니다. 꾸준히 노력하면 성과가 있을 것입니다."
        elif score >= -3:
            base = "다소 어려움이 있을 수 있는 해입니다. 신중한 판단이 필요합니다."
        else:
            base = "도전적인 한 해가 될 것입니다. 충분한 준비와 인내가 필요합니다."
        
        element_advice = {
            '목': " 새로운 시작과 성장의 기회가 있습니다.",
            '화': " 열정과 활력이 넘치는 시기입니다.",
            '토': " 안정과 실속을 추구하기 좋은 때입니다.",
            '금': " 결실을 맺고 정리하는 시기입니다.",
            '수': " 유연하게 대처하며 지혜를 발휘하세요."
        }
        
        return base + element_advice.get(element, "")
    
    def _interpret_monthly_fortune(self, stem: str, branch: str, element: str, 
                                  relationships: Dict) -> str:
        """Generate interpretation for monthly fortune"""
        score = relationships['overall_score']
        
        if score >= 3:
            return f"이번 달은 매우 좋은 운세입니다. {element} 기운이 도움이 됩니다."
        elif score >= 1:
            return f"순조로운 한 달이 예상됩니다. {element} 에너지를 활용하세요."
        elif score >= -1:
            return f"평범한 한 달입니다. {element} 기운에 주의하며 생활하세요."
        else:
            return f"신중함이 필요한 달입니다. {element} 기운과의 조화를 찾으세요."
    
    def _interpret_daily_fortune(self, stem: str, branch: str, element: str, 
                                relationships: Dict) -> str:
        """Generate interpretation for daily fortune"""
        score = relationships['overall_score']
        
        if score >= 2:
            return f"오늘은 길한 날입니다. {element} 기운이 행운을 가져다줍니다."
        elif score >= 0:
            return f"무난한 하루가 될 것입니다. {element} 에너지와 조화를 이루세요."
        else:
            return f"조심스러운 하루입니다. {element} 기운을 주의 깊게 다루세요."
    
    def _get_yearly_advice(self, relationships: Dict) -> List[str]:
        """Get advice based on yearly fortune relationships"""
        advice = []
        
        if relationships['harmonies']:
            advice.append("조화로운 관계가 많아 원만한 한 해가 예상됩니다.")
        
        if relationships['conflicts']:
            advice.append("충돌 에너지가 있으니 대인관계에 신중을 기하세요.")
        
        if relationships['punishments']:
            advice.append("형벌의 기운이 있어 법적 문제나 건강에 주의가 필요합니다.")
        
        if relationships['destructions']:
            advice.append("파괴의 에너지가 있으니 기존 계획을 재검토하세요.")
        
        if relationships['harms']:
            advice.append("해로운 기운이 있어 소통과 이해에 노력이 필요합니다.")
        
        if not advice:
            advice.append("특별한 주의사항 없이 자신의 계획을 추진하세요.")
        
        return advice
    
    def _calculate_lucky_hours(self, day_stem: str, day_branch: str, saju: Dict) -> List[Dict]:
        """Calculate lucky hours for a specific day"""
        lucky_hours = []
        
        # Calculate hourly stems and branches
        hour_branches = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
        hour_times = ['23-01', '01-03', '03-05', '05-07', '07-09', '09-11',
                     '11-13', '13-15', '15-17', '17-19', '19-21', '21-23']
        
        # Day stem determines hour stem pattern
        day_stem_idx = self.heavenly_stems.index(day_stem)
        stem_start_idx = (day_stem_idx * 2) % 10
        
        for i, (branch, time_range) in enumerate(zip(hour_branches, hour_times)):
            hour_stem_idx = (stem_start_idx + i) % 10
            hour_stem = self.heavenly_stems[hour_stem_idx]
            
            # Simple lucky hour calculation based on harmony
            relationships = self._analyze_fortune_relationships(hour_stem, branch, saju)
            
            if relationships['overall_score'] > 0:
                lucky_hours.append({
                    'time': time_range,
                    'stem_branch': f"{hour_stem}{branch}",
                    'score': relationships['overall_score'],
                    'reason': '길시 - 조화로운 시간대'
                })
        
        # Sort by score and return top 3
        lucky_hours.sort(key=lambda x: x['score'], reverse=True)
        return lucky_hours[:3]
    
    def generate_fortune_timeline(self, saju: Dict, birth_date: datetime, gender: str,
                                 reference_year: Optional[int] = None) -> Dict:
        """
        Generate a 20-year fortune timeline (past 10 years to future 10 years)
        
        Args:
            saju: Complete Saju data
            birth_date: Birth date
            gender: 'male' or 'female'
            reference_year: Reference year for timeline (defaults to current year)
            
        Returns:
            Fortune timeline with major change points
        """
        if reference_year is None:
            reference_year = datetime.now().year
        
        start_year = reference_year - 10
        end_year = reference_year + 10
        
        timeline = {
            'reference_year': reference_year,
            'start_year': start_year,
            'end_year': end_year,
            'years': [],
            'major_fortune_periods': [],
            'change_points': [],
            'fortune_flow': {
                'career': [],
                'wealth': [],
                'relationships': [],
                'health': [],
                'overall': []
            }
        }
        
        # Get major fortune periods that cover this timeline
        all_periods = self.get_major_fortune_periods(saju, birth_date, gender)
        current_age = reference_year - birth_date.year
        
        # Filter relevant major fortune periods
        for period in all_periods:
            period_start_year = birth_date.year + period.start_age
            period_end_year = birth_date.year + period.end_age
            
            if period_end_year >= start_year and period_start_year <= end_year:
                timeline['major_fortune_periods'].append({
                    'start_year': max(period_start_year, start_year),
                    'end_year': min(period_end_year, end_year),
                    'period_name': period.combined_name,
                    'element': period.element,
                    'description': period.description,
                    'age_range': f"{period.start_age}-{period.end_age}세"
                })
        
        # Calculate yearly fortunes and detect change points
        previous_score = None
        previous_element = None
        
        for year in range(start_year, end_year + 1):
            # Calculate yearly fortune
            yearly_fortune = self.calculate_yearly_fortune(year, saju)
            age = year - birth_date.year
            
            # Determine if this is current, past, or future
            if year < reference_year:
                time_period = 'past'
            elif year == reference_year:
                time_period = 'current'
            else:
                time_period = 'future'
            
            # Calculate scores for different life aspects
            relationships = yearly_fortune['relationships']
            overall_score = relationships['overall_score']
            
            # Estimate aspect-specific scores based on element and relationships
            element = yearly_fortune['element']
            aspect_scores = self._calculate_aspect_scores(element, relationships)
            
            year_data = {
                'year': year,
                'age': age,
                'time_period': time_period,
                'stem_branch': yearly_fortune['combined_name'],
                'element': element,
                'overall_score': overall_score,
                'interpretation': yearly_fortune['interpretation'],
                'aspects': aspect_scores
            }
            
            timeline['years'].append(year_data)
            
            # Track fortune flow for each aspect
            timeline['fortune_flow']['career'].append(aspect_scores['career'])
            timeline['fortune_flow']['wealth'].append(aspect_scores['wealth'])
            timeline['fortune_flow']['relationships'].append(aspect_scores['relationships'])
            timeline['fortune_flow']['health'].append(aspect_scores['health'])
            timeline['fortune_flow']['overall'].append(overall_score)
            
            # Detect change points
            if previous_score is not None:
                # Major change in fortune score
                score_change = abs(overall_score - previous_score)
                if score_change >= 5:
                    timeline['change_points'].append({
                        'year': year,
                        'type': 'major_shift',
                        'from_score': previous_score,
                        'to_score': overall_score,
                        'direction': 'improvement' if overall_score > previous_score else 'challenge',
                        'description': self._describe_change_point(previous_score, overall_score, element)
                    })
                
                # Element change
                if previous_element != element:
                    timeline['change_points'].append({
                        'year': year,
                        'type': 'element_transition',
                        'from_element': previous_element,
                        'to_element': element,
                        'description': self._describe_element_transition(previous_element, element)
                    })
            
            # Check for major fortune period changes
            for i, period in enumerate(timeline['major_fortune_periods']):
                if year == period['start_year'] and year != start_year:
                    timeline['change_points'].append({
                        'year': year,
                        'type': 'major_fortune_start',
                        'period': period['period_name'],
                        'description': f"새로운 대운 {period['period_name']} 시작 - {period['description']}"
                    })
            
            previous_score = overall_score
            previous_element = element
        
        # Add summary and recommendations
        timeline['summary'] = self._generate_timeline_summary(timeline)
        timeline['recommendations'] = self._generate_timeline_recommendations(timeline, reference_year)
        
        return timeline
    
    def _calculate_aspect_scores(self, element: str, relationships: Dict) -> Dict:
        """Calculate scores for different life aspects based on element and relationships"""
        base_score = relationships['overall_score']
        
        # Element-specific modifiers for each aspect
        element_modifiers = {
            '목': {'career': 2, 'wealth': 1, 'relationships': 1, 'health': 0},
            '화': {'career': 1, 'wealth': 0, 'relationships': 2, 'health': -1},
            '토': {'career': 1, 'wealth': 2, 'relationships': 1, 'health': 1},
            '금': {'career': 1, 'wealth': 2, 'relationships': 0, 'health': 0},
            '수': {'career': 0, 'wealth': 1, 'relationships': 1, 'health': 1}
        }
        
        modifiers = element_modifiers.get(element, {'career': 0, 'wealth': 0, 'relationships': 0, 'health': 0})
        
        # Calculate aspect scores
        scores = {
            'career': min(10, max(-10, base_score + modifiers['career'])),
            'wealth': min(10, max(-10, base_score + modifiers['wealth'])),
            'relationships': min(10, max(-10, base_score + modifiers['relationships'])),
            'health': min(10, max(-10, base_score + modifiers['health']))
        }
        
        # Adjust based on specific relationships
        if relationships['harmonies']:
            scores['relationships'] += 1
            scores['career'] += 1
        
        if relationships['conflicts']:
            scores['health'] -= 1
            scores['relationships'] -= 1
        
        if relationships['destructions']:
            scores['wealth'] -= 1
        
        return scores
    
    def _describe_change_point(self, from_score: int, to_score: int, element: str) -> str:
        """Generate description for a change point"""
        change = to_score - from_score
        
        if change > 0:
            if change >= 7:
                return f"급격한 상승기 - {element} 기운이 크게 도움이 됩니다"
            elif change >= 4:
                return f"호전기 - {element} 에너지가 긍정적으로 작용합니다"
            else:
                return f"점진적 개선 - {element} 기운이 안정을 가져옵니다"
        else:
            if change <= -7:
                return f"큰 도전의 시기 - {element} 기운에 주의가 필요합니다"
            elif change <= -4:
                return f"어려운 시기 - {element} 에너지를 신중히 다루세요"
            else:
                return f"조정기 - {element} 기운과의 균형이 필요합니다"
    
    def _describe_element_transition(self, from_element: str, to_element: str) -> str:
        """Describe element transition"""
        transition_map = {
            ('목', '화'): "성장에서 발현으로 - 노력의 결실이 나타나는 시기",
            ('화', '토'): "열정에서 안정으로 - 기반을 다지는 시기",
            ('토', '금'): "축적에서 정리로 - 성과를 거두는 시기",
            ('금', '수'): "결실에서 지혜로 - 통찰력이 깊어지는 시기",
            ('수', '목'): "지혜에서 새로운 시작으로 - 재도약의 시기",
            ('목', '토'): "성장이 안정으로 전환 - 실속을 추구하는 시기",
            ('화', '금'): "열정이 결실로 - 성과가 구체화되는 시기",
            ('토', '수'): "안정에서 유연함으로 - 변화에 적응하는 시기",
            ('금', '목'): "정리 후 새출발 - 새로운 사이클의 시작",
            ('수', '화'): "지혜가 열정으로 - 활력이 상승하는 시기"
        }
        
        key = (from_element, to_element)
        return transition_map.get(key, f"{from_element}에서 {to_element}로 전환 - 새로운 에너지의 시작")
    
    def _generate_timeline_summary(self, timeline: Dict) -> Dict:
        """Generate summary of the timeline"""
        years_data = timeline['years']
        
        # Find best and worst years
        best_year = max(years_data, key=lambda x: x['overall_score'])
        worst_year = min(years_data, key=lambda x: x['overall_score'])
        
        # Calculate average scores by time period
        past_years = [y for y in years_data if y['time_period'] == 'past']
        future_years = [y for y in years_data if y['time_period'] == 'future']
        
        past_avg = sum(y['overall_score'] for y in past_years) / len(past_years) if past_years else 0
        future_avg = sum(y['overall_score'] for y in future_years) / len(future_years) if future_years else 0
        
        # Identify trends
        overall_flow = timeline['fortune_flow']['overall']
        if len(overall_flow) >= 3:
            recent_trend = 'rising' if overall_flow[-1] > overall_flow[-3] else 'falling' if overall_flow[-1] < overall_flow[-3] else 'stable'
        else:
            recent_trend = 'stable'
        
        return {
            'best_year': {
                'year': best_year['year'],
                'score': best_year['overall_score'],
                'description': best_year['interpretation']
            },
            'worst_year': {
                'year': worst_year['year'],
                'score': worst_year['overall_score'],
                'description': worst_year['interpretation']
            },
            'past_average': round(past_avg, 1),
            'future_average': round(future_avg, 1),
            'trend': recent_trend,
            'major_changes': len(timeline['change_points']),
            'outlook': '긍정적' if future_avg > past_avg else '주의 필요' if future_avg < past_avg else '안정적'
        }
    
    def _generate_timeline_recommendations(self, timeline: Dict, reference_year: int) -> List[str]:
        """Generate recommendations based on timeline analysis"""
        recommendations = []
        summary = timeline['summary']
        
        # Overall trend recommendations
        if summary['outlook'] == '긍정적':
            recommendations.append("앞으로의 운세가 상승세입니다. 적극적인 도전과 투자를 고려하세요.")
        elif summary['outlook'] == '주의 필요':
            recommendations.append("신중한 접근이 필요한 시기입니다. 리스크 관리에 집중하세요.")
        else:
            recommendations.append("안정적인 흐름이 예상됩니다. 꾸준한 노력을 유지하세요.")
        
        # Upcoming change points
        future_changes = [cp for cp in timeline['change_points'] if cp['year'] > reference_year]
        if future_changes:
            next_change = future_changes[0]
            if next_change['type'] == 'major_shift':
                if next_change['direction'] == 'improvement':
                    recommendations.append(f"{next_change['year']}년에 큰 호전이 예상됩니다. 미리 준비하세요.")
                else:
                    recommendations.append(f"{next_change['year']}년에 도전이 예상됩니다. 대비책을 마련하세요.")
        
        # Best year advice
        if summary['best_year']['year'] > reference_year:
            recommendations.append(f"{summary['best_year']['year']}년이 최고의 해가 될 것입니다. 중요한 계획을 이 시기에 맞추세요.")
        
        # Element transitions
        element_changes = [cp for cp in timeline['change_points'] 
                         if cp['type'] == 'element_transition' and cp['year'] >= reference_year]
        if element_changes:
            next_element_change = element_changes[0]
            recommendations.append(f"{next_element_change['year']}년 {next_element_change['to_element']} 기운으로 전환됩니다. {next_element_change['description']}")
        
        return recommendations


def analyze_major_fortune(saju: Dict, birth_date: datetime, gender: str, 
                         current_date: Optional[datetime] = None) -> Dict:
    """
    Convenience function to analyze major fortune
    
    Args:
        saju: Complete Saju data
        birth_date: Birth date
        gender: 'male' or 'female'
        current_date: Current date for analysis
        
    Returns:
        Complete major fortune analysis
    """
    calculator = MajorFortuneCalculator()
    
    # Get all periods
    periods = calculator.get_major_fortune_periods(saju, birth_date, gender)
    
    # Get current period
    current_period = calculator.get_current_major_fortune(saju, birth_date, gender, current_date)
    
    # Find next period
    next_period = None
    if current_period:
        for i, period in enumerate(periods):
            if period.start_age == current_period.start_age and i < len(periods) - 1:
                next_period = periods[i + 1]
                break
    
    # Analyze transition if both periods exist
    transition = None
    if current_period and next_period:
        transition = calculator.analyze_fortune_transition(current_period, next_period)
    
    return {
        'all_periods': periods,
        'current_period': current_period,
        'next_period': next_period,
        'transition_analysis': transition
    }