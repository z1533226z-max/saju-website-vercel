/**
 * 디버그 체크 스크립트
 * 변경사항이 반영되었는지 확인
 */

console.log('%c=== 디버그 체크 시작 ===', 'color: #4ade80; font-size: 18px; font-weight: bold;');
console.log('스크립트 로드 시간:', new Date().toLocaleString('ko-KR'));

// 1. CSS 파일 로드 확인
const styleSheets = Array.from(document.styleSheets);
console.group('📋 로드된 CSS 파일들:');
styleSheets.forEach(sheet => {
    if (sheet.href) {
        const fileName = sheet.href.split('/').pop();
        console.log(`✅ ${fileName}`);
        
        // 새로 추가된 파일 확인
        if (fileName === 'fullscreen-fix.css') {
            console.log('%c   -> 새 파일! fullscreen-fix.css가 로드되었습니다!', 'color: #4ade80;');
        }
    }
});
console.groupEnd();

// 2. Alpine.js 데이터 확인
setTimeout(() => {
    const alpineData = document.querySelector('[x-data]');
    if (alpineData && alpineData._x_dataStack) {
        console.group('🔍 Alpine.js 데이터 확인:');
        const data = alpineData._x_dataStack[0];
        
        // 한글 변환 함수 존재 확인
        if (data.getKoreanStem) {
            console.log('%c✅ getKoreanStem 함수가 존재합니다!', 'color: #4ade80;');
            console.log('테스트:', data.getKoreanStem('갑'), '(갑 -> 양목)');
        } else {
            console.log('%c❌ getKoreanStem 함수가 없습니다!', 'color: #ff4444;');
        }
        
        if (data.getKoreanBranch) {
            console.log('%c✅ getKoreanBranch 함수가 존재합니다!', 'color: #4ade80;');
            console.log('테스트:', data.getKoreanBranch('자'), '(자 -> 쥐)');
        } else {
            console.log('%c❌ getKoreanBranch 함수가 없습니다!', 'color: #ff4444;');
        }
        console.groupEnd();
    }
}, 1000);

// 3. DOM 요소 확인
setTimeout(() => {
    console.group('🏗️ DOM 요소 확인:');
    
    // 한글 해석 요소 확인
    const koreanElements = document.querySelectorAll('.stem-korean, .branch-korean');
    if (koreanElements.length > 0) {
        console.log(`%c✅ 한글 해석 요소 ${koreanElements.length}개 발견!`, 'color: #4ade80;');
        koreanElements.forEach((el, idx) => {
            if (el.textContent) {
                console.log(`   ${idx + 1}. ${el.className}: "${el.textContent}"`);
            }
        });
    } else {
        console.log('%c❌ 한글 해석 요소가 없습니다!', 'color: #ff4444;');
    }
    
    // 해석 카드 그리드 확인
    const interpretationGrid = document.querySelector('.interpretation');
    if (interpretationGrid) {
        const computedStyle = window.getComputedStyle(interpretationGrid);
        console.log('📐 해석 카드 그리드 스타일:');
        console.log('   grid-template-columns:', computedStyle.gridTemplateColumns);
        console.log('   max-width:', computedStyle.maxWidth);
        console.log('   gap:', computedStyle.gap);
    }
    
    console.groupEnd();
}, 1500);

// 4. 캐시 상태 확인
console.group('💾 캐시 정보:');
console.log('페이지 로드 타입:', performance.navigation.type === 1 ? '새로고침' : '첫 로드');
console.log('캐시 사용 여부:', performance.getEntriesByType('navigation')[0]?.transferSize === 0 ? '캐시 사용됨' : '네트워크에서 로드');
console.groupEnd();

// 5. 변경사항 요약
console.group('%c📌 변경사항 체크리스트:', 'color: #fbbf24; font-size: 14px;');
console.log('1. fullscreen-fix.css 파일이 로드되어야 함');
console.log('2. getKoreanStem, getKoreanBranch 함수가 존재해야 함');
console.log('3. .stem-korean, .branch-korean 요소가 DOM에 있어야 함');
console.log('4. 전체화면에서 해석 카드가 적절한 그리드로 표시되어야 함');
console.groupEnd();

console.log('%c=== 디버그 체크 완료 ===', 'color: #4ade80; font-size: 18px; font-weight: bold;');
console.log('%c문제가 지속되면 Ctrl+F5로 강제 새로고침하세요!', 'color: #fbbf24; font-size: 14px;');