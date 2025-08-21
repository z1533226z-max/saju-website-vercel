# 사주팔자 웹사이트 - Vercel 배포 버전

## 🚀 프로젝트 개요
사주팔자 웹사이트의 Vercel 배포용 버전입니다. Flask 백엔드를 Vercel Functions로 변환하여 서버리스 환경에서 작동합니다.

## 📂 프로젝트 구조
```
saju-website-vercel/
├── api/                 # Vercel Functions (Python)
│   ├── core/           # 핵심 계산 모듈
│   ├── data/           # JSON 데이터 파일
│   ├── saju/           # 사주 관련 API Functions
│   │   ├── calculate.py    # 사주 계산
│   │   ├── compatibility.py # 궁합 계산
│   │   └── info.py         # 정보 조회
│   └── health.py       # 헬스체크
├── public/             # 정적 파일 (프론트엔드)
│   ├── index.html      # 메인 페이지
│   ├── css/           # 스타일시트
│   └── js/            # JavaScript 파일
├── vercel.json        # Vercel 설정
├── requirements.txt   # Python 의존성
└── README.md         # 이 파일
```

## 🛠 기술 스택
- **Backend**: Python Vercel Functions
- **Frontend**: HTML5, CSS3, JavaScript, Alpine.js, Chart.js
- **Deployment**: Vercel

## 📌 API 엔드포인트
- `GET /api/health` - 서버 상태 확인
- `POST /api/saju/calculate` - 사주 계산
- `POST /api/saju/compatibility` - 궁합 계산
- `GET /api/saju/info/{type}` - 정보 조회

## 🚀 배포 방법

### 1. Vercel CLI 설치
```bash
npm i -g vercel
```

### 2. 로컬 테스트
```bash
vercel dev
```

### 3. 배포
```bash
vercel --prod
```

## 📝 환경 변수
현재 환경 변수는 필요하지 않습니다.

## 🔗 관련 링크
- [원본 프로젝트](https://github.com/z1533226z-max/saju-website)
- [Vercel 문서](https://vercel.com/docs)

## 📄 라이선스
MIT License

---
*Last Updated: 2025-08-21*
*Deployment Triggered: 2025-08-21 12:08*
