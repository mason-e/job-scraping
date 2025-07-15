# mostly deprecated - should work in theory if you aren't auth blocked, but I usually get auth blocked now :(

from helpers.job_base import JobBase as Parent


class LinkedIn(Parent):
    RESULT_XPATH = "//div[contains(@class, 'base-card')]"
    TITLE_XPATH = ".//h3[contains(@class, 'base-search-card')]"
    COMPANY_XPATH = ".//h4[contains(@class, 'base-search-card')]"
    LOCATION_XPATH = ".//span[contains(@class, 'location')]"
    NEXT_XPATH = "//button[@class='see-more-jobs']"
    LINK_XPATH = ".//a[contains(@class, 'base-card__full-link')]"
    URL = "https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=90000034&keywords=Software%20Engineer&location=Denver%20Metropolitan%20Area"
    SOURCE = "LinkedIn"

linkedIn = LinkedIn()
linkedIn.load_job_url()
linkedIn.scroll_results()
linkedIn.get_results_by_card()
linkedIn.write_to_db()
