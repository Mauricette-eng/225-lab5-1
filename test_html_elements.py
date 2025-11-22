from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestMusicPlaylist(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=options)

    def test_playlist_page_loads(self):
        driver = self.driver
        driver.get("http://10.48.229.152")  # your ClusterIP

        # Ensure homepage loads
        assert "Music Playlist" in driver.page_source, "Homepage did not load correctly"

        # Click "View Playlist" button
        view_button = driver.find_element(By.LINK_TEXT, "View Playlist")
        view_button.click()
        time.sleep(1)

        # Verify playlist page opens
        assert "My Music Playlist" in driver.page_source, "Playlist page did not load correctly"

        print("✔ Selenium test passed — playlist page loads correctly.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

