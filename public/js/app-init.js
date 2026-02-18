/**
 * App initialization - share functions, modal, compass, event delegation
 */

// Chart.js 글로벌 다크 테마 기본값
if (typeof Chart !== 'undefined') {
    Chart.defaults.color = 'rgba(232, 224, 212, 0.7)';
    Chart.defaults.borderColor = 'rgba(212, 175, 55, 0.08)';
}

// Share functions
function shareKakao() {
    if (window.Kakao && Kakao.isInitialized()) {
        Kakao.Share.sendDefault({
            objectType: 'feed',
            content: {
                title: '사주명리 - 당신의 운명을 읽다',
                description: '생년월일시로 보는 정확한 사주 풀이',
                imageUrl: window.location.origin + '/assets/images/og-image.jpg',
                link: {
                    mobileWebUrl: window.location.href,
                    webUrl: window.location.href,
                },
            },
        });
    } else {
        if (navigator.share) {
            navigator.share({
                title: '사주명리 - 당신의 운명을 읽다',
                text: '생년월일시로 보는 정확한 사주 풀이',
                url: window.location.href
            }).catch(function() {});
        } else {
            copyLink();
        }
    }
}

function copyLink(triggerBtn) {
    navigator.clipboard.writeText(window.location.href).then(function() {
        if (!triggerBtn) {
            if (typeof showToast === 'function') showToast('링크가 복사되었습니다!');
            return;
        }
        var originalHTML = triggerBtn.innerHTML;
        triggerBtn.classList.add('copied');
        triggerBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg><span>복사 완료!</span>';
        setTimeout(function() {
            triggerBtn.classList.remove('copied');
            triggerBtn.innerHTML = originalHTML;
        }, 2000);
    }).catch(function() {
        if (typeof showToast === 'function') showToast('링크 복사에 실패했습니다.', 'error');
    });
}

// Modal content data
var _modalContent = {
    '천간': {
        title: '십천간(十天干) 완벽 이해하기',
        body: '<div class="modal-info"><h3>하늘의 10가지 기운</h3><p>십천간은 동양철학에서 하늘의 기운을 10가지로 분류한 것입니다.</p><div class="info-list"><h4>양(陽)의 천간 - 홀수</h4><ul><li><strong>갑(甲)</strong> - 큰 나무 : 리더십, 개척정신</li><li><strong>병(丙)</strong> - 태양 : 밝고 활발함, 열정</li><li><strong>무(戊)</strong> - 산, 큰 땅 : 안정감, 포용력</li><li><strong>경(庚)</strong> - 쇠, 도끼 : 결단력, 추진력</li><li><strong>임(壬)</strong> - 바다, 큰 물 : 지혜, 유연함</li></ul><h4>음(陰)의 천간 - 짝수</h4><ul><li><strong>을(乙)</strong> - 화초, 덩굴 : 유연함, 적응력</li><li><strong>정(丁)</strong> - 촛불, 등불 : 섬세함, 온화함</li><li><strong>기(己)</strong> - 논밭, 정원 : 실용성, 생산성</li><li><strong>신(辛)</strong> - 보석, 장신구 : 예민함, 완벽주의</li><li><strong>계(癸)</strong> - 이슬, 비 : 상상력, 감수성</li></ul></div><div class="fun-fact"><strong>재미있는 사실!</strong><br>"갑질"이라는 말이 여기서 나왔어요. 갑(甲)이 첫 번째라서 상하관계에서 위에 있는 사람을 뜻하게 된 거죠.</div></div>'
    },
    '지지': {
        title: '십이지지(十二地支) 쉽게 배우기',
        body: '<div class="modal-info"><h3>12가지 동물띠의 비밀</h3><p>십이지지는 땅의 기운을 12가지 동물로 표현한 것입니다.</p><div class="info-list"><h4>시간대별 동물과 성격</h4><ul><li><strong>자(子) 쥐</strong> 23-01시 : 영리하고 재치있음</li><li><strong>축(丑) 소</strong> 01-03시 : 성실하고 인내심 강함</li><li><strong>인(寅) 호랑이</strong> 03-05시 : 용맹하고 정의로움</li><li><strong>묘(卯) 토끼</strong> 05-07시 : 온순하고 예민함</li><li><strong>진(辰) 용</strong> 07-09시 : 카리스마, 리더십</li><li><strong>사(巳) 뱀</strong> 09-11시 : 지혜롭고 신중함</li><li><strong>오(午) 말</strong> 11-13시 : 활발하고 자유로움</li><li><strong>미(未) 양</strong> 13-15시 : 평화롭고 예술적</li><li><strong>신(申) 원숭이</strong> 15-17시 : 재주많고 호기심 많음</li><li><strong>유(酉) 닭</strong> 17-19시 : 부지런하고 정확함</li><li><strong>술(戌) 개</strong> 19-21시 : 충직하고 정직함</li><li><strong>해(亥) 돼지</strong> 21-23시 : 복이 많고 순수함</li></ul></div><div class="fun-fact"><strong>알고 계셨나요?</strong><br>고양이가 12띠에 없는 이유는 쥐가 속여서 늦게 도착했다는 재미있는 설화가 있어요.</div></div>'
    },
    '오행': {
        title: '오행(五行) 한눈에 이해하기',
        body: '<div class="modal-info"><h3>우주를 구성하는 5가지 에너지</h3><p>오행은 세상 만물을 구성하는 5가지 기본 에너지입니다.</p><div class="info-list"><h4>5가지 원소와 특징</h4><ul><li><strong>목(木) 나무</strong> - 색: 청색 | 계절: 봄 | 성격: 성장, 발전</li><li><strong>화(火) 불</strong> - 색: 적색 | 계절: 여름 | 성격: 열정, 확산</li><li><strong>토(土) 흙</strong> - 색: 황색 | 계절: 환절기 | 성격: 중재, 안정</li><li><strong>금(金) 쇠</strong> - 색: 백색 | 계절: 가을 | 성격: 결실, 수렴</li><li><strong>수(水) 물</strong> - 색: 흑색 | 계절: 겨울 | 성격: 지혜, 유연</li></ul><h4>상생(相生) - 서로 돕는 관계</h4><p class="cycle-text">나무는 불을 만들고 &rarr; 불은 재(흙)를 만들고 &rarr; 흙에서 금속이 나오고 &rarr; 금속은 물을 모으고 &rarr; 물은 나무를 자라게 해요</p><h4>상극(相剋) - 서로 견제하는 관계</h4><p class="cycle-text">나무는 흙의 영양분을 빼앗고 &rarr; 흙은 물을 막고 &rarr; 물은 불을 끄고 &rarr; 불은 금속을 녹이고 &rarr; 금속은 나무를 자르죠</p></div><div class="fun-fact"><strong>일상 속 오행!</strong><br>한의학, 풍수, 요리, 색채학 등 우리 생활 곳곳에 오행이 숨어있어요.</div></div>'
    }
};

// Modal functions
var _modalTrigger = null;

function showInfoModal(type) {
    var modal = document.getElementById('info-modal');
    var title = document.getElementById('modal-title');
    var body = document.getElementById('modal-body');

    if (_modalContent[type]) {
        title.innerHTML = _modalContent[type].title;
        body.innerHTML = _modalContent[type].body;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        _modalTrigger = document.activeElement;
        var closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) closeBtn.focus();
    }
}

function closeInfoModal() {
    var modal = document.getElementById('info-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    if (_modalTrigger) {
        _modalTrigger.focus();
        _modalTrigger = null;
    }
}

// ESC key + focus trap
document.addEventListener('keydown', function(e) {
    var modal = document.getElementById('info-modal');
    if (!modal || modal.style.display === 'none') return;

    if (e.key === 'Escape') {
        closeInfoModal();
        return;
    }

    if (e.key === 'Tab') {
        var focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusable.length === 0) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (e.shiftKey) {
            if (document.activeElement === first) {
                e.preventDefault();
                last.focus();
            }
        } else {
            if (document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    }
});

// Event delegation for data-action buttons
document.addEventListener('click', function(e) {
    var target = e.target.closest('[data-action]');
    if (!target) return;

    var action = target.dataset.action;
    switch (action) {
        case 'scrollToInput': scrollToInput(); break;
        case 'openSajuGuide': openSajuGuide(); break;
        case 'shareKakao': shareKakao(); break;
        case 'copyLink': copyLink(target); break;
        case 'showFeatures':
            if (window.additionalFeatures) window.additionalFeatures.showFeatures();
            break;
        case 'calculateTaekil': calculateTaekil(); break;
        case 'generateNames': generateNames(); break;
        case 'showInfoModal':
            e.preventDefault();
            showInfoModal(target.dataset.modalType);
            break;
        case 'closeInfoModal': closeInfoModal(); break;
    }
});

function openSajuGuide() {
    showInfoModal('천간');
}

function closeSajuGuide() {
    closeInfoModal();
}

// Initialize Luopan Compass
document.addEventListener('DOMContentLoaded', function() {
    initializeCompass('.logo-mountains-24', '.logo-trigram-ring', '.logo-branches-12', true);
    initializeCompass('.mountains-24', '.trigram-ring', '.branches-12', false);
});

function initializeCompass(mountainsSelector, trigramSelector, branchesSelector, isLogo) {
    var mountains = [
        '壬', '子', '癸', '丑', '艮', '寅', '甲', '卯',
        '乙', '辰', '巽', '巳', '丙', '午', '丁', '未',
        '坤', '申', '庚', '酉', '辛', '戌', '乾', '亥'
    ];

    var trigrams = [
        { symbol: '☰', name: '乾' }, { symbol: '☱', name: '兌' },
        { symbol: '☲', name: '離' }, { symbol: '☳', name: '震' },
        { symbol: '☴', name: '巽' }, { symbol: '☵', name: '坎' },
        { symbol: '☶', name: '艮' }, { symbol: '☷', name: '坤' }
    ];

    var branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

    var mountainRadius = isLogo ? 18 : 130;
    var trigramRadius = isLogo ? 12 : 75;
    var branchRadius = isLogo ? 7 : 50;

    var mountainsContainer = document.querySelector(mountainsSelector);
    if (mountainsContainer) {
        var mountainsToShow = isLogo ? mountains.filter(function(_, i) { return i % 3 === 0; }) : mountains;
        mountainsToShow.forEach(function(mountain, index) {
            var totalMountains = mountainsToShow.length;
            var angle = (index * (360 / totalMountains)) - 90;
            var x = Math.cos(angle * Math.PI / 180) * mountainRadius;
            var y = Math.sin(angle * Math.PI / 180) * mountainRadius;
            var element = document.createElement('div');
            element.className = isLogo ? 'logo-mountain' : 'mountain';
            element.textContent = mountain;
            element.style.transform = 'translate(-50%, -50%) translate(' + x + 'px, ' + y + 'px)';
            mountainsContainer.appendChild(element);
        });
    }

    var trigramRing = document.querySelector(trigramSelector);
    if (trigramRing) {
        trigrams.forEach(function(trigram, index) {
            var angle = (index * 45) - 90;
            var x = Math.cos(angle * Math.PI / 180) * trigramRadius;
            var y = Math.sin(angle * Math.PI / 180) * trigramRadius;
            var element = document.createElement('div');
            element.className = isLogo ? 'logo-trigram' : 'trigram';
            element.textContent = trigram.symbol;
            element.style.transform = 'translate(-50%, -50%) translate(' + x + 'px, ' + y + 'px)';
            trigramRing.appendChild(element);
        });
    }

    if (!isLogo) {
        var branchesContainer = document.querySelector(branchesSelector);
        if (branchesContainer) {
            branches.forEach(function(branch, index) {
                var angle = (index * 30) - 90;
                var x = Math.cos(angle * Math.PI / 180) * branchRadius;
                var y = Math.sin(angle * Math.PI / 180) * branchRadius;
                var element = document.createElement('div');
                element.className = 'branch';
                element.textContent = branch;
                element.style.transform = 'translate(-50%, -50%) translate(' + x + 'px, ' + y + 'px)';
                branchesContainer.appendChild(element);
            });
        }
    }
}
