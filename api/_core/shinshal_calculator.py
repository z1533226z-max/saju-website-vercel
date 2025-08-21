# -*- coding: utf-8 -*-
"""
Shinshal Calculator (신살 계산기)
Calculates auspicious and inauspicious spiritual influences in Saju
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ShinshalResult:
    """Result of shinshal calculation"""
    name: str  # Name of shinshal
    korean_name: str  # Korean name
    type: str  # 'auspicious' or 'inauspicious'
    location: List[str]  # Where it appears (year, month, day, hour)
    strength: float  # Strength score (0-1)
    description: str  # Description of effects
    influence: str  # Specific influence on life
    mitigation: Optional[str] = None  # How to mitigate if inauspicious


class ShinshalCalculator:
    """
    Calculates various shinshal (spiritual influences) in Saju
    Including both auspicious (길신) and inauspicious (흉신) types
    """
    
    def __init__(self):
        """Initialize shinshal calculator with mapping tables"""
        self._initialize_shinshal_maps()
        self._initialize_strength_factors()
        
    def _initialize_shinshal_maps(self):
        """Initialize all shinshal mapping tables"""
        
        # 천을귀인 (Heavenly Noble) - Most powerful auspicious star
        self.tianyi_map = {
            '갑무': ['축', '미'],  # 갑, 무 day stems
            '을기': ['자', '신'],  # 을, 기 day stems
            '병정': ['해', '유'],  # 병, 정 day stems
            '경신': ['인', '오'],  # 경, 신 day stems
            '임계': ['사', '묘']   # 임, 계 day stems
        }
        
        # 월덕귀인 (Monthly Virtue Noble)
        self.monthly_virtue_map = {
            '인': '병', '묘': '갑', '진': '임',
            '사': '경', '오': '병', '미': '갑',
            '신': '경', '유': '무', '술': '병',
            '해': '갑', '자': '임', '축': '경'
        }
        
        # 천덕귀인 (Heavenly Virtue Noble)
        self.heavenly_virtue_map = {
            '정월': '정', '2월': '신', '3월': '임',
            '4월': '신', '5월': '기', '6월': '갑',
            '7월': '계', '8월': '정', '9월': '병',
            '10월': '을', '11월': '경', '12월': '기'
        }
        
        # 문창귀인 (Literary Star)
        self.literary_star_map = {
            '갑': '사', '을': '오', '병': '신', '정': '유',
            '무': '신', '기': '유', '경': '해', '신': '자',
            '임': '인', '계': '묘'
        }
        
        # 학당귀인 (Academic Hall Star)
        self.academic_star_map = {
            '목': ['해', '신'],  # Wood element
            '화': ['인', '유'],  # Fire element
            '토': ['사', '해'],  # Earth element
            '금': ['사', '자'],  # Metal element
            '수': ['신', '묘']   # Water element
        }
        
        # 천의성 (Heavenly Doctor Star)
        self.heavenly_doctor_map = {
            '자': '해', '축': '자', '인': '축', '묘': '인',
            '진': '묘', '사': '진', '오': '사', '미': '오',
            '신': '미', '유': '신', '술': '유', '해': '술'
        }
        
        # 복성귀인 (Fortune Star)
        self.fortune_star_map = {
            '갑': '인', '을': '축', '병': '자', '정': '유',
            '무': '신', '기': '미', '경': '오', '신': '사',
            '임': '진', '계': '묘'
        }
        
        # 장성 (General Star)
        self.general_star_map = {
            '자진신': '자',  # 자, 진, 신 day branches
            '인오술': '오',  # 인, 오, 술 day branches
            '사유축': '유',  # 사, 유, 축 day branches
            '해묘미': '묘'   # 해, 묘, 미 day branches
        }
        
        # 역마 (Post Horse Star) - Travel and movement
        self.post_horse_map = {
            '인오술': '신',  # 인, 오, 술 -> 신
            '신자진': '인',  # 신, 자, 진 -> 인
            '사유축': '해',  # 사, 유, 축 -> 해
            '해묘미': '사'   # 해, 묘, 미 -> 사
        }
        
        # 홍염살 (Red Flame) - Romance and attraction
        self.red_flame_map = {
            '갑': '오', '을': '사', '병': '인', '정': '미',
            '무': '진', '기': '축', '경': '술', '신': '유',
            '임': '자', '계': '신'
        }
        
        # 금여 (Golden Carriage) - Wealth and luxury
        self.golden_carriage_map = {
            '갑': '진', '을': '사', '병': '미', '정': '신',
            '무': '미', '기': '신', '경': '술', '신': '해',
            '임': '축', '계': '인'
        }
        
        # 태극귀인 (Taiji Noble)
        self.taiji_noble_map = {
            '갑을': ['자', '오'],
            '병정': ['묘', '유'],
            '무기': ['진', '술', '축', '미'],
            '경신': ['인', '해'],
            '임계': ['신', '사']
        }
        
        # 삼기귀인 (Three Wonders)
        self.three_wonders = {
            '천상삼기': ['갑', '무', '경'],  # Heavenly three wonders
            '지상삼기': ['을', '병', '정'],  # Earthly three wonders
            '인중삼기': ['임', '계', '신']   # Human three wonders
        }
        
        # 천주귀인 (Heavenly Kitchen) - Food and wealth
        self.heavenly_kitchen_map = {
            '갑': '사', '을': '오', '병': '오', '정': '미',
            '무': '미', '기': '신', '경': '신', '신': '유',
            '임': '해', '계': '자'
        }
        
        # 현침살 (Hanging Needle) - Sharp intelligence
        self.hanging_needle_map = {
            '갑': '유', '을': '신', '병': '자', '정': '해',
            '무': '자', '기': '해', '경': '묘', '신': '인',
            '임': '오', '계': '사'
        }
        
        # --- Inauspicious Shinshal (흉신) ---
        
        # 양인 (Yang Blade) - Extreme energy
        self.yang_blade_map = {
            '갑': '묘', '을': '인', '병': '오', '정': '사',
            '무': '오', '기': '사', '경': '유', '신': '신',
            '임': '자', '계': '해'
        }
        
        # 겁살 (Robbery Star)
        self.robbery_star_map = {
            '인오술': '해',  # 인, 오, 술 -> 해
            '신자진': '사',  # 신, 자, 진 -> 사
            '사유축': '인',  # 사, 유, 축 -> 인
            '해묘미': '신'   # 해, 묘, 미 -> 신
        }
        
        # 화개살 (Canopy Star) - Isolation
        self.canopy_star_map = {
            '인오술': '술',  # 인, 오, 술 -> 술
            '신자진': '진',  # 신, 자, 진 -> 진
            '사유축': '축',  # 사, 유, 축 -> 축
            '해묘미': '미'   # 해, 묘, 미 -> 미
        }
        
        # 고란살 (Loneliness Star)
        self.loneliness_star_map = {
            '인묘진': '사',  # Spring births
            '사오미': '신',  # Summer births
            '신유술': '해',  # Autumn births
            '해자축': '인'   # Winter births
        }
        
        # 백호살 (White Tiger)
        self.white_tiger_map = {
            '갑': '술', '을': '유', '병': '신', '정': '미',
            '무': '신', '기': '미', '경': '오', '신': '사',
            '임': '진', '계': '묘'
        }
        
        # 망신살 (Disgrace Star)
        self.disgrace_star_map = {
            '인오술': '자',  # 인, 오, 술 -> 자
            '신자진': '오',  # 신, 자, 진 -> 오
            '사유축': '묘',  # 사, 유, 축 -> 묘
            '해묘미': '유'   # 해, 묘, 미 -> 유
        }
        
        # 천라지망 (Heaven Net Earth Web)
        self.heaven_net_map = {
            '천라': ['술', '해'],  # Heaven net
            '지망': ['진', '사']   # Earth web
        }
        
        # 급각살 (Sudden Setback)
        self.sudden_setback_map = {
            '갑을': ['유', '신'],
            '병정': ['자', '해'],
            '무기': ['묘', '인'],
            '경신': ['오', '사'],
            '임계': ['축', '미']
        }
        
        # 원진살 (Distant Conflict)
        self.distant_conflict_map = {
            '자': '미', '축': '오', '인': '사', '묘': '진',
            '진': '묘', '사': '인', '오': '축', '미': '자',
            '신': '해', '유': '술', '술': '유', '해': '신'
        }
        
        # 귀문관살 (Ghost Gate)
        self.ghost_gate_map = {
            '춘': ['축', '미'],  # Spring
            '하': ['진', '술'],  # Summer
            '추': ['축', '미'],  # Autumn
            '동': ['진', '술']   # Winter
        }
        
        # 공망 (Emptiness)
        self.emptiness_map = {
            '갑자': ['술', '해'], '갑술': ['신', '유'],
            '갑신': ['오', '미'], '갑오': ['진', '사'],
            '갑진': ['인', '묘'], '갑인': ['자', '축'],
            '을축': ['술', '해'], '을해': ['신', '유'],
            '을유': ['오', '미'], '을미': ['진', '사'],
            '을사': ['인', '묘'], '을묘': ['자', '축'],
            '병인': ['자', '축'], '병자': ['술', '해'],
            '병술': ['신', '유'], '병신': ['오', '미'],
            '병오': ['진', '사'], '병진': ['인', '묘'],
            '정묘': ['자', '축'], '정축': ['술', '해'],
            '정해': ['신', '유'], '정유': ['오', '미'],
            '정미': ['진', '사'], '정사': ['인', '묘'],
            '무진': ['인', '묘'], '무인': ['자', '축'],
            '무자': ['술', '해'], '무술': ['신', '유'],
            '무신': ['오', '미'], '무오': ['진', '사'],
            '기사': ['인', '묘'], '기묘': ['자', '축'],
            '기축': ['술', '해'], '기해': ['신', '유'],
            '기유': ['오', '미'], '기미': ['진', '사'],
            '경오': ['진', '사'], '경진': ['인', '묘'],
            '경인': ['자', '축'], '경자': ['술', '해'],
            '경술': ['신', '유'], '경신': ['오', '미'],
            '신미': ['진', '사'], '신사': ['인', '묘'],
            '신묘': ['자', '축'], '신축': ['술', '해'],
            '신해': ['신', '유'], '신유': ['오', '미'],
            '임신': ['오', '미'], '임오': ['진', '사'],
            '임진': ['인', '묘'], '임인': ['자', '축'],
            '임자': ['술', '해'], '임술': ['신', '유'],
            '계유': ['오', '미'], '계미': ['진', '사'],
            '계사': ['인', '묘'], '계묘': ['자', '축'],
            '계축': ['술', '해'], '계해': ['신', '유']
        }
        
        # 탕화살 (Hot Water) - Accidents
        self.hot_water_map = {
            '인오술': '묘',
            '신자진': '유',
            '사유축': '자',
            '해묘미': '오'
        }
        
        # 도화살 (Peach Blossom) - Romance complications
        self.peach_blossom_map = {
            '인오술': '묘',  # 인, 오, 술 -> 묘
            '신자진': '유',  # 신, 자, 진 -> 유
            '사유축': '오',  # 사, 유, 축 -> 오
            '해묘미': '자'   # 해, 묘, 미 -> 자
        }
        
        # 혈인살 (Blood Blade) - Surgery and injuries
        self.blood_blade_map = {
            '자': '축', '축': '인', '인': '묘', '묘': '진',
            '진': '사', '사': '오', '오': '미', '미': '신',
            '신': '유', '유': '술', '술': '해', '해': '자'
        }
        
    def _initialize_strength_factors(self):
        """Initialize factors that affect shinshal strength"""
        self.strength_factors = {
            'position': {
                'year': 0.7,   # Year pillar - 70% strength
                'month': 0.9,  # Month pillar - 90% strength
                'day': 1.0,    # Day pillar - 100% strength
                'hour': 0.8    # Hour pillar - 80% strength
            },
            'multiple_occurrence': 1.2,  # Boost if appears multiple times
            'conflicting_shinshal': 0.8,  # Reduction if conflicting shinshal present
            'supporting_element': 1.1,    # Boost if element supports
            'season_match': 1.15          # Boost if matches birth season
        }
        
    def calculate_shinshal(self, saju: Dict) -> Dict[str, List[ShinshalResult]]:
        """
        Calculate all shinshal in the given Saju
        
        Args:
            saju: Saju data with year, month, day, hour pillars
            
        Returns:
            Dictionary with 'auspicious' and 'inauspicious' shinshal lists
        """
        results = {
            'auspicious': [],
            'inauspicious': []
        }
        
        # Calculate auspicious shinshal
        results['auspicious'].extend(self._calculate_auspicious_shinshal(saju))
        
        # Calculate inauspicious shinshal
        results['inauspicious'].extend(self._calculate_inauspicious_shinshal(saju))
        
        # Sort by strength
        results['auspicious'].sort(key=lambda x: x.strength, reverse=True)
        results['inauspicious'].sort(key=lambda x: x.strength, reverse=True)
        
        return results
        
    def _calculate_auspicious_shinshal(self, saju: Dict) -> List[ShinshalResult]:
        """Calculate all auspicious shinshal"""
        auspicious = []
        
        # 1. 천을귀인 (Heavenly Noble)
        tianyi = self._check_tianyi_noble(saju)
        if tianyi:
            auspicious.extend(tianyi)
            
        # 2. 월덕귀인 (Monthly Virtue)
        monthly_virtue = self._check_monthly_virtue(saju)
        if monthly_virtue:
            auspicious.append(monthly_virtue)
            
        # 3. 천덕귀인 (Heavenly Virtue)
        heavenly_virtue = self._check_heavenly_virtue(saju)
        if heavenly_virtue:
            auspicious.append(heavenly_virtue)
            
        # 4. 문창귀인 (Literary Star)
        literary = self._check_literary_star(saju)
        if literary:
            auspicious.extend(literary)
            
        # 5. 학당귀인 (Academic Hall)
        academic = self._check_academic_star(saju)
        if academic:
            auspicious.extend(academic)
            
        # 6. 천의성 (Heavenly Doctor)
        doctor = self._check_heavenly_doctor(saju)
        if doctor:
            auspicious.extend(doctor)
            
        # 7. 복성귀인 (Fortune Star)
        fortune = self._check_fortune_star(saju)
        if fortune:
            auspicious.extend(fortune)
            
        # 8. 장성 (General Star)
        general = self._check_general_star(saju)
        if general:
            auspicious.append(general)
            
        # 9. 역마 (Post Horse)
        post_horse = self._check_post_horse(saju)
        if post_horse:
            auspicious.extend(post_horse)
            
        # 10. 홍염살 (Red Flame)
        red_flame = self._check_red_flame(saju)
        if red_flame:
            auspicious.extend(red_flame)
            
        # 11. 금여 (Golden Carriage)
        golden = self._check_golden_carriage(saju)
        if golden:
            auspicious.extend(golden)
            
        # 12. 태극귀인 (Taiji Noble)
        taiji = self._check_taiji_noble(saju)
        if taiji:
            auspicious.extend(taiji)
            
        # 13. 삼기귀인 (Three Wonders)
        wonders = self._check_three_wonders(saju)
        if wonders:
            auspicious.append(wonders)
            
        # 14. 천주귀인 (Heavenly Kitchen)
        kitchen = self._check_heavenly_kitchen(saju)
        if kitchen:
            auspicious.extend(kitchen)
            
        # 15. 현침살 (Hanging Needle)
        needle = self._check_hanging_needle(saju)
        if needle:
            auspicious.extend(needle)
            
        return auspicious
        
    def _calculate_inauspicious_shinshal(self, saju: Dict) -> List[ShinshalResult]:
        """Calculate all inauspicious shinshal"""
        inauspicious = []
        
        # 1. 양인 (Yang Blade)
        yang_blade = self._check_yang_blade(saju)
        if yang_blade:
            inauspicious.extend(yang_blade)
            
        # 2. 겁살 (Robbery Star)
        robbery = self._check_robbery_star(saju)
        if robbery:
            inauspicious.extend(robbery)
            
        # 3. 화개살 (Canopy Star)
        canopy = self._check_canopy_star(saju)
        if canopy:
            inauspicious.extend(canopy)
            
        # 4. 고란살 (Loneliness Star)
        loneliness = self._check_loneliness_star(saju)
        if loneliness:
            inauspicious.append(loneliness)
            
        # 5. 백호살 (White Tiger)
        white_tiger = self._check_white_tiger(saju)
        if white_tiger:
            inauspicious.extend(white_tiger)
            
        # 6. 망신살 (Disgrace Star)
        disgrace = self._check_disgrace_star(saju)
        if disgrace:
            inauspicious.extend(disgrace)
            
        # 7. 천라지망 (Heaven Net Earth Web)
        heaven_net = self._check_heaven_net(saju)
        if heaven_net:
            inauspicious.extend(heaven_net)
            
        # 8. 급각살 (Sudden Setback)
        setback = self._check_sudden_setback(saju)
        if setback:
            inauspicious.extend(setback)
            
        # 9. 원진살 (Distant Conflict)
        distant = self._check_distant_conflict(saju)
        if distant:
            inauspicious.extend(distant)
            
        # 10. 귀문관살 (Ghost Gate)
        ghost = self._check_ghost_gate(saju)
        if ghost:
            inauspicious.extend(ghost)
            
        # 11. 공망 (Emptiness)
        emptiness = self._check_emptiness(saju)
        if emptiness:
            inauspicious.extend(emptiness)
            
        # 12. 탕화살 (Hot Water)
        hot_water = self._check_hot_water(saju)
        if hot_water:
            inauspicious.extend(hot_water)
            
        # 13. 도화살 (Peach Blossom)
        peach = self._check_peach_blossom(saju)
        if peach:
            inauspicious.extend(peach)
            
        # 14. 혈인살 (Blood Blade)
        blood = self._check_blood_blade(saju)
        if blood:
            inauspicious.extend(blood)
            
        # 15. Additional: 역마충 (Post Horse Clash)
        horse_clash = self._check_post_horse_clash(saju)
        if horse_clash:
            inauspicious.extend(horse_clash)
            
        return inauspicious
        
    # --- Auspicious Shinshal Check Methods ---
    
    def _check_tianyi_noble(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Tianyi Noble (천을귀인)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        # Find which group the day stem belongs to
        noble_branches = []
        for group, branches in self.tianyi_map.items():
            if day_stem in group:
                noble_branches = branches
                break
                
        if not noble_branches:
            return results
            
        # Check each pillar for the noble branches
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch in noble_branches:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'tianyi')
            results.append(ShinshalResult(
                name='Tianyi Noble',
                korean_name='천을귀인',
                type='auspicious',
                location=locations,
                strength=strength,
                description='최고의 길신. 귀인의 도움과 보호를 받음',
                influence='고난에서 구원, 귀인 조력, 승진과 출세'
            ))
            
        return results
        
    def _check_monthly_virtue(self, saju: Dict) -> Optional[ShinshalResult]:
        """Check for Monthly Virtue (월덕귀인)"""
        month_branch = saju.get('month', {}).get('earthly', '')
        
        if not month_branch:
            return None
            
        virtue_stem = self.monthly_virtue_map.get(month_branch)
        if not virtue_stem:
            return None
            
        # Check if the virtue stem appears in saju
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            stem = saju.get(position, {}).get('heavenly', '')
            if stem == virtue_stem:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'monthly_virtue')
            return ShinshalResult(
                name='Monthly Virtue',
                korean_name='월덕귀인',
                type='auspicious',
                location=locations,
                strength=strength,
                description='월의 덕을 받아 안정과 평안을 누림',
                influence='정신적 안정, 덕망 있는 인품, 사회적 신뢰'
            )
            
        return None
        
    def _check_heavenly_virtue(self, saju: Dict) -> Optional[ShinshalResult]:
        """Check for Heavenly Virtue (천덕귀인)"""
        # This would require birth month information
        # Simplified implementation
        return None
        
    def _check_literary_star(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Literary Star (문창귀인)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        literary_branch = self.literary_star_map.get(day_stem)
        if not literary_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == literary_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'literary')
            results.append(ShinshalResult(
                name='Literary Star',
                korean_name='문창귀인',
                type='auspicious',
                location=locations,
                strength=strength,
                description='학문과 예술의 재능, 문필의 능력',
                influence='학업 성취, 예술적 재능, 창작 능력'
            ))
            
        return results
        
    def _check_academic_star(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Academic Hall (학당귀인)"""
        results = []
        # Would need day master element for proper calculation
        # Simplified implementation
        return results
        
    def _check_heavenly_doctor(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Heavenly Doctor (천의성)"""
        results = []
        month_branch = saju.get('month', {}).get('earthly', '')
        
        if not month_branch:
            return results
            
        doctor_branch = self.heavenly_doctor_map.get(month_branch)
        if not doctor_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == doctor_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'doctor')
            results.append(ShinshalResult(
                name='Heavenly Doctor',
                korean_name='천의성',
                type='auspicious',
                location=locations,
                strength=strength,
                description='건강과 치유의 능력, 의료 관련 재능',
                influence='건강 회복, 의료업 적성, 치유 능력'
            ))
            
        return results
        
    def _check_fortune_star(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Fortune Star (복성귀인)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        fortune_branch = self.fortune_star_map.get(day_stem)
        if not fortune_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == fortune_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'fortune')
            results.append(ShinshalResult(
                name='Fortune Star',
                korean_name='복성귀인',
                type='auspicious',
                location=locations,
                strength=strength,
                description='복과 행운을 가져오는 길성',
                influence='재물운, 행운, 좋은 기회'
            ))
            
        return results
        
    def _check_general_star(self, saju: Dict) -> Optional[ShinshalResult]:
        """Check for General Star (장성)"""
        day_branch = saju.get('day', {}).get('earthly', '')
        
        if not day_branch:
            return None
            
        # Check which group the day branch belongs to
        general_branch = None
        for group, branch in self.general_star_map.items():
            if day_branch in group:
                general_branch = branch
                break
                
        if not general_branch:
            return None
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == general_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'general')
            return ShinshalResult(
                name='General Star',
                korean_name='장성',
                type='auspicious',
                location=locations,
                strength=strength,
                description='리더십과 통솔력, 권위를 나타냄',
                influence='지도력, 관리 능력, 조직 운영'
            )
            
        return None
        
    def _check_post_horse(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Post Horse (역마)"""
        results = []
        day_branch = saju.get('day', {}).get('earthly', '')
        
        if not day_branch:
            return results
            
        # Find post horse branch
        horse_branch = None
        for group, branch in self.post_horse_map.items():
            if day_branch in group:
                horse_branch = branch
                break
                
        if not horse_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == horse_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'post_horse')
            results.append(ShinshalResult(
                name='Post Horse',
                korean_name='역마',
                type='auspicious',
                location=locations,
                strength=strength,
                description='이동과 변화, 여행과 해외 인연',
                influence='해외 운, 이동 수, 변화와 발전'
            ))
            
        return results
        
    def _check_red_flame(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Red Flame (홍염살)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        flame_branch = self.red_flame_map.get(day_stem)
        if not flame_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == flame_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'red_flame')
            results.append(ShinshalResult(
                name='Red Flame',
                korean_name='홍염살',
                type='auspicious',
                location=locations,
                strength=strength,
                description='매력과 인기, 이성운',
                influence='연애운, 인기, 매력적인 외모'
            ))
            
        return results
        
    def _check_golden_carriage(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Golden Carriage (금여)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        golden_branch = self.golden_carriage_map.get(day_stem)
        if not golden_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == golden_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'golden')
            results.append(ShinshalResult(
                name='Golden Carriage',
                korean_name='금여',
                type='auspicious',
                location=locations,
                strength=strength,
                description='부귀와 명예, 고급스러운 생활',
                influence='재물운, 명예, 사치와 호화'
            ))
            
        return results
        
    def _check_taiji_noble(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Taiji Noble (태극귀인)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        # Find which group the day stem belongs to
        taiji_branches = []
        for group, branches in self.taiji_noble_map.items():
            if day_stem in group:
                taiji_branches = branches
                break
                
        if not taiji_branches:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch in taiji_branches:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'taiji')
            results.append(ShinshalResult(
                name='Taiji Noble',
                korean_name='태극귀인',
                type='auspicious',
                location=locations,
                strength=strength,
                description='철학과 사상, 깊은 통찰력',
                influence='철학적 사고, 종교성, 지혜'
            ))
            
        return results
        
    def _check_three_wonders(self, saju: Dict) -> Optional[ShinshalResult]:
        """Check for Three Wonders (삼기귀인)"""
        stems = []
        for position in ['year', 'month', 'day']:
            stem = saju.get(position, {}).get('heavenly', '')
            if stem:
                stems.append(stem)
                
        if len(stems) < 3:
            return None
            
        # Check each type of three wonders
        for wonder_type, wonder_stems in self.three_wonders.items():
            if all(stem in wonder_stems for stem in stems):
                return ShinshalResult(
                    name='Three Wonders',
                    korean_name='삼기귀인',
                    type='auspicious',
                    location=['year', 'month', 'day'],
                    strength=0.95,
                    description=f'{wonder_type}: 특별한 재능과 행운',
                    influence='비범한 재능, 특별한 행운, 큰 성취'
                )
                
        return None
        
    def _check_heavenly_kitchen(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Heavenly Kitchen (천주귀인)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        kitchen_branch = self.heavenly_kitchen_map.get(day_stem)
        if not kitchen_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == kitchen_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'kitchen')
            results.append(ShinshalResult(
                name='Heavenly Kitchen',
                korean_name='천주귀인',
                type='auspicious',
                location=locations,
                strength=strength,
                description='음식과 관련된 복, 먹을 복',
                influence='음식업 성공, 미식, 풍족한 생활'
            ))
            
        return results
        
    def _check_hanging_needle(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Hanging Needle (현침살)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        needle_branch = self.hanging_needle_map.get(day_stem)
        if not needle_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == needle_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'needle')
            results.append(ShinshalResult(
                name='Hanging Needle',
                korean_name='현침살',
                type='auspicious',
                location=locations,
                strength=strength,
                description='예리한 지능과 통찰력',
                influence='분석력, 비판적 사고, 전문성'
            ))
            
        return results
        
    # --- Inauspicious Shinshal Check Methods ---
    
    def _check_yang_blade(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Yang Blade (양인)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        blade_branch = self.yang_blade_map.get(day_stem)
        if not blade_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == blade_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'yang_blade')
            results.append(ShinshalResult(
                name='Yang Blade',
                korean_name='양인',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='극단적 에너지, 파괴적 성향',
                influence='사고, 수술, 극단적 행동',
                mitigation='식신으로 제어, 종교나 수행'
            ))
            
        return results
        
    def _check_robbery_star(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Robbery Star (겁살)"""
        results = []
        year_branch = saju.get('year', {}).get('earthly', '')
        
        if not year_branch:
            return results
            
        # Find robbery branch
        robbery_branch = None
        for group, branch in self.robbery_star_map.items():
            if year_branch in group:
                robbery_branch = branch
                break
                
        if not robbery_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == robbery_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'robbery')
            results.append(ShinshalResult(
                name='Robbery Star',
                korean_name='겁살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='재물 손실, 도난, 사기',
                influence='금전적 손실, 사기 피해, 도난',
                mitigation='재물 관리 철저, 보안 강화'
            ))
            
        return results
        
    def _check_canopy_star(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Canopy Star (화개살)"""
        results = []
        year_branch = saju.get('year', {}).get('earthly', '')
        
        if not year_branch:
            return results
            
        # Find canopy branch
        canopy_branch = None
        for group, branch in self.canopy_star_map.items():
            if year_branch in group:
                canopy_branch = branch
                break
                
        if not canopy_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == canopy_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'canopy')
            results.append(ShinshalResult(
                name='Canopy Star',
                korean_name='화개살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='고독, 종교성, 예술성',
                influence='독신, 종교 생활, 예술 활동',
                mitigation='사회 활동 증가, 인간관계 노력'
            ))
            
        return results
        
    def _check_loneliness_star(self, saju: Dict) -> Optional[ShinshalResult]:
        """Check for Loneliness Star (고란살)"""
        month_branch = saju.get('month', {}).get('earthly', '')
        
        if not month_branch:
            return None
            
        # Find loneliness branch based on season
        loneliness_branch = None
        for season, branch in self.loneliness_star_map.items():
            if month_branch in season:
                loneliness_branch = branch
                break
                
        if not loneliness_branch:
            return None
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == loneliness_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'loneliness')
            return ShinshalResult(
                name='Loneliness Star',
                korean_name='고란살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='고독, 독신, 가족과 떨어짐',
                influence='독신 생활, 가족 인연 약함',
                mitigation='적극적인 사교 활동, 봉사 활동'
            )
            
        return None
        
    def _check_white_tiger(self, saju: Dict) -> List[ShinshalResult]:
        """Check for White Tiger (백호살)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        tiger_branch = self.white_tiger_map.get(day_stem)
        if not tiger_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == tiger_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'white_tiger')
            results.append(ShinshalResult(
                name='White Tiger',
                korean_name='백호살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='혈광, 수술, 사고',
                influence='부상, 수술, 교통사고',
                mitigation='안전 주의, 건강 관리'
            ))
            
        return results
        
    def _check_disgrace_star(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Disgrace Star (망신살)"""
        results = []
        year_branch = saju.get('year', {}).get('earthly', '')
        
        if not year_branch:
            return results
            
        # Find disgrace branch
        disgrace_branch = None
        for group, branch in self.disgrace_star_map.items():
            if year_branch in group:
                disgrace_branch = branch
                break
                
        if not disgrace_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == disgrace_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'disgrace')
            results.append(ShinshalResult(
                name='Disgrace Star',
                korean_name='망신살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='명예 실추, 망신, 스캔들',
                influence='평판 손상, 구설수, 명예 실추',
                mitigation='언행 조심, 신중한 처신'
            ))
            
        return results
        
    def _check_heaven_net(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Heaven Net Earth Web (천라지망)"""
        results = []
        
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            
            if branch in self.heaven_net_map['천라']:
                results.append(ShinshalResult(
                    name='Heaven Net',
                    korean_name='천라',
                    type='inauspicious',
                    location=[position],
                    strength=self._calculate_strength([position], 'heaven_net'),
                    description='하늘의 그물, 진로 막힘',
                    influence='승진 정체, 발전 제한',
                    mitigation='인내와 노력, 때를 기다림'
                ))
                
            if branch in self.heaven_net_map['지망']:
                results.append(ShinshalResult(
                    name='Earth Web',
                    korean_name='지망',
                    type='inauspicious',
                    location=[position],
                    strength=self._calculate_strength([position], 'earth_web'),
                    description='땅의 그물, 이동 제한',
                    influence='이동 어려움, 정체 상태',
                    mitigation='현재 위치에서 최선'
                ))
                
        return results
        
    def _check_sudden_setback(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Sudden Setback (급각살)"""
        results = []
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        if not day_stem:
            return results
            
        # Find setback branches
        setback_branches = []
        for group, branches in self.sudden_setback_map.items():
            if day_stem in group:
                setback_branches = branches
                break
                
        if not setback_branches:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch in setback_branches:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'setback')
            results.append(ShinshalResult(
                name='Sudden Setback',
                korean_name='급각살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='갑작스런 좌절, 급전직하',
                influence='예상치 못한 실패, 급격한 변화',
                mitigation='신중한 계획, 위험 대비'
            ))
            
        return results
        
    def _check_distant_conflict(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Distant Conflict (원진살)"""
        results = []
        
        branches = {}
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch:
                branches[position] = branch
                
        # Check for conflicts
        for pos1, branch1 in branches.items():
            conflict_branch = self.distant_conflict_map.get(branch1)
            if conflict_branch:
                for pos2, branch2 in branches.items():
                    if pos1 != pos2 and branch2 == conflict_branch:
                        results.append(ShinshalResult(
                            name='Distant Conflict',
                            korean_name='원진살',
                            type='inauspicious',
                            location=[pos1, pos2],
                            strength=self._calculate_strength([pos1, pos2], 'conflict'),
                            description='원거리 충돌, 불화',
                            influence='인간관계 갈등, 소통 어려움',
                            mitigation='이해와 포용, 중재자 활용'
                        ))
                        
        return results
        
    def _check_ghost_gate(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Ghost Gate (귀문관살)"""
        results = []
        # Simplified - would need season calculation
        return results
        
    def _check_emptiness(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Emptiness (공망)"""
        results = []
        
        # Get day pillar
        day_stem = saju.get('day', {}).get('heavenly', '')
        day_branch = saju.get('day', {}).get('earthly', '')
        
        if not day_stem or not day_branch:
            return results
            
        day_pillar = day_stem + day_branch
        empty_branches = self.emptiness_map.get(day_pillar, [])
        
        if not empty_branches:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch in empty_branches:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'emptiness')
            results.append(ShinshalResult(
                name='Emptiness',
                korean_name='공망',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='공허함, 헛수고, 무위',
                influence='노력의 헛됨, 결실 부족',
                mitigation='실질적 목표, 현실적 계획'
            ))
            
        return results
        
    def _check_hot_water(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Hot Water (탕화살)"""
        results = []
        day_branch = saju.get('day', {}).get('earthly', '')
        
        if not day_branch:
            return results
            
        # Find hot water branch
        hot_branch = None
        for group, branch in self.hot_water_map.items():
            if day_branch in group:
                hot_branch = branch
                break
                
        if not hot_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == hot_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'hot_water')
            results.append(ShinshalResult(
                name='Hot Water',
                korean_name='탕화살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='화상, 뜨거운 물 사고',
                influence='화상 위험, 열 관련 사고',
                mitigation='화기 조심, 안전 수칙'
            ))
            
        return results
        
    def _check_peach_blossom(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Peach Blossom (도화살)"""
        results = []
        day_branch = saju.get('day', {}).get('earthly', '')
        
        if not day_branch:
            return results
            
        # Find peach blossom branch
        peach_branch = None
        for group, branch in self.peach_blossom_map.items():
            if day_branch in group:
                peach_branch = branch
                break
                
        if not peach_branch:
            return results
            
        locations = []
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch == peach_branch:
                locations.append(position)
                
        if locations:
            strength = self._calculate_strength(locations, 'peach')
            results.append(ShinshalResult(
                name='Peach Blossom',
                korean_name='도화살',
                type='inauspicious',
                location=locations,
                strength=strength,
                description='과도한 이성 관계, 문란',
                influence='복잡한 이성 관계, 스캔들',
                mitigation='절제와 신중함, 일편단심'
            ))
            
        return results
        
    def _check_blood_blade(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Blood Blade (혈인살)"""
        results = []
        
        for position in ['year', 'month', 'day', 'hour']:
            branch = saju.get(position, {}).get('earthly', '')
            if branch:
                blood_branch = self.blood_blade_map.get(branch)
                if blood_branch:
                    # Check if blood branch exists in saju
                    for pos2 in ['year', 'month', 'day', 'hour']:
                        if saju.get(pos2, {}).get('earthly', '') == blood_branch:
                            results.append(ShinshalResult(
                                name='Blood Blade',
                                korean_name='혈인살',
                                type='inauspicious',
                                location=[position, pos2],
                                strength=self._calculate_strength([position, pos2], 'blood'),
                                description='혈액 관련, 수술, 출혈',
                                influence='수술, 부상, 혈액 질환',
                                mitigation='건강 검진, 안전 주의'
                            ))
                            break
                            
        return results
        
    def _check_post_horse_clash(self, saju: Dict) -> List[ShinshalResult]:
        """Check for Post Horse Clash (역마충)"""
        results = []
        # Check if post horse is being clashed
        # Simplified implementation
        return results
        
    def _calculate_strength(self, locations: List[str], shinshal_type: str) -> float:
        """
        Calculate the strength of a shinshal based on its locations
        
        Args:
            locations: List of positions where shinshal appears
            shinshal_type: Type of shinshal for specific calculations
            
        Returns:
            Strength score between 0 and 1
        """
        if not locations:
            return 0.0
            
        # Base strength from position
        total_strength = 0.0
        for location in locations:
            total_strength += self.strength_factors['position'].get(location, 0.5)
            
        # Average the position strengths
        strength = total_strength / len(locations) if locations else 0.0
        
        # Boost for multiple occurrences
        if len(locations) > 1:
            strength *= self.strength_factors['multiple_occurrence']
            
        # Special adjustments for specific shinshal
        if shinshal_type == 'tianyi':
            strength *= 1.2  # Tianyi is the most powerful
        elif shinshal_type == 'yang_blade':
            if 'month' in locations:
                strength *= 1.15  # Yang blade is stronger in month
        elif shinshal_type == 'emptiness':
            if 'day' in locations:
                strength *= 0.9  # Emptiness affects day pillar less
                
        # Cap at 1.0
        return min(strength, 1.0)
        
    def get_shinshal_summary(self, saju: Dict) -> str:
        """
        Get a text summary of all shinshal in the saju
        
        Args:
            saju: Saju data
            
        Returns:
            Text summary of shinshal influences
        """
        results = self.calculate_shinshal(saju)
        
        summary = []
        summary.append("=== 신살 분석 결과 ===\n")
        
        # Auspicious shinshal
        if results['auspicious']:
            summary.append("【길신 (吉神)】")
            for shinshal in results['auspicious'][:5]:  # Top 5
                summary.append(f"  • {shinshal.korean_name}: {shinshal.influence}")
                summary.append(f"    위치: {', '.join(shinshal.location)} | 강도: {shinshal.strength:.1%}")
            summary.append("")
            
        # Inauspicious shinshal
        if results['inauspicious']:
            summary.append("【흉신 (凶神)】")
            for shinshal in results['inauspicious'][:5]:  # Top 5
                summary.append(f"  • {shinshal.korean_name}: {shinshal.influence}")
                summary.append(f"    위치: {', '.join(shinshal.location)} | 강도: {shinshal.strength:.1%}")
                if shinshal.mitigation:
                    summary.append(f"    대책: {shinshal.mitigation}")
            summary.append("")
            
        return "\n".join(summary)


# Helper function
def calculate_shinshal(saju: Dict) -> Dict[str, List[ShinshalResult]]:
    """
    Convenience function to calculate shinshal
    
    Args:
        saju: Complete Saju data
        
    Returns:
        Dictionary with auspicious and inauspicious shinshal
    """
    calculator = ShinshalCalculator()
    return calculator.calculate_shinshal(saju)