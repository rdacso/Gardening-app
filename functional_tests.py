from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser = webdriver.Chrome("/Users/rdacso/src/gardening/chromedriver")
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertIn('Green Light', self.browser.title)

    # def test_access_registration_page(self):

if __name__ == "__main__":
    unittest.main()