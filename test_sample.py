import os
import warnings
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from notion_client import Client
from dotenv import load_dotenv
from appium import webdriver
from appium.options.common import AppiumOptions

warnings.filterwarnings("ignore", category=FutureWarning)
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
CRED_PATH_FROM_ENV = os.getenv("GOOGLE_CRED_PATH")

PATH_A = f"{CRED_PATH_FROM_ENV}.json" if CRED_PATH_FROM_ENV else ""
FINAL_CRED_PATH = PATH_A if (PATH_A and os.path.exists(PATH_A)) else CRED_PATH_FROM_ENV

# ==========================================
# 구글 스프레드시트 및 노션 로그인 설정
# ==========================================
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(FINAL_CRED_PATH, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("인스타그램자동화 시트")
    sheet = spreadsheet.get_worksheet(0)
    print("🔓 구글 스프레드시트 연결 성공!")
except Exception as e:
    print(f"❌ 구글 시트 연결 실패: {e}")

notion = Client(auth=NOTION_TOKEN)


def report_test_result(tc_id, priority, pre_condition, test_steps, expected_result, result):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if 'sheet' in globals():
        try:
            a_column_values = [val.strip() for val in sheet.col_values(1)]
            target_row = None
            for idx, value in enumerate(a_column_values):
                if value == tc_id:
                    target_row = idx + 1
                    break

            if target_row:
                print(f"🔍 시트에서 {tc_id}를 발견했습니다! -> [{target_row}행]에 업데이트합니다.")
                sheet.update_cell(target_row, 2, "인스타 앱 진입 후 로고 확인 기능")
                sheet.update_cell(target_row, 3, expected_result)
                sheet.update_cell(target_row, 9, result)
                sheet.update_cell(target_row, 10, f"[{result}] {current_time}")
                print(f"🟢 구글 시트 반영 성공!")
        except Exception as e:
            print(f"🔴 구글 시트 입력 에러: {e}")


# ==========================================
# 🚀 진짜 핸드폰 제어 및 실패 스크린샷 검증 시나리오
# ==========================================
def test_instagram_logo_check():
    print("\n▶️ [테스트 시작] 인스타그램 로고 존재 여부 검증")

    my_tc_id = "TC_001"

    # 📱 내 핸드폰을 제어하기 위한 환경 설정 값
    options = AppiumOptions()
    options.set_capability('platformName', 'Android')
    options.set_capability('automationName', 'UiAutomator2')
    options.set_capability('appPackage', 'com.instagram.android')
    # appActivity 줄을 지우거나 주석 처리하고, 아래 옵션을 추가합니다.
    options.set_capability('dontStopAppOnReset', True)
    options.set_capability('noReset', True)

    print("📱 핸드폰에서 인스타그램 앱을 실행하는 중...")
    # Appium 서버를 통해 핸드폰 구동 (Appium 서버가 켜져 있어야 합니다)
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

    try:
        # 억지로 실패를 유도하여 스크린샷이 찍히는지 확인하기 위해 False 설정
        logo_found = False

        print("🔎 화면에서 인스타그램 로고를 찾는 중...")

        # 🚨 여기서 무조건 실패(AssertionError)가 발생합니다!
        assert logo_found == True, "인스타그램 로고를 찾지 못했습니다."

        actual_status = "PASS"
    except AssertionError as e:
        actual_status = "FAIL"

        # 📸 [핵심] 실패한 순간 핸드폰 화면을 그대로 캡처해서 저장합니다!
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/{my_tc_id}_failed.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 [시스템] 테스트 실패로 인해 실제 핸드폰 화면 캡처 완료! -> {screenshot_path}")

        # 에러를 pytest에 다시 던져서 최종 FAIL 처리가 되도록 합니다.
        raise e
    finally:
        # 테스트가 끝나면 제어권을 안전하게 종료합니다.
        driver.quit()

        # 최종 결과를 구글 시트에 전송합니다.
        report_test_result(
            tc_id=my_tc_id,
            priority="P1 (High)",
            pre_condition="인스타그램 앱 설치 상태",
            test_steps="1. 인스타 앱 실행 -> 2. 로고 검색",
            expected_result="메인 화면에 인스타 로고가 보여야 함",
            result=actual_status
        )