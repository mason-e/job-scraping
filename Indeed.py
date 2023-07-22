from JobBase import JobBase as Parent


class Indeed(Parent):
    RESULT_XPATH = "//a[contains(@class, 'result job')]"
    TITLE_XPATH = ".//span[@title]"
    COMPANY_XPATH = ".//span[@class='companyName']"
    LOCATION_XPATH = ".//div[contains(@class, 'companyLocation')]"
    SUMMARY_XPATH = ".//div[@class='summary']"
    SALARY_XPATH = "//div[contains(@class, 'salary-snippet')]"
    NEXT_XPATH = "//a[@aria-label='Next']"
    URL = "https://www.indeed.com/jobs?as_and=engineer&jt=all&radius=50&l=Denver%2C+CO&fromage=1&limit=50&sort=&psf=advsrch"
    SOURCE = "Indeed"


indeed = Indeed(Indeed.URL)

indeed.get_paginated_results(Indeed.RESULT_XPATH)

#indeed.get_results()
#if indeed.validate_results():
#indeed.write_to_db_new()
