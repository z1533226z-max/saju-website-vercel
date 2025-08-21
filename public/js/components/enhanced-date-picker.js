/**
 * Enhanced Date Picker with Lunar/Solar Calendar Toggle
 * Provides seamless switching between lunar and solar calendars
 */

class EnhancedDatePicker {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.calendarType = 'solar'; // 'solar' or 'lunar'
        this.selectedDate = null;
        this.lunarConverter = null; // Will be initialized when needed
        this.init();
    }
    
    init() {
        if (!this.container) return;
        this.render();
        this.attachEventListeners();
    }
    
    render() {
        const html = `
            <div class="enhanced-date-picker">
                <!-- Calendar Type Toggle -->
                <div class="calendar-toggle">
                    <div class="toggle-container">
                        <label class="toggle-switch">
                            <input type="checkbox" id="calendar-type-toggle" ${this.calendarType === 'lunar' ? 'checked' : ''}>
                            <span class="toggle-slider">
                                <span class="toggle-label solar">양력</span>
                                <span class="toggle-label lunar">음력</span>
                            </span>
                        </label>
                        <div class="calendar-type-display">
                            <span class="type-indicator ${this.calendarType}">
                                ${this.calendarType === 'solar' ? '☀️ 양력' : '🌙 음력'}
                            </span>
                        </div>
                    </div>
                </div>
                
                <!-- Date Input Fields -->
                <div class="date-input-group">
                    <div class="date-field">
                        <label for="year-input">년도</label>
                        <select id="year-input" class="date-select">
                            ${this.generateYearOptions()}
                        </select>
                    </div>
                    
                    <div class="date-field">
                        <label for="month-input">월</label>
                        <select id="month-input" class="date-select">
                            ${this.generateMonthOptions()}
                        </select>
                    </div>
                    
                    <div class="date-field">
                        <label for="day-input">일</label>
                        <select id="day-input" class="date-select">
                            ${this.generateDayOptions()}
                        </select>
                    </div>
                    
                    <div class="date-field lunar-leap" style="display: ${this.calendarType === 'lunar' ? 'block' : 'none'}">
                        <label>
                            <input type="checkbox" id="leap-month-check">
                            윤달
                        </label>
                    </div>
                </div>
                
                <!-- Calendar Preview -->
                <div class="calendar-preview">
                    <div class="preview-header">
                        <button class="prev-month" onclick="enhancedDatePicker.changeMonth(-1)">‹</button>
                        <span class="current-month-year"></span>
                        <button class="next-month" onclick="enhancedDatePicker.changeMonth(1)">›</button>
                    </div>
                    <div class="calendar-grid">
                        <!-- Calendar grid will be rendered here -->
                    </div>
                </div>
                
                <!-- Conversion Display -->
                <div class="date-conversion-display">
                    <div class="conversion-result" id="conversion-result">
                        <!-- Conversion result will be shown here -->
                    </div>
                </div>
                
                <!-- Today Button -->
                <div class="today-button-container">
                    <button class="btn-today" onclick="enhancedDatePicker.selectToday()">
                        오늘 날짜 선택
                    </button>
                </div>
            </div>
        `;
        
        this.container.innerHTML = html;
        this.updateCalendarGrid();
    }
    
    generateYearOptions() {
        const currentYear = new Date().getFullYear();
        const startYear = currentYear - 100;
        const endYear = currentYear;
        
        let options = '<option value="">선택</option>';
        for (let year = endYear; year >= startYear; year--) {
            options += `<option value="${year}">${year}년</option>`;
        }
        return options;
    }
    
    generateMonthOptions() {
        let options = '<option value="">선택</option>';
        for (let month = 1; month <= 12; month++) {
            options += `<option value="${month}">${month}월</option>`;
        }
        return options;
    }
    
    generateDayOptions() {
        const yearSelect = document.getElementById('year-input');
        const monthSelect = document.getElementById('month-input');
        
        const year = yearSelect?.value || new Date().getFullYear();
        const month = monthSelect?.value || 1;
        
        const daysInMonth = this.getDaysInMonth(year, month);
        
        let options = '<option value="">선택</option>';
        for (let day = 1; day <= daysInMonth; day++) {
            options += `<option value="${day}">${day}일</option>`;
        }
        return options;
    }
    
    getDaysInMonth(year, month) {
        if (this.calendarType === 'solar') {
            return new Date(year, month, 0).getDate();
        } else {
            // For lunar calendar, we'd need to check the lunar month days
            // Default to 30 for now, but should be calculated properly
            return 30;
        }
    }
    
    attachEventListeners() {
        // Calendar type toggle
        const toggle = document.getElementById('calendar-type-toggle');
        if (toggle) {
            toggle.addEventListener('change', (e) => {
                this.calendarType = e.target.checked ? 'lunar' : 'solar';
                this.onCalendarTypeChange();
            });
        }
        
        // Date input changes
        const yearInput = document.getElementById('year-input');
        const monthInput = document.getElementById('month-input');
        const dayInput = document.getElementById('day-input');
        
        [yearInput, monthInput, dayInput].forEach(input => {
            if (input) {
                input.addEventListener('change', () => {
                    this.onDateChange();
                });
            }
        });
        
        // Leap month checkbox
        const leapCheck = document.getElementById('leap-month-check');
        if (leapCheck) {
            leapCheck.addEventListener('change', () => {
                this.onDateChange();
            });
        }
    }
    
    onCalendarTypeChange() {
        // Update UI
        const typeIndicator = this.container.querySelector('.type-indicator');
        if (typeIndicator) {
            typeIndicator.className = `type-indicator ${this.calendarType}`;
            typeIndicator.textContent = this.calendarType === 'solar' ? '☀️ 양력' : '🌙 음력';
        }
        
        // Show/hide leap month option
        const leapOption = this.container.querySelector('.lunar-leap');
        if (leapOption) {
            leapOption.style.display = this.calendarType === 'lunar' ? 'block' : 'none';
        }
        
        // Convert and display the date
        this.convertAndDisplay();
        
        // Update calendar grid
        this.updateCalendarGrid();
        
        // Trigger custom event
        this.triggerDateChange();
    }
    
    onDateChange() {
        const year = document.getElementById('year-input')?.value;
        const month = document.getElementById('month-input')?.value;
        const day = document.getElementById('day-input')?.value;
        
        if (year && month && day) {
            this.selectedDate = {
                year: parseInt(year),
                month: parseInt(month),
                day: parseInt(day),
                isLunar: this.calendarType === 'lunar',
                isLeapMonth: document.getElementById('leap-month-check')?.checked || false
            };
            
            // Update day options based on selected month
            const daySelect = document.getElementById('day-input');
            if (daySelect) {
                const currentDay = daySelect.value;
                daySelect.innerHTML = this.generateDayOptions();
                daySelect.value = currentDay; // Restore selection if valid
            }
            
            // Convert and display
            this.convertAndDisplay();
            
            // Update calendar grid
            this.updateCalendarGrid();
            
            // Trigger custom event
            this.triggerDateChange();
        }
    }
    
    convertAndDisplay() {
        if (!this.selectedDate) return;
        
        const conversionDiv = document.getElementById('conversion-result');
        if (!conversionDiv) return;
        
        if (this.calendarType === 'solar') {
            // Show lunar conversion
            const lunarDate = this.convertSolarToLunar(
                this.selectedDate.year,
                this.selectedDate.month,
                this.selectedDate.day
            );
            
            conversionDiv.innerHTML = `
                <div class="conversion-item">
                    <span class="conversion-label">음력:</span>
                    <span class="conversion-value">
                        ${lunarDate.year}년 ${lunarDate.isLeapMonth ? '윤' : ''}${lunarDate.month}월 ${lunarDate.day}일
                    </span>
                </div>
            `;
        } else {
            // Show solar conversion
            const solarDate = this.convertLunarToSolar(
                this.selectedDate.year,
                this.selectedDate.month,
                this.selectedDate.day,
                this.selectedDate.isLeapMonth
            );
            
            conversionDiv.innerHTML = `
                <div class="conversion-item">
                    <span class="conversion-label">양력:</span>
                    <span class="conversion-value">
                        ${solarDate.year}년 ${solarDate.month}월 ${solarDate.day}일
                    </span>
                </div>
            `;
        }
    }
    
    updateCalendarGrid() {
        const gridContainer = this.container.querySelector('.calendar-grid');
        if (!gridContainer) return;
        
        const year = parseInt(document.getElementById('year-input')?.value) || new Date().getFullYear();
        const month = parseInt(document.getElementById('month-input')?.value) || new Date().getMonth() + 1;
        
        // Update header
        const headerSpan = this.container.querySelector('.current-month-year');
        if (headerSpan) {
            headerSpan.textContent = `${year}년 ${month}월`;
        }
        
        // Generate calendar grid
        const firstDay = new Date(year, month - 1, 1).getDay();
        const daysInMonth = this.getDaysInMonth(year, month);
        
        let gridHTML = `
            <div class="weekdays">
                <span>일</span><span>월</span><span>화</span><span>수</span>
                <span>목</span><span>금</span><span>토</span>
            </div>
            <div class="days">
        `;
        
        // Empty cells for days before month starts
        for (let i = 0; i < firstDay; i++) {
            gridHTML += '<span class="empty"></span>';
        }
        
        // Days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const isSelected = this.selectedDate && 
                               this.selectedDate.year === year && 
                               this.selectedDate.month === month && 
                               this.selectedDate.day === day;
            
            const isToday = this.isToday(year, month, day);
            
            gridHTML += `
                <span class="day ${isSelected ? 'selected' : ''} ${isToday ? 'today' : ''}"
                      onclick="enhancedDatePicker.selectDate(${year}, ${month}, ${day})">
                    ${day}
                </span>
            `;
        }
        
        gridHTML += '</div>';
        gridContainer.innerHTML = gridHTML;
    }
    
    selectDate(year, month, day) {
        // Update input fields
        document.getElementById('year-input').value = year;
        document.getElementById('month-input').value = month;
        document.getElementById('day-input').value = day;
        
        // Trigger date change
        this.onDateChange();
    }
    
    changeMonth(direction) {
        const yearInput = document.getElementById('year-input');
        const monthInput = document.getElementById('month-input');
        
        let year = parseInt(yearInput?.value) || new Date().getFullYear();
        let month = parseInt(monthInput?.value) || new Date().getMonth() + 1;
        
        month += direction;
        
        if (month > 12) {
            month = 1;
            year++;
        } else if (month < 1) {
            month = 12;
            year--;
        }
        
        yearInput.value = year;
        monthInput.value = month;
        
        this.updateCalendarGrid();
    }
    
    selectToday() {
        const today = new Date();
        
        document.getElementById('year-input').value = today.getFullYear();
        document.getElementById('month-input').value = today.getMonth() + 1;
        document.getElementById('day-input').value = today.getDate();
        
        // Set to solar calendar for today
        const toggle = document.getElementById('calendar-type-toggle');
        if (toggle && toggle.checked) {
            toggle.checked = false;
            this.calendarType = 'solar';
            this.onCalendarTypeChange();
        }
        
        this.onDateChange();
    }
    
    isToday(year, month, day) {
        const today = new Date();
        return year === today.getFullYear() && 
               month === today.getMonth() + 1 && 
               day === today.getDate();
    }
    
    // Lunar-Solar conversion methods (simplified versions)
    convertSolarToLunar(year, month, day) {
        // This would normally use a proper lunar calendar conversion library
        // For now, returning mock data
        return {
            year: year,
            month: month,
            day: day,
            isLeapMonth: false
        };
    }
    
    convertLunarToSolar(year, month, day, isLeapMonth) {
        // This would normally use a proper lunar calendar conversion library
        // For now, returning mock data
        return {
            year: year,
            month: month,
            day: day
        };
    }
    
    triggerDateChange() {
        // Dispatch custom event with selected date data
        const event = new CustomEvent('dateChanged', {
            detail: {
                date: this.selectedDate,
                calendarType: this.calendarType
            }
        });
        
        window.dispatchEvent(event);
    }
    
    getSelectedDate() {
        return this.selectedDate;
    }
}

// Export for use
window.EnhancedDatePicker = EnhancedDatePicker;