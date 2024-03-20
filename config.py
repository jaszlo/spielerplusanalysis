SPIELER_PLUS_URL = "https://www.spielerplus.de"

from pathlib import Path
DOWNLOAD_DIR = str(Path("./downloads").absolute())

BROWSER_ARGS = [
    "--disable-extensions",
    "--disable-infobars",
    "--disable-popup-blocking",
]

START_DATE = "2018-01-01"

PATHS = {
    "acceptCookies": '//*[@id="cmpwelcomebtnyes"]/a',
    "loginStart": '/html/body/div[4]/nav/ul/li[5]/a',
    "inputEmail": '//*[@id="loginform-email"]',
    "inputPassword": '//*[@id="loginform-password"]',
    "loginFinish": '//*[@id="login-form"]/div[1]/div[3]/button',
    "teamSelect": '/html/body/div[8]/div/div/div[1]/div[1]/div/a',
    "calendar": '//*[@id="spCalendar"]/div[2]/div/table',
}  
