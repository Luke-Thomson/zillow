from helium import *
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import lxml
import requests # to get image from the web
import shutil # to save it locally

opts = Options()
opts.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
driver = start_chrome('https://www.zillow.com/homedetails/111-Metcalf-St-Providence-RI-02904/66045108_zpid/', options=opts)
click(Button('view larger view of the 1 photo of this home'))
source = driver.page_source
soup = BeautifulSoup(source, 'lxml')
result = soup.select('#gallery > div > div > div > div > div:nth-child(1) > div > div > picture > img')
print(result)








#try clicking the first image grabing the url then treat it the same as pagination!!!!!
#sources = []
#images = soup.find_all('img')
'''for img in images:
    if img.has_attr('src') and img['src'].startswith('https://photos.zillowstatic.com/') and img['src'] not in sources:
        sources.append(img['src'])'''
'''for i in sources:
    filename = i.split("/")[-1]
    r = requests.get(i, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retreived')'''

    

