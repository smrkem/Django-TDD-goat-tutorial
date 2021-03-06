from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jenn goes to the to-do app homepage
        self.browser.get(self.server_url)

        # She notices the page title and header mentions To-Dos
        self.assertIn('To-Do Lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, she is taken to a new URL,
        # and the page lists "1. Buy peacock feathers" as a to-do item
        inputbox.send_keys(Keys.ENTER)
        jenn_list_url = self.browser.current_url
        self.assertRegex(jenn_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Buy peacock feathers')

        # There is still a text box inviting her to add another item
        # She enters "Make a fly"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, showing both items on her list
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        self.check_for_row_in_list_table('2. Make a fly')

        # Now a new user, Fran comes along to the site.

        ## New browser session to isolate Fran #
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Fran visits the home page. There is no sign of Jenn's list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        # Jenn starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Fran gets her own unique URL
        fran_list_url = self.browser.current_url
        self.assertRegex(fran_list_url, '/lists/[0-9]+')
        self.assertNotEqual(jenn_list_url, fran_list_url)

        # Still there is no trace of Jenn's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Happy


