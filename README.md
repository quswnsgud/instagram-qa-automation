# 📸 Instagram Automation & Reporting System

> **Page Object Model(POM) 패턴 기반의 인스타그램 모바일 자동화 및 노션/구글 시트 연동 테스트 자동화 프로젝트**
> 
> 테스트 자동화 시나리오를 수행하고, 그 결과를 외부 서비스(Notion, Google Sheets)에 실시간으로 기록하는 통합 자동화 시스템입니다.

<br>

## ⚙️ Tech Stack
- **Language**: Python 3.10+
- **Framework**: Pytest
- **Automation Tool**: Appium (UiAutomator2) / Selenium
- **Target OS/Device**: Android (v16) / Device ID: `R3KL106Z49W`
- **Integrations**: Notion API, Google Sheets API (via custom reporter)
- **CI/CD**: GitHub Actions
- **Security**: Dotenv (`.env`)
- **Version Control**: Git, GitHub

<br>

## ✨ 핵심 기능 (Key Features)

### 1. Page Object Model (POM) 패턴 기반 리팩토링
- **가독성 및 유지보수성 향상**: UI 요소(Element)와 테스트 로직을 완벽히 분리하여, 테스트 코드가 한글 소설을 읽듯 직관적이고 명확하게 읽히도록 설계했습니다.
- 복잡한 모바일 드라이버 제어 코드를 페이지 객체 내부(`pages/`)로 캡슐화했습니다.

### 2. 스마트 예외 처리 및 자동 스크린샷 캡처
- 테스트 수행 중 에러(Exception) 발생 시, 이를 감지하여 `screenshots/` 디렉토리에 **실패 시점의 화면을 자동으로 캡처 및 저장**하여 디버깅을 용이하게 만들었습니다.
- 실패 상황에서도 Pytest 프레임워크가 정상적으로 실패를 감지하도록 에러 핸들링을 정교화했습니다.

### 3. 실시간 결과 리포팅 (Notion & Google Sheets 연동)
- 환경 변수(`.env`)로 안전하게 관리되는 자격 증명(Notion Token, Google API Key)을 활용합니다.
- 테스트 완료 후 `report_test_result` 모듈을 통해 **테스트 케이스 ID, 중요도, 수행 단계, 예상 결과, 그리고 성공/실패 여부(PASS/FAIL)를 노션 데이터베이스 및 구글 스프레드시트에 실시간으로 업데이트**합니다.

### 4. GitHub Actions 기반 환경별 테스트 제어 (CI 완공 🎉)
- 코드가 원격 저장소에 푸시되거나 Pull Request가 생성될 때마다 GitHub 가상 우분투 환경에서 파이썬 및 의존성 라이브러리가 자동으로 빌드되도록 파이프라인(`main.yml`)을 구축했습니다.
- **CI 환경 최적화 (Skip 로직)**: 실제 모바일 단말기 연결이 불가능한 GitHub Actions 가상 서버 환경(`CI=true`)을 감지하면 Appium 연결 단계를 안전하게 건너뛰도록(`pytest.skip`) 구현했습니다. 이를 통해 로컬 환경과의 의존성 충돌 없이 빌드 오류 및 코드 결함 여부만 안정적으로 자동 검증합니다.

<br>

## 📋 포함된 테스트 시나리오
현재 구현된 핵심 테스트 시나리오는 다음과 같습니다.

| TC ID | 중요도 | 테스트 시나리오 | 예상 결과 |
| :--- | :--- | :--- | :--- |
| **TC_001** | High | 인스타그램 로그인 및 대시보드 진입 테스트 | 로그인이 성공하여 홈 피드가 정상적으로 표시되어야 함 |

<br>

## 🚀 실행 및 테스트 방법

### 1. 로컬 환경 (Local PC Execution)
실제 단말기 제어 및 인스타그램 앱 구동 테스트는 로컬 컴퓨터에서 수행합니다.
1. **의존성 라이브러리 설치**:
   ```bash
   pip install pytest selenium python-dotenv Appium-Python-Client gspread oauth2client google-auth notion_client