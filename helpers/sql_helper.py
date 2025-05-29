import pyodbc

class SqlDB():
    # DB constants
    SERVER_NAME = "Macetop"
    DATABASE_NAME = "MasonDB"
    CLEANUP_PATH = "./remove_unwanted.sql"
    
    def _connect_db(self):
        return pyodbc.connect("Driver={SQL Server};"
                        "Server=" + self.SERVER_NAME + ";"
                        "Database=" + self.DATABASE_NAME + ";"
                        "Trusted_Connection=yes;")
    
    def execute_script(self, script):
        conn = self._connect_db()
        try:
            db_cursor = conn.cursor()
            if script.startswith("SELECT"):
                result = db_cursor.execute(script).fetchall()
            else:
                db_cursor.execute(script)
                result = "Non-select was executed"
            conn.commit()
            conn.close()
            return result
        except Exception as error:
            # always attempt to close the connection even if something fails here
            conn.close()
            raise error 

    def execute_cleanup(self):
        with open(self.CLEANUP_PATH) as f:
            self.execute_script(f.read())               
    