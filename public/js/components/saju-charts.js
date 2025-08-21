/**
 * Saju Charts Component
 * Handles Chart.js visualizations for Saju data
 */

class SajuCharts {
    constructor() {
        this.charts = {};
        this.colors = {
            wood: '#4CAF50',    // 목 - Green
            fire: '#FF5722',    // 화 - Red
            earth: '#FFC107',   // 토 - Yellow
            metal: '#9E9E9E',   // 금 - Gray
            water: '#2196F3'    // 수 - Blue
        };
        
        this.tenGodsColors = {
            '정관': '#E91E63',
            '편관': '#F44336',
            '정인': '#9C27B0',
            '편인': '#673AB7',
            '정재': '#3F51B5',
            '편재': '#2196F3',
            '비견': '#00BCD4',
            '겁재': '#009688',
            '식신': '#4CAF50',
            '상관': '#8BC34A'
        };
    }
    
    /**
     * Initialize Five Elements Radar Chart
     */
    initFiveElementsRadar(canvasId, elementData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const data = {
            labels: ['목(木)', '화(火)', '토(土)', '금(金)', '수(水)'],
            datasets: [{
                label: '오행 분포',
                data: [
                    elementData['목'] || 0,
                    elementData['화'] || 0,
                    elementData['토'] || 0,
                    elementData['금'] || 0,
                    elementData['수'] || 0
                ],
                backgroundColor: 'rgba(139, 69, 19, 0.2)',
                borderColor: 'rgba(139, 69, 19, 1)',
                borderWidth: 2,
                pointBackgroundColor: [
                    this.colors.wood,
                    this.colors.fire,
                    this.colors.earth,
                    this.colors.metal,
                    this.colors.water
                ],
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(139, 69, 19, 1)',
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        };
        
        const options = {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: Math.max(...Object.values(elementData)) + 1 || 5,
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 12
                        }
                    },
                    pointLabels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.parsed.r}개`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        };
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'radar',
            data: data,
            options: options
        });
    }
    
    /**
     * Initialize Five Elements Bar Chart
     */
    initFiveElementsBar(canvasId, elementData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const labels = ['목(木)', '화(火)', '토(土)', '금(金)', '수(水)'];
        const values = [
            elementData['목'] || 0,
            elementData['화'] || 0,
            elementData['토'] || 0,
            elementData['금'] || 0,
            elementData['수'] || 0
        ];
        const backgroundColors = [
            this.colors.wood,
            this.colors.fire,
            this.colors.earth,
            this.colors.metal,
            this.colors.water
        ];
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '오행 개수',
                    data: values,
                    backgroundColor: backgroundColors.map(color => color + '80'), // Add transparency
                    borderColor: backgroundColors,
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = values.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed.y / total) * 100).toFixed(1);
                                return `${context.parsed.y}개 (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutBounce'
                }
            }
        });
    }
    
    /**
     * Initialize Ten Gods Doughnut Chart
     */
    initTenGodsDoughnut(canvasId, tenGodsData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const labels = Object.keys(tenGodsData);
        const values = Object.values(tenGodsData);
        const colors = labels.map(label => this.tenGodsColors[label] || '#ccc');
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.map(color => color + 'CC'), // Add transparency
                    borderColor: colors,
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            padding: 15,
                            font: {
                                size: 12
                            },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                return data.labels.map((label, i) => ({
                                    text: `${label} (${data.datasets[0].data[i]})`,
                                    fillStyle: data.datasets[0].backgroundColor[i],
                                    strokeStyle: data.datasets[0].borderColor[i],
                                    lineWidth: data.datasets[0].borderWidth,
                                    hidden: false,
                                    index: i
                                }));
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = values.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed}개 (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
    
    /**
     * Initialize Ten Gods Polar Area Chart
     */
    initTenGodsPolar(canvasId, tenGodsData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const labels = Object.keys(tenGodsData);
        const values = Object.values(tenGodsData);
        const colors = labels.map(label => this.tenGodsColors[label] || '#ccc');
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors.map(color => color + '80'),
                    borderColor: colors,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 10,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.r}개`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Initialize Fortune Timeline Chart
     */
    initFortuneTimeline(canvasId, fortuneData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const currentAge = fortuneData.currentAge || 30;
        const ages = fortuneData.ages || ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79'];
        const scores = fortuneData.scores || [60, 65, 70, 85, 75, 80, 70, 65];
        
        // Find current period index
        const currentPeriodIndex = Math.floor(currentAge / 10);
        
        // Create point colors
        const pointColors = ages.map((_, index) => 
            index === currentPeriodIndex ? '#FF5722' : '#8B4513'
        );
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ages,
                datasets: [{
                    label: '운세 흐름',
                    data: scores,
                    borderColor: '#8B4513',
                    backgroundColor: 'rgba(139, 69, 19, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: pointColors,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: ages.map((_, index) => 
                        index === currentPeriodIndex ? 8 : 5
                    ),
                    pointHoverRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
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
                            text: '나이'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            title: function(context) {
                                return context[0].label + '세';
                            },
                            label: function(context) {
                                const label = context.parsed.y + '점';
                                if (context.dataIndex === currentPeriodIndex) {
                                    return label + ' (현재)';
                                }
                                return label;
                            }
                        }
                    },
                    annotation: {
                        annotations: {
                            currentPeriod: {
                                type: 'line',
                                xMin: currentPeriodIndex,
                                xMax: currentPeriodIndex,
                                borderColor: 'rgba(255, 87, 34, 0.5)',
                                borderWidth: 2,
                                borderDash: [5, 5],
                                label: {
                                    enabled: true,
                                    content: '현재',
                                    position: 'start'
                                }
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Initialize Yearly Fortune Bar Chart
     */
    initYearlyFortune(canvasId, yearlyData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const currentYear = new Date().getFullYear();
        const years = yearlyData.years || [
            currentYear - 2,
            currentYear - 1,
            currentYear,
            currentYear + 1,
            currentYear + 2
        ];
        const scores = yearlyData.scores || [65, 70, 75, 80, 72];
        
        // Create colors for bars
        const backgroundColors = years.map(year => 
            year === currentYear ? 'rgba(255, 87, 34, 0.6)' : 'rgba(139, 69, 19, 0.6)'
        );
        const borderColors = years.map(year => 
            year === currentYear ? '#FF5722' : '#8B4513'
        );
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: years.map(year => year + '년'),
                datasets: [{
                    label: '연운',
                    data: scores,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 10,
                            callback: function(value) {
                                return value + '점';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.parsed.y + '점';
                                if (context.label === currentYear + '년') {
                                    return label + ' (올해)';
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Update chart data
     */
    updateChart(canvasId, newData) {
        const chart = this.charts[canvasId];
        if (!chart) return;
        
        // Update data based on chart type
        if (chart.config.type === 'radar' || chart.config.type === 'polarArea') {
            chart.data.datasets[0].data = Object.values(newData);
        } else if (chart.config.type === 'doughnut' || chart.config.type === 'pie') {
            chart.data.labels = Object.keys(newData);
            chart.data.datasets[0].data = Object.values(newData);
        } else if (chart.config.type === 'bar' || chart.config.type === 'line') {
            chart.data.datasets[0].data = newData;
        }
        
        chart.update();
    }
    
    /**
     * Destroy all charts
     */
    destroyAll() {
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.charts = {};
    }
    
    /**
     * Export chart as image
     */
    exportChart(canvasId, filename = 'chart.png') {
        const chart = this.charts[canvasId];
        if (!chart) return;
        
        const link = document.createElement('a');
        link.download = filename;
        link.href = chart.toBase64Image();
        link.click();
    }
    
    /**
     * Get chart instance
     */
    getChart(canvasId) {
        return this.charts[canvasId];
    }
}

// Export for use
window.SajuCharts = SajuCharts;