from selenium.common.exceptions import NoSuchElementException



class BasePage(object):
    '''
    This class describe base structure of all web pages
    of hard_chat application
    '''
    def __init__(self, browser, url, timeout):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True