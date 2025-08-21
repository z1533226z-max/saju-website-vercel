// API Configuration for Production
// 프로덕션 환경에서는 상대 경로 사용 (같은 도메인)
const API_CONFIG = {
    // 개발 환경과 프로덕션 환경 자동 감지
    BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000'  // 개발 환경
        : '',  // 프로덕션 환경 (같은 도메인)
    
    // API 엔드포인트
    ENDPOINTS: {
        CALCULATE: '/api/saju/calculate',
        COMPATIBILITY: '/api/saju/compatibility',
        INFO: '/api/saju/info',
        HEALTH: '/health'
    }
};

// API URL 생성 헬퍼
function getApiUrl(endpoint) {
    return API_CONFIG.BASE_URL + endpoint;
}

// Export for use in other files
window.API_CONFIG = API_CONFIG;
window.getApiUrl = getApiUrl;

console.log('🌍 Environment:', window.location.hostname === 'localhost' ? 'Development' : 'Production');
console.log('📡 API Base URL:', API_CONFIG.BASE_URL || 'Same domain');
