from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
import time


class LoginTest(FunctionalTest):

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n{}'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('Could not find window')

    def wait_to_be_logged_in(self):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('jenn@mockmyid.com', navbar.text)

    def wait_to_be_logged_out(self):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn('jenn@mockmyid.com', navbar.text)

    def test_login_with_persona(self):
        # Jenn goes to the superlists site and sees a "Sign in" link
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A Persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Jenn logs in with her email address
        ## Use mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email').send_keys('jenn@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()

        # The Persona window closes
        self.switch_to_new_window('To-Do')

        # She can see that she is logged in
        self.wait_to_be_logged_in()

        # Refreshing the page, she sees she is still logged in
        self.browser.refresh()
        self.wait_to_be_logged_in()

        # She's had enough and clicks "logout"
        ## Need to pause for a second before clicking?
        time.sleep(1)
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out()

        # Refreshing the page again, she sees she is still logged out
        self.browser.refresh()
        self.wait_to_be_logged_out()

