# conftest.py
import pytest

@pytest.fixture(scope="function")
def driver():
    class FakeDriver:
        def save_screenshot(self, path):
            with open(path, "w") as f:
                f.write("fake_screenshot_data")
            print(f"\n📸 [시스템] 실제 screenshots 폴더에 {path} 파일 생성 완료!")

    yield FakeDriver()