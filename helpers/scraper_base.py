from selenium import webdriver
import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class ScraperBase:
    browser = webdriver.Chrome()

    def __init__(self):
        self.browser.maximize_window()

    def __del__(self):
        self.browser.close()

    def load_page(self, url):
        self.browser.get(url)

    def delay(self, seconds):
        seconds += random.randint(0, 2)
        sleep(seconds)

    def complete_auth(self, username, password, user_xpath, pass_xpath, submit_xpath):
        self.browser.find_element(By.XPATH, user_xpath).send_keys(username)
        self.browser.find_element(By.XPATH, pass_xpath).send_keys(password)
        self.browser.find_element(By.XPATH, submit_xpath).click()
        self.delay(2)

    def get_text(self, element):
        text = element.text
        text = text.replace("  ", "")
        return text.replace("\n", "")

    def get_link(self, element):
        return element.get_attribute('href')

    def is_present(self, xpath):
        return len(self.browser.find_elements(By.XPATH, xpath)) > 0

    def click_next(self, next_xpath):
        self.delay(1)
        if self.is_present(next_xpath):
            next_button = self.browser.find_element(By.XPATH, next_xpath)
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
            self.delay(2)
            try:
                next_button.click()
            except ElementClickInterceptedException:
                # sometimes the element is there but fails to click - catch exception
                # so we can at least get up to current page of results; this also helps if
                # the site disables the button on the last page rather than remove it
                return False
            self.delay(2)
            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()  # in case of pop-ups
            return True
        return False

    def scroll_results(self):
        # for scrolling results rather than paginated - scroll to bottom until it stops loading more results
        self.delay(2)
        webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()  # in case of pop-ups
        self.delay(1)
        latest_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:
            webdriver.ActionChains(self.browser).send_keys(Keys.END).perform()
            self.delay(3)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == latest_height:
                break
            latest_height = new_height

    def get_text_results(self, result_xpath):
        return self.get_all_results(result_xpath, self.get_text)

    def get_text_with_validation(self, parent_element, result_xpath):
        try:
            element = parent_element.find_element(By.XPATH, result_xpath)
        except NoSuchElementException:
            return 'Unknown'
        if element:
            text = self.get_text(element)
            if text != '':
                return text
            else:
                return 'Unknown'

    def get_link_with_validation(self, parent_element, result_xpath):
        try:
            element = parent_element.find_element(By.XPATH, result_xpath)
        except NoSuchElementException:
            return ''
        if element:
            # split off if there is a ? in the link since it is usually unnecessary afterwards
            return self.get_link(element).split('?', 1)[0]

    def get_link_results(self, result_xpath):
        return self.get_all_results(result_xpath, self.get_link)

    def get_all_results(self, result_xpath, method):
        results = self.browser.find_elements(By.XPATH, result_xpath)
        result_list = []
        for result in results:
            text = method(result)
            if text != "":
                result_list.append(text)
            else:
                result_list.append("UNKNOWN")
        return result_list





