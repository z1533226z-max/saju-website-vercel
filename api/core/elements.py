# -*- coding: utf-8 -*-
"""
Five Elements Analysis Module
Analyzes the distribution and balance of the five elements in a Saju
"""

from typing import Dict, List, Tuple
import json
import os


class ElementsAnalyzer:
    """
    Analyzes the five elements distribution in a Saju calculation
    """
    
    def __init__(self):
        """Initialize the elements analyzer with mapping data"""
        self.element_mapping = self._load_element_mapping()
        
    def _load_element_mapping(self) -> Dict:
        """Load element mapping from JSON file"""
        base_path = os.path.dirname(os.path.dirname(__file__))
        mapping_path = os.path.join(base_path, 'data', 'elements_mapping.json')
        
        try:
            with open(mapping_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback mapping if file not found
            return self._get_default_mapping()
    
    def _get_default_mapping(self) -> Dict:
        """Get default element mapping"""
        return {
            'heavenly_stems': {
                '갑': 'wood', '을': 'wood',
                '병': 'fire', '정': 'fire',
                '무': 'earth', '기': 'earth',
                '경': 'metal', '신': 'metal',
                '임': 'water', '계': 'water'
            },
            'earthly_branches': {
                '자': 'water', '축': 'earth',
                '인': 'wood', '묘': 'wood',
                '진': 'earth', '사': 'fire',
                '오': 'fire', '미': 'earth',
                '신': 'metal', '유': 'metal',
                '술': 'earth', '해': 'water'
            }
        }
    
    def analyze_elements(self, saju: Dict) -> Dict[str, float]:
        """
        Analyze the element distribution in a Saju
        
        Args:
            saju: Dictionary containing four pillars
            
        Returns:
            Dictionary with element percentages
        """
        elements_count = {
            'wood': 0,
            'fire': 0,
            'earth': 0,
            'metal': 0,
            'water': 0
        }
        
        # Get the actual mapping
        if 'heavenly_stems' not in self.element_mapping:
            self.element_mapping = self._get_default_mapping()
        
        # Count elements from four pillars
        pillars = ['year', 'month', 'day', 'hour']
        total_count = 0
        
        for pillar in pillars:
            if pillar in saju:
                # Heavenly stem
                heavenly = saju[pillar].get('heavenly', '')
                if heavenly in self.element_mapping['heavenly_stems']:
                    element = self.element_mapping['heavenly_stems'][heavenly]
                    elements_count[element] += 1
                    total_count += 1
                
                # Earthly branch
                earthly = saju[pillar].get('earthly', '')
                if earthly in self.element_mapping['earthly_branches']:
                    element = self.element_mapping['earthly_branches'][earthly]
                    elements_count[element] += 1
                    total_count += 1
        
        # Convert to percentages
        if total_count == 0:
            # Return equal distribution if no valid data
            return {element: 20.0 for element in elements_count}
        
        percentages = {}
        for element, count in elements_count.items():
            percentages[element] = (count / total_count) * 100
        
        return percentages
    
    def analyze_balance(self, elements: Dict[str, float]) -> Dict:
        """
        Analyze the balance of elements
        
        Args:
            elements: Dictionary with element percentages
            
        Returns:
            Analysis of element balance
        """
        # Find dominant and lacking elements
        dominant = max(elements.items(), key=lambda x: x[1])
        lacking = min(elements.items(), key=lambda x: x[1])
        
        # Calculate balance score (0-100, where 100 is perfect balance)
        ideal_percentage = 20.0
        total_deviation = sum(abs(percentage - ideal_percentage) 
                            for percentage in elements.values())
        balance_score = max(0, 100 - total_deviation)
        
        # Determine balance status
        if balance_score >= 80:
            status = 'excellent'
        elif balance_score >= 60:
            status = 'good'
        elif balance_score >= 40:
            status = 'moderate'
        else:
            status = 'imbalanced'
        
        return {
            'dominant_element': dominant[0],
            'dominant_percentage': dominant[1],
            'lacking_element': lacking[0],
            'lacking_percentage': lacking[1],
            'balance_score': balance_score,
            'balance_status': status,
            'recommendation': self._get_balance_recommendation(dominant[0], lacking[0])
        }
    
    def _get_balance_recommendation(self, dominant: str, lacking: str) -> str:
        """Get recommendation for element balance"""
        recommendations = {
            ('wood', 'metal'): 'Balance with metal element',
            ('fire', 'water'): 'Balance with water element',
            ('earth', 'wood'): 'Balance with wood element',
            ('metal', 'fire'): 'Balance with fire element',
            ('water', 'earth'): 'Balance with earth element'
        }
        
        return recommendations.get((dominant, lacking), 
                                  f'Balance {lacking} element for harmony')
    
    def get_element_characteristics(self, element: str) -> Dict:
        """
        Get characteristics of a specific element
        
        Args:
            element: Element name (wood, fire, earth, metal, water)
            
        Returns:
            Dictionary with element characteristics
        """
        if not self.element_mapping or 'characteristics' not in self.element_mapping:
            # Load or use default characteristics
            characteristics = {
                'wood': 'Growth, development, flexibility',
                'fire': 'Passion, vitality, expansion',
                'earth': 'Stability, balance, inclusiveness',
                'metal': 'Justice, determination, convergence',
                'water': 'Wisdom, fluidity, adaptation'
            }
        else:
            characteristics = self.element_mapping.get('characteristics', {})
        
        colors = {
            'wood': ['green', 'blue'],
            'fire': ['red', 'purple'],
            'earth': ['yellow', 'brown'],
            'metal': ['white', 'gray'],
            'water': ['black', 'dark blue']
        }
        
        seasons = {
            'wood': 'spring',
            'fire': 'summer',
            'earth': 'late_summer',
            'metal': 'autumn',
            'water': 'winter'
        }
        
        return {
            'element': element,
            'characteristics': characteristics.get(element, ''),
            'colors': colors.get(element, []),
            'season': seasons.get(element, ''),
            'direction': self._get_element_direction(element)
        }
    
    def _get_element_direction(self, element: str) -> str:
        """Get the direction associated with an element"""
        directions = {
            'wood': 'east',
            'fire': 'south',
            'earth': 'center',
            'metal': 'west',
            'water': 'north'
        }
        return directions.get(element, '')


# Convenience functions
def analyze_saju_elements(saju: Dict) -> Dict[str, float]:
    """
    Convenience function to analyze elements in a Saju
    
    Args:
        saju: Saju calculation result
        
    Returns:
        Element percentages
    """
    analyzer = ElementsAnalyzer()
    return analyzer.analyze_elements(saju)


def get_element_balance(elements: Dict[str, float]) -> Dict:
    """
    Convenience function to analyze element balance
    
    Args:
        elements: Element percentages
        
    Returns:
        Balance analysis
    """
    analyzer = ElementsAnalyzer()
    return analyzer.analyze_balance(elements)