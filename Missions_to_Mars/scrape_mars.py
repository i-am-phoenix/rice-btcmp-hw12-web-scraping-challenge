# Importing modules & dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint as pp

def scrape():
    #-----------------------------------MARS NEWS SITE-----------------------------------#
    # URL of page to be scraped
    url_mars_news = 'https://redplanetscience.com/'

    # Setup splinter
    # simulate opening a Chrome browser window and triggering JS script execution
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Open url_mars_news within teh newly opened browser session
    browser.visit(url_mars_news)
    # Retrieve page with the requests module
    # response = requests.get(url_mars_news)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Extract a single section with main content and then pull all div tags with class="col-md-8"
    results = soup.find('section', class_='image_and_description_container').find_all('div', class_="col-md-8")

    # Initialize news articles dictionary
    articles=[]

    #  Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return post title
            title = result.find('div', class_='content_title').text
            
            # Identify and return post description
            paragraph = result.find('div', class_='article_teaser_body').text
            
            # Creade a dictionary entry
            article_entry = {
                "news_title" : title,
                "news_p"     : paragraph
            }
            
            # Add new article entry to a dictionary 
            articles.append(article_entry)
            
        except AttributeError as e:
            print(e)

    # Close browser window
    browser.quit()

    #-----------------------------------JPL Mars Space Images - Featured Image-----------------------------------#
    jpl_url='https://spaceimages-mars.com/'

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Open url_mars_news within teh newly opened browser session
    browser.visit(jpl_url)

    # Read in page source
    html = browser.html

    # Parse the page source using html.parser
    soup = bs(html, 'html.parser')

    # Find featured image object on teh page and concatenate its locat path to the website url
    featured_image_url = jpl_url + soup.find('img', class_='headerimage fade-in')['src']

    # Close browser window
    browser.quit()

    #-----------------------------------MARS FACTS-----------------------------------#
    url_mars_facts='https://galaxyfacts-mars.com/'

    tables = pd.read_html(url_mars_facts)

    mars_stats_v1=tables[1].rename(columns={0:'Props',1:'Value'})

    #-----------------------------------Mars Hemispheres-----------------------------------#
    mars_hem_url='https://marshemispheres.com/'

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Open url_mars_news within teh newly opened browser session
    browser.visit(mars_hem_url)

    # Read in page source
    html = requests.get(mars_hem_url).text

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    results=soup.find_all('div', class_="description")

    hemisphere_image_urls=[]

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Loop through each hemisphere
    for result in results:
        url_temp = mars_hem_url + result.a['href']    
        title = result.h3.text.replace(" Enhanced", "")
        
        # Open temp_url and look for image element  
        browser.visit(url_temp)
        
        # Read in page source
        html = requests.get(url_temp).text
        
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = bs(html, 'html.parser')
        
        # Pulling out local image url
        results_temp=soup.find_all('dd')[1].a['href']
    #     print(results_temp)
        
        # Full image url
        full_url = mars_hem_url + results_temp
        
        # Create dictionary entry
        hem_dic_entry = {
            "title"   : result.h3.text.replace(" Enhanced", ""),
            "img_url" : full_url
        }
        
        # Append new entry to dictionary     
        hemisphere_image_urls.append(hem_dic_entry)
        
        # print(title)
        # print(url_temp)
        # print(full_url)
        # print('-------------')
        
    # Close browser window
    browser.quit()

    info = {
    "mars_news"            : articles,
    "mars_stats"           : mars_stats_v1.set_index('Props').to_dict('index'),
    
    "hemisphere_image_urls": hemisphere_image_urls
    }

    return info

pp(scrape())