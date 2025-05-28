import pyodbc

class SqlDB():
    # DB constants
    SERVER_NAME = "Macetop"
    DATABASE_NAME = "MasonDB"
    CLEANUP_PATH = "./remove_unwanted.sql"
    SCRIPT_PREFIX = '''INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date])
        VALUES'''
    
    def connect_db(self):
        return pyodbc.connect("Driver={SQL Server};"
                        "Server=" + self.SERVER_NAME + ";"
                        "Database=" + self.DATABASE_NAME + ";"
                        "Trusted_Connection=yes;")
    
    def write_to_db(self, entries, source):
        conn = self.connect_db()
        try:
            db_cursor = conn.cursor()
            script = self.SCRIPT_PREFIX

            for entry in entries:
                script +=  f"('{entry.title}', '{entry.company}', '{entry.location}', '{entry.link}', '{source}', GETDATE()),\n"

            # remove last comma from final entry
            script = script[:-2]

            db_cursor.execute(script)
            # clean up unwanted entries
            with open(self.CLEANUP_PATH) as f:
                db_cursor.execute(f.read())
            conn.commit()
        except Exception as error:
            # always attempt to close the connection even if something fails here
            conn.close()
            raise error
        conn.close()

    