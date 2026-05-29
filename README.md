# Job Scrapers

This repository uses the Selenium Chrome web driver in Python to scrape job boards. The listings found are written to a SQL database. The advantage of this is to remove duplicates and block list matches so they can be aggregated for quick review.

## Setup

### Python

Known working version is Python 3.12, but likely compatible with others.

#### Windows

1. Download from python.org
2. Create venv from repo root directory: `python -m venv venv`
3. Activate the venv: `venv\Scripts\activate`
4. Install dependencies into the venv:
    - `python -m pip install selenium`
    - `python -m pip install pyodbc`

#### Linux

1. `apt install python3.12-venv`
2. Create venv from repo root directory: `python3 -m venv venv`
3. Activate the venv: `source venv/bin/activate`
4. Install dependencies into the venv:
    - `python3 -m pip install selenium`
    - `python3 -m pip install pyodbc`

### Selenium

The chromedriver executable is currently manually downloaded and placed in the root of this repo when a new version is available, from this site:

https://googlechromelabs.github.io/chrome-for-testing/

### Database

The DB scripts are based on MSSQL (SQL Server). It should work with other SQL varieties with some syntax changes. The server and database name would also need to be changed no matter what since they are specific to my machine. The `create_table.sql` script included in this repo shows the schema used.

The `write_to_db()` method does not need to actually run to demonstrate the read ability of the scraper, just the write. 

Possible future work may add ability to write to a JSON file to make this more flexible.

## Usage

Run one of the scripts in the root of the repo, named for the job board. The basic flow of a script is as follows:

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

## Testing

Add pytest with `pip install pytest` (Win) or `apt install python3-pytest` (Linux). Run a file with `_test` in the name with the command `pytest /path/to/file_test.py`