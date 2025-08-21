// 레이아웃 디버그 스크립트
// 화면 크기에 따른 그리드 상태 확인

(function() {
    console.log('🔧 Layout Debug Script Loaded');
    
    // 현재 화면 크기 정보
    function checkViewport() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        let breakpoint = 'mobile';
        
        if (width >= 1920) breakpoint = 'ultra-wide';
        else if (width >= 1440) breakpoint = 'wide';
        else if (width >= 1024) breakpoint = 'desktop';
        else if (width >= 768) breakpoint = 'tablet';
        
        console.log(`📱 Viewport: ${width}x${height} (${breakpoint})`);
        return { width, height, breakpoint };
    }
    
    // 해석 카드 그리드 상태 확인
    function checkInterpretationGrid() {
        const container = document.querySelector('#results-section .interpretation');
        if (!container) {
            console.log('❌ No interpretation container found');
            return;
        }
        
        const computedStyle = window.getComputedStyle(container);
        const gridColumns = computedStyle.gridTemplateColumns;
        const cards = container.querySelectorAll('.interpretation-card');
        
        console.log('📊 Grid Status:');
        console.log(`  - Grid columns: ${gridColumns}`);
        console.log(`  - Total cards: ${cards.length}`);
        
        // 각 카드의 크기 확인
        cards.forEach((card, index) => {
            const rect = card.getBoundingClientRect();
            const style = window.getComputedStyle(card);
            console.log(`  Card ${index + 1}: ${Math.round(rect.width)}x${Math.round(rect.height)}px`);
            
            // 5번째 카드부터 전체 너비 사용하는지 확인
            if (index >= 4) {
                const gridColumn = style.gridColumn;
                if (gridColumn && gridColumn !== 'auto') {
                    console.log(`    → Grid column: ${gridColumn}`);
                }
            }
        });
    }
    
    // CSS 파일 로드 상태 확인
    function checkCSSFiles() {
        const stylesheets = Array.from(document.styleSheets);
        const layoutFixCSS = stylesheets.find(sheet => 
            sheet.href && sheet.href.includes('layout-fix.css')
        );
        
        if (layoutFixCSS) {
            console.log('✅ layout-fix.css loaded successfully');
            try {
                const rules = Array.from(layoutFixCSS.cssRules || layoutFixCSS.rules);
                console.log(`  - Total rules: ${rules.length}`);
            } catch(e) {
                console.log('  - Cannot access rules (CORS)');
            }
        } else {
            console.log('❌ layout-fix.css not found');
        }
    }
    
    // 디버그 정보 출력
    function runDebug() {
        console.log('\n========== Layout Debug Info ==========');
        checkViewport();
        checkCSSFiles();
        checkInterpretationGrid();
        console.log('======================================\n');
    }
    
    // 페이지 로드 시 실행
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', runDebug);
    } else {
        setTimeout(runDebug, 100);
    }
    
    // 리사이즈 시 재확인
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            console.log('\n🔄 Window resized');
            runDebug();
        }, 500);
    });
    
    // 전역 디버그 함수 노출
    window.layoutDebug = {
        check: runDebug,
        viewport: checkViewport,
        grid: checkInterpretationGrid,
        css: checkCSSFiles,
        // 강제로 레이아웃 수정 적용
        forceLayout: function() {
            const container = document.querySelector('#results-section .interpretation');
            if (container) {
                container.style.cssText += 'display: grid !important;';
                console.log('✅ Force layout applied');
                checkInterpretationGrid();
            }
        }
    };
    
    console.log('💡 Use window.layoutDebug.check() to run debug');
})();