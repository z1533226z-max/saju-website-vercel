/**
 * Saju Enhancements V2 Integration
 * Integrates all new enhancement features
 */

// Initialize all enhancement features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeEnhancementsV2();
});

/**
 * Initialize all V2 enhancements
 */
function initializeEnhancementsV2() {
    console.log('Initializing Saju Enhancements V2...');
    
    // Store component instances globally
    window.sajuEnhancements = {
        datePicker: null,
        realtimeCalculator: null,
        resultSharing: null,
        comparison: null
    };
    
    // 1. Initialize Enhanced Date Picker
    initializeDatePicker();
    
    // 2. Initialize Real-time Calculator
    initializeRealtimeCalculator();
    
    // 3. Initialize Result Sharing
    initializeResultSharing();
    
    // 4. Initialize Comparison Mode
    initializeComparisonMode();
    
    // Load required CSS files
    loadEnhancementStyles();
    
    console.log('✅ All V2 enhancements initialized successfully');
}

/**
 * Initialize Enhanced Date Picker
 */
function initializeDatePicker() {
    // Check if there's a suitable container for the date picker
    const dateContainer = document.querySelector('#date-picker-container, .date-input-section, .form-group');
    
    if (dateContainer) {
        // Create container for enhanced date picker
        const pickerContainer = document.createElement('div');
        pickerContainer.id = 'enhanced-date-picker-container';
        
        // Insert at the beginning of the form
        const form = document.querySelector('form, #input-form, .saju-form');
        if (form) {
            form.insertBefore(pickerContainer, form.firstChild);
        } else {
            dateContainer.appendChild(pickerContainer);
        }
        
        // Initialize the enhanced date picker
        window.sajuEnhancements.datePicker = new EnhancedDatePicker('enhanced-date-picker-container');
        console.log('✓ Enhanced Date Picker initialized');
    } else {
        console.warn('No suitable container found for date picker');
    }
}

/**
 * Initialize Real-time Calculator
 */
function initializeRealtimeCalculator() {
    window.sajuEnhancements.realtimeCalculator = new RealtimeCalculator();
    console.log('✓ Real-time Calculator initialized');
}

/**
 * Initialize Result Sharing
 */
function initializeResultSharing() {
    window.sajuEnhancements.resultSharing = new ResultSharing();
    console.log('✓ Result Sharing initialized');
}

/**
 * Initialize Comparison Mode
 */
function initializeComparisonMode() {
    window.sajuEnhancements.comparison = new SajuComparison();
    console.log('✓ Comparison Mode initialized');
}

/**
 * Load CSS files for enhancements
 */
function loadEnhancementStyles() {
    const styles = [
        'css/enhanced-date-picker.css',
        'css/realtime-calculator.css',
        'css/result-sharing.css',
        'css/saju-comparison.css'
    ];
    
    styles.forEach(href => {
        if (!document.querySelector(`link[href="${href}"]`)) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            document.head.appendChild(link);
        }
    });
    
    console.log('✓ Enhancement styles loaded');
}

/**
 * Public API for enhancements
 */
window.SajuEnhancementsV2 = {
    // Get current date selection
    getSelectedDate: function() {
        if (window.sajuEnhancements.datePicker) {
            return window.sajuEnhancements.datePicker.getSelectedDate();
        }
        return null;
    },
    
    // Toggle real-time calculation
    toggleRealtimeCalculation: function(enabled) {
        if (window.sajuEnhancements.realtimeCalculator) {
            window.sajuEnhancements.realtimeCalculator.enabled = enabled;
            window.sajuEnhancements.realtimeCalculator.updateIndicatorStatus();
        }
    },
    
    // Open sharing panel
    openSharingPanel: function() {
        if (window.sajuEnhancements.resultSharing) {
            window.sajuEnhancements.resultSharing.openPanel();
        }
    },
    
    // Open comparison mode
    openComparisonMode: function() {
        if (window.sajuEnhancements.comparison) {
            window.sajuEnhancements.comparison.openComparison();
        }
    },
    
    // Add profile to comparison
    addToComparison: function(sajuData) {
        if (window.sajuEnhancements.comparison) {
            window.sajuEnhancements.comparison.addProfileFromData(sajuData);
        }
    },
    
    // Get share URL for current result
    getShareUrl: function() {
        if (window.sajuEnhancements.resultSharing) {
            return window.sajuEnhancements.resultSharing.shareUrl;
        }
        return null;
    }
};

// Make individual components available globally for direct access
window.enhancedDatePicker = window.sajuEnhancements?.datePicker;
window.realtimeCalculator = window.sajuEnhancements?.realtimeCalculator;
window.resultSharing = window.sajuEnhancements?.resultSharing;
window.sajuComparison = window.sajuEnhancements?.comparison;

console.log('Saju Enhancements V2 loaded and ready');