import datetime  # making folder names
import shutil  # to save it locally
import time  # create delays for browser to catch up
from os import chdir  # download images to the correct folder
from pathlib import Path # creating folder structure

import lxml  # parser for beautiful soup
import requests  # for image download
from bs4 import BeautifulSoup  # find attributes in html for helium
from helium import *  # selenium for interacting with browser window
from selenium.webdriver.chrome.options import Options  # start helium with user agent

# zillow sign in info
email = "capt.kross02@gmail.com"
password = "T?nxV9.83xed/R#"

# starts chrome with user agent
opts = Options()
opts.add_argument(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
)
driver = start_chrome("www.zillow.com/user/acct/login", options=opts)

def sign_in(email, password):
    # signs in
    write(email, into="Email")
    write(password, into="Password")
    click("Sign in")
    time.sleep(3)
    get_favorite()

def get_favorite():
    # goes to favorite page
    go_to("https://www.zillow.com/myzillow/favorites")
    # gets source html from chrome
    source = driver.page_source
    # gets source html and gives it to beautifulsoup for parsing
    soup = BeautifulSoup(source, "lxml")
    # finds all links on the page
    for link in soup.find_all("a"):
        # adds links to list if they're the ones we want and aren't in the list already
        if (
            link.get("href").startswith("/homedetails")
        ):
            yield "https://www.zillow.com" + link.get("href")

for i in get_favorite():
    print(i)
    
sign_in(email, password)
    
