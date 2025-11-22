from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestMusicPlaylist(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_playlist_page_loads(self):
        driver = self.driver

        # 1) Go to the home page (your ClusterIP)
        driver.get("http://10.48.229.152")  # your dev ClusterIP

        # 2) Make sure the home page text is present
        assert "My Music Playlist" in driver.page_source, "Home page did not load correctly"

        # 3) Click the "View My Playlist" button (link)
        view_button = driver.find_element(By.LINK_TEXT, "View My Playlist")
        view_button.click()
        time.sleep(1)  # small wait to let the page load

        # 4) Now check that the playlist page loaded
        assert "Add Song" in driver.page_source, "Playlist page did not show the Add Song form"
        assert "All Songs" in driver.page_source, "Playlist listing did not appear"

        print("✔ Selenium test passed: playlist pages load correctly.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

