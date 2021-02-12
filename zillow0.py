import datetime  # making folder names
import shutil  # to save it locally
import time  # create delays for browser to catch up
from os import chdir  # download images to the correct folder
from pathlib import Path  # creating folder structure

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

# makes folder for scraped data
datetime_object = datetime.date.today()
date = "zillow " + str(datetime_object)
path = Path.cwd() / date
path.mkdir()

# starts browser window
driver = start_chrome("www.zillow.com/user/acct/login", options=opts)

favorites = []
images = []


def signIn(email, password):
    # signs in
    write(email, into="Email")
    write(password, into="Password")
    click("Sign in")
    # goes to favorite page
    time.sleep(3)
    go_to("https://www.zillow.com/myzillow/favorites")
    getFavorites()


def getFavorites():
    # gets source html from chrome
    source = driver.page_source
    # gets source html and gives it to beautifulsoup for parsing
    soup = BeautifulSoup(source, "lxml")
    # finds all links on the page
    for link in soup.find_all("a"):
        # adds links to list if they're the ones we want and aren't in the list already
        if (
            link.get("href").startswith("/homedetails")
            and link.get("href") not in favorites
        ):
            favorites.append("https://www.zillow.com" + link.get("href"))
    nextPage()


def nextPage():
    if Button("Chevron Right").is_enabled():
        click(Button("Chevron Right"))
        getFavorites()
    else:
        pass


def getLink():
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    for link in soup.select(
        "#gallery > div > div > div > div > div:nth-child(1) > div > div > picture > img"
    ):
        if link["src"] not in images:
            images.append(link["src"])
    nextImage()


def nextImage():
    if S(
        "#gallery > div > div > div > ul > li.photo-carousel-right-arrow.zsg-button-group > button > div.zsg-icon-expando-right"
    ).exists():
        click(
            S(
                "#gallery > div > div > div > ul > li.photo-carousel-right-arrow.zsg-button-group > button > div.zsg-icon-expando-right"
            )
        )
        getLink()
    else:
        download()


def download():
    tabname = driver.title
    newpath = path / tabname
    newpath.mkdir()
    chdir(newpath)
    for i in images:
        filename = i.split("/")[-1]
        r = requests.get(i, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            print("Image sucessfully Downloaded: ", filename)
    else:
        print("Image Couldn't be retreived")
    images.clear()


signIn(email, password)

for link in set(favorites):
    go_to(link)
    click(Button("view larger view of the 1 photo of this home"))
    getLink()
    
kill_browser()