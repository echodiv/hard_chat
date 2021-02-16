from pages.base_page import BasePage


class RegisterPage(BasePage):
    '''
    Describe registration page of hard_chat

    Contain registration form:
    - register:
      - name
      - sename
      - email
      - password
      - repeat password
      - phone number
    '''
    
    def go_to_registration_page(self):
        link = self.browser.find_element(By.CSS_SELECTOR, '#registration_link')
        link.click()