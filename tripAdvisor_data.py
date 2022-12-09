from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

HOTEL_URL = "https://www.tripadvisor.com/"
us_loc = ['Chicago','Detroit']
ca_loc = ['Toronto','Montreal']
country_list = ['   Canada   ', '   Michigan   ', '   Illinois   ']

cache_list = []

def main():
    pages = 34
    data_per_page = 30 
    ct = 'Detroit'
    webCrawl(pages, data_per_page, ct)
    caching(f'{ct}_1.csv')
    print('---finish---')

def webCrawl(pagination, data_per_page, city):
    """
    Crawl the official website of TripAdvisor and save the crawled information into a cache.
  
    Parameters:
    pagination (int): the number of pages of the assigned city
    data_per_page (int): the number of data in each page
    city (str): the targeted city whose data is requested by users
  
    Returns:
    no return values
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(HOTEL_URL) 
    time.sleep(5)

    ct = browser.find_element(By.CSS_SELECTOR, '#lithium-root > main > div:nth-child(3) > div > div > div > form > input.qjfqs._G.B-.z._J.Cj.R0')
    ct.send_keys(city)
    ct.send_keys(Keys.ENTER)
    time.sleep(5)

    clickHotel = browser.find_element(By.CSS_SELECTOR, '#search-filters > ul > li:nth-child(2) > a')
    clickHotel.click()
    time.sleep(5)
    
    indices = 1
    for _ in range(pagination-1):
        selectors = []
        
        for i in range(1,data_per_page+6): 
            # The index of six multiples are all advertisements
            if i % 6 != 0: 
                ele = f'#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div.prw_rup.prw_search_search_results.ajax-content > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div:nth-child({i}) > div > div > div > div.ui_column.is-9-desktop.is-8-mobile.is-9-tablet.content-block-column > div.location-meta-block'
                selectors.append(ele)
        
        for i in range(data_per_page):    
            element = browser.find_element(By.CSS_SELECTOR, selectors[i])
            hotel = element.text.split('\n')
            cache = {}
            # print(hotel[2].split(', '))
            if hotel[2].split(',')[-1] in country_list[0] or hotel[2].split(',')[-1] in country_list[1] or hotel[2].split(',')[-1] in country_list[2]:
                cache['Index'] = indices
                indices += 1
                cache['Country'] = 'US' if city in us_loc else 'CA'
                cache['City'] = city
                cache['Hotel'] = hotel[0]
                cache['Address']= hotel[2]
                cache['Popularity'] = int(hotel[1].split(" ")[0].replace(',',''))
                cache_list.append(cache)
        
        # Click "Next"
        next = browser.find_element(By.CSS_SELECTOR, '#BODY_BLOCK_JQUERY_REFLOW > div.page > div > div.ui_container.main_wrap > div > div > div > div > div.content_column.ui_column.is-9-desktop.is-12-tablet.is-12-mobile > div > div.ui_columns.sections_wrapper > div > div.prw_rup.prw_search_search_results.ajax-content > div > div.ui_column.is-12.result-section-footer-columns > div > div > div > a.ui_button.nav.next.primary')
        next.click()
        time.sleep(5)

def caching(filename):
    """
    Cache data into a csv file.

    Parameters:
    filename (str): the name of the output file
    city (str): the city data this file should contain
    
    Retruns:
    no return values
    """
    csv_columns = ['Index', 'Country', 'City', 'Hotel', 'Address', 'Popularity']
    with open(filename,'w') as f:
        data = csv.DictWriter(f, fieldnames=csv_columns)
        data.writeheader()
        for value in cache_list:
            data.writerow(value)

    
if __name__ == '__main__':
    main()