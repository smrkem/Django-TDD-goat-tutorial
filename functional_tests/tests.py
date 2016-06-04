from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        todo_table = self.browser.find_element_by_id('id_list_table')
        rows = todo_table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jenn goes to the to-do app homepage
        self.browser.get(self.live_server_url)

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

        self.check_for_row_in_list_table('1. Buy peacock feathers')

        # There is still a text box inviting her to add another item
        # She enters "Make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, showing both items on her list
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        self.check_for_row_in_list_table('2. Make a fly')

        # There is explanatory text letting Jenn know her list will be available at a generated URL

        # She visits that URL and her list is there.

        self.fail('Finish me...')
        # Happy

