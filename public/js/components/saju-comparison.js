/**
 * Saju Comparison Component
 * Compare multiple Saju analyses side by side
 */

class SajuComparison {
    constructor() {
        this.profiles = [];
        this.maxProfiles = 4;
        this.currentComparisonId = null;
        this.init();
    }
    
    init() {
        this.createComparisonInterface();
        this.attachEventListeners();
    }
    
    createComparisonInterface() {
        const container = document.createElement('div');
        container.id = 'comparison-container';
        container.className = 'comparison-container';
        container.innerHTML = `
            <div class="comparison-header">
                <h2>사주 비교 분석</h2>
                <div class="comparison-controls">
                    <button class="btn-add-profile" onclick="sajuComparison.addProfile()">
                        <span>➕</span> 프로필 추가
                    </button>
                    <button class="btn-clear-all" onclick="sajuComparison.clearAll()">
                        <span>🗑️</span> 전체 삭제
                    </button>
                    <button class="btn-close-comparison" onclick="sajuComparison.closeComparison()">
                        <span>✖️</span> 닫기
                    </button>
                </div>
            </div>
            
            <div class="profiles-grid" id="profiles-grid">
                <!-- Profile cards will be added here -->
            </div>
            
            <div class="comparison-tabs">
                <div class="tabs-header">
                    <button class="tab-btn active" data-tab="overview">개요</button>
                    <button class="tab-btn" data-tab="elements">오행 비교</button>
                    <button class="tab-btn" data-tab="compatibility">궁합 분석</button>
                    <button class="tab-btn" data-tab="detailed">상세 비교</button>
                </div>
                
                <div class="tabs-content">
                    <!-- Overview Tab -->
                    <div class="tab-pane active" id="tab-overview">
                        <div class="overview-content">
                            <h3>프로필 개요</h3>
                            <div id="overview-comparison"></div>
                        </div>
                    </div>
                    
                    <!-- Elements Tab -->
                    <div class="tab-pane" id="tab-elements">
                        <div class="elements-comparison">
                            <h3>오행 분포 비교</h3>
                            <canvas id="elements-comparison-chart"></canvas>
                            <div id="elements-analysis"></div>
                        </div>
                    </div>
                    
                    <!-- Compatibility Tab -->
                    <div class="tab-pane" id="tab-compatibility">
                        <div class="compatibility-content">
                            <h3>상호 궁합 분석</h3>
                            <div id="compatibility-matrix"></div>
                            <div id="compatibility-details"></div>
                        </div>
                    </div>
                    
                    <!-- Detailed Tab -->
                    <div class="tab-pane" id="tab-detailed">
                        <div class="detailed-comparison">
                            <h3>상세 비교 분석</h3>
                            <div id="detailed-comparison-table"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(container);
        
        // Add comparison button to main interface
        this.addComparisonButton();
    }
    
    addComparisonButton() {
        const button = document.createElement('button');
        button.id = 'btn-open-comparison';
        button.className = 'btn-comparison floating-btn';
        button.innerHTML = `
            <span class="comparison-icon">👥</span>
            <span class="comparison-text">비교하기</span>
        `;
        button.onclick = () => this.openComparison();
        
        document.body.appendChild(button);
    }
    
    attachEventListeners() {
        // Tab switching
        document.querySelectorAll('.comparison-tabs .tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });
        
        // Listen for Saju calculations
        window.addEventListener('sajuCalculated', (e) => {
            // Store the latest calculation for quick addition
            this.latestCalculation = e.detail;
        });
    }
    
    openComparison() {
        const container = document.getElementById('comparison-container');
        if (container) {
            container.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Add current result if available
            if (this.latestCalculation && this.profiles.length === 0) {
                this.addProfileFromData(this.latestCalculation);
            }
            
            this.updateComparison();
        }
    }
    
    closeComparison() {
        const container = document.getElementById('comparison-container');
        if (container) {
            container.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    addProfile() {
        if (this.profiles.length >= this.maxProfiles) {
            this.showNotification('최대 4개까지 비교할 수 있습니다.');
            return;
        }
        
        // Create profile input form
        const profileId = Date.now();
        const profileCard = document.createElement('div');
        profileCard.className = 'profile-card';
        profileCard.id = `profile-${profileId}`;
        profileCard.innerHTML = `
            <div class="profile-header">
                <input type="text" class="profile-name" placeholder="이름 입력" value="프로필 ${this.profiles.length + 1}">
                <button class="btn-remove-profile" onclick="sajuComparison.removeProfile('${profileId}')">
                    <span>✖️</span>
                </button>
            </div>
            
            <div class="profile-input">
                <div class="input-group">
                    <label>생년월일</label>
                    <div class="date-inputs">
                        <select class="year-select" data-profile="${profileId}">
                            ${this.generateYearOptions()}
                        </select>
                        <select class="month-select" data-profile="${profileId}">
                            ${this.generateMonthOptions()}
                        </select>
                        <select class="day-select" data-profile="${profileId}">
                            ${this.generateDayOptions()}
                        </select>
                    </div>
                </div>
                
                <div class="input-group">
                    <label>출생시간</label>
                    <select class="hour-select" data-profile="${profileId}">
                        ${this.generateHourOptions()}
                    </select>
                </div>
                
                <div class="input-group">
                    <label>성별</label>
                    <div class="gender-inputs">
                        <label>
                            <input type="radio" name="gender-${profileId}" value="남" checked>
                            <span>남</span>
                        </label>
                        <label>
                            <input type="radio" name="gender-${profileId}" value="여">
                            <span>여</span>
                        </label>
                    </div>
                </div>
                
                <div class="input-group">
                    <label>
                        <input type="checkbox" class="lunar-check" data-profile="${profileId}">
                        <span>음력</span>
                    </label>
                </div>
                
                <button class="btn-calculate-profile" onclick="sajuComparison.calculateProfile('${profileId}')">
                    계산하기
                </button>
            </div>
            
            <div class="profile-result" id="result-${profileId}" style="display: none;">
                <!-- Results will be displayed here -->
            </div>
        `;
        
        const grid = document.getElementById('profiles-grid');
        if (grid) {
            grid.appendChild(profileCard);
        }
        
        // Add profile data
        this.profiles.push({
            id: profileId,
            name: `프로필 ${this.profiles.length + 1}`,
            data: null,
            calculated: false
        });
    }
    
    addProfileFromData(sajuData) {
        if (this.profiles.length >= this.maxProfiles) {
            this.showNotification('최대 4개까지 비교할 수 있습니다.');
            return;
        }
        
        const profileId = Date.now();
        const profileCard = document.createElement('div');
        profileCard.className = 'profile-card calculated';
        profileCard.id = `profile-${profileId}`;
        
        // Extract birth info from data - 수정: 실제 입력 데이터 추출
        const birthInfo = this.extractBirthInfo(sajuData);
        
        profileCard.innerHTML = `
            <div class="profile-header">
                <input type="text" class="profile-name" value="${birthInfo.name || '현재 결과'}">
                <button class="btn-remove-profile" onclick="sajuComparison.removeProfile('${profileId}')">
                    <span>✖️</span>
                </button>
            </div>
            
            <div class="profile-result" id="result-${profileId}">
                <div class="result-summary">
                    <div class="birth-info">
                        <span>${birthInfo.dateStr}</span>
                        <span>${birthInfo.timeStr}</span>
                        <span>${birthInfo.gender}</span>
                    </div>
                    
                    <div class="pillars-display">
                        <div class="pillar">
                            <div class="pillar-title">년주</div>
                            <div class="stem">${sajuData.year?.heavenly_hanja || '-'}</div>
                            <div class="branch">${sajuData.year?.earthly_hanja || '-'}</div>
                        </div>
                        <div class="pillar">
                            <div class="pillar-title">월주</div>
                            <div class="stem">${sajuData.month?.heavenly_hanja || '-'}</div>
                            <div class="branch">${sajuData.month?.earthly_hanja || '-'}</div>
                        </div>
                        <div class="pillar">
                            <div class="pillar-title">일주</div>
                            <div class="stem day-master">${sajuData.day?.heavenly_hanja || '-'}</div>
                            <div class="branch">${sajuData.day?.earthly_hanja || '-'}</div>
                        </div>
                        <div class="pillar">
                            <div class="pillar-title">시주</div>
                            <div class="stem">${sajuData.hour?.heavenly_hanja || '-'}</div>
                            <div class="branch">${sajuData.hour?.earthly_hanja || '-'}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const grid = document.getElementById('profiles-grid');
        if (grid) {
            grid.appendChild(profileCard);
        }
        
        // Add profile data - 입력 데이터 재구성
        const inputData = {
            birthDate: sajuData.inputDate || birthInfo.dateStr || '', 
            birthTime: sajuData.inputTime || birthInfo.timeStr || '',
            gender: sajuData.inputGender || birthInfo.gender || 'neutral',
            isLunar: sajuData.inputIsLunar || false
        };
        
        this.profiles.push({
            id: profileId,
            name: birthInfo.name || '현재 결과',
            data: sajuData,
            inputData: inputData,  // 입력 데이터 저장
            calculated: true
        });
        
        this.updateComparison();
    }
    
    async calculateProfile(profileId) {
        const profile = this.profiles.find(p => p.id === profileId);
        if (!profile) return;
        
        // Collect input data
        const year = document.querySelector(`.year-select[data-profile="${profileId}"]`)?.value;
        const month = document.querySelector(`.month-select[data-profile="${profileId}"]`)?.value;
        const day = document.querySelector(`.day-select[data-profile="${profileId}"]`)?.value;
        const hour = document.querySelector(`.hour-select[data-profile="${profileId}"]`)?.value;
        const gender = document.querySelector(`input[name="gender-${profileId}"]:checked`)?.value;
        const isLunar = document.querySelector(`.lunar-check[data-profile="${profileId}"]`)?.checked;
        
        if (!year || !month || !day || !hour || !gender) {
            this.showNotification('모든 항목을 입력해주세요.');
            return;
        }
        
        // Show loading
        const resultDiv = document.getElementById(`result-${profileId}`);
        if (resultDiv) {
            resultDiv.innerHTML = '<div class="loading">계산 중...</div>';
            resultDiv.style.display = 'block';
        }
        
        try {
            // Call API
            const requestData = {
                birthDate: `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
                birthTime: hour,
                gender: gender,
                isLunar: isLunar
            };
            
            const response = await fetch('/api/saju/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const result = await response.json();
            
            if (result.saju || result.data) {
                const sajuData = result.data || result;
                
                // 중요: 원본 입력 데이터도 함께 저장
                profile.data = sajuData;
                profile.inputData = requestData;  // 입력 데이터 저장
                profile.calculated = true;
                
                // Update display
                this.displayProfileResult(profileId, sajuData);
                this.updateComparison();
            }
        } catch (error) {
            console.error('Error calculating profile:', error);
            // Use mock data for development
            if (window.location.hostname === 'localhost') {
                const mockData = this.generateMockData();
                profile.data = mockData;
                profile.calculated = true;
                this.displayProfileResult(profileId, mockData);
                this.updateComparison();
            }
        }
    }
    
    displayProfileResult(profileId, sajuData) {
        const resultDiv = document.getElementById(`result-${profileId}`);
        if (!resultDiv) return;
        
        resultDiv.innerHTML = `
            <div class="result-summary">
                <div class="pillars-display">
                    <div class="pillar">
                        <div class="pillar-title">년주</div>
                        <div class="stem">${sajuData.year?.heavenly_hanja || '-'}</div>
                        <div class="branch">${sajuData.year?.earthly_hanja || '-'}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-title">월주</div>
                        <div class="stem">${sajuData.month?.heavenly_hanja || '-'}</div>
                        <div class="branch">${sajuData.month?.earthly_hanja || '-'}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-title">일주</div>
                        <div class="stem day-master">${sajuData.day?.heavenly_hanja || '-'}</div>
                        <div class="branch">${sajuData.day?.earthly_hanja || '-'}</div>
                    </div>
                    <div class="pillar">
                        <div class="pillar-title">시주</div>
                        <div class="stem">${sajuData.hour?.heavenly_hanja || '-'}</div>
                        <div class="branch">${sajuData.hour?.earthly_hanja || '-'}</div>
                    </div>
                </div>
                
                <div class="elements-mini">
                    ${this.generateElementsBars(sajuData.elements)}
                </div>
            </div>
        `;
        
        // Hide input form
        const inputDiv = resultDiv.previousElementSibling;
        if (inputDiv && inputDiv.classList.contains('profile-input')) {
            inputDiv.style.display = 'none';
        }
        
        // Add calculated class to card
        const card = document.getElementById(`profile-${profileId}`);
        if (card) {
            card.classList.add('calculated');
        }
    }
    
    removeProfile(profileId) {
        // Remove from profiles array
        this.profiles = this.profiles.filter(p => p.id !== profileId);
        
        // Remove from DOM
        const card = document.getElementById(`profile-${profileId}`);
        if (card) {
            card.remove();
        }
        
        this.updateComparison();
    }
    
    clearAll() {
        if (confirm('모든 프로필을 삭제하시겠습니까?')) {
            this.profiles = [];
            const grid = document.getElementById('profiles-grid');
            if (grid) {
                grid.innerHTML = '';
            }
            this.updateComparison();
        }
    }
    
    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.comparison-tabs .tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
        
        // Update tab panes
        document.querySelectorAll('.comparison-tabs .tab-pane').forEach(pane => {
            pane.classList.toggle('active', pane.id === `tab-${tabName}`);
        });
        
        // Update content based on tab
        this.updateTabContent(tabName);
    }
    
    updateComparison() {
        const calculatedProfiles = this.profiles.filter(p => p.calculated);
        
        if (calculatedProfiles.length < 2) {
            this.showComparisonMessage('2개 이상의 프로필을 추가하여 비교해보세요.');
            return;
        }
        
        // Update all tabs
        this.updateOverview(calculatedProfiles);
        this.updateElementsComparison(calculatedProfiles);
        this.updateCompatibility(calculatedProfiles);
        this.updateDetailedComparison(calculatedProfiles);
    }
    
    updateTabContent(tabName) {
        const calculatedProfiles = this.profiles.filter(p => p.calculated);
        
        switch(tabName) {
            case 'overview':
                this.updateOverview(calculatedProfiles);
                break;
            case 'elements':
                this.updateElementsComparison(calculatedProfiles);
                break;
            case 'compatibility':
                this.updateCompatibility(calculatedProfiles);
                break;
            case 'detailed':
                this.updateDetailedComparison(calculatedProfiles);
                break;
        }
    }
    
    updateOverview(profiles) {
        const container = document.getElementById('overview-comparison');
        if (!container) return;
        
        if (profiles.length < 2) {
            container.innerHTML = '<p class="no-data">비교할 프로필을 추가해주세요.</p>';
            return;
        }
        
        let html = '<div class="overview-grid">';
        
        profiles.forEach(profile => {
            html += `
                <div class="overview-card">
                    <h4>${profile.name}</h4>
                    <div class="overview-details">
                        <div class="detail-item">
                            <span class="label">일간:</span>
                            <span class="value">${profile.data.day?.heavenly || '-'}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">주요 오행:</span>
                            <span class="value">${this.getDominantElement(profile.data.elements)}</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }
    
    updateElementsComparison(profiles) {
        if (profiles.length < 2) return;
        
        const canvas = document.getElementById('elements-comparison-chart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        
        // Prepare data for chart
        const datasets = profiles.map((profile, index) => {
            const elements = profile.data.elements?.distribution || {};
            return {
                label: profile.name,
                data: [
                    elements['목'] || 0,
                    elements['화'] || 0,
                    elements['토'] || 0,
                    elements['금'] || 0,
                    elements['수'] || 0
                ],
                backgroundColor: this.getProfileColor(index, 0.3),
                borderColor: this.getProfileColor(index, 1),
                borderWidth: 2
            };
        });
        
        // Create or update chart
        if (window.elementsComparisonChart) {
            window.elementsComparisonChart.destroy();
        }
        
        window.elementsComparisonChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['목(木)', '화(火)', '토(土)', '금(金)', '수(水)'],
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 5
                    }
                }
            }
        });
    }
    
    async updateCompatibility(profiles) {
        const container = document.getElementById('compatibility-matrix');
        if (!container) return;
        
        if (profiles.length < 2) {
            container.innerHTML = '<p class="no-data">비교할 프로필을 추가해주세요.</p>';
            return;
        }
        
        // Show loading indicator
        container.innerHTML = '<p class="loading">궁합 계산 중...</p>';
        
        // Calculate all compatibility scores first
        const compatibilityScores = {};
        
        for (let i = 0; i < profiles.length; i++) {
            for (let j = 0; j < profiles.length; j++) {
                if (i !== j) {
                    const key = `${i}-${j}`;
                    try {
                        compatibilityScores[key] = await this.calculateCompatibility(profiles[i], profiles[j]);
                    } catch (error) {
                        console.error(`Failed to calculate compatibility for ${key}:`, error);
                        compatibilityScores[key] = 50; // Default score on error
                    }
                }
            }
        }
        
        // Create compatibility matrix with calculated scores
        let html = '<table class="compatibility-table"><thead><tr><th></th>';
        
        profiles.forEach(profile => {
            html += `<th>${profile.name}</th>`;
        });
        
        html += '</tr></thead><tbody>';
        
        for (let i = 0; i < profiles.length; i++) {
            html += `<tr><th>${profiles[i].name}</th>`;
            
            for (let j = 0; j < profiles.length; j++) {
                if (i === j) {
                    html += '<td class="self">-</td>';
                } else {
                    const score = compatibilityScores[`${i}-${j}`] || 50;
                    const scoreClass = score >= 80 ? 'excellent' : score >= 60 ? 'good' : 'average';
                    html += `<td class="${scoreClass}">${Math.round(score)}%</td>`;
                }
            }
            
            html += '</tr>';
        }
        
        html += '</tbody></table>';
        container.innerHTML = html;
    }
    
    updateDetailedComparison(profiles) {
        const container = document.getElementById('detailed-comparison-table');
        if (!container) return;
        
        if (profiles.length < 2) {
            container.innerHTML = '<p class="no-data">비교할 프로필을 추가해주세요.</p>';
            return;
        }
        
        // Create detailed comparison table
        let html = '<table class="detailed-table"><thead><tr><th>항목</th>';
        
        profiles.forEach(profile => {
            html += `<th>${profile.name}</th>`;
        });
        
        html += '</tr></thead><tbody>';
        
        // Compare various aspects
        const aspects = [
            { key: 'year', label: '년주' },
            { key: 'month', label: '월주' },
            { key: 'day', label: '일주' },
            { key: 'hour', label: '시주' }
        ];
        
        aspects.forEach(aspect => {
            html += `<tr><th>${aspect.label}</th>`;
            
            profiles.forEach(profile => {
                const pillar = profile.data[aspect.key];
                if (pillar) {
                    html += `<td>${pillar.heavenly_hanja}${pillar.earthly_hanja}</td>`;
                } else {
                    html += '<td>-</td>';
                }
            });
            
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
    }
    
    // Helper methods
    generateYearOptions() {
        const currentYear = new Date().getFullYear();
        let options = '<option value="">선택</option>';
        for (let year = currentYear; year >= currentYear - 100; year--) {
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
        let options = '<option value="">선택</option>';
        for (let day = 1; day <= 31; day++) {
            options += `<option value="${day}">${day}일</option>`;
        }
        return options;
    }
    
    generateHourOptions() {
        const hours = [
            { value: '23:00', label: '자시 (23:00-01:00)' },
            { value: '01:00', label: '축시 (01:00-03:00)' },
            { value: '03:00', label: '인시 (03:00-05:00)' },
            { value: '05:00', label: '묘시 (05:00-07:00)' },
            { value: '07:00', label: '진시 (07:00-09:00)' },
            { value: '09:00', label: '사시 (09:00-11:00)' },
            { value: '11:00', label: '오시 (11:00-13:00)' },
            { value: '13:00', label: '미시 (13:00-15:00)' },
            { value: '15:00', label: '신시 (15:00-17:00)' },
            { value: '17:00', label: '유시 (17:00-19:00)' },
            { value: '19:00', label: '술시 (19:00-21:00)' },
            { value: '21:00', label: '해시 (21:00-23:00)' }
        ];
        
        let options = '<option value="">선택</option>';
        hours.forEach(hour => {
            options += `<option value="${hour.value}">${hour.label}</option>`;
        });
        return options;
    }
    
    generateElementsBars(elements) {
        if (!elements) return '';
        
        const distribution = elements.distribution || elements;
        const total = Object.values(distribution).reduce((a, b) => a + b, 0);
        
        let html = '<div class="elements-bars-mini">';
        
        ['목', '화', '토', '금', '수'].forEach(element => {
            const count = distribution[element] || 0;
            const percentage = total > 0 ? (count / total) * 100 : 0;
            const color = this.getElementColor(element);
            
            html += `
                <div class="element-bar-mini">
                    <span class="element-name">${element}</span>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: ${percentage}%; background: ${color}"></div>
                    </div>
                    <span class="element-count">${count}</span>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }
    
    getElementColor(element) {
        const colors = {
            '목': '#4CAF50',
            '화': '#FF5722',
            '토': '#FFC107',
            '금': '#9E9E9E',
            '수': '#2196F3'
        };
        return colors[element] || '#999';
    }
    
    getProfileColor(index, alpha) {
        const colors = [
            `rgba(255, 99, 132, ${alpha})`,
            `rgba(54, 162, 235, ${alpha})`,
            `rgba(255, 206, 86, ${alpha})`,
            `rgba(75, 192, 192, ${alpha})`
        ];
        return colors[index % colors.length];
    }
    
    getDominantElement(elements) {
        if (!elements) return '-';
        
        const distribution = elements.distribution || elements;
        let maxElement = '';
        let maxCount = 0;
        
        Object.entries(distribution).forEach(([element, count]) => {
            if (count > maxCount) {
                maxCount = count;
                maxElement = element;
            }
        });
        
        return maxElement || '-';
    }
    
    async calculateCompatibility(profile1, profile2) {
        // inputData가 있으면 사용, 없으면 데이터에서 추출 시도
        const person1Data = profile1.inputData || {
            birthDate: profile1.birthDate || '1990-01-01',
            birthTime: profile1.birthTime || '12:00',
            gender: profile1.gender || 'neutral',
            isLunar: profile1.isLunar || false
        };
        
        const person2Data = profile2.inputData || {
            birthDate: profile2.birthDate || '1990-01-01', 
            birthTime: profile2.birthTime || '12:00',
            gender: profile2.gender || 'neutral',
            isLunar: profile2.isLunar || false
        };
        
        // Use backend API for accurate compatibility calculation
        try {
            const response = await fetch('/api/saju/compatibility', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    person1: person1Data,
                    person2: person2Data
                })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const result = await response.json();
            return result.compatibility?.overall_score || 50;
            
        } catch (error) {
            console.error('Failed to calculate compatibility:', error);
            // Fallback to simple calculation if API fails
            const elements1 = profile1.data?.elements?.distribution || profile1.elements?.distribution || {};
            const elements2 = profile2.data?.elements?.distribution || profile2.elements?.distribution || {};
            
            let score = 50; // Base score
            
            // Check element harmony
            ['목', '화', '토', '금', '수'].forEach(element => {
                const diff = Math.abs((elements1[element] || 0) - (elements2[element] || 0));
                score += (5 - diff) * 2;
            });
            
            // Ensure score is between 0 and 100
            return Math.max(0, Math.min(100, score));
        }
    }
    
    extractBirthInfo(sajuData) {
        return {
            name: sajuData.name || '',
            dateStr: sajuData.birthDate || '',
            timeStr: sajuData.birthTime || '',
            gender: sajuData.gender || ''
        };
    }
    
    generateMockData() {
        const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        
        return {
            year: {
                heavenly: stems[Math.floor(Math.random() * 10)],
                earthly: branches[Math.floor(Math.random() * 12)],
                heavenly_hanja: stems[Math.floor(Math.random() * 10)],
                earthly_hanja: branches[Math.floor(Math.random() * 12)]
            },
            month: {
                heavenly: stems[Math.floor(Math.random() * 10)],
                earthly: branches[Math.floor(Math.random() * 12)],
                heavenly_hanja: stems[Math.floor(Math.random() * 10)],
                earthly_hanja: branches[Math.floor(Math.random() * 12)]
            },
            day: {
                heavenly: stems[Math.floor(Math.random() * 10)],
                earthly: branches[Math.floor(Math.random() * 12)],
                heavenly_hanja: stems[Math.floor(Math.random() * 10)],
                earthly_hanja: branches[Math.floor(Math.random() * 12)]
            },
            hour: {
                heavenly: stems[Math.floor(Math.random() * 10)],
                earthly: branches[Math.floor(Math.random() * 12)],
                heavenly_hanja: stems[Math.floor(Math.random() * 10)],
                earthly_hanja: branches[Math.floor(Math.random() * 12)]
            },
            elements: {
                distribution: {
                    '목': Math.floor(Math.random() * 3) + 1,
                    '화': Math.floor(Math.random() * 3) + 1,
                    '토': Math.floor(Math.random() * 3) + 1,
                    '금': Math.floor(Math.random() * 3) + 1,
                    '수': Math.floor(Math.random() * 3) + 1
                }
            }
        };
    }
    
    showNotification(message) {
        // Create notification if it doesn't exist
        let notification = document.getElementById('comparison-notification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'comparison-notification';
            notification.className = 'comparison-notification';
            document.body.appendChild(notification);
        }
        
        notification.textContent = message;
        notification.classList.add('show');
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
    
    showComparisonMessage(message) {
        const containers = [
            'overview-comparison',
            'elements-analysis',
            'compatibility-matrix',
            'detailed-comparison-table'
        ];
        
        containers.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.innerHTML = `<p class="no-data">${message}</p>`;
            }
        });
    }
}

// Export for use
window.SajuComparison = SajuComparison;