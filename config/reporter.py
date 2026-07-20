import os
import warnings
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from notion_client import Client
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=FutureWarning)
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
CRED_PATH_FROM_ENV = os.getenv("GOOGLE_CRED_PATH")

PATH_A = f"{CRED_PATH_FROM_ENV}.json" if CRED_PATH_FROM_ENV else ""
FINAL_CRED_PATH = PATH_A if (PATH_A and os.path.exists(PATH_A)) else CRED_PATH_FROM_ENV

# ==========================================
# 구글 스프레드시트 초기화
# ==========================================
sheet = None
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

try:
    if FINAL_CRED_PATH and os.path.exists(FINAL_CRED_PATH):
        creds = ServiceAccountCredentials.from_json_keyfile_name(FINAL_CRED_PATH, scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open("인스타그램자동화 시트")
        sheet = spreadsheet.get_worksheet(0)
        print("🔓 [Reporter] 구글 스프레드시트 연결 성공!")
    else:
        print("❌ [Reporter] 구글 시트 키 파일을 찾을 수 없습니다.")
except Exception as e:
    print(f"❌ [Reporter] 구글 시트 초기화 실패: {e}")

notion = Client(auth=NOTION_TOKEN)


# ==========================================
# 결과 전송 공통 함수
# ==========================================
def report_test_result(tc_id, priority, pre_condition, test_steps, expected_result, result):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"🔄 [{tc_id}] 테스트 결과를 매칭하여 저장 중...")

    # 1. 구글 시트 반영
    if sheet is not None:
        try:
            a_column_values = sheet.col_values(1)
            target_row = None

            for idx, value in enumerate(a_column_values):
                if value.strip() == tc_id:
                    target_row = idx + 1
                    break

            if target_row:
                print(f"🔍 시트에서 {tc_id}를 발견했습니다! -> [{target_row}행]에 업데이트합니다.")
                sheet.update_cell(target_row, 2, "인스타 앱 진입 후 새로고침 기능이 동작하는가")
                sheet.update_cell(target_row, 3, expected_result)
                sheet.update_cell(target_row, 9, result)
                sheet.update_cell(target_row, 10, f"[{result}] {current_time}")
            else:
                print(f"ℹ️ 시트 양식에 [{tc_id}]가 없습니다. 맨 아래 행에 새로 추가합니다.")
                row_data = [
                    tc_id, "인스타 앱 진입 후 새로고침 기능이 동작하는가", expected_result,
                    "", "", "", "", "", result, f"[{result}] {current_time}"
                ]
                sheet.append_row(row_data)
            print(f"🟢 구글 시트 반영 성공!")
        except Exception as e:
            print(f"🔴 구글 시트 입력 에러: {e}")
    else:
        print("🔴 구글 시트 연결 핸들이 없어 업데이트를 건너뜁니다.")

    # 2. 노션 데이터베이스 전송
    try:
        payload_properties = {
            "제목 (Title)": {"title": [{"text": {"content": tc_id}}]},
            "Priority": {"rich_text": [{"text": {"content": priority}}]},
            "사전조건 (Pre-condition)": {"rich_text": [{"text": {"content": pre_condition}}]},
            "테스트 스텝 (Test Steps)": {"rich_text": [{"text": {"content": test_steps}}]},
            "기대결과 (Expected Result)": {"rich_text": [{"text": {"content": expected_result}}]},
            "실제결과 (Actual Result)": {"rich_text": [{"text": {"content": f"[{result}] {current_time}"}}]}
        }
        notion.pages.create(parent={"database_id": DATABASE_ID}, properties=payload_properties)
        print("🟢 노션 데이터베이스 결과 추가 완료!")
    except Exception as e:
        print(f"🔴 노션 최종 처리 실패: {e}")