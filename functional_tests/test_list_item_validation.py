from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_item(self):
        # Jenn goes to the homepage and accidentally submits an empty list item.
        # She hits Enter on the empty input box

        # The home page refreshes, and there is an error message saying that
        # list items cannot be blank.

        # She tries again with some text for the new item, which now works.

        # She decides to check if she can submit another blank item on the list page

        # Where she recieves a similar error

        # And she corrects it by filling in some text
        self.fail("Write me!")
