from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_mars_news():
    print("scrape_mars_news function called")
    browser = init_browser()

    # Visit news URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)  
    time.sleep(1)

    news_title = ''
    news_p = ''
    news_list = []

    for x in range(1, 2):

        html = browser.html
        soup = bs(html, 'html.parser')
        #print(soup.prettify())
        news_list = soup.find_all('div', class_='list_text')
#       print(news_list[0])
        news_title = news_list[0].find('div', class_='content_title').text
        print(news_title)
        news_p = news_list[0].find('div', class_='article_teaser_body').text
        print(news_p)
# The code commented allows to retrive all the news. but we need only first and latest news in list   
#       for news_item in news_list:
#         print('page:', x, '-------------')
#         print(news_item)
#         title_list = news_item.find_all('div', class_='content_title')
#         for title in title_list:
#             news_title = title.text
#             print(news_title)
    
#         teaser_text_list = news_item.find_all('div', class_='article_teaser_body')
#         for teaser in teaser_text_list:
#             news_p = teaser.text
#             print(news_p)

        browser.links.find_by_partial_text('More')

    # Store data in a dictionary
    news_data = {
        "news_title": news_title,
        "news_p": news_p
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return news_data


def scrape_mars_image():
    print("scrape_mars_image function called")
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    full_image_button = soup.find('a', class_='button fancybox')
    print(full_image_button)
    try:
        browser.click_link_by_id('full_image')
    except:
        print("Cannot find FULL IMAGE button")

    html = browser.html
    soup = bs(html, 'html.parser')

    try:
        button_link = browser.links.find_by_partial_href('spaceimages/details')
        print(button_link['href'])
        button_link.click()   
    except:
        print("Cannot find FULL IMAGE button")

    html = browser.html
    soup = bs(html, 'html.parser')

    target_url = soup.find('figure', class_='lede').a['href']
    print(target_url)

    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + target_url
    print(featured_image_url)
    # Store data in a dictionary
    image_data = {
        "image_url": featured_image_url,
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return(image_data)

def scrape_mars_facts():
    print('scrape_mars_facts function called')
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    table_list = soup.find('table', id='tablepress-p-mars-no-2')
    #print(table_list.prettify())

    table_rows = table_list.find_all('td', class_='column-1')
    #print(table_rows)
    column_1 = []
    for row in table_rows:
        column_1.append(row.text)
        #print(row.text)      
    print(column_1)

    table_rows = table_list.find_all('td', class_='column-2')
    #print(table_rows)
    column_2 = []
    for row in table_rows:
        column_2.append(row.text)
        #print(row.text)      
    print(column_2)

    mars_df = pd.DataFrame({"key": column_1, 
                       "value": column_2})
    #print(mars_df)

    # Close the browser after scraping
    browser.quit()

    return (mars_df)

def scrape_mars_hemispheres():
    print('scrape_mars_hemispheres function called')
    browser = init_browser()
    base_url = 'https://astrogeology.usgs.gov'
    # Visit USGS Astrogeology
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres_list = soup.find('div', id='product-section')
    #print(hemispheres_list.prettify())

    hem_list = []
    hem_img_list = []
    hemisphere_image_urls =[]

    hemisphere_titles = hemispheres_list.find_all('h3')
    for hemisphere_title in hemisphere_titles:
        hem_list.append(hemisphere_title.text)
    print(hem_list)

    thumbnail_div_list = hemispheres_list.find_all('div', class_="description")
    #print(thumbnail_div_list)
    print('------------------')
    for thumbnail_div in thumbnail_div_list:
        thumbnail_url = thumbnail_div.find('a', class_="itemLink product-item")
        print(thumbnail_url)
        print(thumbnail_url['href'])
        #button_link = browser.links.find_by_partial_href(thumbnail_url['href'])
        thumb_url = base_url + thumbnail_url['href']
        browser.visit(thumb_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        image_url = soup.find('div', class_="downloads")
        #print(image_url.a['href'])
        hem_img_list.append(image_url.a['href'])
        print(hem_img_list)

    for i in range(len(hem_list)):
       hemisphere_image_urls.append({f"title{i}": hem_list[i], 
                                  f"img_url{i}": hem_img_list[i]
                                 })
    print(hemisphere_image_urls)

    # Store data in a dictionary
    hems_data = {
        "title1": hemisphere_image_urls[0]['title0'],
        "img_url1": hemisphere_image_urls[0]['img_url0'],
         "title2": hemisphere_image_urls[1]['title1'],
        "img_url2": hemisphere_image_urls[1]['img_url1'],
        "title3": hemisphere_image_urls[2]['title2'],
        "img_url3": hemisphere_image_urls[2]['img_url2'],
        "title4": hemisphere_image_urls[3]['title3'],
        "img_url4": hemisphere_image_urls[3]['img_url3'], 
    }

    # Close the browser after scraping
    browser.quit()
    return (hems_data)