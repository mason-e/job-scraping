import pyodbc

class SqlDB():
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
    
    def connect_db(self):
        return pyodbc.connect("Driver={SQL Server};"
                        "Server=" + self.SERVER_NAME + ";"
                        "Database=" + self.DATABASE_NAME + ";"
                        "Trusted_Connection=yes;")
    
    def write_to_db(self, entries, source):
        conn = self.connect_db()
        try:
            db_cursor = conn.cursor()
            script = self.SCRIPT
            first_entry = True

            for entry in entries:
                if not first_entry:
                    script += ", \n"

                script += self.SCRIPT_VALUES.replace("@Title@", entry.title.replace("'", "''"))\
                    .replace("@Company@", entry.company.replace("'", "''"))\
                    .replace("@Location@", entry.location.replace("'", "''"))\
                    .replace("@Link@", entry.link.replace("'", "''"))\
                    .replace("@Source@", source)

                first_entry = False

            db_cursor.execute(script)
            db_cursor.execute(self.DUPLICATES)
            db_cursor.execute(self.BLACKLIST.replace("@BLType@", "Company"))
            db_cursor.execute(self.BLACKLIST.replace("@BLType@", "JobTitle"))
            conn.commit()
        except Exception:
            conn.close()
        conn.close()

    