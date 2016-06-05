from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):

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

        # When she hits enter, she is taken to a new URL,
        # and the page lists "1. Buy peacock feathers" as a to-do item
        inputbox.send_keys(Keys.ENTER)
        jenn_list_url = self.browser.current_url
        self.assertRegex(jenn_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Buy peacock feathers')

        # There is still a text box inviting her to add another item
        # She enters "Make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
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
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        # Jenn starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
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

    def test_layout_and_styling(self):
        # Jenn goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # And sees it is nicely styled
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # She starts a new list and sees the list page is also nicely styled
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        ## todo: verify local static style.css
        # self.assertAlmostEqual(inputbox.size['width'], 220, delta=10)


