/**
 * 사주 오행 캐릭터 테스트 — 계산 핵심 (화면 코드 없음, 브라우저·node 공용)
 *
 * - 년주·월주·일주 계산은 api/_core/saju_calculator.py 와 같은 규칙을 그대로 옮겼다
 *   (입춘 2/4 기준 년, 절기 고정일 기준 월, 1900-01-01 갑술일 기준 일).
 *   tests/test_saju_test.py 가 node 로 이 파일을 돌려 파이썬 계산기와 날짜별로 대조한다.
 * - 생년월일은 이 파일 밖(서버·링크)으로 나가지 않는다. 링크에는 typeCode() 결과
 *   (일간 1글자 + 일지 1글자 = 60가지 중 하나)만 들어간다.
 */
(function (root, factory) {
    var core = factory();
    if (typeof module === 'object' && module.exports) module.exports = core;
    else root.SajuTestCore = core;
})(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    var STEMS = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'];
    var STEMS_HANJA = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    var BRANCHES = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해'];
    var BRANCHES_HANJA = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    var ELEMENTS = ['목', '화', '토', '금', '수'];
    var ELEMENTS_HANJA = ['木', '火', '土', '金', '水'];
    // 지지 오행: 자수 축토 인목 묘목 진토 사화 오화 미토 신금 유금 술토 해수
    var BRANCH_ELEMENT = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4];
    // 십신 묶음: (상대 오행 - 내 오행) mod 5
    var TEN_GOD_GROUPS = ['비겁', '식상', '재성', '관성', '인성'];

    // saju_calculator.py 의 solar_terms (절기월 → 절입일) / solar_term_months (양력월 → 절기월)
    var TERM_DAY = { 1: 4, 2: 6, 3: 5, 4: 6, 5: 6, 6: 7, 7: 8, 8: 8, 9: 8, 10: 7, 11: 7, 12: 6 };
    var TERM_MONTH_OF = { 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 1: 12 };
    var MONTH_STEM_START = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0];

    var MIN_YEAR = 1900;
    var MAX_YEAR = 2100;

    function mod(n, m) { return ((n % m) + m) % m; }

    function isValidDate(y, m, d) {
        if (!(Number.isInteger(y) && Number.isInteger(m) && Number.isInteger(d))) return false;
        if (y < MIN_YEAR || y > MAX_YEAR || m < 1 || m > 12 || d < 1) return false;
        return d <= new Date(Date.UTC(y, m, 0)).getUTCDate();
    }

    function sajuYear(y, m, d) {
        return (m === 1 || (m === 2 && d < TERM_DAY[1])) ? y - 1 : y;
    }

    function termMonth(m, d) {
        if (m === 1) return d < TERM_DAY[12] ? 11 : 12;
        var tm = TERM_MONTH_OF[m];
        if (d >= TERM_DAY[tm]) return tm;
        return tm > 1 ? tm - 1 : 12;
    }

    /** 양력 생년월일 → 년·월·일 기둥 (각 {stem, branch} 인덱스). 시주는 쓰지 않는다. */
    function pillars(y, m, d) {
        if (!isValidDate(y, m, d)) throw new RangeError('invalid date');
        var sy = sajuYear(y, m, d);
        var yearStem = mod(sy - 4, 10);
        var tm = termMonth(m, d);
        var days = Math.round((Date.UTC(y, m - 1, d) - Date.UTC(1900, 0, 1)) / 86400000);
        return {
            year: { stem: yearStem, branch: mod(sy - 4, 12) },
            month: { stem: (MONTH_STEM_START[yearStem] + tm - 1) % 10, branch: (tm + 1) % 12 },
            day: { stem: mod(days, 10), branch: mod(10 + days, 12) }
        };
    }

    function stemElement(s) { return Math.floor(s / 2); }

    /** 여섯 글자(년·월·일의 천간·지지) 오행 개수 [목,화,토,금,수] */
    function elementCounts(p) {
        var c = [0, 0, 0, 0, 0];
        ['year', 'month', 'day'].forEach(function (k) {
            c[stemElement(p[k].stem)] += 1;
            c[BRANCH_ELEMENT[p[k].branch]] += 1;
        });
        return c;
    }

    /**
     * 일간을 뺀 다섯 글자의 십신 묶음 점수. 월지는 계절의 힘이 커서 1.5배.
     * 가장 큰 묶음 = '나의 무기'. 동점이면 월지 묶음, 그다음 비겁→인성 순서.
     */
    function tenGodProfile(p) {
        var me = stemElement(p.day.stem);
        var score = [0, 0, 0, 0, 0];
        function add(el, w) { score[mod(el - me, 5)] += w; }
        add(stemElement(p.year.stem), 1);
        add(BRANCH_ELEMENT[p.year.branch], 1);
        add(stemElement(p.month.stem), 1);
        add(BRANCH_ELEMENT[p.month.branch], 1.5);
        add(BRANCH_ELEMENT[p.day.branch], 1);
        var monthGroup = mod(BRANCH_ELEMENT[p.month.branch] - me, 5);
        var best = monthGroup;
        for (var g = 0; g < 5; g++) if (score[g] > score[best]) best = g;
        return { score: score, strongest: best };
    }

    /** 결과 전체 (화면·카드에서 쓰는 값만) */
    function analyze(y, m, d) {
        var p = pillars(y, m, d);
        var counts = elementCounts(p);
        var max = Math.max.apply(null, counts);
        var min = Math.min.apply(null, counts);
        return {
            pillars: p,
            stem: p.day.stem,
            dayBranch: p.day.branch,
            zodiacBranch: p.year.branch,
            counts: counts,
            dominant: counts.indexOf(max),
            lacking: counts.map(function (n, i) { return n === min ? i : -1; }).filter(function (i) { return i >= 0; }),
            tenGods: tenGodProfile(p),
            code: typeCode(p.day.stem, p.day.branch)
        };
    }

    // ── 링크용 유형 코드: 일간(0~9) + 일지(0~b, 12진) 두 글자 ───────────────
    var B12 = '0123456789ab';

    function typeCode(stem, branch) { return String(stem) + B12.charAt(branch); }

    /** 코드 → {stem, branch} 또는 null. 60갑자에 없는 조합(음양 불일치)은 거절. */
    function parseCode(code) {
        if (typeof code !== 'string' || !/^[0-9][0-9ab]$/.test(code)) return null;
        var stem = Number(code.charAt(0));
        var branch = B12.indexOf(code.charAt(1));
        if (stem % 2 !== branch % 2) return null;
        return { stem: stem, branch: branch };
    }

    // ── 궁합 (두 사람의 일간 + 일지만으로 계산, 대칭) ──────────────────────
    var YUKHAP = [[0, 1], [2, 11], [3, 10], [4, 9], [5, 8], [6, 7]];
    var SAMHAP = [[8, 0, 4], [11, 3, 7], [2, 6, 10], [5, 9, 1]];

    function stemRelation(a, b) {
        if (Math.abs(a - b) === 5) return 'hap';                 // 천간합: 갑기·을경·병신·정임·무계
        var ea = stemElement(a), eb = stemElement(b);
        if (ea === eb) return 'same';
        var r = mod(eb - ea, 5);
        if (r === 1) return 'a_feeds_b';                          // a 가 b 를 생함
        if (r === 4) return 'b_feeds_a';
        if (r === 2) return 'a_shapes_b';                         // a 가 b 를 극함
        return 'b_shapes_a';
    }

    function branchRelation(a, b) {
        if (a === b) return 'same';
        if (Math.abs(a - b) === 6) return 'chung';
        for (var i = 0; i < YUKHAP.length; i++) {
            var pr = YUKHAP[i];
            if ((pr[0] === a && pr[1] === b) || (pr[0] === b && pr[1] === a)) return 'yukhap';
        }
        for (var j = 0; j < SAMHAP.length; j++) {
            if (SAMHAP[j].indexOf(a) >= 0 && SAMHAP[j].indexOf(b) >= 0) return 'samhap';
        }
        return 'plain';
    }

    var STEM_BASE = { hap: 91, a_feeds_b: 85, b_feeds_a: 85, same: 79, a_shapes_b: 71, b_shapes_a: 71 };
    var BRANCH_ADJ = { yukhap: 6, samhap: 4, same: 1, plain: 0, chung: -6 };
    var MIN_SCORE = 58;
    var MAX_SCORE = 97;

    /** a, b = {stem, branch(일지)} → {score, stemRel, branchRel} */
    function compatibility(a, b) {
        var sr = stemRelation(a.stem, b.stem);
        var br = branchRelation(a.branch, b.branch);
        // 같은 일간끼리는 1점 덜 줘서 '나와 같은 사람'이 최고점이 되지 않게
        var base = STEM_BASE[sr] - (sr === 'same' && a.stem === b.stem ? 1 : 0);
        var score = Math.max(MIN_SCORE, Math.min(MAX_SCORE, base + BRANCH_ADJ[br]));
        return { score: score, stemRel: sr, branchRel: br };
    }

    return {
        STEMS: STEMS, STEMS_HANJA: STEMS_HANJA, BRANCHES: BRANCHES, BRANCHES_HANJA: BRANCHES_HANJA,
        ELEMENTS: ELEMENTS, ELEMENTS_HANJA: ELEMENTS_HANJA, BRANCH_ELEMENT: BRANCH_ELEMENT,
        TEN_GOD_GROUPS: TEN_GOD_GROUPS, MIN_YEAR: MIN_YEAR, MAX_YEAR: MAX_YEAR,
        MIN_SCORE: MIN_SCORE, MAX_SCORE: MAX_SCORE,
        isValidDate: isValidDate, pillars: pillars, stemElement: stemElement,
        elementCounts: elementCounts, tenGodProfile: tenGodProfile, analyze: analyze,
        typeCode: typeCode, parseCode: parseCode,
        stemRelation: stemRelation, branchRelation: branchRelation, compatibility: compatibility
    };
});
