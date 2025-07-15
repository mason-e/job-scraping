import os
from helpers.job_base import JobBase as Parent


class LinkedIn(Parent):
    RESULT_XPATH = "//div[contains(@class, 'job-card-container relative job-card-list')]"
    TITLE_XPATH = ".//div[contains(@class, 'lockup__title')]"
    COMPANY_XPATH = ".//div[contains(@class, 'lockup__subtitle')]"
    LOCATION_XPATH = ".//div[contains(@class, 'lockup__caption')]"
    NEXT_XPATH = "//button[contains(@class, 'button--next')]"
    LINK_XPATH = ".//a[contains(@class, 'container__link')]"
    URL = "https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=90000034&keywords=Software%20Engineer&location=Denver%20Metropolitan%20Area"
    SOURCE = "LinkedIn"
    AUTH_URL = "https://www.linkedin.com/login"
    AUTH_USER = os.getenv('LinkedInUser')
    AUTH_PASS = os.getenv('LinkedInPassword')
    AUTH_USER_XPATH = "//input[@id='username']"
    AUTH_PASS_XPATH = "//input[@id='password']"
    AUTH_SUBMIT_XPATH = "//button[@type='submit']"
    

linkedIn = LinkedIn()
linkedIn.pre_authenticate()
linkedIn.load_job_url()
linkedIn.scroll_results()
linkedIn.get_results_by_card()
linkedIn.write_to_db()
