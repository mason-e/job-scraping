from JobEntry import JobEntry
from ScraperBase import ScraperBase as Parent
import pyodbc
from selenium.webdriver.common.by import By


class JobBase(Parent):
    # DB constants
    SERVER_NAME = "Macetop"
    DATABASE_NAME = "MasonDB"
    SCRIPT = '''INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date])
        VALUES'''
    SCRIPT_VALUES = "('@Title@', '@Company@', '@Location@', '@Link@', '@Source@', GETDATE())"
    BLACKLIST = '''DELETE T1
        FROM dbo.JobSearchResults AS T1
        INNER JOIN dbo.Blacklist@BLType@ As T2
        ON T1.[@BLType@] LIKE '%' + T2.[@BLType@] + '%' '''
    DUPLICATES = '''WITH CTE AS (SELECT [Company], [JobTitle], [Date], RN = 
        ROW_NUMBER() OVER(PARTITION BY [Company], [JobTitle] ORDER BY [Date] ASC) FROM [JobSearchResults])
        DELETE FROM CTE WHERE RN > 1;'''
    # constants to be defined by implementations of this class for a specific site
    RESULT_XPATH = ""
    TITLE_XPATH = ""
    COMPANY_XPATH = ""
    LOCATION_XPATH = ""
    NEXT_XPATH = ""
    URL = ""
    SOURCE = ""
    # lists for intermediate storage of results
    entries = []
    titles = []
    companies = []
    locations = []
    links = []


    def get_results_new(self, linkXpath):
        results = self.browser.find_elements(By.XPATH, self.RESULT_XPATH)
        for result in results:
            title = self.get_text_with_validation(result, self.TITLE_XPATH)
            company = self.get_text_with_validation(result, self.COMPANY_XPATH)
            location = self.get_text_with_validation(result, self.LOCATION_XPATH)
            link = self.get_link_with_validation(result, linkXpath)
            self.entries.append(JobEntry(title, company, location, link))

    def get_paginated_results(self, linkXpath):
        self.get_results_new(linkXpath)
        if self.click_next(self.NEXT_XPATH):
            self.get_paginated_results(linkXpath)

    def get_scrolling_results(self, linkXpath):
        self.scroll_results()
        self.get_results_new(linkXpath)

    def get_results(self):
        self.titles += self.get_text_results(self.TITLE_XPATH)
        self.companies += self.get_text_results(self.COMPANY_XPATH)
        # self.locations += self.get_text_results(self.LOCATION_XPATH)
        self.links += self.get_link_results(self.TITLE_XPATH)
        for title in self.titles:
            self.locations.append("Unknown")
        # if self.click_next(self.NEXT_XPATH):
        #     self.get_results()

    def make_entries(self):
        if self.validate_results():
            for (title, company, location, link) in zip(self.titles, self.companies, self.locations, self.links):
                self.entries.append(JobEntry(title, company, location, link))

    def validate_results(self):
        validation = len(self.titles) == len(self.companies) and \
                     len(self.companies) == len(self.locations)

        if not validation:
            print("Something wrong with results! Element sizes did not match.")
            print("Titles found: " + len(self.titles).__str__())
            print("Companies found: " + len(self.companies).__str__())
            print("Locations found: " + len(self.locations).__str__())
            print("Links found: " + len(self.links).__str__())

        return validation

    def connect_db(self):
        return pyodbc.connect("Driver={SQL Server};"
                              "Server=" + self.SERVER_NAME + ";"
                              "Database=" + self.DATABASE_NAME + ";"
                              "Trusted_Connection=yes;")

    def write_to_db(self):
        conn = self.connect_db()
        db_cursor = conn.cursor()
        script = self.SCRIPT
        first_entry = True

        for entry in self.entries:
            if not first_entry:
                script += ", \n"

            script += self.SCRIPT_VALUES.replace("@Title@", entry.title.replace("'", "''"))\
                .replace("@Company@", entry.company.replace("'", "''"))\
                .replace("@Location@", entry.location.replace("'", "''"))\
                .replace("@Link@", entry.link.replace("'", "''"))\
                .replace("@Source@", self.SOURCE)

            first_entry = False

        db_cursor.execute(script)
        db_cursor.execute(self.DUPLICATES)
        db_cursor.execute(self.BLACKLIST.replace("@BLType@", "Company"))
        db_cursor.execute(self.BLACKLIST.replace("@BLType@", "JobTitle"))
        conn.commit()
