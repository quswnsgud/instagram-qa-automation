import os
import warnings
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from notion_client import Client
# 🚀 [.env] 파일을 읽어오기 위한 라이브러리 추가
from dotenv import load_dotenv

# 구글 auth 관련 고버전 경고(FutureWarning) 숨기기
warnings.filterwarnings("ignore", category=FutureWarning)

# ==========================================
# [보안설정] 환경 변수(.env) 파일 로드
# ==========================================
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
CRED_PATH_FROM_ENV = os.getenv("GOOGLE_CRED_PATH")

# 구글 키 파일 추적 (기존 .json.json 예외 처리 유지)
PATH_A = f"{CRED_PATH_FROM_ENV}.json" if CRED_PATH_FROM_ENV else ""
FINAL_CRED_PATH = PATH_A if (PATH_A and os.path.exists(PATH_A)) else CRED_PATH_FROM_ENV

# ==========================================
# [설정 1] 구글 스프레드시트 로그인
# ==========================================
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
try:
    if FINAL_CRED_PATH and os.path.exists(FINAL_CRED_PATH):
        creds = ServiceAccountCredentials.from_json_keyfile_name(FINAL_CRED_PATH, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("인스타그램자동화 시트")
        sheet = spreadsheet.get_worksheet(0)
        print("🔓 구글 스프레드시트 연결 성공!")
    else:
        print("❌ 구글 시트 키 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except Exception as e:
    print(f"❌ 구글 시트 초기화 실패: {e}")

# ==========================================
# [설정 2] 노션 API 로그인
# ==========================================
notion = Client(auth=NOTION_TOKEN)


# ==========================================
# [기능] 양쪽 표에 결과 누적 전송 함수
# ==========================================
def report_test_result(row_num, tc_id, priority, pre_condition, test_steps, expected_result, result):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🔄 [{tc_id}] 테스트 결과를 누적 저장 중...")

    # ----------------------------------------
    # 1. 구글 스프레드시트 업데이트 (빈 행 찾아 누적)
    # ----------------------------------------
    if 'sheet' in globals():
        try:
            existing_rows = len(sheet.col_values(1))
            target_row = existing_rows + 1

            if target_row < 6:
                target_row = 6

            sheet.update_cell(target_row, 1, tc_id)
            sheet.update_cell(target_row, 2, "인스타 앱 진입 후 새로고침 기능이 동작하는가")
            sheet.update_cell(target_row, 3, expected_result)
            sheet.update_cell(target_row, 9, result)
            sheet.update_cell(target_row, 10, f"[{result}] {current_time}")

            print(f"🟢 구글 시트 -> 새 빈 줄인 [{target_row}행]에 결과 누적 성공!")
        except Exception as e:
            print(f"🔴 구글 시트 입력 에러: {e}")
    else:
        print("🔴 구글 시트 연결 핸들이 없어 업데이트를 건너뜁니다.")

    # ----------------------------------------
    # 2. 노션 데이터베이스 전송
    # ----------------------------------------
    try:
        payload_properties = {
            "제목 (Title)": {"title": [{"text": {"content": tc_id}}]},
            "Priority": {"rich_text": [{"text": {"content": priority}}]},
            "사전조건 (Pre-condition)": {"rich_text": [{"text": {"content": pre_condition}}]},
            "테스트 스텝 (Test Steps)": {"rich_text": [{"text": {"content": test_steps}}]},
            "기대결과 (Expected Result)": {"rich_text": [{"text": {"content": expected_result}}]},
            "실제결과 (Actual Result)": {"rich_text": [{"text": {"content": f"[{result}] {current_time}"}}]}
        }

        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=payload_properties
        )
        print("🟢 노션 데이터베이스 결과 추가 완료!")
    except Exception as e:
        print(f"🔴 노션 최종 처리 실패: {e}")


if __name__ == "__main__":
    # 내부 테스트용 실행
    report_test_result(
        row_num=6,
        tc_id="TC_001",
        priority="P1 (High)",
        pre_condition="유효한 테스트 계정 로그인 상태",
        test_steps="1. activate_app으로 인스타그램 앱 실행\n2. 화면 로딩 대기\n3. 새로고침 수행",
        expected_result="새로 고침이 정상 적으로 됨",
        result="FAIL"
    )