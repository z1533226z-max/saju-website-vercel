// 궁합 및 추가 기능 JavaScript
(function() {
    console.log('🎯 Additional Features Module Loaded');
    
    // 탭 전환 기능
    function initTabs() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.dataset.tab;
                
                // 모든 탭 비활성화
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // 선택된 탭 활성화
                button.classList.add('active');
                document.getElementById(`tab-${targetTab}`).classList.add('active');
            });
        });
    }
    
    // 시간 선택 변경 이벤트 처리
    function initTimeSelectHandler() {
        const partnerTimeSelect = document.getElementById('partner-time');
        const timeUnknownInfo = document.getElementById('time-unknown-info');
        
        if (partnerTimeSelect && timeUnknownInfo) {
            partnerTimeSelect.addEventListener('change', function() {
                if (this.value === 'unknown') {
                    timeUnknownInfo.classList.add('show');
                } else {
                    timeUnknownInfo.classList.remove('show');
                }
            });
        }
    }
    
    // 궁합 계산 기능
    window.calculateCompatibility = async function(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation(); // 이벤트 버블링 방지
        }
        
        console.log('🔍 calculateCompatibility 호출됨');
        
        // 본인 정보 확인
        if (!window.lastSajuCalculation) {
            alert('먼저 본인의 사주를 계산해주세요.');
            document.getElementById('additional-features').style.display = 'none';
            document.getElementById('input-section').scrollIntoView({ behavior: 'smooth' });
            return;
        }
        
        const partnerDate = document.getElementById('partner-date').value;
        const partnerTime = document.getElementById('partner-time').value;
        const partnerGender = document.getElementById('partner-gender').value;
        const partnerCalendar = document.getElementById('partner-calendar').value;
        
        if (!partnerDate || !partnerTime || !partnerGender) {
            alert('상대방의 모든 정보를 입력해주세요.');
            return;
        }
        
        // 시간 모름 처리 - 오시(정오)를 기본값으로 사용
        const actualPartnerTime = partnerTime === 'unknown' ? '12:30' : partnerTime;
        
        console.log('📊 폼 데이터:', {
            partnerDate,
            partnerTime,
            actualPartnerTime,
            partnerGender,
            partnerCalendar
        });
        
        // 본인 정보 가져오기
        const person1Data = {
            birthDate: window.lastSajuCalculation.birthDate,
            birthTime: window.lastSajuCalculation.birthTime,
            gender: window.lastSajuCalculation.gender,
            isLunar: window.lastSajuCalculation.isLunar || false
        };
        
        const requestData = {
            person1: person1Data,
            person2: {
                birthDate: partnerDate,
                birthTime: actualPartnerTime,
                gender: partnerGender,
                isLunar: partnerCalendar === 'lunar',
                isTimeUnknown: partnerTime === 'unknown'  // 시간 모름 플래그
            }
        };
        
        console.log('📤 궁합 계산 요청 데이터:', JSON.stringify(requestData, null, 2));
        
        try {
            console.log('🌐 API 호출 시작: /api/saju/compatibility');
            
            const response = await fetch('/api/saju/compatibility', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            console.log('📥 API 응답 상태:', response.status, response.ok, response.statusText);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API 에러 응답:', errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('📊 API 응답 데이터:', JSON.stringify(data, null, 2));
            
            // 백엔드 응답 형식 확인
            if (data.status === 'success' && data.compatibility) {
                console.log('정상 궁합 결과 표시');
                displayCompatibilityResult(data.compatibility);
            } else if (data.compatibility) {
                // status 필드가 없어도 compatibility가 있으면 사용
                console.log('compatibility 데이터만 있는 경우');
                displayCompatibilityResult(data.compatibility);
            } else if (data.overall_score) {
                // 직접 궁합 데이터가 반환된 경우
                console.log('직접 궁합 데이터 반환');
                displayCompatibilityResult(data);
            } else {
                console.error('예상치 못한 응답 형식:', data);
                // 예상치 못한 형식이어도 데이터가 있으면 시도
                if (data) {
                    displayCompatibilityResult(data);
                }
            }
        } catch (error) {
            console.error('API 호출 오류:', error);
            // API 실패 시 에러 메시지 표시하고 기본 기능은 유지
            console.warn('백엔드 연결 실패 - 기본 궁합 표시');
            
            // 기본 궁합 데이터 생성 (랜덤 아닌 고정된 계산식 사용)
            const person1Date = new Date(window.lastSajuCalculation.birthDate);
            const person2Date = new Date(document.getElementById('partner-date').value);
            
            // 날짜 기반 점수 계산 (일관된 결과)
            const yearDiff = Math.abs(person1Date.getFullYear() - person2Date.getFullYear());
            const monthDiff = Math.abs(person1Date.getMonth() - person2Date.getMonth());
            const dayDiff = Math.abs(person1Date.getDate() - person2Date.getDate());
            
            // 고정된 계산식으로 점수 생성
            let baseScore = 75;
            if (yearDiff <= 3) baseScore += 10;
            else if (yearDiff <= 7) baseScore += 5;
            else if (yearDiff > 12) baseScore -= 10;
            
            if (monthDiff <= 2) baseScore += 5;
            else if (monthDiff >= 6) baseScore += 3;
            
            // 띠 궁합 (12년 주기)
            const zodiacDiff = yearDiff % 12;
            if (zodiacDiff === 0) baseScore += 8;
            else if (zodiacDiff === 4 || zodiacDiff === 8) baseScore += 10;
            else if (zodiacDiff === 6) baseScore -= 8;
            
            const finalScore = Math.max(50, Math.min(95, baseScore));
            
            // 기본 설명 생성
            let advice = '';
            if (finalScore >= 85) {
                advice = '💕 매우 좋은 궁합! 자연스럽게 서로에게 끌리고 편안함을 느끼는 관계입니다. 서로의 장점을 인정하고 단점을 보완해주는 이상적인 파트너입니다.';
            } else if (finalScore >= 70) {
                advice = '💖 좋은 궁합! 서로를 존중하고 배려한다면 행복한 관계를 유지할 수 있습니다. 함께 성장할 수 있는 긍정적인 관계입니다.';
            } else if (finalScore >= 60) {
                advice = '💗 보통 궁합. 서로의 차이를 인정하고 노력한다면 좋은 관계로 발전할 수 있습니다. 대화와 이해가 중요한 관계입니다.';
            } else {
                advice = '💔 도전적인 관계. 많은 이해와 인내가 필요하지만, 그만큼 성장할 수 있는 관계입니다. 서로의 다름을 인정하고 존중하는 것이 중요합니다.';
            }
            
            // 세부 점수 계산
            const stemScore = Math.max(40, Math.min(100, finalScore + (yearDiff % 10) - 5));
            const elementScore = Math.max(40, Math.min(100, finalScore - (monthDiff * 2)));
            const branchScore = Math.max(40, Math.min(100, finalScore + (dayDiff % 5)));
            
            // 기본 궁합 데이터 구조
            const fallbackData = {
                overall_score: finalScore,
                element_compatibility: elementScore,
                heavenly_stem_compatibility: stemScore,
                earthly_branch_compatibility: branchScore,
                compatibility_level: finalScore >= 85 ? '매우 좋음' : finalScore >= 70 ? '좋음' : finalScore >= 60 ? '보통' : '노력 필요',
                advice: advice,
                details: {
                    day_master1: window.lastSajuCalculation.result?.day?.heavenly || '-',
                    day_master2: '-',
                    dominant_element1: '-',
                    dominant_element2: '-'
                }
            };
            
            displayCompatibilityResult(fallbackData);
        }
    };
    
    // 궁합 결과 표시
    function displayCompatibilityResult(compatibility) {
        console.log('🎨 displayCompatibilityResult 호출됨:', compatibility);
        
        const resultDiv = document.getElementById('compatibility-result');
        const scoreValue = document.querySelector('.score-value');
        let message = document.getElementById('compatibility-message');
        
        if (!resultDiv) {
            console.error('❌ compatibility-result 요소를 찾을 수 없음');
            return;
        }
        
        if (!scoreValue) {
            console.error('❌ score-value 요소를 찾을 수 없음');
            return;
        }
        
        // 입력 정보 표시
        const person1Info = document.getElementById('person1-info');
        const person2Info = document.getElementById('person2-info');
        
        if (person1Info && window.lastSajuCalculation) {
            const gender1 = window.lastSajuCalculation.gender === 'male' ? '남성' : '여성';
            const calendar1 = window.lastSajuCalculation.isLunar ? '음력' : '양력';
            person1Info.innerHTML = `${gender1} / ${calendar1}<br>${window.lastSajuCalculation.birthDate}`;
        }
        
        if (person2Info) {
            const partnerGender = document.getElementById('partner-gender').value;
            const gender2 = partnerGender === 'male' ? '남성' : '여성';
            const partnerCalendar = document.getElementById('partner-calendar').value;
            const calendar2 = partnerCalendar === 'lunar' ? '음력' : '양력';
            const partnerDate = document.getElementById('partner-date').value;
            person2Info.innerHTML = `${gender2} / ${calendar2}<br>${partnerDate}`;
        }
        
        // 점수 표시 (백엔드 필드명에 맞게 수정)
        scoreValue.textContent = Math.round(compatibility.overall_score || 75);
        
        // 메시지 요소가 없으면 생성
        if (!message) {
            console.log('💬 compatibility-message 요소가 없어서 생성');
            const parentDiv = document.querySelector('.compatibility-advice');
            if (parentDiv) {
                message = document.createElement('div');
                message.id = 'compatibility-message';
                parentDiv.appendChild(message);
            } else {
                console.error('❌ compatibility-advice 요소를 찾을 수 없음');
                return;
            }
        }
        
        // 메시지 표시 - 디버깅 로그 추가
        console.log('📝 받은 advice:', compatibility.advice);
        
        // 기존 내용 완전 삭제 - DOM 조작 최적화
        message.innerHTML = '';
        
        // 스타일 리셋
        message.style.cssText = 'padding: 0; margin: 0; background: transparent;';
        
        if (compatibility.advice && compatibility.advice.length > 0) {
            // advice 문자열을 문장 단위로 분리
            const adviceText = String(compatibility.advice);
            const adviceItems = adviceText.split(/(?<=[.!?])\s+/).filter(item => item.trim());
            
            console.log('분리된 advice 항목:', adviceItems);
            
            // 이모지와 테마 매핑
            const emojiThemes = {
                '💝': 'theme-perfect',
                '💕': 'theme-excellent',
                '💖': 'theme-great',
                '💗': 'theme-good',
                '💔': 'theme-challenge',
                '🌟': 'theme-star',
                '✨': 'theme-sparkle',
                '⚡': 'theme-energy',
                '🧠': 'theme-mental',
                '💭': 'theme-thought',
                '🤔': 'theme-thinking',
                '💰': 'theme-wealth',
                '🏠': 'theme-home',
                '🌙': 'theme-moon',
                '☀️': 'theme-sun',
                '🌈': 'theme-rainbow',
                '👩‍❤️‍👨': 'theme-couple',
                '👨‍❤️‍👩': 'theme-couple',
                '👨‍❤️‍👨': 'theme-couple',
                '👩‍❤️‍👩': 'theme-couple',
                '🌗': 'theme-halfmoon',
                '🌓': 'theme-halfmoon',
                '💡': 'theme-tip'
            };
            
            // 컨테이너 생성
            const detailedContainer = document.createElement('div');
            detailedContainer.className = 'compatibility-advice-detailed';
            
            // 각 항목을 개별 요소로 생성
            adviceItems.forEach((item, index) => {
                const trimmedItem = item.trim();
                if (trimmedItem) {
                    // 테마 결정
                    let themeClass = 'theme-default';
                    for (const [emoji, theme] of Object.entries(emojiThemes)) {
                        if (trimmedItem.includes(emoji)) {
                            themeClass = theme;
                            break;
                        }
                    }
                    
                    // p 요소 생성
                    const p = document.createElement('p');
                    p.className = `advice-item ${themeClass}`;
                    p.style.cssText = `animation-delay: ${0.1 * (index + 1)}s; opacity: 0; animation: fadeInUp 0.5s ease forwards;`;
                    p.textContent = trimmedItem;
                    
                    detailedContainer.appendChild(p);
                }
            });
            
            // 컨테이너를 메시지에 추가
            message.appendChild(detailedContainer);
            
            // 애니메이션 재시작을 위한 강제 리플로우
            void message.offsetHeight;
            
        } else {
            // 기본 메시지
            const defaultContainer = document.createElement('div');
            defaultContainer.className = 'compatibility-advice-detailed';
            
            const p = document.createElement('p');
            p.className = 'advice-item theme-default';
            p.style.cssText = 'animation-delay: 0.1s; opacity: 0; animation: fadeInUp 0.5s ease forwards;';
            p.textContent = '서로를 이해하고 보완하는 좋은 관계입니다.';
            
            defaultContainer.appendChild(p);
            message.appendChild(defaultContainer);
        }
        
        // 세부 점수 표시 (실제 백엔드 응답에 맞게)
        const stemScore = Math.round(compatibility.heavenly_stem_compatibility || 70);
        const elementScore = Math.round(compatibility.element_compatibility || 70);
        const branchScore = Math.round(compatibility.earthly_branch_compatibility || 70);
        
        updateProgressBar('love', stemScore);
        updateProgressBar('wealth', elementScore);
        updateProgressBar('family', branchScore);
        
        // 점수 텍스트도 업데이트
        document.getElementById('love-score').textContent = stemScore + '점';
        document.getElementById('wealth-score').textContent = elementScore + '점';
        document.getElementById('family-score').textContent = branchScore + '점';
        
        // 궁합 레벨 표시
        const levelElement = document.querySelector('.compatibility-level');
        if (levelElement) {
            levelElement.textContent = compatibility.compatibility_level || '좋음';
        }
        
        // 상세 정보 표시
        if (compatibility.details) {
            const detailsElement = document.querySelector('.compatibility-details');
            if (detailsElement) {
                detailsElement.innerHTML = `
                    <p><strong>본인 일간:</strong> ${compatibility.details.day_master1 || '-'}</p>
                    <p><strong>상대 일간:</strong> ${compatibility.details.day_master2 || '-'}</p>
                    <p><strong>본인 주요 오행:</strong> ${compatibility.details.dominant_element1 || '-'}</p>
                    <p><strong>상대 주요 오행:</strong> ${compatibility.details.dominant_element2 || '-'}</p>
                `;
            }
        }
        
        // 결과 섹션 표시
        resultDiv.style.display = 'block';
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
    


    
    // 프로그레스 바 업데이트
    function updateProgressBar(type, value) {
        const progressMap = {
            'love': 'love-progress',
            'wealth': 'wealth-progress',
            'family': 'family-progress'
        };
        
        const progressBar = document.getElementById(progressMap[type]);
        if (progressBar) {
            const progress = progressBar.querySelector('.progress');
            if (progress) {
                progress.style.width = `${value}%`;
                // 점수에 따른 색상 변경
                if (value >= 80) {
                    progress.style.backgroundColor = '#ff6b9d';
                } else if (value >= 60) {
                    progress.style.backgroundColor = '#feca57';
                } else {
                    progress.style.backgroundColor = '#48dbfb';
                }
            }
        }
    }
    
    // 택일 계산
    window.calculateTaekil = function() {
        const type = document.getElementById('taekil-type').value;
        const month = document.getElementById('taekil-month').value;
        
        if (!month) {
            alert('희망 기간을 선택해주세요.');
            return;
        }
        
        // 임시 결과 생성
        const resultDiv = document.getElementById('taekil-result');
        const datesDiv = document.querySelector('.taekil-dates');
        
        const goodDates = generateGoodDates(month, type);
        
        datesDiv.innerHTML = goodDates.map(date => `
            <div class="date-card">
                <div class="date-header">${date.date}</div>
                <div class="date-info">
                    <p><strong>길일 등급:</strong> ${date.grade}</p>
                    <p><strong>추천 이유:</strong> ${date.reason}</p>
                    <p><strong>주의사항:</strong> ${date.caution}</p>
                </div>
            </div>
        `).join('');
        
        resultDiv.style.display = 'block';
    };
    
    // 좋은 날짜 생성 (임시)
    function generateGoodDates(month, type) {
        const dates = [];
        const reasons = {
            wedding: ['천생연분의 기운', '부부화합의 날', '가정번영의 기운'],
            moving: ['새로운 시작의 기운', '번영과 발전의 날', '안정과 평화의 기운'],
            business: ['재물번창의 기운', '사업번창의 날', '고객만족의 기운'],
            contract: ['신뢰구축의 기운', '상호이익의 날', '원만한 협상의 기운']
        };
        
        // 월의 임의 날짜 3개 선택
        for (let i = 0; i < 3; i++) {
            const day = Math.floor(Math.random() * 28) + 1;
            dates.push({
                date: `${month}-${String(day).padStart(2, '0')}`,
                grade: ['대길', '길', '중길'][i],
                reason: reasons[type][i],
                caution: '오후 시간대 추천'
            });
        }
        
        return dates.sort((a, b) => a.date.localeCompare(b.date));
    };
    
    // 작명 기능
    window.generateNames = function() {
        const surname = document.getElementById('surname').value;
        const gender = document.getElementById('naming-gender').value;
        
        if (!surname) {
            alert('성씨를 입력해주세요.');
            return;
        }
        
        const resultDiv = document.getElementById('naming-result');
        const suggestionsDiv = document.querySelector('.name-suggestions');
        
        const names = generateRandomNames(surname, gender);
        
        suggestionsDiv.innerHTML = names.map(name => `
            <div class="name-card">
                <h4>${name.full}</h4>
                <p><strong>한자:</strong> ${name.hanja}</p>
                <p><strong>의미:</strong> ${name.meaning}</p>
                <p><strong>획수:</strong> ${name.strokes}</p>
            </div>
        `).join('');
        
        resultDiv.style.display = 'block';
    };
    
    // 이름 생성 (임시)
    function generateRandomNames(surname, gender) {
        const maleNames = [
            { name: '준서', hanja: '俊瑞', meaning: '뛰어나고 상서로운', strokes: '9-13' },
            { name: '민준', hanja: '敏俊', meaning: '민첩하고 준수한', strokes: '11-9' },
            { name: '서준', hanja: '瑞俊', meaning: '상서롭고 뛰어난', strokes: '13-9' }
        ];
        
        const femaleNames = [
            { name: '서연', hanja: '瑞妍', meaning: '상서롭고 아름다운', strokes: '13-7' },
            { name: '지안', hanja: '智安', meaning: '지혜롭고 평안한', strokes: '12-6' },
            { name: '하은', hanja: '夏恩', meaning: '여름의 은혜', strokes: '10-10' }
        ];
        
        const selectedNames = gender === 'male' ? maleNames : femaleNames;
        
        return selectedNames.map(n => ({
            full: surname + n.name,
            hanja: n.hanja,
            meaning: n.meaning,
            strokes: n.strokes
        }));
    };
    
    // 초기화
    document.addEventListener('DOMContentLoaded', function() {
        initTabs();
        initTimeSelectHandler(); // 시간 선택 핸들러 초기화
        
        // 궁합 폼 이벤트 리스너 - 이벤트 위임 사용
        document.addEventListener('submit', function(e) {
            if (e.target && e.target.id === 'compatibility-form') {
                console.log('📋 궁합 폼 submit 이벤트 감지');
                e.preventDefault();
                e.stopPropagation();
                calculateCompatibility(e);
            }
        });
        
        // 클릭 이벤트 위임으로 버튼 처리
        document.addEventListener('click', function(e) {
            // 궁합 계산 버튼 처리
            if (e.target && (e.target.classList.contains('btn-calculate-compatibility') || 
                            e.target.closest('.btn-calculate-compatibility'))) {
                console.log('🔘 궁합 계산 버튼 클릭');
                e.preventDefault();
                e.stopPropagation();
                
                const form = document.getElementById('compatibility-form');
                if (form) {
                    // 폼 유효성 검사
                    if (form.checkValidity()) {
                        calculateCompatibility(e);
                    } else {
                        form.reportValidity();
                    }
                }
            }
        });
    });
    
    // 전역 노출
    window.additionalFeatures = {
        showFeatures: function() {
            console.log('🚀 showFeatures 호출됨');
            
            const section = document.getElementById('additional-features');
            if (section) {
                section.style.display = 'block';
                section.scrollIntoView({ behavior: 'smooth' });
                
                // 탭 초기화 재실행
                initTabs();
                initTimeSelectHandler();
                
                // 폼 초기화 - 폼 리셋
                const compatibilityForm = document.getElementById('compatibility-form');
                if (compatibilityForm) {
                    // 폼 리셋 (선택적)
                    // compatibilityForm.reset();
                    console.log('📋 궁합 폼 확인됨');
                }
                
                // 본인 정보가 있으면 궁합 폼에 자동 입력
                if (window.lastSajuCalculation) {
                    const info = window.lastSajuCalculation;
                    
                    // 날짜 포맷팅
                    const birthDate = new Date(info.birthDate);
                    const dateStr = `${birthDate.getFullYear()}년 ${birthDate.getMonth() + 1}월 ${birthDate.getDate()}일`;
                    const genderStr = info.gender === 'male' ? '남성' : '여성';
                    
                    // 본인 정보 표시
                    const person1Date = document.getElementById('person1-date');
                    const person1Time = document.getElementById('person1-time');
                    const person1Gender = document.getElementById('person1-gender');
                    
                    if (person1Date) person1Date.textContent = dateStr + (info.isLunar ? ' (음력)' : ' (양력)');
                    if (person1Time) {
                        // 십이지시 이름과 시간 범위 표시
                        const hourDisplay = info.birthHourName || info.birthTime;
                        const timeRange = info.birthTimeRange ? ` (${info.birthTimeRange})` : '';
                        person1Time.textContent = hourDisplay + timeRange;
                    }
                    if (person1Gender) person1Gender.textContent = genderStr;
                    
                    // 본인 정보 카드 스타일 업데이트
                    const personCard = document.querySelector('.person-card');
                    if (personCard) {
                        personCard.classList.add('has-data');
                    }
                } else {
                    // 사주 계산이 안 되어 있으면 안내
                    const person1Date = document.getElementById('person1-date');
                    const person1Time = document.getElementById('person1-time');
                    const person1Gender = document.getElementById('person1-gender');
                    
                    if (person1Date) {
                        person1Date.innerHTML = `<span style="color: #ef4444;">먼저 사주를 계산해주세요</span>`;
                        person1Time.textContent = '-';
                        person1Gender.textContent = '-';
                        
                        // 사주 계산하러 가기 버튼 추가
                        const infoDisplay = document.querySelector('.info-display');
                        if (infoDisplay && !infoDisplay.querySelector('.go-to-calc')) {
                            const button = document.createElement('button');
                            button.className = 'btn-primary go-to-calc';
                            button.textContent = '사주 계산하러 가기';
                            button.style.marginTop = '1rem';
                            button.onclick = function() {
                                document.getElementById('additional-features').style.display = 'none';
                                document.getElementById('input-section').scrollIntoView({ behavior: 'smooth' });
                            };
                            infoDisplay.appendChild(button);
                        }
                    }
                }
            }
        },
        hideFeatures: function() {
            const section = document.getElementById('additional-features');
            if (section) {
                section.style.display = 'none';
            }
        }
    };
    
    console.log('💡 Use window.additionalFeatures.showFeatures() to display additional features');
})();