import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramLoginPage:
    def __init__(self, driver):
        """Appium 드라이버를 받아와서 클래스 내부에서 쓸 수 있게 저장합니다."""
        self.driver = driver
        # 최대 15초 동안 화면 요소를 기다려줄 대기 객체를 생성합니다.
        self.wait = WebDriverWait(self.driver, 15)

        # 화면 요소들의 주소(Locator)
        self.username_input = (By.XPATH, '//android.widget.EditText[contains(@content-desc, "사용자 이름")]')
        self.password_input = (By.XPATH, '//android.widget.EditText[contains(@content-desc, "비밀번호")]')
        self.login_button = (By.XPATH, '//android.widget.Button[contains(@content-desc, "로그인")]')

    def enter_username(self, username):
        """아이디를 입력하는 기능 (동적 대기 적용)"""
        # 1. 아이디 입력창이 화면에 나타날 때까지 최대 15초 동안 똑똑하게 기다립니다.
        element = self.wait.until(EC.presence_of_element_located(self.username_input))
        element.click()
        time.sleep(1)
        element.send_keys(username)
        print(f"▶️ 아이디 입력 완료: {username}")

    def enter_password(self, password):
        """비밀번호를 입력하는 기능 (동적 대기 적용)"""
        # 2. 비밀번호 입력창이 나타날 때까지 기다립니다.
        element = self.wait.until(EC.presence_of_element_located(self.password_input))
        element.click()
        time.sleep(1)
        element.send_keys(password)
        print("▶️ 비밀번호 입력 완료")

    def click_login(self):
        """로그인 버튼을 누르는 기능 (동적 대기 적용)"""
        # 3. 로그인 버튼이 클릭할 수 있는 상태가 될 때까지 기다립니다.
        element = self.wait.until(EC.element_to_be_clickable(self.login_button))
        element.click()
        print("▶️ 로그인 버튼 클릭 완료")
        time.sleep(7)