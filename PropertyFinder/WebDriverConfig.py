from selenium import webdriver
from config import executable_path

class WebDriverConfig:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("incognito")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--start-maximized")

        # Disable images
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.add_experimental_option("prefs", prefs)
        self.driver = self.get_driver()

    def get_driver(self):
        return webdriver.Chrome(executable_path=executable_path, options=self.options)

    @classmethod
    def create_and_get_driver(cls):
        return cls().driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()