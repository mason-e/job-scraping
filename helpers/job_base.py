from helpers.job_entry import JobEntry
from helpers import query_helper, sql_helper
from helpers.scraper_base import ScraperBase as Parent
from selenium.webdriver.common.by import By


class JobBase(Parent):
    # constants to be defined by implementations of this class for a specific site
    RESULT_XPATH = ""
    TITLE_XPATH = ""
    COMPANY_XPATH = ""
    LOCATION_XPATH = ""
    NEXT_XPATH = ""
    LINK_XPATH = ""
    URL = ""
    SOURCE = ""
    # only need to be used if user authentication is required to see results
    AUTH_URL = ""
    AUTH_USER = ""
    AUTH_PASS = ""
    AUTH_USER_XPATH = ""
    AUTH_PASS_XPATH = ""
    AUTH_SUBMIT_XPATH = ""
    # lists for intermediate storage of results
    entries = []
    titles = []
    companies = []
    locations = []
    links = []

    def load_job_url(self):
        self.load_page(self.URL)

    def pre_authenticate(self):
        self.load_page(self.AUTH_URL)
        self.complete_auth(self.AUTH_USER, self.AUTH_PASS, self.AUTH_USER_XPATH, self.AUTH_PASS_XPATH, self.AUTH_SUBMIT_XPATH)

    def get_results_by_card(self):
        # method for getting all key info off of a single result "card" in the DOM
        results = self.browser.find_elements(By.XPATH, self.RESULT_XPATH)
        for result in results:
            title = self.get_text_with_validation(result, self.TITLE_XPATH)
            company = self.get_text_with_validation(result, self.COMPANY_XPATH)
            location = self.get_text_with_validation(result, self.LOCATION_XPATH)
            link = self.get_link_with_validation(result, self.LINK_XPATH)
            self.entries.append(JobEntry(title, company, location, link))
        if self.click_next(self.NEXT_XPATH):
            self.get_results_by_card()

    def write_to_db(self):
        database = sql_helper.SqlDB()
        queries = query_helper.QueryHelpers()
        script = queries.make_create_script(self.entries, self.SOURCE)
        database.execute_script(script)
        database.execute_cleanup()
