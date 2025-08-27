USE [MasonDB]
GO

/****** Object:  Table [dbo].[JobSearchResults]    Script Date: 5/28/2025 1:18:08 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[JobSearchResults](
	[id] [smallint] IDENTITY(1,1) NOT NULL,
	[JobTitle] [nvarchar](200) NOT NULL,
	[Company] [nvarchar](200) NOT NULL,
	[Location] [nvarchar](100) NOT NULL,
	[Link] [nvarchar](400) NOT NULL,
	[Source] [nvarchar](50) NOT NULL,
	[Date] [date] NOT NULL,
 CONSTRAINT [PK_JobSearchResults] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

