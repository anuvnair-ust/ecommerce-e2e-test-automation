from pages.base_page import BasePage


class AccountPage(BasePage):
    path = "/signup"

    def __init__(self, page):
        self.page = page
        self.gender_mr = page.locator("#id_gender1")
        self.gender_mrs = page.locator("#id_gender2")

        self.name = page.locator("#name")
        self.email = page.locator("#email")
        self.password = page.locator("#password")

        self.birth_day = page.locator("#days")
        self.birth_month = page.locator("#months")
        self.birth_year = page.locator("#years")

        self.newsletter = page.locator("#newsletter")
        self.offers = page.locator("#optin")

        self.first_name = page.locator("#first_name")
        self.last_name = page.locator("#last_name")
        self.company = page.locator("#company")
        self.address1 = page.locator("#address1")
        self.address2 = page.locator("#address2")
        self.country = page.locator("#country")
        self.state = page.locator("#state")
        self.city = page.locator("#city")
        self.zipcode = page.locator("#zipcode")
        self.mobile_number = page.locator("#mobile_number")        
        self.create_button = page.locator('[data-qa="create-account"]')
        
        self.account_created = page.locator('[data-qa="account-created"]')
        self.continue_button = page.locator('[data-qa="continue-button"]')

    def fill_form(self, user):

        if user.title == "Mrs":
            self.gender_mrs.check()
        else:
            self.gender_mr.check()


        self.password.fill(user.password)
        self.birth_day.select_option(user.birth_day)
        self.birth_month.select_option(label=_month_name(user.birth_month))
        self.birth_year.select_option(user.birth_year)
        self.newsletter.check()
        self.offers.check()
        self.first_name.fill(user.first_name)
        self.last_name.fill(user.last_name)
        self.company.fill(user.company)
        self.address1.fill(user.address1)
        self.address2.fill(user.address2)
        self.country.select_option(user.country)
        self.state.fill(user.state)
        self.city.fill(user.city)
        self.zipcode.fill(user.zipcode)
        self.mobile_number.fill(user.mobile_number)

    def submit(self):
        self.click_and_wait(self.create_button)

    def continue_after_creation(self):
        self.click_and_wait(self.continue_button)




_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _month_name(month_number):
    return _MONTHS[int(month_number) - 1]
