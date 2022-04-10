import requests
from bs4 import BeautifulSoup
import datetime
import os  # checking file
import csv
import re

base_url = 'https://www.bestbuy.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

# --------------create a csv file
file_exists = True

if not os.path.exists('./price.cvs'):
    file_exists = False

with open('lexi_ipad_case_search.csv', 'a') as file:
    writer = csv.writer(file, lineterminator='\n')
    # create row and columns
    fields = ['Timestamp', 'Product Name', 'Sale Price(USD)', 'Original Price(USD)', 'Model', 'SKU', 'Rating', 'Link']

    # if it does not exist then write to file
    if not file_exists:
        writer.writerow(fields)
    # --------------create a csv file

    for page in range(0, 6):
        url = f'https://www.bestbuy.com/site/searchpage.jsp?cp={page}&id=pcat17071&st=ipad+11+case'
        r = requests.get(url, headers=headers)
        s = BeautifulSoup(r.content, 'html.parser')

        items = s.findAll('li', {'class': 'sku-item'})[:-1]
        for item in items:
            # ----------
            # Get Sponsored Items List
            # ----------
            prod_title_block = item.find('div', {'class': 'sku-title'})
            prod_name = prod_title_block.find('h4', {'class': 'sku-header'}).get_text().strip()
            # prod_link = prod_name.find('a')
            # ----------------------Links Loop Moved

            price_block = item.find('div', {'class': 'priceView-hero-price priceView-customer-price'})
            prod_list_price = price_block.find('span').get_text().strip().replace('$', '')
            try:
                # Create try and except for this not all have this section
                prod_original_price = item.find('div',
                                                {'class': 'pricing-price__regular-price'}).get_text().strip().replace(
                    'Was $', '')
                prod_sku = item.findAll('span', {'class': 'sku-value'})[1].get_text().strip()
                prod_model = item.findAll('span', {'class': 'sku-value'})[0].get_text().strip()
            except:
                prod_original_price = 'No Sale'
                prod_sku = 'No SKU Found'
                prod_model = 'No Model'

            rating_block = item.find('div', {'class': 'ratings-reviews'})
            try:
                prod_rating = float(rating_block.find('p', {'class': 'visually-hidden'}).get_text().strip()[13:15])
            except:
                prod_rating = 'Check Manually'
                pass

            for link in prod_title_block.find_all('a'):
                # display the actual urls
                prod_link = base_url + link['href']
                # prod_link = prod_name.find('a', )
                # Store in Dictionary
                prod_details = {
                    'name': prod_name,
                    'sale': prod_list_price,
                    'original': prod_original_price,
                    'model': prod_model,
                    'sku': prod_sku,
                    'rating': prod_rating,
                    'link': prod_link
                }

                # print(prod_link)


            # csv files code ----------------
            # change this format later
            timestamp = f'{datetime.datetime.date(datetime.datetime.now())}, {datetime.datetime.time(datetime.datetime.now())}'
            writer.writerow(
                [timestamp, prod_name, prod_list_price, prod_original_price, prod_model, prod_sku, prod_rating,
                 str(prod_link)])
            print('Finished exporting to cvs file.... ')
# csv files code ----------------
