# -*- coding: utf-8 -*-
"""
Saju Interpretation Engine
Generates comprehensive interpretations based on calculated Saju and elements
"""

import json
import os
from typing import Dict, List, Optional
from .ten_gods_calculator import TenGodsCalculator, analyze_saju_ten_gods
from .major_fortune_calculator import MajorFortuneCalculator, analyze_major_fortune


class Interpreter:
    """
    Interprets Saju calculation results and generates comprehensive readings
    """
    
    def __init__(self):
        """Initialize the interpreter with interpretation data"""
        self.interpretations = {}
        self.elements_mapping = {}
        self.ten_gods_calculator = TenGodsCalculator()  # Initialize Ten Gods calculator
        self.major_fortune_calculator = MajorFortuneCalculator()  # Initialize Major Fortune calculator
        self.load_interpretation_data()
    
    def load_interpretation_data(self):
        """Load interpretation data from JSON files"""
        base_path = os.path.dirname(os.path.dirname(__file__))
        
        # Load basic interpretations
        interpretations_path = os.path.join(base_path, 'data', 'interpretations.json')
        try:
            with open(interpretations_path, 'r', encoding='utf-8') as f:
                self.interpretations = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.interpretations = self._get_default_interpretations()
        
        # Load detailed day stem interpretations
        self.detailed_interpretations = {}
        detailed_path = os.path.join(base_path, 'data', 'day_stems_detailed')
        if os.path.exists(detailed_path):
            for filename in os.listdir(detailed_path):
                if filename.endswith('.json'):
                    stem_name = filename.replace('.json', '')
                    file_path = os.path.join(detailed_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.detailed_interpretations[stem_name] = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        continue
        
        # Load elements mapping
        elements_path = os.path.join(base_path, 'data', 'elements_mapping.json')
        try:
            with open(elements_path, 'r', encoding='utf-8') as f:
                self.elements_mapping = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.elements_mapping = {}
    
    def _get_default_interpretations(self) -> Dict:
        """Get default interpretations if file not found"""
        return {
            'day_stems': {
                '갑': {
                    'summary': '갑목은 큰 나무를 상징하며 성장과 발전의 기운을 가지고 있습니다.',
                    'personality': '갑목일주는 성격이 곧고 바르며 정의감이 강합니다.',
                    'career': '리더십이 있어 관리직이나 교육 분야에서 성공할 수 있습니다.',
                    'wealth': '재물은 꾸준히 늘어나며 안정적인 편입니다.',
                    'health': '간과 눈 건강에 주의가 필요합니다.',
                    'relationships': '인간관계는 원만하며 신뢰를 중시합니다.'
                }
            },
            'elements': {},
            'gender_modifiers': {
                'male': {},
                'female': {}
            }
        }
    
    def generate_interpretation(self, saju: Dict, elements: Dict, gender: str) -> Dict:
        """
        Generate complete interpretation based on Saju and elements
        
        Args:
            saju: Dictionary containing four pillars
            elements: Dictionary with element percentages
            gender: 'male' or 'female'
            
        Returns:
            Dictionary containing all interpretation sections
        """
        # Check if detailed interpretation is available
        day_stem = saju.get('day', {}).get('heavenly', '')
        detailed = self.get_detailed_interpretation(day_stem, gender, elements)
        
        # Calculate Ten Gods analysis with detailed interpretation
        ten_gods_analysis = self.ten_gods_calculator.get_all_ten_gods(saju)
        
        # Generate personalized Ten Gods interpretation
        ten_gods_interpretation = self._generate_ten_gods_interpretation(ten_gods_analysis, gender)
        
        # Calculate Major Fortune periods
        birth_info = saju.get('birth_info', {})
        birth_date_str = birth_info.get('date', '')
        if birth_date_str:
            from datetime import datetime
            try:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
                major_fortune_analysis = analyze_major_fortune(saju, birth_date, gender)
                
                # Generate fortune timeline (20-year view)
                fortune_timeline = self.major_fortune_calculator.generate_fortune_timeline(
                    saju, birth_date, gender
                )
            except:
                major_fortune_analysis = None
                fortune_timeline = None
        else:
            major_fortune_analysis = None
            fortune_timeline = None
        
        if detailed:
            # Return detailed interpretation if available
            return {
                'summary': detailed.get('summary', self.generate_summary(saju, elements)),
                'personality': detailed.get('personality', self.generate_personality(saju, gender)),
                'fortune': detailed.get('fortune', self.generate_fortune(saju, elements)),
                'health': detailed.get('health', self.generate_health(saju, elements)),
                'career': detailed.get('career', self.generate_career(saju, elements)),
                'relationships': detailed.get('relationships', self.generate_relationships(saju, gender, elements)),
                'elements_analysis': self.analyze_elements(elements),
                'special_patterns': self.find_special_patterns(saju),
                'yearly_outlook': detailed.get('yearly_outlook', self.generate_yearly_outlook(saju)),
                'detailed_available': True,
                'ten_gods': detailed.get('ten_gods', None),
                'ten_gods_analysis': ten_gods_analysis,
                'ten_gods_interpretation': ten_gods_interpretation,
                'spiritual_growth': detailed.get('spiritual_growth', None),
                'major_fortune': major_fortune_analysis,
                'fortune_timeline': fortune_timeline
            }
        else:
            # Fallback to basic interpretation
            return {
                'summary': self.generate_summary(saju, elements),
                'personality': self.generate_personality(saju, gender),
                'fortune': self.generate_fortune(saju, elements),
                'health': self.generate_health(saju, elements),
                'career': self.generate_career(saju, elements),
                'relationships': self.generate_relationships(saju, gender, elements),
                'elements_analysis': self.analyze_elements(elements),
                'special_patterns': self.find_special_patterns(saju),
                'yearly_outlook': self.generate_yearly_outlook(saju),
                'ten_gods_analysis': ten_gods_analysis,
                'ten_gods_interpretation': ten_gods_interpretation,
                'detailed_available': False,
                'major_fortune': major_fortune_analysis
            }
    
    def get_detailed_interpretation(self, day_stem: str, gender: str, elements: Dict) -> Optional[Dict]:
        """
        Get detailed interpretation for specific day stem
        
        Args:
            day_stem: Day heavenly stem character
            gender: 'male' or 'female'
            elements: Element percentages
            
        Returns:
            Detailed interpretation dictionary or None
        """
        # Map stems to file names
        stem_mapping = {
            '갑': 'gap_wood',
            '을': 'eul_wood',
            '병': 'byeong_fire',
            '정': 'jeong_fire',
            '무': 'mu_earth',
            '기': 'gi_earth',
            '경': 'gyeong_metal',
            '신': 'sin_metal',
            '임': 'im_water',
            '계': 'gye_water'
        }
        
        stem_file = stem_mapping.get(day_stem)
        if not stem_file or stem_file not in self.detailed_interpretations:
            return None
        
        detailed = self.detailed_interpretations[stem_file]
        
        # Format response based on detailed data
        return {
            'summary': self._format_summary_detailed(detailed),
            'personality': self._format_personality_detailed(detailed, gender),
            'fortune': self._format_wealth_detailed(detailed),
            'health': self._format_health_detailed(detailed),
            'career': self._format_career_detailed(detailed),
            'relationships': self._format_relationships_detailed(detailed, gender),
            'yearly_outlook': self._format_yearly_outlook(detailed),
            'ten_gods': detailed.get('ten_gods_interpretation', {}),
            'spiritual_growth': detailed.get('spiritual_growth', {})
        }
    
    def _format_summary_detailed(self, detailed: Dict) -> str:
        """Format detailed summary interpretation"""
        basic = detailed.get('basic', {})
        nature = basic.get('nature', '')
        characteristics = basic.get('characteristics', [])[:3]
        
        return f"{detailed.get('name', '')} - {nature}. 특징: {', '.join(characteristics)}"
    
    def _format_personality_detailed(self, detailed: Dict, gender: str) -> str:
        """Format detailed personality interpretation"""
        personality = detailed.get('personality_detailed', {})
        core_traits = personality.get('core_traits', {})
        emotional = personality.get('emotional_patterns', {})
        
        # Get key personality traits
        traits_summary = []
        for key, value in list(core_traits.items())[:3]:
            traits_summary.append(value)
        
        return ' '.join(traits_summary[:2])
    
    def _format_wealth_detailed(self, detailed: Dict) -> str:
        """Format detailed wealth interpretation"""
        wealth = detailed.get('wealth_detailed', {})
        financial_traits = wealth.get('financial_traits', {})
        accumulation = wealth.get('wealth_accumulation', {})
        
        earning = financial_traits.get('earning_ability', '')
        methods = accumulation.get('methods', [])[:2]
        
        return f"{earning} 주요 재물 획득 방법: {', '.join(methods)}"
    
    def _format_health_detailed(self, detailed: Dict) -> str:
        """Format detailed health interpretation"""
        health = detailed.get('health_detailed', {})
        constitution = health.get('physical_constitution', {})
        mental = health.get('mental_health', {})
        
        weak_areas = constitution.get('weak_areas', '')
        common_issues = constitution.get('common_issues', [])[:2]
        
        return f"주의 필요 부위: {weak_areas}. 흔한 건강 문제: {', '.join(common_issues)}"
    
    def _format_career_detailed(self, detailed: Dict) -> str:
        """Format detailed career interpretation"""
        career = detailed.get('career_detailed', {})
        suitable_fields = career.get('suitable_fields', [])[:3]
        environment = career.get('work_environment', {})
        ideal = environment.get('ideal', '')
        
        return f"적합 직종: {', '.join(suitable_fields)}. 이상적 환경: {ideal}"
    
    def _format_relationships_detailed(self, detailed: Dict, gender: str) -> str:
        """Format detailed relationships interpretation"""
        love = detailed.get('love_marriage', {})
        romantic = love.get('romantic_style', {})
        ideal_partner = love.get('ideal_partner', {})
        marriage = love.get('marriage_life', {})
        
        approach = romantic.get('approach', '')
        strengths = marriage.get('strengths', '')
        
        return f"{approach} {strengths}"
    
    def _format_yearly_outlook(self, detailed: Dict) -> str:
        """Format yearly outlook from detailed interpretation"""
        wealth = detailed.get('wealth_detailed', {})
        luck = wealth.get('financial_luck', {})
        
        good_periods = luck.get('good_periods', '')
        lucky_directions = luck.get('lucky_directions', '')
        
        return f"길한 시기: {good_periods}. 행운의 방향: {lucky_directions}"
    
    def generate_summary(self, saju: Dict, elements: Dict) -> str:
        """Generate overall summary of the Saju reading"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        dominant_element = self._get_dominant_element(elements)
        
        # Get base interpretation from day stem
        base = self.interpretations.get('day_stems', {}).get(
            day_stem, {}
        ).get('summary', '당신의 사주는 독특한 특성을 보여줍니다.')
        
        # Add element description
        element_desc = {
            'wood': '성장과 발전의 기운이 강합니다.',
            'fire': '열정과 활력이 돋보입니다.',
            'earth': '안정과 균형이 강조됩니다.',
            'metal': '결단력과 정의감이 강합니다.',
            'water': '지혜와 적응력이 뛰어납니다.'
        }
        
        element_addition = element_desc.get(dominant_element, '')
        
        return f"{base} {element_addition}"
    
    def generate_personality(self, saju: Dict, gender: str) -> str:
        """Generate personality interpretation"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        # Get base personality interpretation
        base = self.interpretations.get('day_stems', {}).get(
            day_stem, {}
        ).get('personality', '독특한 개성을 가지고 있습니다.')
        
        # Add gender-specific modifier
        gender_mod = self.interpretations.get('gender_modifiers', {}).get(
            gender, {}
        ).get(day_stem, '')
        
        if gender_mod:
            return f"{base} {gender_mod}"
        return base
    
    def generate_fortune(self, saju: Dict, elements: Dict) -> str:
        """Generate wealth and fortune interpretation"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        # Get base wealth interpretation
        base_fortune = self.interpretations.get('day_stems', {}).get(
            day_stem, {}
        ).get('wealth', '')
        
        if base_fortune:
            return base_fortune
        
        # Analyze based on elements
        metal_percentage = elements.get('metal', 0)
        water_percentage = elements.get('water', 0)
        
        # Fallback analysis based on elements
        if metal_percentage > 25:
            return '재물운이 강하며 부를 축적할 좋은 기회가 많습니다.'
        elif water_percentage > 25:
            return '재물이 자연스럽게 들어오지만 신중한 관리가 필요합니다.'
        else:
            return '꾸준한 노력으로 안정적인 재물 성장이 기대됩니다.'
    
    def generate_health(self, saju: Dict, elements: Dict) -> str:
        """Generate health interpretation"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        lacking_element = self._get_lacking_element(elements)
        
        # Get base health interpretation
        base_health = self.interpretations.get('day_stems', {}).get(
            day_stem, {}
        ).get('health', '')
        
        if base_health:
            return base_health
        
        # Fallback to element-based health advice
        health_advice = {
            'wood': 'Pay attention to liver and eye health. Regular exercise is beneficial.',
            'fire': 'Heart and circulation need attention. Manage stress levels.',
            'earth': 'Digestive system requires care. Maintain balanced diet.',
            'metal': 'Respiratory system needs attention. Fresh air is important.',
            'water': 'Kidney health is important. Stay well hydrated.'
        }
        
        return health_advice.get(lacking_element, '전반적인 건강 균형을 유지하세요.')
    
    def generate_career(self, saju: Dict, elements: Dict) -> str:
        """Generate career interpretation"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        dominant_element = self._get_dominant_element(elements)
        
        # Get base career interpretation
        base_career = self.interpretations.get('day_stems', {}).get(
            day_stem, {}
        ).get('career', '')
        
        if base_career:
            return base_career
        
        # Fallback to element-based career guide
        career_guide = {
            'wood': 'Education, healthcare, and creative fields are favorable.',
            'fire': 'Entertainment, marketing, and leadership roles suit you.',
            'earth': 'Real estate, agriculture, and stability-focused careers are good.',
            'metal': 'Finance, law, and technical fields are promising.',
            'water': 'Communication, travel, and flexible careers are beneficial.'
        }
        
        return career_guide.get(dominant_element, '다양한 직업 경로가 열려 있습니다.')
    
    def generate_relationships(self, saju: Dict, gender: str, elements: Dict) -> str:
        """Generate relationship interpretation"""
        day_stem = saju.get('day', {}).get('heavenly', '')
        
        # Get base relationship interpretation
        base_relationship = self.interpretations.get('day_stems', {}).get(
            day_stem, {}
        ).get('relationships', '')
        
        if base_relationship:
            return base_relationship
        
        # Fallback relationship description
        relationship_desc = 'Relationships are generally harmonious. '
        
        if gender == 'male':
            relationship_desc += 'Show understanding and patience with your partner.'
        else:
            relationship_desc += 'Communication and trust are key to happiness.'
        
        return relationship_desc
    
    def analyze_elements(self, elements: Dict) -> Dict:
        """Analyze element balance and provide advice"""
        dominant = self._get_dominant_element(elements)
        lacking = self._get_lacking_element(elements)
        
        # Calculate balance score
        ideal_percentage = 20
        total_deviation = sum(abs(elements.get(e, 0) - ideal_percentage) 
                            for e in ['wood', 'fire', 'earth', 'metal', 'water'])
        balance_score = max(0, 100 - total_deviation)
        
        return {
            'dominant_element': dominant,
            'dominant_percentage': elements.get(dominant, 0),
            'lacking_element': lacking,
            'lacking_percentage': elements.get(lacking, 0),
            'balance_score': balance_score,
            'balance_advice': self._generate_balance_advice(dominant, lacking),
            'element_distribution': elements
        }
    
    def find_special_patterns(self, saju: Dict) -> List[Dict]:
        """Find special patterns in the Saju"""
        patterns = []
        
        # Check for heavenly stem combinations
        stems = [
            saju.get('year', {}).get('heavenly', ''),
            saju.get('month', {}).get('heavenly', ''),
            saju.get('day', {}).get('heavenly', ''),
            saju.get('hour', {}).get('heavenly', '')
        ]
        
        # Check for earthly branch combinations
        branches = [
            saju.get('year', {}).get('earthly', ''),
            saju.get('month', {}).get('earthly', ''),
            saju.get('day', {}).get('earthly', ''),
            saju.get('hour', {}).get('earthly', '')
        ]
        
        # Simple pattern detection
        if len(set(stems)) < 3:
            patterns.append({
                'name': '천간 중복',
                'description': '동일한 천간이 여러 개 나타납니다',
                'effect': '특정 오행의 기운이 강하게 집중됩니다'
            })
        
        if len(set(branches)) < 3:
            patterns.append({
                'name': '지지 중복',
                'description': '동일한 지지가 여러 개 나타납니다',
                'effect': 'Concentrated energy pattern'
            })
        
        return patterns
    
    def generate_yearly_outlook(self, saju: Dict) -> str:
        """Generate yearly fortune outlook"""
        year_pillar = saju.get('year', {})
        
        if year_pillar:
            return '올해는 성장과 발전의 새로운 기회가 있습니다.'
        
        return '올해는 안정과 점진적인 발전에 집중하세요.'
    
    def _get_dominant_element(self, elements: Dict) -> str:
        """Get the dominant element"""
        if not elements:
            return 'earth'
        return max(elements.items(), key=lambda x: x[1])[0]
    
    def _get_lacking_element(self, elements: Dict) -> str:
        """Get the lacking element"""
        if not elements:
            return 'water'
        return min(elements.items(), key=lambda x: x[1])[0]
    
    def _generate_balance_advice(self, dominant: str, lacking: str) -> str:
        """Generate advice for element balance"""
        advice_map = {
            ('wood', 'metal'): '금(金) 기운을 보충하여 균형을 맞추세요',
            ('fire', 'water'): '수(水) 기운을 더해 열기를 식혀주세요',
            ('earth', 'wood'): '목(木) 기운을 보충하여 성장을 도모하세요',
            ('metal', 'fire'): '화(火) 기운을 더해 따뜻함을 가져오세요',
            ('water', 'earth'): '토(土) 기운을 보충하여 안정감을 높이세요'
        }
        
        return advice_map.get((dominant, lacking), 
                             '오행의 균형을 유지하여 조화를 이루세요')
    
    def _generate_ten_gods_interpretation(self, ten_gods_analysis: Dict, gender: str) -> Dict:
        """
        Generate personalized interpretation based on Ten Gods analysis
        
        Args:
            ten_gods_analysis: Ten Gods calculation results
            gender: 'male' or 'female'
            
        Returns:
            Dictionary containing personalized Ten Gods interpretations
        """
        if not ten_gods_analysis:
            return {}
        
        interpretation = {
            'overview': '',
            'personality': '',
            'career_guidance': '',
            'wealth_fortune': '',
            'relationship_advice': '',
            'life_strategy': '',
            'spiritual_message': ''
        }
        
        # Get key components from analysis
        dominant_gods = ten_gods_analysis.get('dominant_gods', [])
        lacking_gods = ten_gods_analysis.get('lacking_gods', [])
        balance = ten_gods_analysis.get('balance', {})
        category_strength = ten_gods_analysis.get('category_strength', {})
        relations = ten_gods_analysis.get('relations', {})
        
        # Generate overview based on balance status
        balance_status = balance.get('status', '균형')
        if balance_status == '균형':
            interpretation['overview'] = '십성이 균형을 이루어 조화로운 사주입니다. 각 분야에서 안정적인 발전이 가능합니다.'
        elif balance_status == '약간 불균형':
            interpretation['overview'] = '십성이 약간 치우쳐 있지만 보완 가능한 수준입니다. 부족한 부분을 의식적으로 개발하세요.'
        elif balance_status == '불균형':
            interpretation['overview'] = '십성의 불균형이 뚜렷합니다. 강한 부분을 활용하되 약한 부분을 보강하는 노력이 필요합니다.'
        else:
            interpretation['overview'] = '십성이 극도로 불균형합니다. 전문 분야에 집중하되 균형을 위한 의식적 노력이 중요합니다.'
        
        # Analyze personality based on dominant Ten Gods
        personality_traits = []
        for god in dominant_gods[:2]:  # Focus on top 2 dominant gods
            if '비견' in god or '겁재' in god:
                personality_traits.append('독립심이 강하고 자기주장이 뚜렷합니다')
            elif '식신' in god:
                personality_traits.append('창의적이고 예술적 감각이 뛰어납니다')
            elif '상관' in god:
                personality_traits.append('혁신적이고 개혁적인 성향이 강합니다')
            elif '정재' in god:
                personality_traits.append('성실하고 안정을 추구하는 성향입니다')
            elif '편재' in god:
                personality_traits.append('사업 수완이 있고 기회 포착 능력이 뛰어납니다')
            elif '정관' in god:
                personality_traits.append('책임감이 강하고 리더십이 있습니다')
            elif '편관' in god:
                personality_traits.append('추진력과 결단력이 뛰어납니다')
            elif '정인' in god:
                personality_traits.append('학구적이고 지혜로운 성향입니다')
            elif '편인' in god:
                personality_traits.append('직관적이고 영적 감각이 발달했습니다')
        
        interpretation['personality'] = ' '.join(personality_traits) if personality_traits else '균형잡힌 성격으로 다양한 재능을 보유하고 있습니다.'
        
        # Career guidance based on category strengths
        career_focus = []
        if category_strength.get('self', 0) > 30:
            career_focus.append('독립적인 사업이나 프리랜서 활동이 유리합니다')
        if category_strength.get('output', 0) > 30:
            career_focus.append('창의적인 분야나 교육, 예술 분야가 적합합니다')
        if category_strength.get('wealth', 0) > 30:
            career_focus.append('재무, 금융, 사업 분야에서 성공 가능성이 높습니다')
        if category_strength.get('power', 0) > 30:
            career_focus.append('관리직, 공직, 리더십 포지션이 적합합니다')
        if category_strength.get('resource', 0) > 30:
            career_focus.append('학술, 연구, 교육 분야에서 능력을 발휘할 수 있습니다')
        
        interpretation['career_guidance'] = ' '.join(career_focus) if career_focus else '다양한 분야에서 균형잡힌 능력을 발휘할 수 있습니다.'
        
        # Wealth fortune analysis
        wealth_strength = category_strength.get('wealth', 0)
        if wealth_strength > 40:
            interpretation['wealth_fortune'] = '재물운이 매우 강합니다. 다양한 수입원을 통해 부를 축적할 수 있으나, 과욕은 경계하세요.'
        elif wealth_strength > 20:
            interpretation['wealth_fortune'] = '안정적인 재물운을 가지고 있습니다. 꾸준한 노력으로 경제적 안정을 이룰 수 있습니다.'
        elif wealth_strength > 10:
            interpretation['wealth_fortune'] = '재물운이 약간 부족하지만, 전문성 개발을 통해 수입을 늘릴 수 있습니다.'
        else:
            interpretation['wealth_fortune'] = '재물보다는 다른 가치를 추구하는 것이 좋습니다. 정신적 만족이 물질적 성공보다 중요합니다.'
        
        # Relationship advice based on gender and Ten Gods
        if gender == 'male':
            wealth_gods = category_strength.get('wealth', 0)
            if wealth_gods > 30:
                interpretation['relationship_advice'] = '이성에게 인기가 많고 연애 기회가 많습니다. 진실된 관계를 선택하는 지혜가 필요합니다.'
            elif wealth_gods < 10:
                interpretation['relationship_advice'] = '연애보다 자기 계발에 집중하는 시기입니다. 자연스러운 만남을 기다리세요.'
            else:
                interpretation['relationship_advice'] = '안정적인 연애와 결혼이 가능합니다. 상대방을 존중하고 배려하는 마음이 중요합니다.'
        else:  # female
            power_gods = category_strength.get('power', 0)
            if power_gods > 30:
                interpretation['relationship_advice'] = '강한 매력으로 이성을 끌어당깁니다. 상대방의 내면을 보는 안목이 필요합니다.'
            elif power_gods < 10:
                interpretation['relationship_advice'] = '독립적인 삶을 추구하는 경향이 있습니다. 파트너와 균형잡힌 관계를 만들어가세요.'
            else:
                interpretation['relationship_advice'] = '조화로운 연애와 결혼생활이 가능합니다. 서로 성장하는 관계를 추구하세요.'
        
        # Life strategy based on lacking categories
        strategies = []
        if category_strength.get('self', 0) < 10:
            strategies.append('자신감과 독립성을 기르는 것이 중요합니다')
        if category_strength.get('output', 0) < 10:
            strategies.append('창의성과 표현력을 개발하세요')
        if category_strength.get('wealth', 0) < 10:
            strategies.append('경제 관념과 재테크 능력을 키우세요')
        if category_strength.get('power', 0) < 10:
            strategies.append('리더십과 책임감을 발전시키세요')
        if category_strength.get('resource', 0) < 10:
            strategies.append('지속적인 학습과 정신적 성장을 추구하세요')
        
        interpretation['life_strategy'] = ' '.join(strategies[:2]) if strategies else '현재의 강점을 최대한 활용하면서 균형잡힌 삶을 추구하세요.'
        
        # Spiritual message
        if balance_status == '균형':
            interpretation['spiritual_message'] = '내면의 조화를 유지하며 주변과 함께 성장하는 삶을 살아가세요.'
        else:
            interpretation['spiritual_message'] = '자신의 독특함을 인정하고 수용하며, 부족한 부분은 겸손하게 배워나가세요.'
        
        return interpretation


# Helper functions
def get_interpretation(saju: Dict, elements: Dict, gender: str) -> Dict:
    """
    Convenience function to get interpretation
    
    Args:
        saju: Saju calculation result
        elements: Element analysis result
        gender: 'male' or 'female'
    
    Returns:
        Complete interpretation dictionary
    """
    interpreter = Interpreter()
    return interpreter.generate_interpretation(saju, elements, gender)