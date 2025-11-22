from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestPlaylist(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=options)

    def test_songs_present(self):
        driver = self.driver

        # Your Dev cluster IP — KEEP AS IS
        driver.get("http://10.48.229.152/playlist")

        # Wait for main table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        page = driver.page_source

        # Check for 10 test songs
        for i in range(10):
            title = f"Test Song {i}"
            artist = f"Test Artist {i}"
            assert title in page, f"Song '{title}' not found!"
            assert artist in page, f"Artist '{artist}' not found!"

        print("✔ All test songs verified!")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
