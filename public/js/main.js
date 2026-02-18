/**
 * Main JavaScript for Saju Website
 */

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Load configuration
    // Version info available via APP_CONFIG.APP.VERSION
    
    // Initialize Google Analytics
    if (APP_CONFIG.FEATURES.ENABLE_ANALYTICS) {
        initializeAnalytics();
    }
    
    // AdSense: 자동 광고는 index.html <head> 스크립트만으로 동작
    // Kakao SDK: 미사용 (Web Share API + 링크 복사로 대체)

    // Initialize theme
    initializeTheme();
    
    // Initialize smooth scrolling
    initializeSmoothScroll();
    
    // Initialize animations
    initializeAnimations();
    
    // Load saved form data if exists
    loadSavedFormData();
}

/**
 * Initialize Google Analytics
 */
function initializeAnalytics() {
    if (typeof gtag === 'undefined') {
        // Load Google Analytics script
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${APP_CONFIG.ANALYTICS.TRACKING_ID}`;
        document.head.appendChild(script);
        
        window.dataLayer = window.dataLayer || [];
        window.gtag = function() { dataLayer.push(arguments); };
        gtag('js', new Date());
        gtag('config', APP_CONFIG.ANALYTICS.TRACKING_ID);
    }
}

// AdSense: 자동 광고 사용 (index.html <head> 스크립트만으로 동작, 수동 배치 불필요)
// Kakao SDK: 미사용 (shareKakao()에서 Web Share API → 링크 복사 fallback 처리)

/**
 * Initialize theme (light/dark mode)
 */
function initializeTheme() {
    if (!APP_CONFIG.FEATURES.ENABLE_DARK_MODE) return;
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem(APP_CONFIG.STORAGE.THEME);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else if (prefersDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    // Listen for theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem(APP_CONFIG.STORAGE.THEME)) {
            document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
        }
    });
}

/**
 * Initialize smooth scrolling
 */
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize scroll animations
 */
function initializeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Load saved form data
 */
function loadSavedFormData() {
    const savedData = localStorage.getItem(APP_CONFIG.STORAGE.FORM_DATA);
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            // Data will be loaded by Alpine.js component
            // Form data loaded from localStorage
        } catch (error) {
            // Silently ignore corrupted localStorage data
        }
    }
}

/**
 * Scroll to input section
 */
function scrollToInput() {
    const inputSection = document.getElementById('input-section');
    if (inputSection) {
        inputSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// shareKakao() and copyLink() are defined in index.html inline script
// with enhanced features (Web Share API fallback, button state change)

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = APP_CONFIG.UI.TOAST_DURATION) {
    // duration이 숫자로 올 때 (이전 호출 방식 호환)
    if (typeof type === 'number') {
        duration = type;
        type = 'info';
    }
    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Create new toast
    const toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', type === 'error' ? 'assertive' : 'polite');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--color-text-primary);
        color: var(--color-text-inverse);
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 9999;
        animation: slideUp 0.3s ease-out;
    `;
    
    document.body.appendChild(toast);
    
    // Remove after duration
    setTimeout(() => {
        toast.style.animation = 'slideDown 0.3s ease-out';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
}

/**
 * Debounce function for performance
 */
function debounce(func, wait = APP_CONFIG.UI.DEBOUNCE_DELAY) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Format date for display
 */
function formatDate(year, month, day, isLunar = false) {
    const calendarType = isLunar ? '음력' : '양력';
    return `${calendarType} ${year}년 ${month}월 ${day}일`;
}

/**
 * Get time period name
 */
function getTimePeriodName(hour) {
    const hourNum = parseInt(hour.split(':')[0]);
    
    for (const [name, info] of Object.entries(APP_CONFIG.TIME_ZONES)) {
        const start = parseInt(info.start.split(':')[0]);
        const end = parseInt(info.end.split(':')[0]);
        
        if (start > end) { // Crosses midnight
            if (hourNum >= start || hourNum < end) {
                return `${name} (${info.zodiac})`;
            }
        } else {
            if (hourNum >= start && hourNum < end) {
                return `${name} (${info.zodiac})`;
            }
        }
    }
    
    return hour;
}

/**
 * Validate email format
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Add CSS animation styles
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            transform: translate(-50%, 100%);
            opacity: 0;
        }
        to {
            transform: translate(-50%, 0);
            opacity: 1;
        }
    }
    
    @keyframes slideDown {
        from {
            transform: translate(-50%, 0);
            opacity: 1;
        }
        to {
            transform: translate(-50%, 100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Export functions for global use
window.scrollToInput = scrollToInput;
window.showToast = showToast;
window.formatDate = formatDate;
window.getTimePeriodName = getTimePeriodName;
window.debounce = debounce;