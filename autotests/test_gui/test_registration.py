from pages.auth.registration import RegisterPage

def test_guest_can_go_to_registration_page(browser):
    link = "http://localhost:5000/"
    page = MainPage(browser, link)
    page.open()
    page.go_to_registration_page()