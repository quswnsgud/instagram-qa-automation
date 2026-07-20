import pytest
import os
import time
from pages.login_page import InstagramLoginPage
from config.reporter import report_test_result


def test_instagram_login_flow(driver):
    """
    [TC_001] 인스타그램 로그인 및 대시보드 진입 테스트
    """
    tc_id = "TC_001"
    priority = "High"
    pre_condition = "인스타그램 앱 설치 및 실행 상태"
    test_steps = "1. 아이디 입력\n2. 비밀번호 입력\n3. 로그인 버튼 클릭"
    expected_result = "로그인이 성공하여 홈 피드가 정상적으로 표시되어야 함"

    # 1. 분리해 둔 페이지 객체(POM)를 가져옵니다.
    login_page = InstagramLoginPage(driver)

    try:
        # 2. 한글 소설을 읽듯이 아주 직관적으로 동작을 수행합니다.
        # 기존의 복잡한 find_element 코드가 사라져서 보기 아주 편해졌습니다.
        login_page.enter_username("your_instagram_id")  # 실제 아이디 입력
        login_page.enter_password("your_instagram_pw")  # 실제 비밀번호 입력
        login_page.click_login()

        # 3. 로그인 성공 후 결과 기록
        report_test_result(
            tc_id=tc_id,
            priority=priority,
            pre_condition=pre_condition,
            test_steps=test_steps,
            expected_result=expected_result,
            result="PASS"
        )

    except Exception as e:
        print(f"❌ 테스트 실패 에러 발생: {e}")

        # 에러 발생 시 스크린샷 저장
        screenshot_dir = "screenshots"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, f"{tc_id}_failed.png")
        driver.save_screenshot(screenshot_path)
        print(f"📸 실패 스크린샷 저장 완료: {screenshot_path}")

        # 실패 결과 기록
        report_test_result(
            tc_id=tc_id,
            priority=priority,
            pre_condition=pre_condition,
            test_steps=test_steps,
            expected_result=expected_result,
            result="FAIL"
        )
        raise e  # pytest가 실패로 감지할 수 있도록 에러를 다시 던집니다.