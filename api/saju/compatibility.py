"""
Vercel Function for Compatibility calculation
"""
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _core.saju_calculator import SajuCalculator
from _core.elements import ElementsAnalyzer
from _core.compatibility import CompatibilityAnalyzer
from _core.lunar_converter_improved import ImprovedLunarConverter

def handler(req, res):
    """Handle request for compatibility calculation"""
    
    # Handle CORS
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
    
    if req.method == 'OPTIONS':
        return res.status(200).send('')
    
    if req.method != 'POST':
        return res.status(405).json({'error': 'Method not allowed'})
    
    try:
        data = req.body
        
        # Initialize components
        saju_calculator = SajuCalculator()
        elements_analyzer = ElementsAnalyzer()
        compatibility_analyzer = CompatibilityAnalyzer()
        lunar_converter = ImprovedLunarConverter()
        
        # Process both persons
        persons = []
        for person_key in ['person1', 'person2']:
            person_data = data[person_key]
            
            # Parse date
            birth_date = datetime.strptime(person_data['birthDate'], '%Y-%m-%d')
            birth_time = person_data['birthTime']
            is_lunar = person_data.get('isLunar', False)
            
            # Convert lunar to solar if needed
            if is_lunar:
                try:
                    converted_date = lunar_converter.lunar_to_solar(
                        birth_date.year, birth_date.month, birth_date.day
                    )
                    if converted_date:
                        birth_date = datetime(converted_date[0], converted_date[1], converted_date[2])
                except:
                    pass
            
            # Calculate Saju
            saju_result = saju_calculator.calculate_saju(
                birth_date.year,
                birth_date.month,
                birth_date.day,
                birth_time
            )
            
            # Analyze elements
            elements_result = elements_analyzer.analyze_elements(saju_result)
            
            persons.append({
                'saju': saju_result,
                'elements': elements_result
            })
        
        # Calculate compatibility
        compatibility_result = compatibility_analyzer.analyze_compatibility(
            persons[0]['saju'],
            persons[1]['saju'],
            persons[0]['elements'],
            persons[1]['elements']
        )
        
        # Format response
        response_data = {
            'person1': persons[0],
            'person2': persons[1],
            'compatibility': compatibility_result
        }
        
        return res.status(200).json(response_data)
        
    except Exception as e:
        print(f"Error in compatibility handler: {str(e)}")
        return res.status(500).json({'error': str(e)})
