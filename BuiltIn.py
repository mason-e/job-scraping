from helpers.job_base import JobBase as Parent


class BuiltIn(Parent):
    RESULT_XPATH = "//div[@id='main'][@class='row']"
    LINK_XPATH = ".//a[@data-id='job-card-title']"
    TITLE_XPATH = ".//a[@data-id='job-card-title']"
    COMPANY_XPATH = ".//a[@data-id='company-title']"
    # below is fragile, but works; get the text that's a "cousin" of the location pin image
    LOCATION_XPATH = ".//i[contains(@class, 'fa-location-dot')]/../following-sibling::div/span"
    NEXT_XPATH = "//i[contains(@class, 'fa-chevron-right')]//parent::a"
    URL = "https://www.builtincolorado.com/jobs/remote/hybrid/office/dev-engineering?search=software+engineer&daysSinceUpdated=1&state=Colorado&country=USA&allLocations=true"
    SOURCE = "BuiltInColorado"


builtIn = BuiltIn()
builtIn.load_job_url()
builtIn.get_results_by_card()
builtIn.cleanup_unwanted()