import pytest
from sql_helper import SqlDB
from job_entry import JobEntry
   
database = SqlDB()

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    pass
    yield
    _cleanup_test_data()

def _cleanup_test_data():
    conn = database.connect_db()
    try:
        db_cursor = conn.cursor()
        db_cursor.execute("DELETE FROM dbo.JobSearchResults WHERE [Source] = 'Test'")
        conn.commit()
        conn.close()
    except Exception as error:
        # always close
        conn.close()
        raise error
    
def _seed_test_data(script):
    conn = database.connect_db()
    try:
        db_cursor = conn.cursor()
        db_cursor.execute(script)
        conn.commit()
        conn.close()
    except Exception as error:
        # always close
        conn.close()
        raise error

def test_convert_entries_to_sql_script():
    entries = [
        JobEntry("Test job 1", "Test company 1", "Test location 1", "Test link 1"),
        JobEntry("Test job 2", "Test company 2", "Test location 2", "Test link 2")
    ]
    
    script = database._make_create_script(entries, "Test")
    assert script == "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Test job 1', 'Test company 1', 'Test location 1', 'Test link 1', 'Test', GETDATE()),\n('Test job 2', 'Test company 2', 'Test location 2', 'Test link 2', 'Test', GETDATE())"

def test_escapes_single_quotes():
    entries = [
        JobEntry("Don't break stuff", "Aren't quotes dangerous", "It'll be fine", "Here's a link")
    ]
    script = database._make_create_script(entries, "Test")
    assert script == "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Don''t break stuff', 'Aren''t quotes dangerous', 'It''ll be fine', 'Here''s a link', 'Test', GETDATE())"

def test_duplicate_entries_same_day():
    entries = [
        JobEntry("Software Engineer", "Redundinc", "Everywhere", "link1"),
        JobEntry("Software Engineer", "Redundinc", "Nowhere", "link2")
    ]
    database.write_to_db(entries, "Test")
    # todo: read entries, verify only one ... always the link1 one?

def test_duplicate_entries_prior_day():
    # todo: dynamic yesterday date? or who cares
    script = "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Software Engineer', 'Redundinc', 'Somewhere', 'oldlink', 'Test', '2025-05-27')"
    _seed_test_data(script)
    entries = [
        JobEntry("Software Engineer", "Redundinc", "Anywhere", "link2")
    ]
    database.write_to_db(entries, "Test")
    # todo: read entries, verify only the oldlink

def test_blocked_entries_name_not_saved():
    # todo: add test company name and job title to actual DB, make a "control" that does save
    pass