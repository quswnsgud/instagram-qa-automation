# 📸 Instagram Automation & Reporting System

> **Page Object Model(POM) 패턴 기반의 인스타그램 자동화 및 노션/구글 시트 연동 테스트 자동화 프로젝트**
> 
> 테스트 자동화 시나리오를 수행하고, 그 결과를 외부 서비스(Notion, Google Sheets)에 실시간으로 기록하는 통합 자동화 시스템입니다.

<br>

## ⚙️ Tech Stack
- **Language**: Python
- **Framework**: Pytest
- **Libraries**: Selenium
- **Integrations**: Notion API, Google Sheets API (via custom reporter)
- **Security**: Dotenv (`.env`)
- **Version Control**: Git, GitHub

<br>

## ✨ 핵심 기능 (Key Features)

### 1. Page Object Model (POM) 패턴 기반 리팩토링
- **가독성 및 유지보수성 향상**: UI 요소(Element)와 테스트 로직을 완벽히 분리하여, 테스트 코드가 한글 소설을 읽듯 직관적이고 명확하게 읽히도록 설계했습니다.
- 복잡한 `find_element` 코드를 페이지 객체 내부로 캡슐화했습니다.

### 2. 스마트 예외 처리 및 자동 스크린샷 캡처
- 테스트 수행 중 에러(Exception) 발생 시, 이를 감지하여 `screenshots/` 디렉토리에 **실패 시점의 화면을 자동으로 캡처 및 저장**하여 디버깅을 용이하게 만들었습니다.
- 실패 상황에서도 Pytest 프레임워크가 정상적으로 실패를 감지하도록 에러 핸들링을 정교화했습니다.

### 3. 실시간 결과 리포팅 (Notion & Google Sheets 연동)
- 환경 변수(`.env`)로 안전하게 관리되는 자격 증명(Notion Token, Google API Key)을 활용합니다.
- 테스트 완료 후 `report_test_result` 모듈을 통해 **테스트 케이스 ID, 중요도, 수행 단계, 예상 결과, 그리고 성공/실패 여부(PASS/FAIL)를 노션 데이터베이스 및 구글 스프레드시트에 실시간으로 업데이트**합니다.

<br>

## 📋 포함된 테스트 시나리오
현재 구현된 핵심 테스트 시나리오는 다음과 같습니다.

| TC ID | 중요도 | 테스트 시나리오 | 예상 결과 |
| :--- | :--- | :--- | :--- |
| **TC_001** | High | 인스타그램 로그인 및 대시보드 진입 테스트 | 로그인이 성공하여 홈 피드가 정상적으로 표시되어야 함 |

<br>

## 📁 Project Structure
```text
├── config/          # 환경 설정 및 결과 리포터 관리 (reporter.py 등)
├── pages/           # 웹 페이지 객체 (요소 및 액션 정의 - login_page.py 등)
├── tests/           # 실제 자동화 테스트 시나리오 (test_instagram_flow.py 등)
├── screenshots/     # 테스트 실패 시 스크린샷이 자동 저장되는 폴더
├── .env             # 환경 변수 파일 (Git 관리 제외 ⚠️)
├── .gitignore       # Git 제외 설정 파일
└── README.md        # 프로젝트 설명 문서 (현재 파일)