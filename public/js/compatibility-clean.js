// 궁합 기능 - 깔끔한 버전
(function() {
    'use strict';
    
    console.log('✨ 궁합 모듈 로드됨');
    
    // 궁합 계산 함수
    async function calculateCompatibility(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        console.log('🎯 궁합 계산 시작');
        
        // 1. 본인 정보 확인
        if (!window.lastSajuCalculation) {
            alert('먼저 본인의 사주를 계산해주세요.');
            document.getElementById('input-section').scrollIntoView({ behavior: 'smooth' });
            return;
        }
        
        // 2. 폼 데이터 가져오기
        const partnerDate = document.getElementById('partner-date').value;
        const partnerTime = document.getElementById('partner-time').value;
        const partnerGender = document.getElementById('partner-gender').value;
        const partnerCalendar = document.getElementById('partner-calendar').value;
        
        // 3. 유효성 검사
        if (!partnerDate || !partnerTime || !partnerGender) {
            alert('상대방의 모든 정보를 입력해주세요.');
            return;
        }
        
        // 4. API 요청 데이터 준비
        const requestData = {
            person1: {
                birthDate: window.lastSajuCalculation.birthDate,
                birthTime: window.lastSajuCalculation.birthTime,
                gender: window.lastSajuCalculation.gender,
                isLunar: window.lastSajuCalculation.isLunar || false
            },
            person2: {
                birthDate: partnerDate,
                birthTime: partnerTime === 'unknown' ? '12:30' : partnerTime,
                gender: partnerGender,
                isLunar: partnerCalendar === 'lunar'
            }
        };
        
        console.log('📤 요청 데이터:', requestData);
        
        // 5. API 호출
        try {
            const response = await fetch('http://localhost:5000/api/saju/compatibility', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('✅ API 응답:', data);
            
            // 6. 결과 표시
            if (data.compatibility) {
                displayResult(data.compatibility);
            } else if (data.overall_score) {
                displayResult(data);
            }
            
        } catch (error) {
            console.error('❌ API 오류:', error);
            // 폴백 데이터로 표시
            displayResult(generateFallbackData(partnerDate, partnerGender));
        }
    }
    
    // 결과 표시 함수
    function displayResult(compatibility) {
        console.log('📊 결과 표시:', compatibility);
        
        const resultDiv = document.getElementById('compatibility-result');
        if (!resultDiv) return;
        
        // 점수 표시
        const scoreElement = document.querySelector('.score-value');
        if (scoreElement) {
            scoreElement.textContent = Math.round(compatibility.overall_score || 75);
        }
        
        // 레벨 표시
        const levelElement = document.querySelector('.compatibility-level');
        if (levelElement) {
            levelElement.textContent = compatibility.compatibility_level || '좋음';
        }
        
        // 메시지 표시
        const messageElement = document.getElementById('compatibility-message');
        if (messageElement && compatibility.advice) {
            messageElement.innerHTML = `<p>${compatibility.advice}</p>`;
        }
        
        // 세부 점수
        updateProgressBar('love', compatibility.heavenly_stem_compatibility || 70);
        updateProgressBar('wealth', compatibility.element_compatibility || 70);
        updateProgressBar('family', compatibility.earthly_branch_compatibility || 70);
        
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
                
                // 색상 설정
                if (value >= 80) {
                    progress.style.backgroundColor = '#ff6b9d';
                } else if (value >= 60) {
                    progress.style.backgroundColor = '#feca57';
                } else {
                    progress.style.backgroundColor = '#48dbfb';
                }
            }
        }
        
        // 점수 텍스트 업데이트
        const scoreText = document.getElementById(type + '-score');
        if (scoreText) {
            scoreText.textContent = value + '점';
        }
    }
    
    // 폴백 데이터 생성
    function generateFallbackData(partnerDate, partnerGender) {
        const person1Date = new Date(window.lastSajuCalculation.birthDate);
        const person2Date = new Date(partnerDate);
        
        const yearDiff = Math.abs(person1Date.getFullYear() - person2Date.getFullYear());
        const baseScore = 75 - (yearDiff > 10 ? 10 : 0) + (yearDiff < 3 ? 10 : 0);
        
        return {
            overall_score: Math.max(50, Math.min(95, baseScore)),
            heavenly_stem_compatibility: Math.max(40, Math.min(100, baseScore + 5)),
            element_compatibility: Math.max(40, Math.min(100, baseScore - 5)),
            earthly_branch_compatibility: Math.max(40, Math.min(100, baseScore)),
            compatibility_level: baseScore >= 70 ? '좋음' : '보통',
            advice: baseScore >= 70 ? 
                '서로를 이해하고 보완하는 좋은 관계입니다.' : 
                '서로의 차이를 인정하고 노력한다면 좋은 관계로 발전할 수 있습니다.'
        };
    }
    
    // 이벤트 리스너 등록
    function initCompatibility() {
        console.log('🎯 궁합 이벤트 초기화');
        
        // 폼 찾기
        const form = document.getElementById('compatibility-form');
        if (!form) {
            console.log('⚠️ 궁합 폼을 찾을 수 없음');
            return;
        }
        
        // 기존 리스너 제거
        const newForm = form.cloneNode(true);
        form.parentNode.replaceChild(newForm, form);
        
        // 새 리스너 등록
        newForm.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();
            calculateCompatibility(e);
        });
        
        console.log('✅ 궁합 폼 이벤트 등록 완료');
    }
    
    // 탭 기능
    function initTabs() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.dataset.tab;
                
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                button.classList.add('active');
                const targetContent = document.getElementById(`tab-${targetTab}`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }
    
    // 추가 기능 표시
    window.showAdditionalFeatures = function() {
        const section = document.getElementById('additional-features');
        if (!section) return;
        
        section.style.display = 'block';
        section.scrollIntoView({ behavior: 'smooth' });
        
        // 궁합 이벤트 재초기화
        setTimeout(initCompatibility, 100);
        
        // 본인 정보 표시
        if (window.lastSajuCalculation) {
            const info = window.lastSajuCalculation;
            const birthDate = new Date(info.birthDate);
            
            const person1Date = document.getElementById('person1-date');
            const person1Time = document.getElementById('person1-time');
            const person1Gender = document.getElementById('person1-gender');
            
            if (person1Date) {
                person1Date.textContent = `${birthDate.getFullYear()}년 ${birthDate.getMonth() + 1}월 ${birthDate.getDate()}일`;
            }
            if (person1Time) {
                person1Time.textContent = info.birthTime || '-';
            }
            if (person1Gender) {
                person1Gender.textContent = info.gender === 'male' ? '남성' : '여성';
            }
        }
    };
    
    // 택일 계산 (간단 버전)
    window.calculateTaekil = function() {
        const type = document.getElementById('taekil-type').value;
        const month = document.getElementById('taekil-month').value;
        
        if (!month) {
            alert('희망 기간을 선택해주세요.');
            return;
        }
        
        const resultDiv = document.getElementById('taekil-result');
        const datesDiv = document.querySelector('.taekil-dates');
        
        // 간단한 결과 생성
        const dates = [];
        for (let i = 0; i < 3; i++) {
            const day = 5 + (i * 7);
            dates.push({
                date: `${month}-${String(day).padStart(2, '0')}`,
                grade: ['대길', '길', '중길'][i],
                reason: '좋은 기운이 모이는 날'
            });
        }
        
        datesDiv.innerHTML = dates.map(date => `
            <div class="date-card">
                <div class="date-header">${date.date}</div>
                <div class="date-info">
                    <p><strong>길일 등급:</strong> ${date.grade}</p>
                    <p><strong>추천 이유:</strong> ${date.reason}</p>
                </div>
            </div>
        `).join('');
        
        resultDiv.style.display = 'block';
    };
    
    // 작명 기능 (간단 버전)
    window.generateNames = function() {
        const surname = document.getElementById('surname').value;
        const gender = document.getElementById('naming-gender').value;
        
        if (!surname) {
            alert('성씨를 입력해주세요.');
            return;
        }
        
        const resultDiv = document.getElementById('naming-result');
        const suggestionsDiv = document.querySelector('.name-suggestions');
        
        const names = gender === 'male' ? 
            [{ name: '준서', meaning: '뛰어나고 상서로운' },
             { name: '민준', meaning: '민첩하고 준수한' },
             { name: '서준', meaning: '상서롭고 뛰어난' }] :
            [{ name: '서연', meaning: '상서롭고 아름다운' },
             { name: '지안', meaning: '지혜롭고 평안한' },
             { name: '하은', meaning: '여름의 은혜' }];
        
        suggestionsDiv.innerHTML = names.map(n => `
            <div class="name-card">
                <h4>${surname}${n.name}</h4>
                <p><strong>의미:</strong> ${n.meaning}</p>
            </div>
        `).join('');
        
        resultDiv.style.display = 'block';
    };
    
    // DOM 로드 시 초기화
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initTabs();
            initCompatibility();
        });
    } else {
        initTabs();
        initCompatibility();
    }
    
    // 전역 함수 노출
    window.calculateCompatibility = calculateCompatibility;
    
    console.log('✅ 궁합 모듈 초기화 완료');
})();
