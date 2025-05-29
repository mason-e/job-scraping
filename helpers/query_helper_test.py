from query_helper import QueryHelpers
from job_entry import JobEntry

queries = QueryHelpers()

def test_convert_entries_to_sql_script():
    entries = [
        JobEntry("Test job 1", "Test company 1", "Test location 1", "Test link 1"),
        JobEntry("Test job 2", "Test company 2", "Test location 2", "Test link 2")
    ]
    
    script = queries.make_create_script(entries, "Test")
    assert script == "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Test job 1', 'Test company 1', 'Test location 1', 'Test link 1', 'Test', GETDATE()),\n('Test job 2', 'Test company 2', 'Test location 2', 'Test link 2', 'Test', GETDATE())"

def test_escapes_single_quotes():
    entries = [
        JobEntry("Don't break stuff", "Aren't quotes dangerous", "It'll be fine", "Here's a link")
    ]
    script = queries.make_create_script(entries, "Test")
    assert script == "INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES ('Don''t break stuff', 'Aren''t quotes dangerous', 'It''ll be fine', 'Here''s a link', 'Test', GETDATE())"