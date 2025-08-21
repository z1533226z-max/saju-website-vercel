// 파일 확인용 스크립트
console.log('Index.html backup test');
const scripts = document.querySelectorAll('script');
scripts.forEach((script, index) => {
    if (script.src) {
        console.log(`External script ${index}: ${script.src}`);
    } else {
        console.log(`Inline script ${index}: ${script.textContent.substring(0, 50)}...`);
    }
});

// sajuForm이 정의되어 있는지 확인
if (typeof sajuForm !== 'undefined') {
    console.log('sajuForm is defined');
    console.log('sajuForm type:', typeof sajuForm);
}

// Alpine.js 컴포넌트 확인
if (typeof Alpine !== 'undefined') {
    console.log('Alpine.js loaded');
}
