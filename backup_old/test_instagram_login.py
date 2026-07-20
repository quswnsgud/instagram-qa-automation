import os
import time
import warnings
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from appium import webdriver
from appium.options.common import AppiumOptions
from selenium.webdriver.common.by import By

warnings.filterwarnings("ignore", category=FutureWarning)
load_dotenv()

# 구글 시트 연동 설정 (기존 설정 유지)
CRED_PATH_FROM_ENV = os.getenv("GOOGLE_CRED_PATH")
PATH_A = f"{CRED_PATH_FROM_ENV}.json" if CRED_PATH_FROM_ENV else ""
FINAL_CRED_PATH = PATH_A if (PATH_A and os.path.exists(PATH_A)) else CRED_PATH_FROM_ENV

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(FINAL_CRED_PATH, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("인스타그램자동화 시트")
    sheet = spreadsheet.get_worksheet(0)
except Exception as e:
    print(f"❌ 구글 시트 연결 실패: {e}")


def report_test_result(tc_id, expected_result, result):
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
                sheet.update_cell(target_row, 2, "인스타 로그인 기능 검증")
                sheet.update_cell(target_row, 3, expected_result)
                sheet.update_cell(target_row, 9, result)
                sheet.update_cell(target_row, 10, f"[{result}] {current_time}")
                print(f"🟢 구글 시트 [{target_row}행]에 반영 성공!")
        except Exception as e:
            print(f"🔴 구글 시트 입력 에러: {e}")


# ==========================================
# 🎯 [TC_002] 인스타그램 로그인 입력 및 클릭 테스트
# ==========================================
def test_instagram_login_process():
    print("\n▶️ [테스트 시작] 인스타그램 로그인 기능 검증")

    my_tc_id = "TC_002"  # 👈 7행(TC_002)에 저장됩니다!

    options = AppiumOptions()
    options.set_capability('platformName', 'Android')
    options.set_capability('automationName', 'UiAutomator2')
    options.set_capability('appPackage', 'com.instagram.android')
    options.set_capability('dontStopAppOnReset', True)
    options.set_capability('noReset', True)

    print("📱 핸드폰에서 인스타그램 앱을 실행하는 중...")
    driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

    actual_status = "FAIL"
    try:
        # --------------------------------------------------
        # 🚀 [진짜 자동화 동작 부분] 아이디/비번 입력 및 로그인 클릭
        # --------------------------------------------------
        print("💡 앱 진입 완료 - 화면 요소를 찾는 중...")
        time.sleep(5)  # 로그인 화면이 완전히 로딩될 때까지 5초 대기

        # 1. 사용자 이름(아이디) 입력창 찾아서 클릭하고 글자 타이핑하기
        username_xpath = '//android.widget.EditText[@content-desc="사용자 이름, 이메일 주소 또는 휴대폰 번호,"]'
        username_field = driver.find_element(By.XPATH, username_xpath)
        username_field.click()
        time.sleep(1)
        username_field.send_keys("내_인스타_진짜_아이디")  # 👈 ⚠️ 여기에 본인 인스타 아이디 적기!
        print("▶️ 아이디 입력 완료")
        time.sleep(1)

        # 2. 비밀번호 입력창 찾아서 클릭하고 글자 타이핑하기
        password_xpath = '//android.widget.EditText[@content-desc="비밀번호,"]'
        password_field = driver.find_element(By.XPATH, password_xpath)
        password_field.click()
        time.sleep(1)
        password_field.send_keys("내_인스타_진짜_비밀번호")  # 👈 ⚠️ 여기에 본인 인스타 비밀번호 적기!
        print("▶️ 비밀번호 입력 완료")
        time.sleep(1)

        # 3. 로그인 버튼 찾아서 마우스 클릭하기
        login_btn_xpath = '//android.widget.Button[@content-desc="로그인"]/android.view.ViewGroup'
        login_button = driver.find_element(By.XPATH, login_btn_xpath)
        login_button.click()
        print("▶️ 로그인 버튼 클릭 완료")

        # 로그인 시도 후 화면이 넘어가거나 로딩되는 시간을 고려해 대기
        time.sleep(7)

        # 여기까지 에러 없이 통과했다면 성공 처리
        actual_status = "PASS"

    except Exception as e:
        actual_status = "FAIL"
        os.makedirs("../screenshots", exist_ok=True)
        driver.save_screenshot(f"screenshots/{my_tc_id}_failed.png")
        print(f"📸 [시스템] 테스트 실패 스크린샷 저장 완료")
        raise e
    finally:
        driver.quit()
        report_test_result(
            tc_id=my_tc_id,
            expected_result="아이디/비번 입력 후 로그인 시도가 정상적으로 되어야 함",
            result=actual_status
        )