#\!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lunar Calendar Converter Module
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import lunarcalendar


class LunarConverter:
    """Lunar-Solar calendar converter class"""
    
    def __init__(self):
        """Initialize converter"""
        self.min_year = 1900
        self.max_year = 2100
        
    def lunar_to_solar(self, year: int, month: int, day: int, 
                       is_leap_month: bool = False) -> datetime:
        """Convert lunar date to solar date"""
        try:
            lunar = lunarcalendar.Lunar(year, month, day, isleap=is_leap_month)
            solar = lunarcalendar.Converter.Lunar2Solar(lunar)
            return datetime(solar.year, solar.month, solar.day)
        except Exception as e:
            raise ValueError(f"Lunar conversion error: {str(e)}")
    
    def solar_to_lunar(self, date: datetime) -> Dict:
        """Convert solar date to lunar date"""
        try:
            solar = lunarcalendar.Solar(date.year, date.month, date.day)
            lunar = lunarcalendar.Converter.Solar2Lunar(solar)
            return {
                'year': lunar.year,
                'month': lunar.month,
                'day': lunar.day,
                'is_leap_month': lunar.isleap
            }
        except Exception as e:
            raise ValueError(f"Solar conversion error: {str(e)}")
    
    def validate_lunar_date(self, year: int, month: int, day: int,
                           is_leap_month: bool = False) -> bool:
        """Validate lunar date"""
        if not (self.min_year <= year <= self.max_year):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 30):
            return False
        
        try:
            self.lunar_to_solar(year, month, day, is_leap_month)
            return True
        except:
            return False
    
    def get_leap_month(self, year: int) -> Optional[int]:
        """Get leap month for a year"""
        for month in range(1, 13):
            try:
                self.lunar_to_solar(year, month, 1, is_leap_month=True)
                return month
            except:
                continue
        return None
    
    def get_lunar_new_year(self, year: int) -> datetime:
        """Get Lunar New Year date"""
        return self.lunar_to_solar(year, 1, 1, False)
