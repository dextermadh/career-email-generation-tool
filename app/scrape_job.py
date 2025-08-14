from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
import time 

class ScrapeJob: 
    def __init__(self, url):
        self.url = url 
    
    def selenium_configure(self): 
        # configure selenium to run headless 
        chrome_options = Options() 
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
    
        return chrome_options
    
    def selenium_scrape(self): 
        # start the web driver
        driver = webdriver.Chrome(options=self.selenium_configure()) 
        driver.get(self.url) 
        
        time.sleep(5)  # await til js
        
        # get the page soruce
        html = driver.page_source
        driver.quit()
        
        # parse the html with beautifulsoup
        soup = BeautifulSoup(html, 'html.parser')
        
        page_text = soup.get_text(separator='\n', strip=True)
        return page_text
        