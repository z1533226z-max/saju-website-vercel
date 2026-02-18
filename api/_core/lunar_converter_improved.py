#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improved Lunar Calendar Converter Module
음력 변환 개선 버전 - 오류 처리 강화
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import logging
import lunarcalendar

logger = logging.getLogger('saju')


class ImprovedLunarConverter:
    """개선된 음력-양력 변환 클래스"""
    
    def __init__(self):
        """Initialize converter"""
        self.min_year = 1900
        self.max_year = 2100
        
        # 음력 월별 일수 (평년 기준, 윤달 제외)
        # 실제로는 매년 다르지만 대략적인 범위
        self.lunar_month_days = {
            1: [29, 30], 2: [29, 30], 3: [29, 30], 
            4: [29, 30], 5: [29, 30], 6: [29, 30],
            7: [29, 30], 8: [29, 30], 9: [29, 30],
            10: [29, 30], 11: [29, 30], 12: [29, 30]
        }
    
    def lunar_to_solar(self, year: int, month: int, day: int, 
                       is_leap_month: bool = False) -> Optional[datetime]:
        """
        음력을 양력으로 변환 (개선된 오류 처리)
        
        Args:
            year: 음력 연도
            month: 음력 월 (1-12)
            day: 음력 일 (1-30)
            is_leap_month: 윤달 여부
            
        Returns:
            datetime 객체 또는 None (변환 실패 시)
        """
        try:
            # 기본 범위 검사
            if not (self.min_year <= year <= self.max_year):
                logger.warning(f" 연도 범위 초과: {year}")
                return None
                
            if not (1 <= month <= 12):
                logger.warning(f" 잘못된 월: {month}")
                return None
                
            # 일반적으로 음력은 29일 또는 30일
            if not (1 <= day <= 30):
                logger.warning(f" 잘못된 일: {day}")
                return None
            
            # 윤달 검증
            if is_leap_month:
                leap_month = self.get_leap_month(year)
                if leap_month != month:
                    logger.warning(f" {year}년 {month}월은 윤달이 아님 (윤달: {leap_month}월)")
                    # 윤달이 아닌 경우 일반 달로 처리
                    is_leap_month = False
            
            # 실제 변환 시도
            lunar = lunarcalendar.Lunar(year, month, day, isleap=is_leap_month)
            solar = lunarcalendar.Converter.Lunar2Solar(lunar)
            return datetime(solar.year, solar.month, solar.day)
            
        except Exception as e:
            # 상세한 오류 정보 제공
            logger.error(f" 음력 변환 실패: {year}-{month:02d}-{day:02d} (윤달:{is_leap_month})")
            logger.error(f" 원인: {str(e)}")
            
            # 대체 처리: 날짜 조정 시도
            if day == 30:
                logger.debug(f" 29일로 재시도...")
                try:
                    lunar = lunarcalendar.Lunar(year, month, 29, isleap=is_leap_month)
                    solar = lunarcalendar.Converter.Lunar2Solar(lunar)
                    result = datetime(solar.year, solar.month, solar.day)
                    logger.info(f" 29일로 변환 성공: {result.strftime('%Y-%m-%d')}")
                    return result
                except Exception:
                    pass
                    
            return None
    
    def solar_to_lunar(self, date: datetime) -> Dict:
        """양력을 음력으로 변환"""
        try:
            solar = lunarcalendar.Solar(date.year, date.month, date.day)
            lunar = lunarcalendar.Converter.Solar2Lunar(solar)
            return {
                'year': lunar.year,
                'month': lunar.month,
                'day': lunar.day,
                'is_leap_month': lunar.isleap,
                'success': True
            }
        except Exception as e:
            logger.error(f" 양력 변환 실패: {date}")
            return {
                'year': date.year,
                'month': date.month,
                'day': date.day,
                'is_leap_month': False,
                'success': False,
                'error': str(e)
            }
    
    def validate_lunar_date(self, year: int, month: int, day: int,
                           is_leap_month: bool = False) -> bool:
        """
        음력 날짜 유효성 검사 (개선된 버전)
        실제 변환을 시도하여 정확한 검증
        """
        if not (self.min_year <= year <= self.max_year):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 30):
            return False
        
        # 실제 변환 시도로 검증
        try:
            lunar = lunarcalendar.Lunar(year, month, day, isleap=is_leap_month)
            lunarcalendar.Converter.Lunar2Solar(lunar)
            return True
        except Exception:
            return False

    def get_leap_month(self, year: int) -> Optional[int]:
        """해당 연도의 윤달 확인"""
        for month in range(1, 13):
            try:
                lunar = lunarcalendar.Lunar(year, month, 1, isleap=True)
                lunarcalendar.Converter.Lunar2Solar(lunar)
                return month
            except Exception:
                continue
        return None

    def get_lunar_month_days(self, year: int, month: int, is_leap: bool = False) -> int:
        """
        특정 음력 월의 일수 확인
        """
        # 29일과 30일 시도
        for day in [30, 29]:
            try:
                lunar = lunarcalendar.Lunar(year, month, day, isleap=is_leap)
                lunarcalendar.Converter.Lunar2Solar(lunar)
                return day
            except Exception:
                continue
        return 29  # 기본값
    
    def smart_convert(self, date_str: str, is_lunar: bool = False) -> Dict:
        """
        스마트 변환: 문자열 입력을 받아 안전하게 변환
        
        Args:
            date_str: 'YYYY-MM-DD' 형식의 날짜 문자열
            is_lunar: 음력 여부
            
        Returns:
            변환 결과 딕셔너리
        """
        try:
            parts = date_str.split('-')
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            
            if is_lunar:
                # 음력 -> 양력 변환
                result = self.lunar_to_solar(year, month, day)
                if result:
                    return {
                        'success': True,
                        'original': date_str,
                        'converted': result.strftime('%Y-%m-%d'),
                        'datetime': result,
                        'type': 'lunar_to_solar'
                    }
                else:
                    # 실패 시 원본 반환
                    return {
                        'success': False,
                        'original': date_str,
                        'converted': date_str,
                        'datetime': datetime.strptime(date_str, '%Y-%m-%d'),
                        'type': 'failed_conversion',
                        'message': '음력 변환 실패, 원본 날짜 사용'
                    }
            else:
                # 양력은 그대로 반환
                return {
                    'success': True,
                    'original': date_str,
                    'converted': date_str,
                    'datetime': datetime.strptime(date_str, '%Y-%m-%d'),
                    'type': 'solar'
                }
                
        except Exception as e:
            return {
                'success': False,
                'original': date_str,
                'error': str(e),
                'type': 'error'
            }
    
    def get_lunar_new_year(self, year: int) -> datetime:
        """설날 날짜 반환"""
        result = self.lunar_to_solar(year, 1, 1, False)
        return result if result else datetime(year, 2, 1)  # 대략적인 설날


# 테스트 코드
if __name__ == "__main__":
    converter = ImprovedLunarConverter()
    
    print("="*60)
    print("개선된 음력 변환기 테스트")
    print("="*60)
    
    test_cases = [
        ("2024-01-01", True),   # 2024년 음력 1월 1일
        ("2023-08-15", True),   # 2023년 음력 8월 15일
        ("1990-05-15", True),   # 1990년 음력 5월 15일
        ("2023-01-30", True),   # 존재하지 않는 날짜
        ("2024-05-15", False),  # 양력
    ]
    
    for date_str, is_lunar in test_cases:
        result = converter.smart_convert(date_str, is_lunar)
        print(f"\n입력: {date_str} ({'음력' if is_lunar else '양력'})")
        print(f"성공: {result.get('success')}")
        print(f"변환: {result.get('converted')}")
        if not result.get('success'):
            print(f"메시지: {result.get('message', result.get('error'))}")
