# Spielerplus Web Analysis

This repository contains Python scripts for scraping data from Spielerplus, analyzing attendance, and storing the data into a local DuckDB database.
This tool is only needed when you do not have the required permission to look at those statistic in the spilerplus app itself.

## Files

1. **config.py**: This file contains configuration information such as XPaths and options for Selenium. Make sure to set appropriate values before running the scraper.

2. **scraper.py**: This is the web scraper script used to gather data from Spielerplus. Before running this script, ensure you have set your credentials in `credentials.py`, where `EMAIL` and `PASSWORD` variables need to be defined.

3. **data.py**: After downloading the files into the `./download` folder, this script allows you to analyze the attendance of players on a team. It fetches the data from downloaded files and stores it into a local DuckDB database.

4. **credentials.py**: This file is required by `scraper.py` and should contain your credentials for logging into Spielerplus. Define the `EMAIL` and `PASSWORD` variables in this file.

## Usage

1. Set up your configuration in `config.py` according to your requirements.
2. Define your Spielerplus credentials in `credentials.py`.
3. Run `scraper.py` to gather data from Spielerplus.
4. After downloading the files into the `./download` folder, run `data.py` to analyze attendance and store the data into a local DuckDB database.

## Requirements

- Python 3.x
- Selenium
- DuckDB
- WebDriverManager
- pandas

Install the dependencies using:
```sh
pip install selenium duckdb pandas webdriver-manager
```

