/**
 * 사주 오행 캐릭터 테스트 — 화면·카드·공유·초대 궁합
 *
 * 개인정보: 생년월일은 이 페이지 안에서만 계산하고 서버로 보내지도, 브라우저에 저장하지도 않는다.
 * 링크에 들어가는 것은 유형 코드(일간+일지 두 글자, 60가지)와 사용자가 직접 쓴 별명뿐이다.
 * 의존: saju-test-core.js(SajuTestCore), saju-test-data.js(SAJU_TEST_DATA)
 */
(function () {
    'use strict';

    var Core = window.SajuTestCore;
    var DATA = window.SAJU_TEST_DATA;
    var SITE = 'https://saju.gon.ai.kr';
    var BASE = '/saju-test/';
    var OG_DIR = '/assets/images/saju-test/';
    var KAKAO_SDK = {
        src: 'https://t1.kakaocdn.net/kakao_js_sdk/2.8.3/kakao.min.js',
        integrity: 'sha384-oroumrnFVE0xtgqyDZJARgERibXg2C28380uaUZz2kHDS5CR7tu20eGiOU6GkTpy'
    };
    var NICK_MAX = 8;

    // ── 작은 도우미 ──────────────────────────────────────────────
    function h(tag, attrs, children) {
        var el = document.createElement(tag);
        if (attrs) Object.keys(attrs).forEach(function (k) {
            if (k === 'text') el.textContent = attrs[k];
            else if (k === 'class') el.className = attrs[k];
            else if (k === 'style') el.style.cssText = attrs[k];
            else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), attrs[k]);
            else if (attrs[k] !== false && attrs[k] != null) el.setAttribute(k, attrs[k] === true ? '' : attrs[k]);
        });
        (children || []).forEach(function (c) {
            if (c == null) return;
            el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
        });
        return el;
    }

    function iconSvg(icon, size, label) {
        var NS = 'http://www.w3.org/2000/svg';
        var svg = document.createElementNS(NS, 'svg');
        svg.setAttribute('viewBox', '0 0 100 100');
        svg.setAttribute('width', size);
        svg.setAttribute('height', size);
        svg.setAttribute('class', 'st-icon');
        if (label) { svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', label); }
        else svg.setAttribute('aria-hidden', 'true');
        icon.forEach(function (p) {
            var path = document.createElementNS(NS, 'path');
            path.setAttribute('d', p.d);
            if (p.stroke) {
                path.setAttribute('fill', 'none');
                path.setAttribute('stroke', p.stroke);
                path.setAttribute('stroke-width', p.w);
                path.setAttribute('stroke-linecap', 'round');
            } else path.setAttribute('fill', p.fill);
            svg.appendChild(path);
        });
        return svg;
    }

    // 받침 유무로 조사 고르기 (은/는, 이/가, 와/과, 을/를). '민지(소나무)'처럼 괄호가 붙으면 괄호 앞 낱말 기준
    function josa(word, pair) {
        var base = word.replace(/\([^)]*\)$/, '') || word;
        var c = base.charCodeAt(base.length - 1);
        var has = c >= 0xAC00 && c <= 0xD7A3 && (c - 0xAC00) % 28 !== 0;
        return word + (has ? pair[0] : pair[1]);
    }

    function cleanNick(s) {
        if (!s) return '';
        return String(s).replace(/[\u0000-\u001f<>"'`&]/g, '').trim().slice(0, NICK_MAX);
    }

    function track(name, params) {
        if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
    }

    var toastTimer;
    function toast(msg) {
        var el = document.getElementById('st-toast');
        if (!el) { el = h('div', { id: 'st-toast', class: 'st-toast', role: 'status' }); document.body.appendChild(el); }
        el.textContent = msg;
        el.hidden = false;
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () { el.hidden = true; }, 2200);
    }

    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return legacyCopy(text); });
        }
        return Promise.resolve(legacyCopy(text));
    }

    function legacyCopy(text) {
        var ta = h('textarea', { style: 'position:fixed;top:-1000px;opacity:0' });
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
        document.body.removeChild(ta);
        return ok;
    }

    /** Web Share API → 안 되면 링크 복사 */
    function shareLink(payload, method) {
        if (navigator.share) {
            return navigator.share(payload).then(function () {
                track('saju_test_share', { method: 'web_share', target: method });
            }, function () { /* 사용자가 닫음 */ });
        }
        return copyText(payload.url).then(function (ok) {
            toast(ok ? '링크를 복사했어요. 원하는 곳에 붙여 넣으세요!' : '복사에 실패했어요. 주소창의 링크를 길게 눌러 복사해 주세요.');
            if (ok) track('saju_test_share', { method: 'copy', target: method });
        });
    }

    // ── 링크 ──────────────────────────────────────────────────────
    function typeUrl(t) { return SITE + BASE + t.slug + '/'; }

    function inviteUrl(code, nick) {
        var q = 'from=' + code + (nick ? '&n=' + encodeURIComponent(nick) : '');
        return SITE + BASE + '?' + q;
    }

    function pairUrl(codeA, nickA, codeB, nickB) {
        var q = 'pair=' + codeA + codeB;
        if (nickA) q += '&n=' + encodeURIComponent(nickA);
        if (nickB) q += '&m=' + encodeURIComponent(nickB);
        return SITE + BASE + '?' + q;
    }

    function readQuery() {
        var p = new URLSearchParams(window.location.search);
        var out = { from: Core.parseCode(p.get('from') || ''), n: cleanNick(p.get('n')), m: cleanNick(p.get('m')), pair: null };
        var pair = p.get('pair') || '';
        if (/^[0-9][0-9ab][0-9][0-9ab]$/.test(pair)) {
            var a = Core.parseCode(pair.slice(0, 2)), b = Core.parseCode(pair.slice(2));
            if (a && b) out.pair = [a, b];
        }
        return out;
    }

    // ── 궁합 문장 ────────────────────────────────────────────────
    var FEED_TEXT = ['나무가 불씨를 키우듯', '불이 타고 남은 재가 흙을 기름지게 하듯', '흙 속에서 광물이 단단해지듯',
        '차가운 쇠에 이슬이 맺히듯', '물이 나무를 자라게 하듯'];
    var SHAPE_TEXT = ['나무뿌리가 흙을 붙잡아 주듯', '불이 쇠를 달궈 쓸모 있게 만들듯', '둑이 물길을 잡아 주듯',
        '도끼가 나무를 다듬어 좋은 재목을 만들듯', '물이 불길을 알맞게 다스리듯'];
    var BRANCH_TEXT = {
        yukhap: '태어난 날의 지지(일지)가 육합이에요. 생활 리듬과 속마음이 잘 맞물려서, 같이 있을수록 편해지는 조합입니다.',
        samhap: '태어난 날의 지지(일지)가 삼합이에요. 같은 방향을 보는 팀 같은 사이라 함께 목표를 세우면 힘이 붙습니다.',
        chung: '태어난 날의 지지(일지)가 충(沖)이에요. 생활 리듬이 달라 부딪힐 때가 있지만, 서로 못 보던 면을 보게 해 주는 자극이 됩니다.',
        same: '태어난 날의 지지(일지)가 같아요. 생활 습관이 닮아 편하지만, 고집도 닮을 수 있어요.',
        plain: '태어난 날의 지지(일지)끼리는 큰 충돌도 끌림도 없는 무난한 사이라, 일간의 관계가 궁합을 좌우합니다.'
    };

    function scoreLabel(s) {
        if (s >= 92) return '찰떡 운명 콤비';
        if (s >= 85) return '서로 키워 주는 사이';
        if (s >= 78) return '말 안 해도 통하는 단짝';
        if (s >= 70) return '서로를 단단하게 만드는 자극 메이트';
        return '알아 갈수록 반전 케미';
    }

    /** a, b = {stem, branch, nick} → {score, label, lines[], tip} */
    function compatText(a, b) {
        var r = Core.compatibility(a, b);
        var ta = DATA.types[a.stem], tb = DATA.types[b.stem];
        var na = (a.nick || '나') + '(' + ta.name + ')', nb = (b.nick || '친구') + '(' + tb.name + ')';
        var ea = Core.stemElement(a.stem), eb = Core.stemElement(b.stem);
        var line, tip;
        if (r.stemRel === 'hap') {
            line = josa(na, ['과', '와']) + ' ' + josa(nb, ['은', '는']) + ' 천간합(天干合) — 서로 끌어당겨 하나가 되는 짝이에요. '
                + '성향은 달라도 같이 있으면 이상하게 편하고, 함께할수록 각자의 장점이 커집니다.';
            tip = '너무 편해서 서로에게 소홀해지지 않게, 고마운 건 말로 표현해 주세요.';
        } else if (r.stemRel === 'same') {
            line = '둘 다 ' + DATA.elements[ea].word + '(' + DATA.elements[ea].name + ') 기운 — 말 안 해도 통하는 비화(比和) 관계예요. '
                + '취향과 속도가 비슷해 금방 친해지지만, 같은 곳에서 부딪히면 둘 다 물러서지 않을 수 있어요.';
            tip = '역할을 나눠 맡으면 경쟁 대신 최고의 팀이 됩니다.';
        } else if (r.stemRel === 'a_feeds_b' || r.stemRel === 'b_feeds_a') {
            var giverA = r.stemRel === 'a_feeds_b';
            var giver = giverA ? na : nb, taker = giverA ? nb : na;
            line = josa(giver, ['이', '가']) + ' ' + josa(taker, ['을', '를']) + ' 살려 주는 상생(相生) 관계 — '
                + FEED_TEXT[giverA ? ea : eb] + '. 한쪽은 챙겨 주는 기쁨을, 다른 쪽은 든든함을 느끼는 사이예요.';
            tip = '주는 쪽이 지치지 않게, 받는 쪽도 먼저 고마움을 표현해 주면 오래 갑니다.';
        } else {
            var shaperA = r.stemRel === 'a_shapes_b';
            var shaper = shaperA ? na : nb, shaped = shaperA ? nb : na;
            line = josa(shaper, ['이', '가']) + ' ' + josa(shaped, ['을', '를']) + ' 다듬어 주는 상극(相剋) 관계 — '
                + SHAPE_TEXT[shaperA ? ea : eb] + '. 처음엔 부딪혀도 서로를 단단하게 만드는 자극이 되는 사이예요.';
            tip = '지적보다 응원을 먼저 — 같은 말도 순서만 바꾸면 훨씬 부드럽게 전해집니다.';
        }
        return { score: r.score, label: scoreLabel(r.score), lines: [line, BRANCH_TEXT[r.branchRel]], tip: tip };
    }

    function bestMatch(stem) {
        return DATA.types[(stem + 5) % 10];          // 천간합 짝
    }

    // ── 카드 그리기 (canvas) — OG 이미지 생성 스크립트도 이 함수를 쓴다 ───────────
    var FONT_SANS = '"Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif';
    var FONT_SERIF = '"Noto Serif KR", "Nanum Myeongjo", serif';

    function fontsReady(text) {
        if (!document.fonts || !document.fonts.load) return Promise.resolve();
        var loads = ['900 80px "Noto Serif KR"', '700 40px "Noto Sans KR"', '400 40px "Noto Sans KR"']
            .map(function (f) { return document.fonts.load(f, text).catch(function () {}); });
        var timeout = new Promise(function (res) { setTimeout(res, 2500); });
        return Promise.race([Promise.all(loads), timeout]);
    }

    function drawIcon(ctx, icon, x, y, size) {
        ctx.save();
        ctx.translate(x, y);
        ctx.scale(size / 100, size / 100);
        icon.forEach(function (p) {
            var path = new Path2D(p.d);
            if (p.stroke) {
                ctx.strokeStyle = p.stroke; ctx.lineWidth = p.w; ctx.lineCap = 'round'; ctx.stroke(path);
            } else { ctx.fillStyle = p.fill; ctx.fill(path); }
        });
        ctx.restore();
    }

    function fitText(ctx, text, maxW, weight, size, family) {
        var s = size;
        do { ctx.font = weight + ' ' + s + 'px ' + family; s -= 4; } while (ctx.measureText(text).width > maxW && s > 20);
    }

    function wrapLines(ctx, text, maxW) {
        var words = text.split(' '), lines = [], cur = '';
        words.forEach(function (w) {
            var t = cur ? cur + ' ' + w : w;
            if (ctx.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t;
        });
        if (cur) lines.push(cur);
        return lines;
    }

    function background(ctx, W, H, color) {
        var g = ctx.createLinearGradient(0, 0, 0, H);
        g.addColorStop(0, '#0C0B10');
        g.addColorStop(0.55, '#15131d');
        g.addColorStop(1, '#1d1a26');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, W, H);
        ctx.strokeStyle = 'rgba(212,175,55,0.35)';
        ctx.lineWidth = 4;
        ctx.strokeRect(28, 28, W - 56, H - 56);
        return color;
    }

    function glow(ctx, cx, cy, r, color) {
        var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
        g.addColorStop(0, color + '66');
        g.addColorStop(1, color + '00');
        ctx.fillStyle = g;
        ctx.fillRect(cx - r, cy - r, 2 * r, 2 * r);
    }

    /**
     * kind: 'card'(1080×1920 개인 결과) | 'og'(1200×630 유형 소개) | 'og-main'(1200×630 테스트 대표)
     * r: analyze() 결과(card 일 때), stem: 유형 번호(og 일 때)
     */
    function drawCard(canvas, kind, opts) {
        var ctx = canvas.getContext('2d');
        var gold = '#D4AF37', goldLight = '#F0D78C', text = '#E8E0D4', sub = '#9B918A';
        ctx.textBaseline = 'alphabetic';

        if (kind === 'og-main') {
            canvas.width = 1200; canvas.height = 630;
            background(ctx, 1200, 630);
            ctx.textAlign = 'center';
            ctx.fillStyle = gold; ctx.font = '500 34px ' + FONT_SANS;
            ctx.fillText('사주 오행 캐릭터 테스트', 600, 120);
            ctx.fillStyle = goldLight; fitText(ctx, '나는 어떤 자연일까?', 1040, 900, 96, FONT_SERIF);
            ctx.fillText('나는 어떤 자연일까?', 600, 235);
            ctx.fillStyle = text; ctx.font = '400 38px ' + FONT_SANS;
            ctx.fillText('생년월일만 넣으면 1초 — 10가지 캐릭터 + 친구 궁합', 600, 305);
            DATA.types.forEach(function (t, i) {
                var x = 80 + (i % 5) * 220, y = i < 5 ? 340 : 455;
                drawIcon(ctx, t.icon, x + 50, y, 100);
            });
            ctx.fillStyle = sub; ctx.font = '400 26px ' + FONT_SANS;
            ctx.fillText('saju.gon.ai.kr/saju-test', 600, 585);
            return canvas;
        }

        if (kind === 'og') {
            var t = DATA.types[opts.stem];
            canvas.width = 1200; canvas.height = 630;
            background(ctx, 1200, 630);
            glow(ctx, 270, 315, 260, t.color);
            drawIcon(ctx, t.icon, 90, 135, 360);
            ctx.textAlign = 'left';
            ctx.fillStyle = gold; ctx.font = '500 32px ' + FONT_SANS;
            ctx.fillText('사주 오행 캐릭터 테스트', 520, 150);
            ctx.fillStyle = sub; ctx.font = '400 32px ' + FONT_SANS;
            ctx.fillText(t.label + ' 일간', 520, 215);
            ctx.fillStyle = goldLight; fitText(ctx, t.name, 620, 900, 92, FONT_SERIF);
            ctx.fillText(t.name, 520, 320);
            ctx.fillStyle = text; ctx.font = '400 36px ' + FONT_SANS;
            wrapLines(ctx, t.tagline, 620).slice(0, 2).forEach(function (l, i) { ctx.fillText(l, 520, 390 + i * 50); });
            ctx.fillStyle = gold; ctx.font = '500 30px ' + FONT_SANS;
            ctx.fillText(t.keywords.join('  '), 520, 500);
            ctx.fillStyle = sub; ctx.font = '400 26px ' + FONT_SANS;
            ctx.fillText('너는 어떤 자연이야? saju.gon.ai.kr/saju-test', 520, 570);
            return canvas;
        }

        // 개인 결과 카드 (휴대폰 세로 9:16)
        var r = opts.result, tt = DATA.types[r.stem], W = 1080, H = 1920;
        canvas.width = W; canvas.height = H;
        background(ctx, W, H);
        glow(ctx, W / 2, 560, 420, tt.color);
        ctx.textAlign = 'center';
        ctx.fillStyle = gold; ctx.font = '500 40px ' + FONT_SANS;
        ctx.fillText('사주 오행 캐릭터 테스트', W / 2, 140);
        ctx.fillStyle = text; ctx.font = '500 54px ' + FONT_SANS;
        ctx.fillText(opts.nick ? josa(opts.nick + '님', ['은', '는']) : '나는', W / 2, 240);
        drawIcon(ctx, tt.icon, (W - 500) / 2, 300, 500);
        ctx.fillStyle = goldLight; fitText(ctx, tt.name, 940, 900, 124, FONT_SERIF);
        ctx.fillText(tt.name, W / 2, 935);
        ctx.fillStyle = sub; ctx.font = '400 40px ' + FONT_SANS;
        ctx.fillText(tt.label + ' 일간 · ' + (tt.yang ? '양' : '음') + '의 ' + DATA.elements[tt.element].word, W / 2, 1010);
        ctx.fillStyle = text; ctx.font = '500 46px ' + FONT_SANS;
        wrapLines(ctx, tt.tagline, 920).slice(0, 2).forEach(function (l, i) { ctx.fillText(l, W / 2, 1090 + i * 60); });
        ctx.fillStyle = gold; ctx.font = '500 42px ' + FONT_SANS;
        ctx.fillText(tt.keywords.join('   '), W / 2, 1200);

        // 오행 막대
        var top = 1260, rowH = 66, maxC = Math.max(3, Math.max.apply(null, r.counts));
        ctx.fillStyle = 'rgba(255,255,255,0.04)';
        ctx.fillRect(90, top - 30, W - 180, rowH * 5 + 40);
        DATA.elements.forEach(function (el, i) {
            var y = top + i * rowH + 30;
            ctx.textAlign = 'left'; ctx.fillStyle = text; ctx.font = '500 38px ' + FONT_SANS;
            ctx.fillText(el.name + ' ' + el.word, 130, y);
            ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fillRect(330, y - 26, 560, 28);
            ctx.fillStyle = el.color; ctx.fillRect(330, y - 26, 560 * r.counts[i] / maxC, 28);
            ctx.textAlign = 'right'; ctx.fillStyle = text;
            ctx.fillText(String(r.counts[i]), 950, y);
        });

        ctx.textAlign = 'center';
        var tg = DATA.tenGods[r.tenGods.strongest];
        ctx.fillStyle = text; ctx.font = '500 42px ' + FONT_SANS;
        ctx.fillText('나의 무기 · ' + tg.key + '(' + tg.power + ')', W / 2, 1680);
        ctx.fillText('찰떡 짝꿍 · ' + bestMatch(r.stem).name, W / 2, 1750);
        ctx.fillStyle = gold; ctx.font = '400 34px ' + FONT_SANS;
        ctx.fillText('saju.gon.ai.kr/saju-test  ·  친구랑 궁합 보기', W / 2, 1850);
        return canvas;
    }

    window.SajuTestCard = { draw: drawCard, fontsReady: fontsReady };

    // ── 카카오 (공개 JavaScript 키가 서버 환경변수에 있을 때만) ─────────────
    var kakaoReady = null;
    function initKakao() {
        if (kakaoReady) return kakaoReady;
        kakaoReady = fetch('/api/share/config', { credentials: 'omit' })
            .then(function (res) { return res.ok ? res.json() : {}; })
            .then(function (cfg) {
                if (!cfg || !cfg.kakaoJsKey) return false;
                return new Promise(function (resolve) {
                    var s = document.createElement('script');
                    s.src = KAKAO_SDK.src; s.integrity = KAKAO_SDK.integrity; s.crossOrigin = 'anonymous';
                    s.onload = function () {
                        try { if (!window.Kakao.isInitialized()) window.Kakao.init(cfg.kakaoJsKey); resolve(true); }
                        catch (e) { resolve(false); }
                    };
                    s.onerror = function () { resolve(false); };
                    document.head.appendChild(s);
                });
            })
            .catch(function () { return false; });
        return kakaoReady;
    }

    function kakaoButton(label, build) {
        var btn = h('button', { type: 'button', class: 'st-btn st-kakao', hidden: true, text: label,
            onclick: function () {
                var msg = build();
                try {
                    window.Kakao.Share.sendDefault({
                        objectType: 'feed',
                        content: { title: msg.title, description: msg.text, imageUrl: msg.image,
                            link: { mobileWebUrl: msg.url, webUrl: msg.url } },
                        buttons: [{ title: msg.button, link: { mobileWebUrl: msg.url, webUrl: msg.url } }]
                    });
                    track('saju_test_share', { method: 'kakao', target: msg.target });
                } catch (e) { shareLink({ title: msg.title, text: msg.text, url: msg.url }, msg.target); }
            } });
        initKakao().then(function (ok) { if (ok) btn.hidden = false; });
        return btn;
    }

    // ── 화면 ──────────────────────────────────────────────────────
    var state = { query: null, result: null, nick: '', cardUrl: null };

    function elementBars(counts) {
        var maxC = Math.max(3, Math.max.apply(null, counts));
        return h('div', { class: 'st-bars', role: 'list', 'aria-label': '오행 분포' }, DATA.elements.map(function (el, i) {
            return h('div', { class: 'st-bar', role: 'listitem' }, [
                h('span', { text: el.name + ' ' + el.word }),
                h('span', { class: 'st-bar-track' }, [h('span', { class: 'st-bar-fill',
                    style: 'display:block;width:' + Math.round(100 * counts[i] / maxC) + '%;background:' + el.color })]),
                h('span', { text: String(counts[i]) })
            ]);
        }));
    }

    function fact(title, lines) {
        return h('div', { class: 'st-fact' }, [h('h3', { text: title })].concat(lines.map(function (l) {
            return typeof l === 'string' ? h('p', { text: l }) : l;
        })));
    }

    function renderResult(r, nick) {
        var t = DATA.types[r.stem];
        var tg = DATA.tenGods[r.tenGods.strongest];
        var lacking = r.lacking.map(function (i) { return DATA.elements[i].name + '(' + DATA.elements[i].word + ')'; });
        var match = bestMatch(r.stem);
        var box = document.getElementById('st-result');
        box.textContent = '';
        box.hidden = false;

        box.appendChild(h('div', { class: 'st-result-head' }, [
            iconSvg(t.icon, 132, t.name),
            h('p', { class: 'st-type-label', text: (nick ? josa(nick + '님', ['은', '는']) + ' ' : '') + t.label + ' 일간' }),
            h('h2', { class: 'st-type-name', text: t.name }),
            h('p', { class: 'st-tagline', text: t.tagline }),
            h('p', { class: 'st-keywords', text: t.keywords.join(' ') })
        ]));
        box.appendChild(elementBars(r.counts));
        box.appendChild(h('p', { class: 'st-hint', text: '태어난 해·달·날의 여섯 글자(천간·지지)에 담긴 오행 개수예요. 태어난 시간은 넣지 않았어요.' }));

        var lackingLines = r.counts[r.lacking[0]] === 0
            ? [lacking.join(', ') + ' 기운이 비어 있어요.'].concat(r.lacking.map(function (i) { return DATA.lackingTips[i]; }))
            : ['다섯 기운이 모두 들어 있는 고른 편이에요. 가장 적은 것은 ' + lacking.join(', ') + '입니다.'];
        box.appendChild(h('div', { class: 'st-facts' }, [
            fact('나의 무기 — ' + tg.key + '(' + tg.power + ')', [t.tenGods[r.tenGods.strongest]]),
            fact('주변에서 자주 듣는 말', ['"' + t.heard + '"']),
            fact('강점', [t.strengths.join(' · ')]),
            fact('연애할 때', [t.love]),
            fact('채우면 좋은 기운', lackingLines),
            fact('찰떡 짝꿍 유형', [h('p', {}, [h('a', { href: BASE + match.slug + '/', text: match.name + ' (' + match.label + ')' }),
                ' — 천간합으로 서로 끌어당기는 짝이에요.'])])
        ]));
        box.appendChild(h('p', { style: 'margin-top:1rem;text-align:center' },
            [h('a', { href: BASE + t.slug + '/', class: 'st-btn st-ghost', text: "'" + t.name + "' 유형 자세히 보기 →" })]));

        // 카드 + 공유
        var img = h('img', { class: 'st-card-preview', alt: t.name + ' 결과 카드', width: '1080', height: '1920' });
        var shareBox = h('div', { class: 'st-card-box', id: 'st-share' }, [
            h('h2', { text: '결과 카드', style: 'margin:0 0 0.5rem;font-size:1.2rem;text-align:center' }),
            img,
            h('p', { class: 'st-card-note', text: '휴대폰에서는 이미지를 길게 눌러도 저장할 수 있어요.' })
        ]);
        var grid = h('div', { class: 'st-btn-grid' });
        var saveBtn = h('button', { type: 'button', class: 'st-btn', text: '이미지 저장', onclick: saveCard });
        var fileShareBtn = h('button', { type: 'button', class: 'st-btn st-ghost', text: '이미지 공유', hidden: true, onclick: shareCardFile });
        var linkBtn = h('button', { type: 'button', class: 'st-btn st-ghost', text: '결과 링크 공유', onclick: function () {
            shareLink({ title: "나는 '" + t.name + "' 유형", text: t.tagline + ' — 너는 어떤 자연이야?', url: typeUrl(t) }, 'result');
        } });
        var copyBtn = h('button', { type: 'button', class: 'st-btn st-ghost', text: '링크 복사', onclick: function () {
            copyText(typeUrl(t)).then(function (ok) { toast(ok ? '결과 링크를 복사했어요!' : '복사에 실패했어요.'); if (ok) track('saju_test_share', { method: 'copy', target: 'result' }); });
        } });
        var kakao = kakaoButton('카카오톡으로 결과 보내기', function () {
            return { title: "나는 '" + t.name + "' 유형", text: t.tagline, image: SITE + OG_DIR + 'og-' + t.slug + '.jpg',
                url: typeUrl(t), button: '나도 테스트하기', target: 'result' };
        });
        kakao.classList.add('st-wide');
        saveBtn.classList.add('st-wide');
        fileShareBtn.classList.add('st-wide');
        [saveBtn, linkBtn, copyBtn, fileShareBtn, kakao].forEach(function (b) { grid.appendChild(b); });
        shareBox.appendChild(grid);
        box.appendChild(shareBox);

        // 친구 초대 (초대 링크에는 유형 코드와 별명만)
        var inviteLink = inviteUrl(r.code, nick);
        var inviteBox = h('div', { class: 'st-card-box st-invite-banner', id: 'st-invite-cta' }, [
            h('h2', { text: '친구 초대해 궁합 보기' }),
            h('p', { text: '초대 링크를 받은 친구가 생년월일을 넣으면 둘의 궁합이 나와요. 링크에는 내 생년월일이 들어가지 않고, 친구의 생년월일도 나에게 보이지 않아요.' }),
            h('div', { class: 'st-btn-grid' }, [
                h('button', { type: 'button', class: 'st-btn st-wide', text: '친구에게 초대장 보내기', onclick: function () {
                    shareLink({ title: '사주 궁합 초대장', text: (nick || '친구') + '님이 궁합 초대장을 보냈어요! 생년월일 넣고 우리 궁합 확인해 봐 (서로 생일은 안 보여요)', url: inviteLink }, 'invite');
                    track('saju_test_invite_send', { type_slug: t.slug });
                } }),
                (function () {
                    var k = kakaoButton('카카오톡으로 초대하기', function () {
                        return { title: '사주 궁합 초대장이 도착했어요', text: (nick || '친구') + '님과 나는 어떤 궁합일까? 생년월일만 넣으면 1초!',
                            image: SITE + OG_DIR + 'og-main.jpg', url: inviteLink, button: '궁합 보러 가기', target: 'invite' };
                    });
                    k.classList.add('st-wide');
                    return k;
                })()
            ])
        ]);
        box.appendChild(inviteBox);
        box.appendChild(h('p', { style: 'text-align:center;margin-top:1rem' }, [h('button', { type: 'button', class: 'st-btn st-ghost',
            text: '다시 하기', onclick: function () { window.location.href = BASE; } })]));

        // 카드 그림은 글꼴을 받은 뒤 그린다
        fontsReady(t.name + t.tagline + t.label + (nick || '') + '사주오행캐릭터테스트나의무기찰떡짝꿍').then(function () {
            var canvas = drawCard(document.createElement('canvas'), 'card', { result: r, nick: nick });
            canvas.toBlob(function (blob) {
                if (!blob) return;
                if (state.cardUrl) URL.revokeObjectURL(state.cardUrl);
                state.cardBlob = blob;
                state.cardUrl = URL.createObjectURL(blob);
                img.src = state.cardUrl;
                try {
                    var f = new File([blob], 'saju-' + t.slug + '.png', { type: 'image/png' });
                    if (navigator.canShare && navigator.canShare({ files: [f] })) fileShareBtn.hidden = false;
                } catch (e) { /* File 생성자 없는 브라우저 */ }
            }, 'image/png');
        });
        track('saju_test_result', { type_slug: t.slug, invited: state.query.from ? 1 : 0 });
    }

    function saveCard() {
        if (!state.cardUrl) { toast('카드를 만드는 중이에요. 잠시 뒤 다시 눌러 주세요.'); return; }
        var t = DATA.types[state.result.stem];
        var a = h('a', { href: state.cardUrl, download: 'saju-' + t.slug + '.png' });
        document.body.appendChild(a); a.click(); document.body.removeChild(a);
        track('saju_test_share', { method: 'download', target: 'card' });
    }

    function shareCardFile() {
        var t = DATA.types[state.result.stem];
        var f = new File([state.cardBlob], 'saju-' + t.slug + '.png', { type: 'image/png' });
        navigator.share({ files: [f], title: "나는 '" + t.name + "' 유형", text: typeUrl(t) }).then(function () {
            track('saju_test_share', { method: 'web_share_file', target: 'card' });
        }, function () {});
    }

    function renderCompat(container, a, b, opts) {
        var c = compatText(a, b);
        var ta = DATA.types[a.stem], tb = DATA.types[b.stem];
        container.textContent = '';
        container.hidden = false;
        container.appendChild(h('h2', { text: opts.title, style: 'margin:0 0 1rem;text-align:center;font-size:1.25rem' }));
        container.appendChild(h('div', { class: 'st-pair-icons' }, [iconSvg(ta.icon, 84, ta.name), h('span', { class: 'st-heart', text: '♥', 'aria-hidden': 'true' }), iconSvg(tb.icon, 84, tb.name)]));
        container.appendChild(h('div', { class: 'st-pair-names' }, [h('span', { text: (a.nick || '나') + ' · ' + ta.name }), h('span', { text: (b.nick || '친구') + ' · ' + tb.name })]));
        container.appendChild(h('div', { class: 'st-score' }, [
            h('div', { class: 'st-score-num', text: c.score + '점' }),
            h('div', { class: 'st-score-label', text: c.label })
        ]));
        c.lines.forEach(function (l) { container.appendChild(h('p', { text: l })); });
        container.appendChild(fact('오래 가는 팁', [c.tip]));
        container.appendChild(h('p', { class: 'st-disclaimer', text: '궁합 지수(' + Core.MIN_SCORE + '~' + Core.MAX_SCORE + '점)는 두 사람의 일간·일지 관계로 정한 재미용 지표예요. 관계를 단정하지 않으며, 생시까지 넣은 정식 궁합은 궁합 메뉴에서 볼 수 있어요.' }));
        if (opts.actions) container.appendChild(opts.actions);
    }

    function onSubmit(ev) {
        ev.preventDefault();
        var f = ev.target;
        var y = Number(f.year.value), m = Number(f.month.value), d = Number(f.day.value);
        var err = document.getElementById('st-error');
        if (!Core.isValidDate(y, m, d)) { err.textContent = '생년월일을 다시 확인해 주세요.'; return; }
        err.textContent = '';
        var nick = cleanNick(f.nick.value);
        var r = Core.analyze(y, m, d);
        state.result = r; state.nick = nick;
        renderResult(r, nick);

        var q = state.query;
        var compatBox = document.getElementById('st-compat');
        if (q.from) {
            var inviter = { stem: q.from.stem, branch: q.from.branch, nick: q.n || '친구' };
            var me = { stem: r.stem, branch: r.dayBranch, nick: nick || '나' };
            var back = pairUrl(Core.typeCode(inviter.stem, inviter.branch), q.n, r.code, nick);
            var actions = h('div', { class: 'st-btn-grid' }, [
                h('button', { type: 'button', class: 'st-btn st-wide', text: inviter.nick + '님에게 궁합 결과 보내기', onclick: function () {
                    shareLink({ title: '우리 사주 궁합 결과', text: inviter.nick + ' × ' + me.nick + ' 궁합 결과가 나왔어요!', url: back }, 'pair');
                } })
            ]);
            renderCompat(compatBox, inviter, me, { title: inviter.nick + '님과 나의 궁합', actions: actions });
            track('saju_test_pair_result', { from_invite: 1, score: Core.compatibility(inviter, me).score });
            compatBox.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            document.getElementById('st-result').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function fillDateSelects(form) {
        var thisYear = new Date().getFullYear();
        function opts(sel, from, to, desc, unit) {
            sel.appendChild(h('option', { value: '', text: unit }));
            for (var i = desc ? to : from; desc ? i >= from : i <= to; i += desc ? -1 : 1) {
                sel.appendChild(h('option', { value: String(i), text: String(i) }));
            }
        }
        opts(form.year, Core.MIN_YEAR + 30, Math.min(thisYear, Core.MAX_YEAR), true, '년');
        opts(form.month, 1, 12, false, '월');
        opts(form.day, 1, 31, false, '일');
    }

    function init() {
        if (!Core || !DATA) return;
        state.query = readQuery();
        var q = state.query;
        var form = document.getElementById('st-form');
        fillDateSelects(form);
        form.addEventListener('submit', onSubmit);

        if (q.pair) {
            var pairBox = document.getElementById('st-pair');
            renderCompat(pairBox, { stem: q.pair[0].stem, branch: q.pair[0].branch, nick: q.n || '친구 1' },
                { stem: q.pair[1].stem, branch: q.pair[1].branch, nick: q.m || '친구 2' },
                { title: (q.n || '친구 1') + ' × ' + (q.m || '친구 2') + ' 궁합',
                  actions: h('p', { style: 'text-align:center;margin-top:1rem' }, [h('a', { href: '#st-form', class: 'st-btn', text: '나도 테스트하고 친구 초대하기' })]) });
            track('saju_test_pair_open', {});
        }
        if (q.from) {
            var who = q.n || '친구';
            var banner = document.getElementById('st-invite');
            banner.hidden = false;
            banner.querySelectorAll('[data-st="inviter"]').forEach(function (el) { el.textContent = who; });
            var it = DATA.types[q.from.stem];
            banner.querySelector('[data-st="inviter-type"]').textContent = it.name;
            document.getElementById('st-submit').textContent = josa(who + '님', ['과', '와']) + ' 궁합 보기';
            track('saju_test_invite_open', {});
        }
        initKakao();
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
