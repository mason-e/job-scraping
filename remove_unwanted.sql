-- this removes any duplicate entries, keeping the oldest
WITH CTE AS (SELECT [Company], [JobTitle], [Date], RN = 
        ROW_NUMBER() OVER(PARTITION BY [Company], [JobTitle] ORDER BY [Date] ASC) FROM [JobSearchResults])
        DELETE FROM CTE WHERE RN > 1

-- removes any entries that match a company on the block list
DELETE T1
        FROM dbo.JobSearchResults AS T1
        INNER JOIN dbo.BlacklistCompany As T2
        ON T1.Company LIKE '%' + T2.Company + '%'

-- removes any entries that match a job title on the block list
DELETE T3
        FROM dbo.JobSearchResults AS T3
        INNER JOIN dbo.BlacklistJobTitle As T4
        ON T3.JobTitle LIKE '%' + T4.JobTitle + '%'
