from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    title, paragraph = mars_news(browser)

    data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": featured_image(browser),
        "weather": mars_weather(),
        "table": mars_facts(),
        "hemi_image": mars_hemispheres(browser),
        
    }
    browser.quit()
    return data

def mars_news(browser):

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(2)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract title text
    title = soup.find('li', class_='slide').find('div', class_='content_title').text
    
    # Extract paragraph texts 
    paragraph = soup.find('li', class_='slide').find('div', class_="article_teaser_body").text
   
    return title, paragraph

def featured_image(browser):
    
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    #will take you to the url
    browser.visit(url)
    
    time.sleep(2)

    #access the html that is currently on the page in the browser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #find the featured image
    picture = soup.find('div', class_='carousel_container').find("article")["style"]
    feature_img = picture.split("'")[1]
    feature_img_url = "https://www.jpl.nasa.gov" + feature_img
    
    return feature_img_url

def mars_weather():
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    weather = soup.find('div', class_='js-tweet-text-container').find('p', class_="TweetTextSize").text
    
    return weather

def mars_facts():
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'
    
    # use the read_html function in Pandas to automatically scrape any tabular data from a page.
    table = pd.read_html(url)
    df = table[0]
    # Assign the columns heading
    df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    df.set_index('Description', inplace=True)

    mars_html_table = df.to_html()

    mars_table = mars_html_table.replace('\n', '')
   
    return mars_table

def mars_hemispheres(browser):
    
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='description')


    #create list for hemisphere url
    url_list = []

    for picture in items:
    
        title = picture.find('h3').text
        browser.click_link_by_partial_text (title)
       
        time.sleep(2)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        mars_url = soup.find('div', class_='downloads').find('a')['href']
        hemi = {
            'title':title,
            'image_url':mars_url
        }
        url_list.append (hemi)
        browser.back()
        
    return url_list
