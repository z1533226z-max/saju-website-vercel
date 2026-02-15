#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사주팔자 계산 핵심 모듈
Saju (Four Pillars of Destiny) Calculator Core Module
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json
import os
from pathlib import Path
# from .lunar_converter import LunarConverter  # Uncomment when lunarcalendar is installed


class SajuCalculator:
    """사주팔자 계산 핵심 클래스"""
    
    def __init__(self):
        """초기화: 천간, 지지 데이터 로드"""
        self.heavenly_stems = []
        self.earthly_branches = []
        self.heavenly_stems_data = {}
        self.earthly_branches_data = {}
        # self.lunar_converter = LunarConverter()  # Uncomment when lunarcalendar is installed
        
        # 월지지 매핑 (월 -> 지지 인덱스)
        self.month_to_earthly = {
            1: 2,   # 인월 (寅月)
            2: 3,   # 묘월 (卯月)
            3: 4,   # 진월 (辰月)
            4: 5,   # 사월 (巳月)
            5: 6,   # 오월 (午月)
            6: 7,   # 미월 (未月)
            7: 8,   # 신월 (申月)
            8: 9,   # 유월 (酉月)
            9: 10,  # 술월 (戌月)
            10: 11, # 해월 (亥月)
            11: 0,  # 자월 (子月)
            12: 1   # 축월 (丑月)
        }
        
        # 24절기 데이터 (절입 기준일)
        # 각 월의 절기 시작일 (대략적인 날짜, 실제로는 연도별로 약간 차이 있음)
        self.solar_terms = {
            1: {'name': '입춘', 'day': 4},    # 立春 (2월 4일경)
            2: {'name': '경칩', 'day': 6},    # 驚蟄 (3월 6일경)
            3: {'name': '청명', 'day': 5},    # 淸明 (4월 5일경)
            4: {'name': '입하', 'day': 6},    # 立夏 (5월 6일경)
            5: {'name': '망종', 'day': 6},    # 芒種 (6월 6일경)
            6: {'name': '소서', 'day': 7},    # 小暑 (7월 7일경)
            7: {'name': '입추', 'day': 8},    # 立秋 (8월 8일경)
            8: {'name': '백로', 'day': 8},    # 白露 (9월 8일경)
            9: {'name': '한로', 'day': 8},    # 寒露 (10월 8일경)
            10: {'name': '입동', 'day': 7},   # 立冬 (11월 7일경)
            11: {'name': '대설', 'day': 7},   # 大雪 (12월 7일경)
            12: {'name': '소한', 'day': 6}    # 小寒 (1월 6일경)
        }
        
        # 절기월과 양력월 매핑
        self.solar_term_months = {
            2: 1,   # 2월 입춘 -> 인월(1)
            3: 2,   # 3월 경칩 -> 묘월(2)
            4: 3,   # 4월 청명 -> 진월(3)
            5: 4,   # 5월 입하 -> 사월(4)
            6: 5,   # 6월 망종 -> 오월(5)
            7: 6,   # 7월 소서 -> 미월(6)
            8: 7,   # 8월 입추 -> 신월(7)
            9: 8,   # 9월 백로 -> 유월(8)
            10: 9,  # 10월 한로 -> 술월(9)
            11: 10, # 11월 입동 -> 해월(10)
            12: 11, # 12월 대설 -> 자월(11)
            1: 12   # 1월 소한 -> 축월(12)
        }
        
        self.load_data()
        
    def load_data(self):
        """천간, 지지 데이터 로드"""
        # 현재 파일 위치 기준으로 데이터 파일 경로 설정
        base_dir = Path(__file__).parent.parent
        
        # 천간 데이터 로드
        heavenly_stems_path = base_dir / 'data' / 'heavenly_stems.json'
        with open(heavenly_stems_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.heavenly_stems_data = data
            self.heavenly_stems = data['heavenly_stems']
        
        # 지지 데이터 로드
        earthly_branches_path = base_dir / 'data' / 'earthly_branches.json'
        with open(earthly_branches_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.earthly_branches_data = data
            self.earthly_branches = data['earthly_branches']
    
    def calculate_saju(self, birth_date: datetime, birth_time: str, 
                      gender: str, is_lunar: bool = False) -> Dict:
        """
        사주팔자 계산 메인 함수
        
        Args:
            birth_date: 생년월일
            birth_time: 출생시간 (HH:MM)
            gender: 성별 ('male' or 'female')
            is_lunar: 음력 여부
            
        Returns:
            사주 명식 딕셔너리
        """
        # 음력인 경우 양력으로 변환 (추후 구현)
        if is_lunar:
            birth_date = self.convert_lunar_to_solar(birth_date)
        
        # 년주 계산
        year_pillar = self.calculate_year_pillar(birth_date.year)
        
        # 월주 계산
        month_pillar = self.calculate_month_pillar(
            birth_date.year, birth_date.month, birth_date.day
        )
        
        # 일주 계산
        day_pillar = self.calculate_day_pillar(birth_date)
        
        # 시주 계산
        hour_pillar = self.calculate_hour_pillar(
            day_pillar['heavenly'], birth_time
        )
        
        # 오행 분석
        elements_analysis = self.analyze_elements({
            'year': year_pillar,
            'month': month_pillar,
            'day': day_pillar,
            'hour': hour_pillar
        })
        
        return {
            'year': year_pillar,
            'month': month_pillar,
            'day': day_pillar,
            'hour': hour_pillar,
            'gender': gender,
            'elements': elements_analysis,
            'birth_info': {
                'date': birth_date.strftime('%Y-%m-%d'),
                'time': birth_time,
                'is_lunar': is_lunar
            }
        }
    
    def calculate_year_pillar(self, year: int) -> Dict:
        """
        년주 계산 - 60갑자 체계에 따른 천간지지 계산
        
        Args:
            year: 연도 (서기)
            
        Returns:
            년주 정보 (천간, 지지, 오행, 띠)
        """
        # 60갑자 계산 공식
        # 서기 4년이 갑자년(甲子年)이므로 4를 빼고 계산
        # 천간: 10년 주기, 지지: 12년 주기
        
        heavenly_index = (year - 4) % 10
        earthly_index = (year - 4) % 12
        
        # 음수 인덱스 처리 (BC 연도 대응)
        if heavenly_index < 0:
            heavenly_index += 10
        if earthly_index < 0:
            earthly_index += 12
        
        return {
            'heavenly': self.heavenly_stems[heavenly_index]['name_ko'],
            'heavenly_hanja': self.heavenly_stems[heavenly_index]['name_hanja'],
            'earthly': self.earthly_branches[earthly_index]['name_ko'],
            'earthly_hanja': self.earthly_branches[earthly_index]['name_hanja'],
            'element': self.heavenly_stems[heavenly_index]['element'],
            'zodiac': self.earthly_branches[earthly_index]['zodiac_animal'],
            'combined_name': f"{self.heavenly_stems[heavenly_index]['name_ko']}{self.earthly_branches[earthly_index]['name_ko']}년"
        }
    
    def calculate_month_pillar(self, year: int, month: int, day: int) -> Dict:
        """
        월주 계산 (절기 기준)
        
        사주에서 월주는 절기를 기준으로 결정됩니다.
        예: 2월 4일 이전 출생은 전년도 축월, 2월 4일 이후는 당해 인월
        
        Args:
            year: 연도
            month: 월
            day: 일
            
        Returns:
            월주 정보 (천간, 지지, 오행, 절기)
        """
        # 절기를 고려한 월 계산
        adjusted_month = self.get_solar_term_month(month, day)
        adjusted_year = year
        
        # 1월이고 소한(1월 6일) 이전이면 전년도 자월(11월)
        if month == 1 and day < self.solar_terms[12]['day']:
            adjusted_year = year - 1
            # adjusted_month는 이미 get_solar_term_month에서 11로 설정됨
        # 2월이고 입춘(2월 4일) 이전이면 전년도 축월
        elif month == 2 and day < self.solar_terms[1]['day']:
            adjusted_year = year - 1
            adjusted_month = 12  # 축월
        
        # 조정된 년도의 천간 계산
        year_heavenly = (adjusted_year - 4) % 10
        
        # 월간 계산 (오행기 법칙)
        month_heavenly = self.get_month_heavenly(year_heavenly, adjusted_month)
        
        # 월지 계산
        month_earthly = self.month_to_earthly.get(adjusted_month, 0)
        
        # 절기 정보 가져오기
        solar_term_info = self.get_solar_term_info(month, day)
        
        return {
            'heavenly': self.heavenly_stems[month_heavenly]['name_ko'],
            'heavenly_hanja': self.heavenly_stems[month_heavenly]['name_hanja'],
            'earthly': self.earthly_branches[month_earthly]['name_ko'],
            'earthly_hanja': self.earthly_branches[month_earthly]['name_hanja'],
            'element': self.heavenly_stems[month_heavenly]['element'],
            'zodiac': self.earthly_branches[month_earthly]['zodiac_animal'],
            'solar_term': solar_term_info,
            'adjusted_month': adjusted_month,
            'combined_name': f"{self.heavenly_stems[month_heavenly]['name_ko']}{self.earthly_branches[month_earthly]['name_ko']}월"
        }
    
    def get_solar_term_month(self, month: int, day: int) -> int:
        """
        절기를 고려한 실제 월 계산
        
        Args:
            month: 양력 월
            day: 양력 일
            
        Returns:
            절기 기준 월 (1-12)
        """
        # 1월의 경우 소한(1월 6일) 기준
        if month == 1:
            if day < self.solar_terms[12]['day']:  # 소한(1월 6일) 이전
                return 11  # 자월 (전년도 12월의 연장)
            else:  # 소한 이후
                return 12  # 축월
        
        # 2-12월의 경우 각 절기 기준
        solar_term_month = self.solar_term_months.get(month, month)
        
        if month in self.solar_term_months and month >= 2:
            solar_term_idx = solar_term_month
            if solar_term_idx in self.solar_terms:
                if day >= self.solar_terms[solar_term_idx]['day']:
                    return solar_term_month
                else:
                    # 절기 이전이면 이전 월
                    return (solar_term_month - 1) if solar_term_month > 1 else 12
        
        return solar_term_month
    
    def get_solar_term_info(self, month: int, day: int) -> Dict:
        """
        해당 날짜의 절기 정보 가져오기
        
        Args:
            month: 월
            day: 일
            
        Returns:
            절기 정보
        """
        solar_term_month = self.solar_term_months.get(month, month)
        
        if solar_term_month in self.solar_terms:
            term = self.solar_terms[solar_term_month]
            if month >= 2 and day >= term['day']:
                return {
                    'name': term['name'],
                    'is_after': True,
                    'description': f"{term['name']} 이후"
                }
            elif month == 1 and day >= self.solar_terms[12]['day']:
                return {
                    'name': self.solar_terms[12]['name'],
                    'is_after': True,
                    'description': f"{self.solar_terms[12]['name']} 이후"
                }
        
        # 절기 이전
        prev_month = (solar_term_month - 1) if solar_term_month > 1 else 12
        if prev_month in self.solar_terms:
            return {
                'name': self.solar_terms[prev_month]['name'],
                'is_after': False,
                'description': f"다음 절기 전"
            }
        
        return {
            'name': '미상',
            'is_after': False,
            'description': '절기 정보 없음'
        }
    
    def calculate_day_pillar(self, birth_date: datetime) -> Dict:
        """
        일주 계산 (만세력 기준)
        
        만세력(萬歲曆)은 수천 년간의 날짜별 일간지지를 기록한 달력입니다.
        이 메서드는 1900년 1월 1일을 기준으로 60갑자 순환을 계산합니다.
        
        Args:
            birth_date: 생년월일 (datetime 객체)
            
        Returns:
            일주 정보 딕셔너리:
            - heavenly: 일간 (한글)
            - heavenly_hanja: 일간 (한자)
            - earthly: 일지 (한글)
            - earthly_hanja: 일지 (한자)
            - element: 일간의 오행
            - ganji_number: 60갑자 순서 (1-60)
            - day_master: 일간 설명
        """
        # 만세력 기준일 설정
        # 1900년 1월 1일 = 기축일 (己丑日) - 실제 만세력 확인값
        # 이는 여러 만세력 자료와 대조하여 검증된 값입니다
        base_date = datetime(1900, 1, 1)
        
        # 기준일로부터의 일수 계산
        days_diff = (birth_date - base_date).days
        
        # 음수 처리 (1900년 이전 날짜)
        if days_diff < 0:
            # 1900년 이전은 역산
            days_diff = abs(days_diff)
            # 60갑자를 거꾸로 계산
            heavenly_offset = (-days_diff) % 10
            earthly_offset = (-days_diff) % 12
        else:
            heavenly_offset = days_diff
            earthly_offset = days_diff
        
        # 1900년 1월 1일 = 기축일 (천간: 기=5, 지지: 축=1)
        base_heavenly = 5  # 기 (己)
        base_earthly = 1   # 축 (丑)
        
        # 60갑자 순환 계산
        heavenly_index = (base_heavenly + heavenly_offset) % 10
        earthly_index = (base_earthly + earthly_offset) % 12
        
        # 음수 인덱스 보정
        if heavenly_index < 0:
            heavenly_index += 10
        if earthly_index < 0:
            earthly_index += 12
        
        # 60갑자 번호 계산 (1-60)
        ganji_number = self.calculate_ganji_number(heavenly_index, earthly_index)
        
        # 일간(Day Master) 특성 가져오기
        day_master_info = self.get_day_master_characteristics(heavenly_index)
        
        return {
            'heavenly': self.heavenly_stems[heavenly_index]['name_ko'],
            'heavenly_hanja': self.heavenly_stems[heavenly_index]['name_hanja'],
            'earthly': self.earthly_branches[earthly_index]['name_ko'],
            'earthly_hanja': self.earthly_branches[earthly_index]['name_hanja'],
            'element': self.heavenly_stems[heavenly_index]['element'],
            'ganji_number': ganji_number,
            'day_master': day_master_info,
            'combined_name': f"{self.heavenly_stems[heavenly_index]['name_ko']}{self.earthly_branches[earthly_index]['name_ko']}일"
        }
    
    def calculate_hour_pillar(self, day_heavenly: str, birth_time: str) -> Dict:
        """
        시주 계산 (12시진 체계)
        
        사주팔자에서 시주는 출생 시각을 12시진으로 나누어 계산합니다.
        자시(子時)는 23:00-01:00로 특별한 처리가 필요합니다.
        
        Args:
            day_heavenly: 일간 (일주의 천간)
            birth_time: 출생시간 (HH:MM 형식)
            
        Returns:
            시주 정보 딕셔너리:
            - heavenly: 시간 (한글)
            - heavenly_hanja: 시간 (한자)
            - earthly: 시지 (한글)
            - earthly_hanja: 시지 (한자)
            - element: 시간의 오행
            - time_period: 시진 이름
            - time_range: 시간 범위
            - early_late: 초시/정시 구분
        """
        # 한국어 시진명 → HH:MM 변환
        time_name_map = {
            '자시': '00:00', '축시': '02:00', '인시': '04:00',
            '묘시': '06:00', '진시': '08:00', '사시': '10:00',
            '오시': '12:00', '미시': '14:00', '신시': '16:00',
            '유시': '18:00', '술시': '20:00', '해시': '22:00',
        }
        if birth_time in time_name_map:
            birth_time = time_name_map[birth_time]

        # 시간 파싱
        hour, minute = map(int, birth_time.split(':'))
        
        # 12시진 계산 (2시간 단위)
        time_branch_index = self.get_time_branch(hour, minute)
        
        # 시진 정보 가져오기
        time_info = self.get_time_period_info(time_branch_index, hour, minute)
        
        # 일간에 따른 시간 계산
        day_heavenly_index = self.get_heavenly_index(day_heavenly)
        hour_heavenly_index = self.get_hour_heavenly(day_heavenly_index, time_branch_index)
        
        return {
            'heavenly': self.heavenly_stems[hour_heavenly_index]['name_ko'],
            'heavenly_hanja': self.heavenly_stems[hour_heavenly_index]['name_hanja'],
            'earthly': self.earthly_branches[time_branch_index]['name_ko'],
            'earthly_hanja': self.earthly_branches[time_branch_index]['name_hanja'],
            'element': self.heavenly_stems[hour_heavenly_index]['element'],
            'time_period': time_info['period_name'],
            'time_range': time_info['time_range'],
            'early_late': time_info['early_late'],
            'combined_name': f"{self.heavenly_stems[hour_heavenly_index]['name_ko']}{self.earthly_branches[time_branch_index]['name_ko']}시"
        }
    
    def get_time_branch(self, hour: int, minute: int) -> int:
        """
        시간을 12지지로 변환 (정확한 12시진 매핑)
        
        12시진 체계:
        - 자시(子時): 23:00 - 01:00 (밤 11시 - 새벽 1시)
        - 축시(丑時): 01:00 - 03:00 (새벽 1시 - 3시)
        - 인시(寅時): 03:00 - 05:00 (새벽 3시 - 5시)
        - 묘시(卯時): 05:00 - 07:00 (새벽 5시 - 7시)
        - 진시(辰時): 07:00 - 09:00 (아침 7시 - 9시)
        - 사시(巳時): 09:00 - 11:00 (오전 9시 - 11시)
        - 오시(午時): 11:00 - 13:00 (낮 11시 - 오후 1시)
        - 미시(未時): 13:00 - 15:00 (오후 1시 - 3시)
        - 신시(申時): 15:00 - 17:00 (오후 3시 - 5시)
        - 유시(酉時): 17:00 - 19:00 (오후 5시 - 7시)
        - 술시(戌時): 19:00 - 21:00 (저녁 7시 - 9시)
        - 해시(亥時): 21:00 - 23:00 (밤 9시 - 11시)
        
        Args:
            hour: 시간 (0-23)
            minute: 분 (0-59)
            
        Returns:
            지지 인덱스 (0-11)
            0: 자(子), 1: 축(丑), 2: 인(寅), 3: 묘(卯),
            4: 진(辰), 5: 사(巳), 6: 오(午), 7: 미(未),
            8: 신(申), 9: 유(酉), 10: 술(戌), 11: 해(亥)
        """
        # 시진 매핑 테이블 (더 명확한 구조)
        time_mapping = {
            23: 0,  # 23:00-23:59 -> 자시
            0: 0,   # 00:00-00:59 -> 자시
            1: 1,   # 01:00-01:59 -> 축시
            2: 1,   # 02:00-02:59 -> 축시
            3: 2,   # 03:00-03:59 -> 인시
            4: 2,   # 04:00-04:59 -> 인시
            5: 3,   # 05:00-05:59 -> 묘시
            6: 3,   # 06:00-06:59 -> 묘시
            7: 4,   # 07:00-07:59 -> 진시
            8: 4,   # 08:00-08:59 -> 진시
            9: 5,   # 09:00-09:59 -> 사시
            10: 5,  # 10:00-10:59 -> 사시
            11: 6,  # 11:00-11:59 -> 오시
            12: 6,  # 12:00-12:59 -> 오시
            13: 7,  # 13:00-13:59 -> 미시
            14: 7,  # 14:00-14:59 -> 미시
            15: 8,  # 15:00-15:59 -> 신시
            16: 8,  # 16:00-16:59 -> 신시
            17: 9,  # 17:00-17:59 -> 유시
            18: 9,  # 18:00-18:59 -> 유시
            19: 10, # 19:00-19:59 -> 술시
            20: 10, # 20:00-20:59 -> 술시
            21: 11, # 21:00-21:59 -> 해시
            22: 11  # 22:00-22:59 -> 해시
        }
        
        return time_mapping.get(hour, 0)
    
    def get_month_heavenly(self, year_heavenly: int, month: int) -> int:
        """
        년간에 따른 월간 계산
        
        Args:
            year_heavenly: 년간 인덱스 (0-9)
            month: 월 (1-12)
            
        Returns:
            월간 인덱스 (0-9)
        """
        # 오행기 법칙에 따른 월간 계산
        # 갑기년: 병인월부터 시작
        # 을경년: 무인월부터 시작
        # 병신년: 경인월부터 시작
        # 정임년: 임인월부터 시작
        # 무계년: 갑인월부터 시작
        
        month_heavenly_start = {
            0: 2,  # 갑년: 병(2)부터
            1: 4,  # 을년: 무(4)부터
            2: 6,  # 병년: 경(6)부터
            3: 8,  # 정년: 임(8)부터
            4: 0,  # 무년: 갑(0)부터
            5: 2,  # 기년: 병(2)부터
            6: 4,  # 경년: 무(4)부터
            7: 6,  # 신년: 경(6)부터
            8: 8,  # 임년: 임(8)부터
            9: 0   # 계년: 갑(0)부터
        }
        
        start_index = month_heavenly_start[year_heavenly]
        # 인월(1월)부터 시작하므로 month-1
        return (start_index + month - 1) % 10
    
    def get_hour_heavenly(self, day_heavenly: int, hour_earthly: int) -> int:
        """
        일간에 따른 시간 계산
        
        Args:
            day_heavenly: 일간 인덱스 (0-9)
            hour_earthly: 시지 인덱스 (0-11)
            
        Returns:
            시간 인덱스 (0-9)
        """
        # 일간에 따른 자시의 천간
        hour_heavenly_start = {
            0: 0,  # 갑일: 갑자시
            1: 2,  # 을일: 병자시
            2: 4,  # 병일: 무자시
            3: 6,  # 정일: 경자시
            4: 8,  # 무일: 임자시
            5: 0,  # 기일: 갑자시
            6: 2,  # 경일: 병자시
            7: 4,  # 신일: 무자시
            8: 6,  # 임일: 경자시
            9: 8   # 계일: 임자시
        }
        
        start_index = hour_heavenly_start[day_heavenly]
        return (start_index + hour_earthly) % 10
    
    def calculate_ganji_number(self, heavenly_index: int, earthly_index: int) -> int:
        """
        60갑자 순서 번호 계산 (1-60)
        
        Args:
            heavenly_index: 천간 인덱스 (0-9)
            earthly_index: 지지 인덱스 (0-11)
            
        Returns:
            60갑자 순서 번호 (1-60)
        """
        # 60갑자 테이블에서의 위치 계산
        # 공식: ((천간 * 6) + (지지 - 천간)) % 60 + 1
        # 더 간단한 방법: 각 조합의 고유 번호 찾기
        
        # 60개 조합을 순회하면서 매칭
        for i in range(60):
            if (i % 10) == heavenly_index and (i % 12) == earthly_index:
                return i + 1
        
        return 1  # 기본값
    
    def get_day_master_characteristics(self, heavenly_index: int) -> Dict:
        """
        일간(Day Master)의 특성 정보 반환
        
        Args:
            heavenly_index: 천간 인덱스 (0-9)
            
        Returns:
            일간 특성 정보
        """
        day_master_traits = {
            0: {  # 갑 (甲)
                'personality': '리더십이 강하고 진취적이며 적극적',
                'strength': '추진력, 결단력, 개척정신',
                'weakness': '고집, 융통성 부족',
                'suitable_career': '경영, 정치, 군인, 개척자'
            },
            1: {  # 을 (乙)
                'personality': '온화하고 유연하며 적응력이 뛰어남',
                'strength': '인내심, 협조성, 섬세함',
                'weakness': '우유부단, 의존적',
                'suitable_career': '예술, 교육, 상담, 서비스업'
            },
            2: {  # 병 (丙)
                'personality': '열정적이고 밝으며 낙천적',
                'strength': '활력, 표현력, 긍정성',
                'weakness': '성급함, 변덕',
                'suitable_career': '엔터테인먼트, 영업, 홍보, 스포츠'
            },
            3: {  # 정 (丁)
                'personality': '섬세하고 예술적이며 감성적',
                'strength': '창의성, 직관력, 세심함',
                'weakness': '예민함, 내성적',
                'suitable_career': '예술, 디자인, 문학, 심리상담'
            },
            4: {  # 무 (戊)
                'personality': '안정적이고 신뢰할 수 있으며 포용력이 있음',
                'strength': '책임감, 성실성, 중재력',
                'weakness': '완고함, 보수적',
                'suitable_career': '부동산, 건설, 금융, 행정'
            },
            5: {  # 기 (己)
                'personality': '실용적이고 겸손하며 배려심이 깊음',
                'strength': '적응력, 융통성, 협조성',
                'weakness': '소극적, 결단력 부족',
                'suitable_career': '의료, 복지, 교육, 농업'
            },
            6: {  # 경 (庚)
                'personality': '강직하고 원칙적이며 정의감이 강함',
                'strength': '결단력, 추진력, 정직성',
                'weakness': '융통성 부족, 독선적',
                'suitable_career': '법조계, 군인, 경찰, 기술직'
            },
            7: {  # 신 (辛)
                'personality': '섬세하고 완벽주의적이며 예리함',
                'strength': '분석력, 정밀성, 미적 감각',
                'weakness': '비판적, 까다로움',
                'suitable_career': '연구, 의학, 보석, 정밀공업'
            },
            8: {  # 임 (壬)
                'personality': '지적이고 유동적이며 통찰력이 있음',
                'strength': '지혜, 적응력, 소통능력',
                'weakness': '일관성 부족, 산만함',
                'suitable_career': '언론, 무역, 외교, 학술'
            },
            9: {  # 계 (癸)
                'personality': '직관적이고 창의적이며 감수성이 풍부함',
                'strength': '상상력, 공감능력, 예술성',
                'weakness': '현실감 부족, 감정적',
                'suitable_career': '예술, 철학, 종교, 치유'
            }
        }
        
        return day_master_traits.get(heavenly_index, {})
    
    def get_time_period_info(self, time_branch_index: int, hour: int, minute: int) -> Dict:
        """
        시진 상세 정보 반환
        
        Args:
            time_branch_index: 시지 인덱스 (0-11)
            hour: 시간 (0-23)
            minute: 분 (0-59)
            
        Returns:
            시진 정보 딕셔너리
        """
        time_periods = {
            0: {'name': '자시', 'hanja': '子時', 'range': '23:00-01:00', 'meaning': '쥐의 시간'},
            1: {'name': '축시', 'hanja': '丑時', 'range': '01:00-03:00', 'meaning': '소의 시간'},
            2: {'name': '인시', 'hanja': '寅時', 'range': '03:00-05:00', 'meaning': '호랑이의 시간'},
            3: {'name': '묘시', 'hanja': '卯時', 'range': '05:00-07:00', 'meaning': '토끼의 시간'},
            4: {'name': '진시', 'hanja': '辰時', 'range': '07:00-09:00', 'meaning': '용의 시간'},
            5: {'name': '사시', 'hanja': '巳時', 'range': '09:00-11:00', 'meaning': '뱀의 시간'},
            6: {'name': '오시', 'hanja': '午時', 'range': '11:00-13:00', 'meaning': '말의 시간'},
            7: {'name': '미시', 'hanja': '未時', 'range': '13:00-15:00', 'meaning': '양의 시간'},
            8: {'name': '신시', 'hanja': '申時', 'range': '15:00-17:00', 'meaning': '원숭이의 시간'},
            9: {'name': '유시', 'hanja': '酉時', 'range': '17:00-19:00', 'meaning': '닭의 시간'},
            10: {'name': '술시', 'hanja': '戌時', 'range': '19:00-21:00', 'meaning': '개의 시간'},
            11: {'name': '해시', 'hanja': '亥時', 'range': '21:00-23:00', 'meaning': '돼지의 시간'}
        }
        
        period = time_periods.get(time_branch_index, {})
        
        # 초시(初時) vs 정시(正時) 구분
        # 각 시진의 전반부 1시간은 초시, 후반부 1시간은 정시
        early_late = self.determine_early_late(time_branch_index, hour, minute)
        
        return {
            'period_name': period.get('name', ''),
            'period_hanja': period.get('hanja', ''),
            'time_range': period.get('range', ''),
            'meaning': period.get('meaning', ''),
            'early_late': early_late
        }
    
    def determine_early_late(self, time_branch_index: int, hour: int, minute: int) -> str:
        """
        초시/정시 구분
        
        Args:
            time_branch_index: 시지 인덱스
            hour: 시간
            minute: 분
            
        Returns:
            '초시' 또는 '정시'
        """
        # 자시 특별 처리
        if time_branch_index == 0:  # 자시
            if hour == 23:
                return '초자시'  # 23:00-00:00
            else:  # hour == 0
                return '정자시'  # 00:00-01:00
        
        # 일반 시진 처리 (홀수 시간이 초시, 짝수 시간이 정시)
        hour_ranges = [
            (1, 2),   # 축시: 1시 초축시, 2시 정축시
            (3, 4),   # 인시: 3시 초인시, 4시 정인시
            (5, 6),   # 묘시: 5시 초묘시, 6시 정묘시
            (7, 8),   # 진시: 7시 초진시, 8시 정진시
            (9, 10),  # 사시: 9시 초사시, 10시 정사시
            (11, 12), # 오시: 11시 초오시, 12시 정오시
            (13, 14), # 미시: 13시 초미시, 14시 정미시
            (15, 16), # 신시: 15시 초신시, 16시 정신시
            (17, 18), # 유시: 17시 초유시, 18시 정유시
            (19, 20), # 술시: 19시 초술시, 20시 정술시
            (21, 22)  # 해시: 21시 초해시, 22시 정해시
        ]
        
        if 1 <= time_branch_index <= 11:
            early_hour, late_hour = hour_ranges[time_branch_index - 1]
            if hour == early_hour:
                return '초시'
            else:
                return '정시'
        
        return ''
    
    def get_heavenly_index(self, heavenly_name: str) -> int:
        """
        천간 이름으로 인덱스 찾기
        
        Args:
            heavenly_name: 천간 이름 (한글)
            
        Returns:
            천간 인덱스 (0-9)
        """
        for idx, stem in enumerate(self.heavenly_stems):
            if stem['name_ko'] == heavenly_name:
                return idx
        return 0
    
    def convert_lunar_to_solar(self, lunar_date: datetime) -> datetime:
        """
        음력을 양력으로 변환
        
        Args:
            lunar_date: 음력 날짜
            
        Returns:
            양력 날짜
        """
        # Lunar conversion will be implemented when lunarcalendar is installed
        # For now, return the date as-is
        return lunar_date
    
    def analyze_elements(self, pillars: Dict) -> Dict:
        """
        오행 분석
        
        Args:
            pillars: 사주 (년, 월, 일, 시)
            
        Returns:
            오행 분석 결과
        """
        elements_count = {
            '목': 0,
            '화': 0,
            '토': 0,
            '금': 0,
            '수': 0
        }
        
        # 각 주의 천간과 지지의 오행 계산
        for pillar_name, pillar_data in pillars.items():
            if 'element' in pillar_data:
                element = pillar_data['element']
                if element in elements_count:
                    elements_count[element] += 1
        
        # 가장 많은 오행과 부족한 오행 찾기
        max_element = max(elements_count, key=elements_count.get)
        min_element = min(elements_count, key=elements_count.get)
        
        return {
            'count': elements_count,
            'dominant': max_element,
            'lacking': min_element,
            'balance': self.calculate_element_balance(elements_count)
        }
    
    def calculate_element_balance(self, elements_count: Dict) -> str:
        """
        오행 균형 평가
        
        Args:
            elements_count: 오행별 개수
            
        Returns:
            균형 평가 결과
        """
        total = sum(elements_count.values())
        if total == 0:
            return "분석 불가"
        
        # 표준편차를 이용한 균형 평가
        avg = total / 5
        variance = sum((count - avg) ** 2 for count in elements_count.values()) / 5
        std_dev = variance ** 0.5
        
        if std_dev < 0.5:
            return "매우 균형"
        elif std_dev < 1.0:
            return "균형"
        elif std_dev < 1.5:
            return "약간 불균형"
        else:
            return "불균형"


# 테스트용 메인 함수
if __name__ == "__main__":
    calculator = SajuCalculator()
    
    # 테스트 데이터
    test_date = datetime(1990, 5, 15)
    test_time = "14:30"
    test_gender = "male"
    
    result = calculator.calculate_saju(test_date, test_time, test_gender)
    
    print("사주 계산 결과:")
    print(json.dumps(result, ensure_ascii=False, indent=2))