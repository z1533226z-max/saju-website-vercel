/**
 * 사주팔자 폼 개선 버전 - 한자 의미 설명 강화
 * 2025-08-19 업데이트
 */

window.sajuForm = function() {
    return {
        // 기본 데이터
        birthYear: '',
        birthMonth: '',
        birthDay: '',
        selectedHour: '',
        gender: '',
        calendarType: 'solar',
        loading: false,
        showResults: false,
        showExtendedFeatures: false,
        resultTab: 'basic',
        
        // 결과 데이터
        saju: {
            year: { heavenly: '', earthly: '' },
            month: { heavenly: '', earthly: '' },
            day: { heavenly: '', earthly: '' },
            hour: { heavenly: '', earthly: '' }
        },
        elements: [],
        interpretation: {},
        tenGods: {},
        majorFortune: {},
        fortuneTimeline: {},
        balance: {},
        pattern: null,
        shinshal: null,
        yongshin: null,
        
        // 천간 한글 및 설명
        heavenlyStemInfo: {
            '갑': { korean: '갑', meaning: '큰 나무', element: '목(+)', color: '#2D7A2D' },
            '을': { korean: '을', meaning: '작은 나무', element: '목(-)', color: '#4CAF50' },
            '병': { korean: '병', meaning: '태양', element: '화(+)', color: '#FF6B6B' },
            '정': { korean: '정', meaning: '촛불', element: '화(-)', color: '#FF9999' },
            '무': { korean: '무', meaning: '산', element: '토(+)', color: '#8B7355' },
            '기': { korean: '기', meaning: '논밭', element: '토(-)', color: '#BDB76B' },
            '경': { korean: '경', meaning: '쇠', element: '금(+)', color: '#808080' },
            '신': { korean: '신', meaning: '보석', element: '금(-)', color: '#C0C0C0' },
            '임': { korean: '임', meaning: '바다', element: '수(+)', color: '#1E5BA8' },
            '계': { korean: '계', meaning: '샘물', element: '수(-)', color: '#87CEEB' }
        },
        
        // 지지 한글 및 설명
        earthlyBranchInfo: {
            '자': { korean: '자', animal: '쥐', time: '23-01시', element: '수', symbol: '🐭' },
            '축': { korean: '축', animal: '소', time: '01-03시', element: '토', symbol: '🐮' },
            '인': { korean: '인', animal: '호랑이', time: '03-05시', element: '목', symbol: '🐯' },
            '묘': { korean: '묘', animal: '토끼', time: '05-07시', element: '목', symbol: '🐰' },
            '진': { korean: '진', animal: '용', time: '07-09시', element: '토', symbol: '🐲' },
            '사': { korean: '사', animal: '뱀', time: '09-11시', element: '화', symbol: '🐍' },
            '오': { korean: '오', animal: '말', time: '11-13시', element: '화', symbol: '🐴' },
            '미': { korean: '미', animal: '양', time: '13-15시', element: '토', symbol: '🐑' },
            '신': { korean: '신', animal: '원숭이', time: '15-17시', element: '금', symbol: '🐵' },
            '유': { korean: '유', animal: '닭', time: '17-19시', element: '금', symbol: '🐓' },
            '술': { korean: '술', animal: '개', time: '19-21시', element: '토', symbol: '🐕' },
            '해': { korean: '해', animal: '돼지', time: '21-23시', element: '수', symbol: '🐷' }
        },
        
        // 개선된 한글 변환 함수들
        getStemFullInfo(stem) {
            const info = this.heavenlyStemInfo[stem];
            if (!info) return { korean: stem, meaning: '', element: '' };
            return info;
        },
        
        getBranchFullInfo(branch) {
            const info = this.earthlyBranchInfo[branch];
            if (!info) return { korean: branch, animal: '', time: '', element: '' };
            return info;
        },
        
        // 기존 함수들 (호환성 유지)
        getKoreanStem(stem) {
            const info = this.heavenlyStemInfo[stem];
            return info ? `${info.korean}(${info.meaning})` : stem;
        },
        
        getKoreanBranch(branch) {
            const info = this.earthlyBranchInfo[branch];
            return info ? `${info.korean}(${info.animal}띠)` : branch;
        },
        
        getStemElement(stem) {
            const info = this.heavenlyStemInfo[stem];
            if (!info) return '';
            const elementEmoji = {
                '목(+)': '🌲', '목(-)': '🌿',
                '화(+)': '☀️', '화(-)': '🕯️',
                '토(+)': '⛰️', '토(-)': '🌾',
                '금(+)': '⚔️', '금(-)': '💎',
                '수(+)': '🌊', '수(-)': '💧'
            };
            return `${elementEmoji[info.element] || ''} ${info.element}`;
        },
        
        getBranchAnimal(branch) {
            const info = this.earthlyBranchInfo[branch];
            return info ? `${info.symbol} ${info.animal}띠` : '';
        },

        // 결과 아래 '함께 보면 좋은 운세' 링크: 년주 지지 = 띠, 일주 천간 = 일간
        branchZodiacKeys: {
            '자': 'rat', '축': 'ox', '인': 'tiger', '묘': 'rabbit', '진': 'dragon', '사': 'snake',
            '오': 'horse', '미': 'goat', '신': 'monkey', '유': 'rooster', '술': 'dog', '해': 'pig'
        },

        get zodiacKey() {
            return this.branchZodiacKeys[this.saju?.year?.earthly] || '';
        },

        get zodiacName() {
            const info = this.earthlyBranchInfo[this.saju?.year?.earthly];
            return info ? `${info.animal}띠` : '';
        },

        get dayStemLabel() {
            const stem = this.saju?.day?.heavenly;
            if (!this.heavenlyStemInfo[stem]) return '';
            const hanja = this.saju?.day?.heavenly_hanja;
            return hanja ? `${stem}(${hanja})` : stem;
        },
        
        // 년도 옵션 생성
        get yearOptions() {
            const years = [];
            const currentYear = new Date().getFullYear();
            for (let year = currentYear; year >= 1930; year--) {
                years.push(year);
            }
            return years;
        },
        
        // 시간 옵션
        timeOptions: [
            { value: '00:30', name: '자시', time: '23:00-01:00' },
            { value: '02:30', name: '축시', time: '01:00-03:00' },
            { value: '04:30', name: '인시', time: '03:00-05:00' },
            { value: '06:30', name: '묘시', time: '05:00-07:00' },
            { value: '08:30', name: '진시', time: '07:00-09:00' },
            { value: '10:30', name: '사시', time: '09:00-11:00' },
            { value: '12:30', name: '오시', time: '11:00-13:00' },
            { value: '14:30', name: '미시', time: '13:00-15:00' },
            { value: '16:30', name: '신시', time: '15:00-17:00' },
            { value: '18:30', name: '유시', time: '17:00-19:00' },
            { value: '20:30', name: '술시', time: '19:00-21:00' },
            { value: '22:30', name: '해시', time: '21:00-23:00' }
        ],
        
        // 사주 계산
        async calculateSaju() {
            // 입력 검증
            if (!this.birthYear || !this.birthMonth || !this.birthDay || !this.selectedHour || !this.gender) {
                if (typeof showToast === 'function') {
                    showToast('모든 항목을 입력해주세요.', 'warning');
                } else {
                    alert('모든 항목을 입력해주세요.');
                }
                return;
            }
            
            this.loading = true;

            // Disable submit button during API flight
            var submitBtn = document.querySelector('.submit-button');
            if (submitBtn) submitBtn.disabled = true;

            try {
                // API 호출 데이터 준비
                const formData = {
                    birthDate: `${this.birthYear}-${String(this.birthMonth).padStart(2, '0')}-${String(this.birthDay).padStart(2, '0')}`,
                    birthTime: this.selectedHour,
                    gender: this.gender,
                    isLunar: this.calendarType === 'lunar'
                };
                
                // API 호출
                const response = await fetch('/api/saju/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();

                if (!response.ok || result.status === 'error') {
                    throw new Error(result.error || '서버 오류가 발생했습니다.');
                }
                
                // 결과 데이터 매핑
                this.mapResultData(result);
                
                // 선택한 시간의 십이지시 이름 찾기
                const selectedTimeOption = this.timeOptions.find(opt => opt.value === formData.birthTime);
                const hourName = selectedTimeOption ? selectedTimeOption.name : formData.birthTime;
                
                // 사주 계산 정보를 전역 변수에 저장 (궁합 등에서 사용)
                window.lastSajuCalculation = {
                    birthDate: formData.birthDate,
                    birthTime: formData.birthTime,
                    birthHourName: hourName,  // 십이지시 이름 저장
                    birthTimeRange: selectedTimeOption ? selectedTimeOption.time : '',  // 시간 범위
                    gender: formData.gender,
                    isLunar: formData.isLunar,
                    name: this.name || '본인',
                    result: result
                };
                
                // 차트 그리기
                this.drawCharts();
                
                // 결과 표시
                this.showResults = true;
                
                // 결과 섹션으로 스크롤
                setTimeout(() => {
                    document.getElementById('results-section')?.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }, 100);
                
            } catch (error) {
                console.error('Error:', error);
                if (typeof showToast === 'function') {
                    showToast('사주 계산 중 오류가 발생했습니다. 다시 시도해주세요.', 'error');
                } else {
                    alert('사주 계산 중 오류가 발생했습니다. 다시 시도해주세요.');
                }
            } finally {
                this.loading = false;
                // Re-enable submit button
                var submitBtn = document.querySelector('.submit-button');
                if (submitBtn) submitBtn.disabled = false;
            }
        },
        
        // 결과 데이터 매핑
        mapResultData(result) {
            // 사주 데이터 매핑
            this.saju = result.saju || this.saju;
            
            // 오행 데이터 매핑
            if (result.elements) {
                this.elements = Object.entries(result.elements).map(([key, value]) => ({
                    name: this.getElementName(key),
                    value: Math.round(value),
                    color: this.getElementColor(key)
                }));
            }
            
            // 해석 데이터 매핑
            this.interpretation = result.interpretation || {};
            
            // 십성 데이터 매핑
            if (result.interpretation?.ten_gods) {
                this.tenGods = result.interpretation.ten_gods;
            }
            
            // 대운 데이터 매핑
            if (result.interpretation?.major_fortune) {
                this.majorFortune = result.interpretation.major_fortune;
            }
            
            // 운세 타임라인 매핑
            if (result.interpretation?.fortune_timeline) {
                this.fortuneTimeline = result.interpretation.fortune_timeline;
            }
            
            // 오행 균형 데이터 매핑
            if (result.balance) {
                this.balance = result.balance;
            }

            // 격국 분석 매핑
            this.pattern = result.pattern || null;

            // 신살 분석 매핑
            this.shinshal = result.shinshal || null;

            // 용신 분석 매핑
            this.yongshin = result.yongshin || null;
        },
        
        // 차트 그리기
        drawCharts() {
            // 오행 차트 그리기
            this.drawElementsChart();
            
            // 운세 차트 그리기 (있을 경우)
            if (this.fortuneTimeline?.years) {
                this.drawFortuneChart();
            }
        },
        
        // 오행 차트 그리기
        drawElementsChart() {
            const ctx = document.getElementById('elements-chart');
            if (!ctx) return;
            
            // 기존 차트 제거
            if (window.elementsChart) {
                window.elementsChart.destroy();
            }
            
            // 새 차트 생성
            window.elementsChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: this.elements.map(e => e.name),
                    datasets: [{
                        data: this.elements.map(e => e.value),
                        backgroundColor: this.elements.map(e => e.color),
                        borderWidth: 2,
                        borderColor: 'rgba(12, 11, 16, 0.8)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.label + ': ' + context.parsed + '%';
                                }
                            }
                        }
                    }
                }
            });
        },
        
        // 운세 차트 그리기
        drawFortuneChart() {
            const ctx = document.getElementById('fortune-chart');
            if (!ctx || !this.fortuneTimeline?.years) {
                return;
            }
            
            // 기존 차트 제거
            if (window.fortuneChart) {
                window.fortuneChart.destroy();
            }
            
            // 새 차트 생성
            // 데이터의 최소/최대값 계산하여 Y축 범위 동적 설정
            const scores = this.fortuneTimeline.years.map(y => {
                // overall_score가 0이어도 유효한 값이므로, undefined/null 체크만 수행
                if (y.overall_score !== undefined && y.overall_score !== null) {
                    return y.overall_score;
                } else if (y.fortune_score !== undefined && y.fortune_score !== null) {
                    return y.fortune_score;
                } else {
                    console.warn('Missing score for year:', y.year);
                    return 0; // 기본값을 0으로 설정 (50이 아닌)
                }
            });
            const minScore = Math.min(...scores);
            const maxScore = Math.max(...scores);
            const padding = 10; // 위아래 여백을 좀 더 늘림
            
            // 현재 년도 찾기
            const currentYear = new Date().getFullYear();
            const currentYearIndex = this.fortuneTimeline.years.findIndex(y => y.year === currentYear);
            
            // 최고점과 최저점 인덱스 찾기
            const maxIndex = scores.indexOf(maxScore);
            const minIndex = scores.indexOf(minScore);
            
            // 현재 년도를 표시하는 세로선 플러그인
            const currentYearPlugin = {
                id: 'currentYear',
                afterDraw: function(chart) {
                    if (currentYearIndex >= 0) {
                        const ctx = chart.ctx;
                        const x = chart.scales.x.getPixelForValue(currentYearIndex);
                        const topY = chart.scales.y.top;
                        const bottomY = chart.scales.y.bottom;
                        
                        // 세로선 그리기
                        ctx.save();
                        ctx.beginPath();
                        ctx.moveTo(x, topY);
                        ctx.lineTo(x, bottomY);
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'rgba(212, 175, 55, 0.4)';
                        ctx.setLineDash([5, 5]);
                        ctx.stroke();
                        ctx.restore();

                        // "현재" 텍스트 표시
                        ctx.save();
                        ctx.fillStyle = '#D4AF37';
                        ctx.font = 'bold 12px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.fillText('현재', x, topY - 5);
                        ctx.restore();
                    }
                }
            };
            
            window.fortuneChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: this.fortuneTimeline.years.map(y => y.year),
                    datasets: [{
                        label: '운세 지수',
                        data: scores,
                        borderColor: '#D4AF37',
                        backgroundColor: 'rgba(212, 175, 55, 0.08)',
                        tension: 0.3,
                        fill: true,
                        pointRadius: function(context) {
                            const index = context.dataIndex;
                            // 현재 년도, 최고점, 최저점은 크게 표시
                            if (index === currentYearIndex || index === maxIndex || index === minIndex) {
                                return 8;
                            }
                            return 4;
                        },
                        pointHoverRadius: 10,
                        pointBackgroundColor: function(context) {
                            const index = context.dataIndex;
                            if (index === currentYearIndex) return '#F0D78C'; // 현재 년도 - 밝은 골드
                            if (index === maxIndex) return '#4ade80'; // 최고점 - 그린
                            if (index === minIndex) return '#fb923c'; // 최저점 - 오렌지
                            return '#D4AF37';
                        },
                        pointBorderColor: 'rgba(12, 11, 16, 0.8)',
                        pointBorderWidth: 2,
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            min: Math.floor(minScore - padding),
                            max: Math.ceil(maxScore + padding),
                            ticks: {
                                color: 'rgba(232, 224, 212, 0.6)',
                                stepSize: Math.ceil((maxScore - minScore + 2*padding) / 10),
                                callback: function(value) {
                                    return value + '점';
                                }
                            },
                            grid: {
                                color: 'rgba(212, 175, 55, 0.06)'
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: 'rgba(232, 224, 212, 0.6)',
                                maxRotation: 45,
                                minRotation: 45
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                            labels: {
                                color: 'rgba(232, 224, 212, 0.8)',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleFont: {
                                size: 14
                            },
                            bodyFont: {
                                size: 13
                            },
                            padding: 12,
                            displayColors: false,
                            callbacks: {
                                title: function(context) {
                                    const yearData = this.fortuneTimeline?.years?.[context[0].dataIndex];
                                    const year = yearData?.year;
                                    const currentYear = new Date().getFullYear();
                                    let title = `${year}년 (${yearData?.age}세)`;
                                    
                                    if (year === currentYear) {
                                        title += ' 📍 현재';
                                    }
                                    
                                    return title;
                                }.bind(this),
                                label: function(context) {
                                    const yearData = this.fortuneTimeline?.years?.[context.dataIndex];
                                    const score = context.parsed.y;
                                    const allScores = context.chart.data.datasets[0].data;
                                    const maxScore = Math.max(...allScores);
                                    const minScore = Math.min(...allScores);
                                    
                                    let label = [`운세 점수: ${score}점`];
                                    
                                    if (score === maxScore) {
                                        label[0] += ' 🌟 최고';
                                    } else if (score === minScore) {
                                        label[0] += ' ⚠️ 주의';
                                    }
                                    
                                    if (yearData) {
                                        label.push(`천간지지: ${yearData.stem_branch || ''}`);
                                        label.push(`${yearData.interpretation || ''}`);
                                    }
                                    
                                    return label;
                                }.bind(this)
                            }
                        },
                        // 데이터 포인트에 값 표시
                        datalabels: {
                            display: false // 너무 복잡해지지 않도록 비활성화
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    animation: {
                        duration: 1500,
                        easing: 'easeInOutQuart'
                    },
                    plugins: [currentYearPlugin]
                }
            });
        },
        
        // 오행 이름 변환
        getElementName(element) {
            const names = {
                'wood': '목(木)',
                'fire': '화(火)',
                'earth': '토(土)',
                'metal': '금(金)',
                'water': '수(水)'
            };
            return names[element] || element;
        },
        
        // 오행 색상
        getElementColor(element) {
            const colors = {
                'wood': '#7B9E89',
                'fire': '#D4736A',
                'earth': '#C8A882',
                'metal': '#A8A5A0',
                'water': '#6B8CAE'
            };
            return colors[element] || '#888';
        },
        
        // 추가 기능 토글
        toggleExtendedFeatures() {
            this.showExtendedFeatures = !this.showExtendedFeatures;
            
            if (this.showExtendedFeatures) {
                setTimeout(() => {
                    document.getElementById('extended-features')?.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }, 100);
            }
        },
        
        // 초기화
        init() {
            // Alpine.js에서 자동으로 init() 호출
            return this;
        }
    };
};