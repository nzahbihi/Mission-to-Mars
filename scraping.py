# Import Splinter, BeautifulSoup, and Pandas.
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_data": hemisphere_data()
    }
    
    # Stop webdriver and return data.
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the Mars NASA News Site.
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page.
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first <a> tag and save it as 'news_title'.
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text.
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL.
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button.
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup.
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling.
    try:
        # Find the relative image URL.
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL.
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

# ## Mars Facts

def mars_facts():
    # Add try/except for error handling.
    try:
        # Use 'read_html' to scrape the facts table into a dataframe.
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe.
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe to HTML format, add bootstrap.
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data.
    print(scrape_all())

# ## Hemisphere data
def hemisphere_data():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    html = browser.html
    img_soup = soup(html, 'html.parser')


    for i in range(4):
        hemispheres = {}
    
        browser.is_element_present_by_css('div.list_text', wait_time=1)
    
        full_image_elem = browser.links.find_by_partial_text('Enhanced')[i]
        full_image_elem.click()
    
        img_url = browser.links.find_by_text('Sample')['href']
    
        title = browser.find_by_css('h2.title').text
    
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
    
        browser.back()

    return hemisphere_image_urls