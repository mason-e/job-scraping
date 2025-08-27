class QueryHelpers():
    SCRIPT_PREFIX = '''INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES '''

    def make_create_script(self, entries, source):
        script = self.SCRIPT_PREFIX

        for entry in entries:
            script +=  f"('{entry.title[0:200].replace("'", "''")}', '{entry.company[0:200].replace("'", "''")}', '{entry.location[0:100].replace("'", "''")}', '{entry.link[0:400].replace("'", "''")}', '{source}', GETDATE()),\n"

        # remove last comma from final entry
        return script[:-2]