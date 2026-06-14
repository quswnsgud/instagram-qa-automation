# test_sample.py

# 함수의 괄호 안에 'driver'를 적어주면 conftest.py에 있는 driver 설정을 자동으로 땡겨옵니다.
def test_instagram_logo_check(driver):
    print("\n📱 인스타그램 앱을 실행하고 로고를 찾는 중...")

    logo_found = False  # 로고를 못 찾았다고 가정을 해봅시다 (실패 유도)

    # 로고가 무조건 True(발견됨)여야 합격이야!
    assert logo_found == True