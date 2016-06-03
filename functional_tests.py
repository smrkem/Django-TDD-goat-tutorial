import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jenn goes to the to-do app homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title mentions To-Dos
        self.assertIn('To-Do Lists', self.browser.title)
        self.fail('Finish me...')

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box

        # When she hits enter, the page updates showing
        # "1. Buy peacock feathers" as a to-do item

        # There is still a text box inviting her to add another item
        # She enters "Make a fly"

        # The page updates again, showing both items on her list

        # There is explanatory text letting Jenn know her list will be available at a generated URL

        # She visits that URL and her list is there.

        # Happy

if __name__ == '__main__':
    unittest.main(warnings='ignore')
