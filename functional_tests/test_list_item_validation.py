from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Jenn goes to the homepage and accidentally submits an empty list item.
        # She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "List items can't be empty")

        # She tries again with some text for the new item, which now works.
        self.get_item_input_box().send_keys('some to-do item\n')
        self.check_for_row_in_list_table('1. some to-do item')

        # She decides to check if she can submit another blank item on the list page
        self.get_item_input_box().send_keys('\n')

        # Where she recieves a similar error
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "List items can't be empty")

        # And she corrects it by filling in some text
        self.get_item_input_box().send_keys('another to-do item\n')
        self.check_for_row_in_list_table('1. some to-do item')
        self.check_for_row_in_list_table('2. another to-do item')

    def test_cannot_add_duplicate_item(self):
        # Jenn starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Start using real items\n')
        self.check_for_row_in_list_table('1. Start using real items')

        # She accidentally enters a duplicate item
        self.get_item_input_box().send_keys('Start using real items\n')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1. Start using real items')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "List item already exists in your list")