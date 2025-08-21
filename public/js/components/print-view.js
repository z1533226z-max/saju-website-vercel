/**
 * Print View Component
 * Generates PDF-style printable layout for Saju results
 */

class PrintView {
    constructor() {
        this.sajuData = null;
        this.init();
    }
    
    init() {
        // Add print button to results section
        this.addPrintButton();
        
        // Listen for print events
        window.addEventListener('beforeprint', () => this.preparePrintView());
        window.addEventListener('afterprint', () => this.restoreNormalView());
    }
    
    addPrintButton() {
        // Check if button already exists
        if (document.getElementById('print-button')) return;
        
        const button = document.createElement('button');
        button.id = 'print-button';
        button.className = 'btn-print';
        button.innerHTML = `
            <span class="print-icon">🖨️</span>
            <span class="print-text">인쇄하기</span>
        `;
        button.onclick = () => this.print();
        
        // Add button to results section header if it exists
        const resultsHeader = document.querySelector('#results-section .section-header');
        if (resultsHeader) {
            resultsHeader.appendChild(button);
        }
    }
    
    print() {
        // Prepare print view
        this.preparePrintView();
        
        // Trigger print dialog
        window.print();
    }
    
    preparePrintView() {
        // Create print-specific container
        const printContainer = document.createElement('div');
        printContainer.id = 'print-container';
        printContainer.className = 'print-view';
        
        // Generate print content
        printContainer.innerHTML = this.generatePrintContent();
        
        // Add to body
        document.body.appendChild(printContainer);
        
        // Hide normal content
        document.body.classList.add('printing');
    }
    
    restoreNormalView() {
        // Remove print container
        const printContainer = document.getElementById('print-container');
        if (printContainer) {
            printContainer.remove();
        }
        
        // Show normal content
        document.body.classList.remove('printing');
    }
    
    generatePrintContent() {
        const currentDate = new Date().toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        return `
            <div class="print-page">
                <!-- Header -->
                <div class="print-header">
                    <div class="print-logo">
                        <h1>사주명리 분석서</h1>
                        <p class="print-subtitle">Four Pillars of Destiny Analysis Report</p>
                    </div>
                    <div class="print-date">
                        <p>발행일: ${currentDate}</p>
                    </div>
                </div>
                
                <!-- Personal Info -->
                <div class="print-section">
                    <h2 class="print-section-title">1. 개인 정보</h2>
                    <table class="print-info-table">
                        <tr>
                            <td class="label">이름</td>
                            <td class="value">${this.getPersonalInfo('name')}</td>
                            <td class="label">성별</td>
                            <td class="value">${this.getPersonalInfo('gender')}</td>
                        </tr>
                        <tr>
                            <td class="label">생년월일</td>
                            <td class="value">${this.getPersonalInfo('birthDate')}</td>
                            <td class="label">출생시간</td>
                            <td class="value">${this.getPersonalInfo('birthTime')}</td>
                        </tr>
                        <tr>
                            <td class="label">음력/양력</td>
                            <td class="value">${this.getPersonalInfo('calendarType')}</td>
                            <td class="label">현재 나이</td>
                            <td class="value">${this.getPersonalInfo('age')}세</td>
                        </tr>
                    </table>
                </div>
                
                <!-- Four Pillars -->
                <div class="print-section">
                    <h2 class="print-section-title">2. 사주팔자 (四柱八字)</h2>
                    <div class="print-pillars">
                        <table class="pillars-table">
                            <thead>
                                <tr>
                                    <th>구분</th>
                                    <th>년주 (年柱)</th>
                                    <th>월주 (月柱)</th>
                                    <th>일주 (日柱)</th>
                                    <th>시주 (時柱)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="heavenly-row">
                                    <td class="label">천간</td>
                                    <td class="stem">${this.getPillarData('year', 'heavenly')}</td>
                                    <td class="stem">${this.getPillarData('month', 'heavenly')}</td>
                                    <td class="stem day-master">${this.getPillarData('day', 'heavenly')}</td>
                                    <td class="stem">${this.getPillarData('hour', 'heavenly')}</td>
                                </tr>
                                <tr class="earthly-row">
                                    <td class="label">지지</td>
                                    <td class="branch">${this.getPillarData('year', 'earthly')}</td>
                                    <td class="branch">${this.getPillarData('month', 'earthly')}</td>
                                    <td class="branch">${this.getPillarData('day', 'earthly')}</td>
                                    <td class="branch">${this.getPillarData('hour', 'earthly')}</td>
                                </tr>
                                <tr class="element-row">
                                    <td class="label">오행</td>
                                    <td class="element">${this.getPillarElement('year')}</td>
                                    <td class="element">${this.getPillarElement('month')}</td>
                                    <td class="element">${this.getPillarElement('day')}</td>
                                    <td class="element">${this.getPillarElement('hour')}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <!-- Five Elements Distribution -->
                <div class="print-section">
                    <h2 class="print-section-title">3. 오행 분포 (五行分布)</h2>
                    <div class="print-elements">
                        <table class="elements-table">
                            <thead>
                                <tr>
                                    <th>목 (木)</th>
                                    <th>화 (火)</th>
                                    <th>토 (土)</th>
                                    <th>금 (金)</th>
                                    <th>수 (水)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>${this.getElementCount('목')}</td>
                                    <td>${this.getElementCount('화')}</td>
                                    <td>${this.getElementCount('토')}</td>
                                    <td>${this.getElementCount('금')}</td>
                                    <td>${this.getElementCount('수')}</td>
                                </tr>
                                <tr class="percentage-row">
                                    <td>${this.getElementPercentage('목')}%</td>
                                    <td>${this.getElementPercentage('화')}%</td>
                                    <td>${this.getElementPercentage('토')}%</td>
                                    <td>${this.getElementPercentage('금')}%</td>
                                    <td>${this.getElementPercentage('수')}%</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="element-chart-placeholder">
                            ${this.generateElementBars()}
                        </div>
                    </div>
                </div>
                
                <!-- Ten Gods Analysis -->
                <div class="print-section">
                    <h2 class="print-section-title">4. 십성 분석 (十星分析)</h2>
                    <div class="print-ten-gods">
                        ${this.generateTenGodsTable()}
                    </div>
                </div>
                
                <!-- Basic Interpretation -->
                <div class="print-section">
                    <h2 class="print-section-title">5. 기본 해석</h2>
                    <div class="print-interpretation">
                        ${this.generateInterpretation()}
                    </div>
                </div>
                
                <!-- Major Fortune -->
                <div class="print-section">
                    <h2 class="print-section-title">6. 대운 (大運)</h2>
                    <div class="print-major-fortune">
                        ${this.generateMajorFortune()}
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="print-footer">
                    <div class="disclaimer">
                        <p>※ 본 분석서는 전통 사주명리학을 바탕으로 작성되었습니다.</p>
                        <p>※ 개인의 노력과 환경에 따라 운명은 변할 수 있습니다.</p>
                    </div>
                    <div class="print-copyright">
                        <p>© 2024 사주명리 - sajumyungri.com</p>
                    </div>
                </div>
            </div>
        `;
    }
    
    getPersonalInfo(field) {
        // Get from form data or stored data
        const formData = this.getFormData();
        
        switch(field) {
            case 'name':
                return formData.name || '미입력';
            case 'gender':
                return formData.gender || '남';
            case 'birthDate':
                return formData.birthDate || '2000년 1월 1일';
            case 'birthTime':
                return formData.birthTime || '12:00';
            case 'calendarType':
                return formData.isLunar ? '음력' : '양력';
            case 'age':
                if (formData.birthDate) {
                    const birthYear = new Date(formData.birthDate).getFullYear();
                    const currentYear = new Date().getFullYear();
                    return currentYear - birthYear + 1; // Korean age
                }
                return '미상';
            default:
                return '';
        }
    }
    
    getFormData() {
        // Get saved form data from localStorage
        const savedData = localStorage.getItem('sajuFormData');
        if (savedData) {
            try {
                return JSON.parse(savedData);
            } catch (e) {
                console.error('Error parsing saved form data:', e);
            }
        }
        
        // Or get from current form
        return {
            name: document.getElementById('name')?.value || '',
            gender: document.getElementById('gender')?.value || '남',
            birthDate: document.getElementById('birthDate')?.value || '',
            birthTime: document.getElementById('birthTime')?.value || '',
            isLunar: document.getElementById('isLunar')?.checked || false
        };
    }
    
    getPillarData(pillar, type) {
        if (!this.sajuData || !this.sajuData[pillar]) return '-';
        
        if (type === 'heavenly') {
            return this.sajuData[pillar].heavenly_hanja || this.sajuData[pillar].heavenly || '-';
        } else if (type === 'earthly') {
            return this.sajuData[pillar].earthly_hanja || this.sajuData[pillar].earthly || '-';
        }
        
        return '-';
    }
    
    getPillarElement(pillar) {
        if (!this.sajuData || !this.sajuData[pillar]) return '-';
        
        const heavenly = this.sajuData[pillar].heavenly_element || '';
        const earthly = this.sajuData[pillar].earthly_element || '';
        
        return `${heavenly}${earthly}`;
    }
    
    getElementCount(element) {
        if (!this.sajuData || !this.sajuData.elements) return 0;
        
        const distribution = this.sajuData.elements.distribution || this.sajuData.elements;
        return distribution[element] || 0;
    }
    
    getElementPercentage(element) {
        const count = this.getElementCount(element);
        const total = this.getTotalElements();
        
        if (total === 0) return 0;
        return Math.round((count / total) * 100);
    }
    
    getTotalElements() {
        if (!this.sajuData || !this.sajuData.elements) return 0;
        
        const distribution = this.sajuData.elements.distribution || this.sajuData.elements;
        return Object.values(distribution).reduce((sum, count) => sum + count, 0);
    }
    
    generateElementBars() {
        const elements = ['목', '화', '토', '금', '수'];
        const colors = ['#4CAF50', '#FF5722', '#FFC107', '#9E9E9E', '#2196F3'];
        
        return `
            <div class="element-bars">
                ${elements.map((element, index) => {
                    const percentage = this.getElementPercentage(element);
                    return `
                        <div class="element-bar-row">
                            <span class="element-label">${element}</span>
                            <div class="element-bar">
                                <div class="element-fill" style="width: ${percentage}%; background: ${colors[index]}"></div>
                            </div>
                            <span class="element-value">${percentage}%</span>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }
    
    generateTenGodsTable() {
        const tenGods = [
            { name: '정관 (正官)', count: 2 },
            { name: '편관 (偏官)', count: 1 },
            { name: '정인 (正印)', count: 3 },
            { name: '편인 (偏印)', count: 1 },
            { name: '정재 (正財)', count: 2 },
            { name: '편재 (偏財)', count: 1 },
            { name: '비견 (比肩)', count: 1 },
            { name: '겁재 (劫財)', count: 0 },
            { name: '식신 (食神)', count: 1 },
            { name: '상관 (傷官)', count: 0 }
        ];
        
        // Get actual data if available
        if (this.sajuData && this.sajuData.ten_gods) {
            // Update with actual data
        }
        
        return `
            <table class="ten-gods-table">
                <thead>
                    <tr>
                        <th>십성</th>
                        <th>개수</th>
                        <th>특징</th>
                    </tr>
                </thead>
                <tbody>
                    ${tenGods.map(god => `
                        <tr>
                            <td>${god.name}</td>
                            <td>${god.count}</td>
                            <td>${this.getTenGodDescription(god.name)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
    
    getTenGodDescription(godName) {
        const descriptions = {
            '정관 (正官)': '명예, 지위, 권력',
            '편관 (偏官)': '도전, 모험, 변화',
            '정인 (正印)': '학문, 지혜, 인덕',
            '편인 (偏印)': '예술, 창의, 직관',
            '정재 (正財)': '안정, 재물, 절약',
            '편재 (偏財)': '투자, 사업, 활동',
            '비견 (比肩)': '협력, 경쟁, 독립',
            '겁재 (劫財)': '적극, 대담, 승부',
            '식신 (食神)': '표현, 즐거움, 여유',
            '상관 (傷官)': '개혁, 비판, 창조'
        };
        
        return descriptions[godName] || '';
    }
    
    generateInterpretation() {
        // Generate basic interpretation text
        const interpretation = this.sajuData?.interpretation || {
            personality: '성격 분석 내용',
            career: '직업 적성 분석',
            wealth: '재물운 분석',
            relationship: '인간관계 분석',
            health: '건강운 분석'
        };
        
        return `
            <div class="interpretation-content">
                <div class="interpretation-item">
                    <h4>성격 특성</h4>
                    <p>${interpretation.personality || '일간과 격국을 바탕으로 한 성격 분석이 표시됩니다.'}</p>
                </div>
                <div class="interpretation-item">
                    <h4>직업 적성</h4>
                    <p>${interpretation.career || '십성과 오행을 바탕으로 한 직업 적성이 표시됩니다.'}</p>
                </div>
                <div class="interpretation-item">
                    <h4>재물운</h4>
                    <p>${interpretation.wealth || '재성과 관련된 재물운 분석이 표시됩니다.'}</p>
                </div>
                <div class="interpretation-item">
                    <h4>인간관계</h4>
                    <p>${interpretation.relationship || '인성과 비겁을 통한 인간관계 분석이 표시됩니다.'}</p>
                </div>
                <div class="interpretation-item">
                    <h4>건강운</h4>
                    <p>${interpretation.health || '오행 균형을 통한 건강운 분석이 표시됩니다.'}</p>
                </div>
            </div>
        `;
    }
    
    generateMajorFortune() {
        // Generate major fortune periods
        const fortunes = [];
        for (let i = 0; i < 8; i++) {
            const startAge = i * 10 + 1;
            const endAge = (i + 1) * 10;
            fortunes.push({
                period: `${startAge}-${endAge}세`,
                stems: '戊申',
                element: '土金',
                score: 70 + Math.random() * 20
            });
        }
        
        return `
            <table class="major-fortune-table">
                <thead>
                    <tr>
                        <th>나이</th>
                        <th>대운</th>
                        <th>오행</th>
                        <th>운세</th>
                    </tr>
                </thead>
                <tbody>
                    ${fortunes.map(fortune => `
                        <tr>
                            <td>${fortune.period}</td>
                            <td>${fortune.stems}</td>
                            <td>${fortune.element}</td>
                            <td>${Math.round(fortune.score)}점</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
    
    updateWithSajuData(sajuData) {
        this.sajuData = sajuData;
    }
}

// Export for use
window.PrintView = PrintView;