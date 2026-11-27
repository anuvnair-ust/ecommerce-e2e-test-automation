from pages.base_page import BasePage


class CartModal(BasePage):

    def __init__(self, page):
        self.page = page
        self.modal = page.locator("#cartModal")
        self.message = page.locator("#cartModal .modal-body")
        self.view_cart_link = page.locator('#cartModal a[href="/view_cart"]')
        self.continue_button = page.locator("#cartModal button.close-modal")

    def wait_until_visible(self):
        self.modal.wait_for(state="visible", timeout=10000)

    def view_cart(self):
        self.click_and_wait(self.view_cart_link)
        

    def continue_shopping(self):
        self.continue_button.click()
        self.modal.wait_for(state="hidden", timeout=10000)
