class QueryHelpers():
    SCRIPT_PREFIX = '''INSERT INTO dbo.JobSearchResults ([JobTitle], [Company], [Location], [Link], [Source], [Date]) VALUES '''

    def make_create_script(self, entries, source):
        script = self.SCRIPT_PREFIX

        for entry in entries:
            script +=  f"('{entry.title.replace("'", "''")}', '{entry.company.replace("'", "''")}', '{entry.location.replace("'", "''")}', '{entry.link.replace("'", "''")}', '{source}', GETDATE()),\n"

        # remove last comma from final entry
        return script[:-2]