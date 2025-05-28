# Job Scrapers

This repository uses the Selenium Chrome web driver in Python to scrape job boards. The listings found are written to a SQL database. The advantage of this is to remove duplicates and block list matches so they can be aggregated for quick review.

## Setup

### Python

Known working version is Python 3.12, but likely compatible with others.

### Selenium

Use `pip` to install `selenium` dependency in code. The chromedriver executable is currently manually downloaded and placed in the root of this repo when a new version is available, from this site:

https://googlechromelabs.github.io/chrome-for-testing/

### Database

The DB scripts are based on MSSQL (SQL Server). It should work with other SQL varieties with some syntax changes. The server and database name would also need to be changed no matter what since they are specific to my machine. The `create_table.sql` script included in this repo shows the schema used.

Use `pip` to install the `pyodbc` dependency.

The `write_to_db()` method does not need to actually run to demonstrate the read ability of the scraper, just the write. 

Possible future work may add ability to write to a JSON file to make this more flexible.

## Usage

Run one of the scripts that is named for a job board site, not the base class scripts. The basic flow of a script is as follows:

1. Load a job board with past day of results
2. Collect results in an object:
    - It will scroll through the whole page if it's a continuously loading scroll, then collect results
    - It will attempt to page through to the end if it's paginated, collecting results on each page
3. Write the results to database

## Sites

Here are the sites it scrapes so far:

- LinkedIn
- Built In Colorado

### Deprecated Sites

#### Indeed
Stopped functioning once I started running into "verify you are human" checks.