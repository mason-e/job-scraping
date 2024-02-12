from JobBase import JobBase as Parent


class LinkedIn(Parent):
    RESULT_XPATH = "//div[contains(@class, 'base-card')]"
    TITLE_XPATH = ".//h3[contains(@class, 'base-search-card')]"
    COMPANY_XPATH = ".//h4[contains(@class, 'base-search-card')]"
    LOCATION_XPATH = ".//span[contains(@class, 'location')]"
    SUMMARY_XPATH = ".//p[contains(@class, 'snippet')]"
    NEXT_XPATH = "//button[@class='see-more-jobs']"
    LINK_XPATH = ".//a[contains(@class, 'base-card__full-link')]"
    URL = "https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=90000034&keywords=Software%20Engineer&location=" \
          "Denver%20Metropolitan%20Area"
    SOURCE = "LinkedIn"

    def advance_results(self):
        self.scroll_results()

    def get_results(self):
        self.advance_results()
        self.titles += self.get_text_results(self.TITLE_XPATH)
        self.companies += self.get_text_results(self.COMPANY_XPATH)
        self.locations += self.get_text_results(self.LOCATION_XPATH)
        self.summaries += self.get_text_results(self.TITLE_XPATH) # summaries currently not showing for all, quick hack to make list sizes equal
        self.links += self.get_link_results(self.LINK_XPATH)


linkedIn = LinkedIn(LinkedIn.URL)

linkedIn.get_scrolling_results(linkedIn.LINK_XPATH)

#linkedin.get_results()
#if linkedin.validate_results():
linkedIn.write_to_db_new()
