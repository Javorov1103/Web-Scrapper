import asyncio
import aiohttp
import csv
import time
from bs4 import BeautifulSoup
from product import Product
from xml_creator import create_gomba_xml
import re
import os


# async def save_product(product):
#     with open('man_shoes.csv','a',encoding='utf8') as csv_file:
#         write = csv.writer(csv_file)
#         write.writerow(product)
        
        
# async def add_product(product, counter):
#     create_gomba_xml(product, counter)
    
async def scrape(url, parameter_counter_id,size_counter,categoryId,categoryName):
    async with aiohttp.ClientSession() as session:
        # print(url)
        async with session.get(url) as resp:
            try:
                product = Product()
                product.categoryId = categoryId
                product.categoryName = categoryName
                body = await resp.text()
                soup = BeautifulSoup(body, 'html.parser')
                # selecting the product name
                title = soup.select_one('.product-title').get_text()
                product.title = title
                
                titleElements = title.split('-')
                
                product.code = titleElements[1]
                
                # selecting the product images
                images_box = soup.find('div', attrs={'class': 'rtwpvg-slider-wrapper'})
                images = []
                for img in images_box.findAll("img"):
                    images.append(img['src'])
                    
                product.images = images
                
                numbers =[]
                #selecting the product available numbers
                numbers_elements = soup.find('ul', attrs={'class': 'wvs-style-squared'})
                if(numbers_elements is not None):
                    numbers = numbers_elements['data-attribute_values']
                    numbers = re.findall('\d+', numbers)
                    
                product.sizes = numbers
                product.sizes_ids = []
                sizes_ids = []
                for i in range(len(product.sizes)):
                    sizes_ids.append(size_counter)
                    size_counter += 1
                
                
                #selecting the product price
                price_element = soup.find('p', attrs={"class": 'product-page-price'}).find('bdi')
                if(price_element is not None):
                    price = price_element.get_text()
                    price = price.replace('лв.', '')
                    price = price.strip()
                    product.price = price
            
                
                #selecting details
                details = soup.find('div', attrs={'id': 'tab-description'})
                if(details is not None):
                    description_element = details.find('p')
                    if(description_element is not None):
                        description = description_element.get_text()
                        product.description = description
                
                
                lis = details.find_all('li')
                lisTexts = []
                for li in lis:
                    lisTexts.append(li.get_text())
                
                #save the product into the csv
                # await save_product(product)
                create_gomba_xml(product, parameter_counter_id,sizes_ids)
            except:
                print(url)
            
            return size_counter
            
async def main():
        start_time = time.time()
        parameter_counter_id = 1
        size_counter = 1
        tasks = []
        files = os.listdir('./Product links csvs')
        categoryId = 0
        
        #test
        # files = ['Мъжки мокасини.csv',]
        for file_name in files:  
            categoryId += 1 
            file_path = f'./Product links csvs\{file_name}'        
            with open(file_path) as file:
                categoryName = file_name.replace('.csv','')
                csv_reader = csv.DictReader(file)
                i=1
                for row in csv_reader:
                    # the url from csv can be found in csv_row['url']
                    url = row['productLink']
                    # url = url.replace(" ", "%20")
                    # task = asyncio.create_task(scrape(url))
                    # tasks.append(task)
                    size_counter = await scrape(url, parameter_counter_id,size_counter,categoryId,categoryName)
                    parameter_counter_id += 1
                    # size_counter = i*6
                    i += 1
                
                
        #await scrape('https://sarapenbg.com/product/%d0%ba%d0%be%d0%b6%d0%b5%d0%bd%d0%b8-%d0%bc%d1%8a%d0%b6%d0%ba%d0%b8-%d0%be%d0%b1%d1%83%d0%b2%d0%ba%d0%b8-%d0%b2-%d1%81%d0%b8%d0%bd-%d1%86%d0%b2%d1%8f%d1%82-0430185/',parameter_counter_id,size_counter)
        
        print('Saving the output of extracted information')
        await asyncio.gather(*tasks)
        
        time_difference = time.time() - start_time
        print(f'Scraping time: %.2f seconds.' % time_difference)
        
        
loop = asyncio.get_event_loop()
loop.run_until_complete(main())