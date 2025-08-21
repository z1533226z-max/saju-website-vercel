// 궁합 디버깅 테스트
console.log('🔍 궁합 디버깅 스크립트 로드됨');

// 전역 이벤트 리스너로 모든 submit 이벤트 감지
document.addEventListener('submit', function(e) {
    console.log('📋 Submit 이벤트 감지:', e.target, e.target.id);
}, true); // capture phase에서 감지

// 전역 이벤트 리스너로 모든 클릭 이벤트 감지
document.addEventListener('click', function(e) {
    if (e.target.type === 'submit' || e.target.tagName === 'BUTTON') {
        console.log('🔘 버튼 클릭 감지:', e.target, e.target.className, e.target.textContent);
    }
}, true);

// compatibility-form 직접 확인
setTimeout(() => {
    const form = document.getElementById('compatibility-form');
    if (form) {
        console.log('✅ compatibility-form 발견:', form);
        
        // 기존 이벤트 리스너 제거하고 새로 등록
        const newForm = form.cloneNode(true);
        form.parentNode.replaceChild(newForm, form);
        
        newForm.addEventListener('submit', function(e) {
            console.log('🎯 폼 Submit 이벤트 직접 처리');
            e.preventDefault();
            e.stopPropagation();
            
            if (typeof calculateCompatibility === 'function') {
                console.log('📞 calculateCompatibility 함수 호출');
                calculateCompatibility(e);
            } else {
                console.error('❌ calculateCompatibility 함수를 찾을 수 없음');
            }
        });
        
        console.log('✅ 새 이벤트 리스너 등록 완료');
    } else {
        console.log('⚠️ compatibility-form을 찾을 수 없음');
    }
}, 1000);

// calculateCompatibility 함수 확인
setTimeout(() => {
    if (typeof calculateCompatibility === 'function') {
        console.log('✅ calculateCompatibility 함수 존재');
    } else if (typeof window.calculateCompatibility === 'function') {
        console.log('✅ window.calculateCompatibility 함수 존재');
    } else {
        console.error('❌ calculateCompatibility 함수를 찾을 수 없음');
    }
}, 2000);
