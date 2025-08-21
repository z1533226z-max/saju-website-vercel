/**
 * Configuration for Saju Website
 */

const APP_CONFIG = {
    // API Configuration
    API: {
        BASE_URL: '', // Use relative paths for Vercel
        ENDPOINTS: {
            CALCULATE: '/api/saju/calculate',
            HISTORY: '/api/history',
            COMPATIBILITY: '/api/saju/compatibility',
            INFO: {
                HEAVENLY_STEMS: '/api/saju/info/heavenly_stems',
                EARTHLY_BRANCHES: '/api/saju/info/earthly_branches',
                ELEMENTS: '/api/saju/info/elements'
            }
        },
        TIMEOUT: 30000, // 30 seconds
        RETRY_ATTEMPTS: 3
    },
    
    // Application Settings
    APP: {
        VERSION: '1.0.0',
        NAME: '사주팔자',
        DESCRIPTION: '생년월일시로 보는 운세',
        DEFAULT_LANGUAGE: 'ko',
        DEBUG_MODE: window.location.hostname === 'localhost'
    },
    
    // Feature Flags
    FEATURES: {
        ENABLE_HISTORY: true,
        ENABLE_COMPATIBILITY: true,
        ENABLE_SHARE: true,
        ENABLE_DARK_MODE: true,
        ENABLE_ANALYTICS: true,
        ENABLE_ADS: true
    },
    
    // Google AdSense Configuration
    ADSENSE: {
        CLIENT_ID: 'ca-pub-XXXXXXXXXXXXXXXX', // Replace with actual AdSense client ID
        SLOTS: {
            TOP_BANNER: 'XXXXXXXXXX',
            INFEED: 'XXXXXXXXXX',
            DISPLAY: 'XXXXXXXXXX',
            MATCHED: 'XXXXXXXXXX'
        }
    },
    
    // Google Analytics Configuration
    ANALYTICS: {
        TRACKING_ID: 'G-XXXXXXXXXX', // Replace with actual GA tracking ID
        EVENTS: {
            CALCULATE: 'calculate_saju',
            SHARE: 'share_result',
            VIEW_DETAIL: 'view_detail'
        }
    },
    
    // Kakao SDK Configuration
    KAKAO: {
        APP_KEY: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' // Replace with actual Kakao app key
    },
    
    // Local Storage Keys
    STORAGE: {
        FORM_DATA: 'sajuFormData',
        HISTORY: 'sajuHistory',
        SETTINGS: 'sajuSettings',
        THEME: 'sajuTheme'
    },
    
    // Validation Rules
    VALIDATION: {
        MIN_YEAR: 1900,
        MAX_YEAR: new Date().getFullYear(),
        MIN_MONTH: 1,
        MAX_MONTH: 12,
        MIN_DAY: 1,
        MAX_DAY: 31
    },
    
    // UI Settings
    UI: {
        ANIMATION_DURATION: 300,
        SCROLL_OFFSET: 100,
        TOAST_DURATION: 3000,
        DEBOUNCE_DELAY: 500
    },
    
    // Color Mappings for Elements
    ELEMENTS: {
        COLORS: {
            '목': '#7B9E89',
            '화': '#D4736A',
            '토': '#C8A882',
            '금': '#A8A5A0',
            '수': '#6B8CAE'
        },
        NAMES: {
            '목': '목(木)',
            '화': '화(火)',
            '토': '토(土)',
            '금': '금(金)',
            '수': '수(水)'
        }
    },
    
    // Time Zones for Saju Calculation
    TIME_ZONES: {
        '자시': { start: '23:00', end: '01:00', zodiac: '쥐' },
        '축시': { start: '01:00', end: '03:00', zodiac: '소' },
        '인시': { start: '03:00', end: '05:00', zodiac: '호랑이' },
        '묘시': { start: '05:00', end: '07:00', zodiac: '토끼' },
        '진시': { start: '07:00', end: '09:00', zodiac: '용' },
        '사시': { start: '09:00', end: '11:00', zodiac: '뱀' },
        '오시': { start: '11:00', end: '13:00', zodiac: '말' },
        '미시': { start: '13:00', end: '15:00', zodiac: '양' },
        '신시': { start: '15:00', end: '17:00', zodiac: '원숭이' },
        '유시': { start: '17:00', end: '19:00', zodiac: '닭' },
        '술시': { start: '19:00', end: '21:00', zodiac: '개' },
        '해시': { start: '21:00', end: '23:00', zodiac: '돼지' }
    }
};

// Freeze configuration to prevent modifications
Object.freeze(APP_CONFIG);

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APP_CONFIG;
}