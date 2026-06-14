# conftest.py
import os
import pytest
from instagram_tc_test import report_test_result


@pytest.fixture(scope="function")
def driver():
    class FakeDriver:
        def save_screenshot(self, path):
            with open(path, "w") as f:
                f.write("fake_screenshot_data")
            print(f"\n📸 [시스템] 실제 screenshots 폴더에 {path} 파일 생성 완료!")

    yield FakeDriver()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        result_status = "PASS" if report.passed else "FAIL"

        if result_status == "FAIL":
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.name}_failed.png"

            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                driver.save_screenshot(screenshot_path)

        print(f"\n📢 [리포팅] {item.name} 테스트 결과를 구글 시트와 노션으로 자동 전송합니다...")

        report_test_result(
            row_num=6,
            tc_id=item.name,
            priority="P1 (High)",
            pre_condition="유효한 테스트 계정 로그인 상태",
            test_steps="pytest를 통한 자동화 검증 수행",
            expected_result="새로 고침이 정상 적으로 됨",
            result=result_status
        )