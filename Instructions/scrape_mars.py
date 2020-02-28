from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def scrape():
    browser = init_browser()
    
    
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Retrieve page with the requests module. response is HTML page
    #response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Extract title text
    title = soup.title.text
    mars_data['title'] = title

    # Print all paragraph texts
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        print(paragraph.text)

        
    mars_data['paragraph'] = paragraph

    # Close the browser after scraping
    browser.quit()

    # Return results
    #return mars_data
    return title, paragraph
