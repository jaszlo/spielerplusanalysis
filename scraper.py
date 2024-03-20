import pandas as pd
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time

from credentials import *
from config import *



class Driver(object):


    def __init__(self, headless=True, startAt=START_DATE):
        # Setting up options for Chrome WebDriver
        self.options = webdriver.ChromeOptions()
        for arg in BROWSER_ARGS:
            self.options.add_argument(arg)

        # Set download directory and headless mode
        self.options.add_experimental_option("prefs", {"download.default_directory": DOWNLOAD_DIR})
        if headless:
            self.options.add_argument("--headless")

        # Initialize Chrome WebDriver using WebDriver Manager
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options, keep_alive=True)

        # Open 'Spieler Plus' website
        self.driver.get(SPIELER_PLUS_URL)

        # Accept cookies and click on start login
        self.find_element(PATHS["acceptCookies"]).click()
        self.find_element(PATHS["loginStart"]).click()

        # Enter email and password
        self.find_element(PATHS["inputEmail"]).send_keys(EMAIL)
        self.find_element(PATHS["inputPassword"]).send_keys(PASSWORD)

        # Click on finish login button and select team
        self.find_element(PATHS["loginFinish"]).click()
        self.find_element(PATHS["teamSelect"]).click()

        # Open calendar page with start date
        self.current_date = pd.to_datetime(startAt)
        self.driver.get(f"{SPIELER_PLUS_URL}/events/calendar?date={startAt}")
    
    def find_element(self, xpath, limit=100):
        for _ in range(limit):
            try:
                return self.driver.find_element(by=By.XPATH, value=xpath)
            except Exception as e:
                time.sleep(0.1)

    def next_month(self):
        self.current_date = pd.to_datetime(self.current_date) + pd.DateOffset(months=1)
        self.driver.get(f"{SPIELER_PLUS_URL}/events/calendar?date={self.current_date.strftime('%Y-%m-%d')}")


    def download_attendance(self, training_id, event_type):
        export_url = f"{SPIELER_PLUS_URL}/{event_type}/print-participant-list?id={training_id}&exportCsv=1"
        self.driver.get(export_url)

    def scrape_month(self):
        calendar = self.find_element(PATHS["calendar"])
        events = calendar.find_elements(By.TAG_NAME, "a")
        for event in events:
            try:
                link = event.get_attribute("href")
                event_type = "training" if "training" in link else "game"
                training_id = link.split("?id=")[-1]
                self.download_attendance(training_id, event_type)
            except Exception as e:
                pass

def reached_current_month(driver):
    now = datetime.now()
    return now.year == driver.current_date.year and now.month == driver.current_date.month

def main():
    d = Driver(headless=False)
    while not reached_current_month(d):
        d.scrape_month()
        d.next_month()

if __name__ == "__main__":
    main()
    pass