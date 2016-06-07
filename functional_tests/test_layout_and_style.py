from .base import FunctionalTest


class LayoutAndStyleTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Jenn goes to the home page
        self.browser.get(self.server_url)
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
