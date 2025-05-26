from JobBase import JobBase as Parent


class BuiltIn(Parent):
    RESULT_XPATH = "//div[@id='main'][@class='row']"
    LINK_XPATH = "//a[@data-id='job-card-title']"
    TITLE_XPATH = "//a[@data-id='job-card-title']"
    COMPANY_XPATH = "//a[@data-id='company-title']"
    LOCATION_XPATH = "unknown" # location selectors are too generic to use
    NEXT_XPATH = "//i[contains(@class, 'fa-chevron-right')]//parent::a"
    URL = "https://www.builtincolorado.com/jobs/remote/hybrid/office/dev-engineering?search=software+engineer&daysSinceUpdated=7&state=Colorado&country=USA&allLocations=true"
    SOURCE = "BuiltInColorado"


builtIn = BuiltIn(BuiltIn.URL)

builtIn.get_results()
builtIn.make_entries()

builtIn.write_to_db()