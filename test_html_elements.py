from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestPlaylist(unittest.TestCase):

    def setUp(self):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=opts)

    def test_playlist(self):
        driver = self.driver

        # CHANGE THIS TO YOUR DEV IP
        driver.get("http://10.48.229.152/playlist")

        # Wait until the table loads
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Check for the 10 generated test songs
        for i in range(10):
            title = f"Test Song {i}"
            artist = f"Artist {i}"

            page = driver.page_source

            assert title in page, f"Song title {title} not found"
            assert artist in page, f"Artist {artist} not found"

        print("Playlist test passed — all songs verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

