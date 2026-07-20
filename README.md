# 📸 Instagram Automation Project

> **Page Object Model(POM) 패턴을 적용한 인스타그램 자동화 및 크롤링 프로젝트**
> 
> 주기적으로 공부하고 개발한 내용을 기록하는 저장소입니다.

<br>

## ⚙️ Tech Stack
- **Language**: Python
- **Libraries**: Selenium, Custom Libraries
- **Security**: Dotenv (`.env`)
- **Version Control**: Git, GitHub

<br>

## 🚀 지금까지 완료한 내용

### 1. Page Object Model (POM) 패턴 적용 및 리팩토링
- **목적**: 코드의 재사용성을 높이고 유지보수를 쉽게 하기 위해 구조를 개선했습니다.
- **성과**: 로직과 페이지 요소를 분리하여 코드가 한결 깔끔해졌으며, 리팩토링 이후 **테스트 실행까지 성공적으로 완료**했습니다.

### 2. 프로젝트 보안 강화 (.env 도입)
- GitHub에 코드를 올리기 전, 민감한 개인 정보(예: Notion Token, Google API Key 등)가 노출되는 것을 방지했습니다.
- `.env` 파일을 통해 환경 변수로 자격 증명을 안전하게 관리하도록 설정했습니다.

### 3. Git 및 GitHub 저장소 연동
- 로컬 저장소(`git init`)를 초기화하고 첫 번째 커밋을 완료했습니다.
- 리팩토링된 안전한 코드를 원격 저장소(GitHub)에 `push`하여 백업 및 버전 관리를 시작했습니다.

<br>

## 📁 Project Structure
현재 프로젝트는 구조화된 POM 패턴에 따라 아래와 같이 구성되어 있습니다.

```text
├── config/          # 환경 설정 및 변수 관리
├── pages/           # 웹 페이지 객체 (요소 및 액션 정의)
├── tests/           # 실제 자동화 테스트 시나리오
├── .env             # 환경 변수 파일 (Git 관리 제외 ⚠️)
├── .gitignore       # Git 제외 설정 파일
└── README.md        # 프로젝트 설명 문서 (현재 파일)