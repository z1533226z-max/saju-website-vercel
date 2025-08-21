/**
 * Fortune Timeline Component
 * Visualizes 대운 (Major Fortune) and 세운 (Yearly Fortune) flow
 */

class FortuneTimeline {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentAge = 30; // Will be calculated from birth date
        this.majorFortunes = [];
        this.yearlyFortunes = [];
        this.init();
    }
    
    init() {
        if (!this.container) return;
        this.render();
    }
    
    render() {
        const html = `
            <div class="fortune-timeline-container">
                <div class="timeline-header">
                    <h3>운세 흐름도</h3>
                    <div class="timeline-controls">
                        <button class="btn-zoom-in" onclick="fortuneTimeline.zoomIn()">
                            <span>🔍+</span>
                        </button>
                        <button class="btn-zoom-out" onclick="fortuneTimeline.zoomOut()">
                            <span>🔍-</span>
                        </button>
                        <button class="btn-reset-zoom" onclick="fortuneTimeline.resetZoom()">
                            <span>↺</span>
                        </button>
                    </div>
                </div>
                
                <div class="timeline-body">
                    <!-- Major Fortune Timeline -->
                    <div class="major-fortune-timeline">
                        <h4>대운 (大運)</h4>
                        <div class="timeline-track" id="major-fortune-track">
                            <!-- Major fortune periods will be rendered here -->
                        </div>
                    </div>
                    
                    <!-- Yearly Fortune Timeline -->
                    <div class="yearly-fortune-timeline">
                        <h4>세운 (歲運)</h4>
                        <div class="timeline-track" id="yearly-fortune-track">
                            <!-- Yearly fortunes will be rendered here -->
                        </div>
                    </div>
                    
                    <!-- Combined Fortune Graph -->
                    <div class="combined-fortune-graph">
                        <h4>종합 운세 그래프</h4>
                        <canvas id="combined-fortune-chart"></canvas>
                    </div>
                </div>
                
                <!-- Fortune Details Panel -->
                <div class="fortune-details-panel" id="fortune-details">
                    <h4>운세 상세</h4>
                    <div class="details-content">
                        <p>시간대를 클릭하여 상세 정보를 확인하세요.</p>
                    </div>
                </div>
            </div>
        `;
        
        this.container.innerHTML = html;
        this.initializeTimelines();
    }
    
    initializeTimelines() {
        // Initialize with sample data - would be replaced with actual Saju data
        this.majorFortunes = this.generateMajorFortunes();
        this.yearlyFortunes = this.generateYearlyFortunes();
        
        this.renderMajorFortunes();
        this.renderYearlyFortunes();
        this.renderCombinedGraph();
    }
    
    generateMajorFortunes() {
        // Generate major fortune periods (10-year cycles)
        const fortunes = [];
        const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        
        for (let i = 0; i < 8; i++) {
            const startAge = i * 10 + 1;
            const endAge = (i + 1) * 10;
            const stemIndex = (i * 2) % 10;
            const branchIndex = (i * 2) % 12;
            
            fortunes.push({
                period: `${startAge}-${endAge}세`,
                stem: stems[stemIndex],
                branch: branches[branchIndex],
                score: 50 + Math.random() * 40,
                element: this.getElementFromStemBranch(stems[stemIndex], branches[branchIndex]),
                description: this.getFortuneDescription(i),
                isCurrent: startAge <= this.currentAge && this.currentAge <= endAge
            });
        }
        
        return fortunes;
    }
    
    generateYearlyFortunes() {
        // Generate yearly fortunes for recent and upcoming years
        const fortunes = [];
        const currentYear = new Date().getFullYear();
        const birthYear = currentYear - this.currentAge;
        
        for (let year = currentYear - 5; year <= currentYear + 10; year++) {
            const age = year - birthYear;
            fortunes.push({
                year: year,
                age: age,
                stem: this.getYearStem(year),
                branch: this.getYearBranch(year),
                score: 50 + Math.random() * 40,
                element: this.getYearElement(year),
                isCurrent: year === currentYear,
                isPast: year < currentYear,
                isFuture: year > currentYear
            });
        }
        
        return fortunes;
    }
    
    renderMajorFortunes() {
        const track = document.getElementById('major-fortune-track');
        if (!track) return;
        
        const html = this.majorFortunes.map((fortune, index) => `
            <div class="fortune-period ${fortune.isCurrent ? 'current' : ''}" 
                 data-index="${index}"
                 onclick="fortuneTimeline.showFortuneDetails('major', ${index})">
                <div class="period-header">
                    <span class="period-age">${fortune.period}</span>
                    <span class="period-score">${Math.round(fortune.score)}점</span>
                </div>
                <div class="period-content">
                    <div class="period-stems">
                        <span class="stem">${fortune.stem}</span>
                        <span class="branch">${fortune.branch}</span>
                    </div>
                    <div class="period-element">${fortune.element}</div>
                    <div class="period-bar">
                        <div class="bar-fill" style="width: ${fortune.score}%; background: ${this.getScoreColor(fortune.score)}"></div>
                    </div>
                </div>
            </div>
        `).join('');
        
        track.innerHTML = html;
    }
    
    renderYearlyFortunes() {
        const track = document.getElementById('yearly-fortune-track');
        if (!track) return;
        
        const html = `
            <div class="yearly-timeline-scroll">
                ${this.yearlyFortunes.map((fortune, index) => `
                    <div class="yearly-period ${fortune.isCurrent ? 'current' : ''} ${fortune.isPast ? 'past' : ''}" 
                         data-index="${index}"
                         onclick="fortuneTimeline.showFortuneDetails('yearly', ${index})">
                        <div class="year-label">${fortune.year}</div>
                        <div class="year-age">${fortune.age}세</div>
                        <div class="year-stems">
                            <span class="stem">${fortune.stem}</span>
                            <span class="branch">${fortune.branch}</span>
                        </div>
                        <div class="year-score">
                            <div class="score-dot" style="background: ${this.getScoreColor(fortune.score)}"></div>
                            <span>${Math.round(fortune.score)}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        track.innerHTML = html;
        
        // Auto-scroll to current year
        this.scrollToCurrentYear();
    }
    
    renderCombinedGraph() {
        const canvas = document.getElementById('combined-fortune-chart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        
        // Prepare data for combined graph
        const currentYear = new Date().getFullYear();
        const labels = [];
        const majorData = [];
        const yearlyData = [];
        
        // Create data points for graph
        for (let year = currentYear - 5; year <= currentYear + 10; year++) {
            labels.push(year);
            
            // Find corresponding major fortune
            const age = year - (currentYear - this.currentAge);
            const majorFortune = this.majorFortunes.find(f => {
                const [startAge, endAge] = f.period.split('-').map(s => parseInt(s));
                return age >= startAge && age <= endAge;
            });
            majorData.push(majorFortune ? majorFortune.score : 50);
            
            // Find yearly fortune
            const yearlyFortune = this.yearlyFortunes.find(f => f.year === year);
            yearlyData.push(yearlyFortune ? yearlyFortune.score : 50);
        }
        
        // Create chart
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: '대운',
                        data: majorData,
                        borderColor: '#8B4513',
                        backgroundColor: 'rgba(139, 69, 19, 0.1)',
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: '세운',
                        data: yearlyData,
                        borderColor: '#FF5722',
                        backgroundColor: 'rgba(255, 87, 34, 0.1)',
                        tension: 0.4,
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointRadius: 3,
                        pointHoverRadius: 5
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 0,
                        max: 100,
                        ticks: {
                            stepSize: 10,
                            callback: function(value) {
                                return value + '점';
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '연도'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                const year = context[0].label;
                                const age = year - (currentYear - this.currentAge);
                                return `${year}년 (${age}세)`;
                            }.bind(this)
                        }
                    }
                }
            }
        });
    }
    
    showFortuneDetails(type, index) {
        const panel = document.getElementById('fortune-details');
        if (!panel) return;
        
        const detailsContent = panel.querySelector('.details-content');
        
        if (type === 'major') {
            const fortune = this.majorFortunes[index];
            detailsContent.innerHTML = `
                <div class="fortune-detail-card">
                    <h5>대운 ${fortune.period}</h5>
                    <div class="detail-items">
                        <div class="detail-item">
                            <span class="label">천간지지:</span>
                            <span class="value">${fortune.stem}${fortune.branch}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">오행:</span>
                            <span class="value">${fortune.element}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">운세 점수:</span>
                            <span class="value">${Math.round(fortune.score)}점</span>
                        </div>
                    </div>
                    <div class="detail-description">
                        <p>${fortune.description}</p>
                    </div>
                    ${fortune.isCurrent ? '<div class="current-badge">현재 대운</div>' : ''}
                </div>
            `;
        } else if (type === 'yearly') {
            const fortune = this.yearlyFortunes[index];
            detailsContent.innerHTML = `
                <div class="fortune-detail-card">
                    <h5>${fortune.year}년 (${fortune.age}세)</h5>
                    <div class="detail-items">
                        <div class="detail-item">
                            <span class="label">천간지지:</span>
                            <span class="value">${fortune.stem}${fortune.branch}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">오행:</span>
                            <span class="value">${fortune.element}</span>
                        </div>
                        <div class="detail-item">
                            <span class="label">운세 점수:</span>
                            <span class="value">${Math.round(fortune.score)}점</span>
                        </div>
                    </div>
                    ${fortune.isCurrent ? '<div class="current-badge">올해</div>' : ''}
                </div>
            `;
        }
        
        // Highlight selected period
        document.querySelectorAll('.fortune-period, .yearly-period').forEach(el => {
            el.classList.remove('selected');
        });
        
        const selector = type === 'major' ? '.fortune-period' : '.yearly-period';
        const selectedElement = document.querySelector(`${selector}[data-index="${index}"]`);
        if (selectedElement) {
            selectedElement.classList.add('selected');
        }
    }
    
    scrollToCurrentYear() {
        const currentYearElement = document.querySelector('.yearly-period.current');
        if (currentYearElement) {
            const scrollContainer = document.querySelector('.yearly-timeline-scroll');
            if (scrollContainer) {
                const containerWidth = scrollContainer.offsetWidth;
                const elementOffset = currentYearElement.offsetLeft;
                const elementWidth = currentYearElement.offsetWidth;
                scrollContainer.scrollLeft = elementOffset - (containerWidth / 2) + (elementWidth / 2);
            }
        }
    }
    
    getScoreColor(score) {
        if (score >= 80) return '#4CAF50';  // Excellent - Green
        if (score >= 70) return '#8BC34A';  // Good - Light Green
        if (score >= 60) return '#FFC107';  // Average - Yellow
        if (score >= 50) return '#FF9800';  // Below Average - Orange
        return '#F44336';  // Poor - Red
    }
    
    getElementFromStemBranch(stem, branch) {
        const stemElements = {
            '甲': '木', '乙': '木',
            '丙': '火', '丁': '火',
            '戊': '土', '己': '土',
            '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        };
        const branchElements = {
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        };
        
        return `${stemElements[stem] || ''}${branchElements[branch] || ''}`;
    }
    
    getFortuneDescription(periodIndex) {
        const descriptions = [
            '유년기의 순수함과 성장의 시기입니다. 기초를 다지는 중요한 때입니다.',
            '청소년기의 열정과 도전의 시기입니다. 학업과 진로 결정이 중요합니다.',
            '청년기의 활력과 시작의 시기입니다. 사회 진출과 관계 형성이 활발합니다.',
            '장년기의 안정과 성취의 시기입니다. 경력과 가정이 중요한 시기입니다.',
            '중년기의 성숙과 책임의 시기입니다. 리더십과 지혜가 빛나는 때입니다.',
            '중년 후기의 수확과 나눔의 시기입니다. 경험을 활용하는 시기입니다.',
            '노년기의 지혜와 여유의 시기입니다. 인생을 정리하고 즐기는 때입니다.',
            '노년 후기의 평안과 회고의 시기입니다. 후대에 지혜를 전하는 때입니다.'
        ];
        
        return descriptions[periodIndex] || '운세의 흐름이 지속됩니다.';
    }
    
    getYearStem(year) {
        const stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
        return stems[(year - 4) % 10];
    }
    
    getYearBranch(year) {
        const branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
        return branches[(year - 4) % 12];
    }
    
    getYearElement(year) {
        const stem = this.getYearStem(year);
        const branch = this.getYearBranch(year);
        return this.getElementFromStemBranch(stem, branch);
    }
    
    updateWithSajuData(sajuData) {
        // Update timeline with actual Saju calculation data
        if (!sajuData) return;
        
        if (sajuData.birthDate) {
            const birthYear = new Date(sajuData.birthDate).getFullYear();
            const currentYear = new Date().getFullYear();
            this.currentAge = currentYear - birthYear;
        }
        
        if (sajuData.majorFortunes) {
            this.majorFortunes = sajuData.majorFortunes;
            this.renderMajorFortunes();
        }
        
        if (sajuData.yearlyFortunes) {
            this.yearlyFortunes = sajuData.yearlyFortunes;
            this.renderYearlyFortunes();
        }
        
        this.renderCombinedGraph();
    }
    
    zoomIn() {
        // Implement zoom functionality
        const tracks = document.querySelectorAll('.timeline-track');
        tracks.forEach(track => {
            const currentScale = track.style.transform ? 
                parseFloat(track.style.transform.match(/scale\(([\d.]+)\)/)?.[1] || 1) : 1;
            const newScale = Math.min(currentScale * 1.2, 2);
            track.style.transform = `scaleX(${newScale})`;
        });
    }
    
    zoomOut() {
        const tracks = document.querySelectorAll('.timeline-track');
        tracks.forEach(track => {
            const currentScale = track.style.transform ? 
                parseFloat(track.style.transform.match(/scale\(([\d.]+)\)/)?.[1] || 1) : 1;
            const newScale = Math.max(currentScale * 0.8, 0.5);
            track.style.transform = `scaleX(${newScale})`;
        });
    }
    
    resetZoom() {
        const tracks = document.querySelectorAll('.timeline-track');
        tracks.forEach(track => {
            track.style.transform = 'scaleX(1)';
        });
    }
}

// Export for use
window.FortuneTimeline = FortuneTimeline;