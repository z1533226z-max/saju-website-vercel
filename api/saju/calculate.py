"""
Vercel Function for Saju calculation
"""
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _core.saju_calculator import SajuCalculator
from _core.elements import ElementsAnalyzer
from _core.interpretation import Interpreter
from _core.lunar_converter_improved import ImprovedLunarConverter

def handler(req, res):
    """Handle request for Saju calculation"""
    
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
        interpreter = Interpreter()
        lunar_converter = ImprovedLunarConverter()
        
        # Input validation
        required_fields = ['birthDate', 'birthTime', 'gender']
        for field in required_fields:
            if field not in data:
                return res.status(400).json({'error': f'{field}가 필요합니다'})
        
        # Parse date
        birth_date = datetime.strptime(data['birthDate'], '%Y-%m-%d')
        birth_time = data['birthTime']
        gender = data['gender']
        is_lunar = data.get('isLunar', False)
        
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
        
        # Get interpretation
        interpretation_result = interpreter.interpret(saju_result, elements_result)
        
        # Format response
        response_data = {
            'saju': saju_result,
            'elements': elements_result['percentages'],
            'elements_detail': elements_result,
            'interpretation': interpretation_result,
            'input': {
                'birthDate': data['birthDate'],
                'birthTime': birth_time,
                'gender': gender,
                'isLunar': is_lunar
            }
        }
        
        return res.status(200).json(response_data)
        
    except Exception as e:
        print(f"Error in calculate handler: {str(e)}")
        return res.status(500).json({'error': str(e)})
