import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


# =====================================================================
# 📦 [과거 백업] 리포팅/가상 테스트용 FakeDriver (필요할 때 주석을 풀어 사용하세요)
# =====================================================================
# @pytest.fixture(scope="function")
# def driver():
#     class FakeDriver:
#         def save_screenshot(self, path):
#             with open(path, "w") as f:
#                 f.write("fake_screenshot_data")
#             print(f"\n📸 [시스템] 실제 screenshots 폴더에 {path} 파일 생성 완료!")
#
#     yield FakeDriver()
# =====================================================================


# =====================================================================
# 📱 [현재 사용] 실제 새 단말기(Galaxy) 연결용 Appium 드라이버
# =====================================================================
@pytest.fixture(scope="function")
def driver():
    # 📍 깃허브 액션 환경(CI)인지 확인하여 가상 서버 환경이면 테스트를 건너뜁니다.
    if os.getenv("CI") == "true":
        pytest.skip("깃허브 액션 환경에서는 Appium 서버 연결을 건너뜁니다.")

    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'

    # 📍 오늘 확인 완료한 새 기기 ID (반영 완료)
    options.device_name = 'R3KL106Z49W'

    # 📍 [여기만 수정!] 본인 핸드폰의 안드로이드 버전 숫자를 적어주세요 (예: '13' 또는 '14')
    options.platform_version = '16'

    # 인스타그램 앱 설정
    options.app_package = 'com.instagram.android'
    options.app_activity = 'com.instagram.mainactivity.MainActivity'
    options.no_reset = True

    # 로컬 Appium 서버에 연결 (Appium v2 기준 기본 주소)
    real_driver = webdriver.Remote('http://localhost:4723', options=options)

    yield real_driver

    # 테스트 완료 후 드라이버 종료
    real_driver.quit()