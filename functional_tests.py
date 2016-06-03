import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jenn goes to the to-do app homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mentions To-Dos
        self.assertIn('To-Do Lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates showing
        # "1. Buy peacock feathers" as a to-do item
        inputbox.send_keys(Keys.ENTER)

        todo_table = self.browser.find_element_by_id('id_list_table')
        rows = todo_table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Buy peacock feathers' for row in rows)
        )

        # There is still a text box inviting her to add another item
        # She enters "Make a fly"

        # The page updates again, showing both items on her list

        # There is explanatory text letting Jenn know her list will be available at a generated URL

        # She visits that URL and her list is there.

        self.fail('Finish me...')
        # Happy

if __name__ == '__main__':
    unittest.main(warnings='ignore')
