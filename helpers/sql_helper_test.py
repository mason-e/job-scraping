from datetime import date, timedelta
import pytest
from sql_helper import SqlDB
   
database = SqlDB()

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    pass
    yield
    _cleanup_test_data()

def _cleanup_test_data():
    database.execute_script("DELETE FROM dbo.JobSearchResults WHERE [Source] = 'Test'")

def _read_data(where_clause):
    return database.execute_script(f"SELECT * FROM dbo.JobSearchResults WHERE {where_clause}")

def test_add_entry():
    setup_script = "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Software Engineer', 'Fake Company', 'Remote', 'online', 'Test', GETDATE())"
    database.execute_script(setup_script)
    result = _read_data("[Company] = 'Fake Company'")
    assert len(result) == 1

def test_remove_duplicate_entries_same_day():
    setup_script = "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Software Engineer', 'Redundinc', 'Everywhere', 'link1', 'Test', GETDATE()),\n('Software Engineer', 'Redundinc', 'Nowhere', 'link2', 'Test', GETDATE())"
    database.execute_script(setup_script)
    database.execute_cleanup()
    result = _read_data("[Company] = 'Redundinc'")
    assert len(result) == 1
    assert "link1" in result[0]

def test_remove_duplicate_entries_prior_day():
    yesterday = date.today() - timedelta(days=1)
    setup_script = f"INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Software Engineer', 'Redundinc', 'Somewhere', 'oldlink', 'Test', '{yesterday}'),\n('Software Engineer', 'Redundinc', 'Somewhere', 'newlink', 'Test', GETDATE())"
    database.execute_script(setup_script)
    database.execute_cleanup()
    result = _read_data("[Company] = 'Redundinc'")
    assert len(result) == 1
    assert "oldlink" in result[0]

def test_blocked_entries_case_insensitive_not_saved():
    # blocked values were added independently of the test
    # "Megacorp" for company and "pencil pusher" for title
    setup_script = "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Software Engineer', 'MegaCorp', 'Remote', 'Link', 'Test', GETDATE()),\n('Pencil Pusher', 'somecompany', 'Remote', 'Link', 'Test', GETDATE()),\n('Standard Job', 'Control Entry', 'Remote', 'Link', 'Test', GETDATE())"
    database.execute_script(setup_script)
    database.execute_cleanup()
    result = _read_data("[Source] = 'Test'")
    assert len(result) == 1
    assert "Control Entry" in result[0]