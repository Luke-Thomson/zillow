from helium import *  # selenium for interacting with browser window
from selenium.webdriver.chrome.options import Options  # start helium with user agent
import time  # create delays for browser to catch up
from bs4 import BeautifulSoup  # find attributes in html for helium
import lxml  # parser for beautiful soup
import requests  # for image download
import shutil  # to save it locally
from pathlib import Path #creating folder structur
import datetime #making folder names
from os import chdir #download images to the correct folder

datetime_object = datetime.date.today()
date = 'zillow ' + str(datetime_object)
path = Path.cwd() / date
path.mkdir()

opts = Options()
opts.add_argument(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
)
driver = start_chrome(
    "https://www.zillow.com/homedetails/20724-N-112th-St-Scottsdale-AZ-85255/95170899_zpid/",
    options=opts,
)

click(Button("view larger view of the 1 photo of this home"))

links = []


def getLink():
    source = driver.page_source
    soup = BeautifulSoup(source, "lxml")
    for link in soup.select(
        "#gallery > div > div > div > div > div:nth-child(1) > div > div > picture > img"
    ):
        if link["src"] not in links:
            links.append(link["src"])
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
    newpath = path / 'home details'
    newpath.mkdir()
    chdir(newpath)
    for i in links:
        filename = i.split("/")[-1]
        r = requests.get(i, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            print("Image sucessfully Downloaded: ", filename)
    else:
        print("Image Couldn't be retreived")


getLink()

kill_browser()