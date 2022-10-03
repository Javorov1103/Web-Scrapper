import aiohttp
from bs4 import BeautifulSoup
import csv
import asyncio  
            
async def main():
    url = 'https://sarapenbg.com/product-category/%d0%b4%d0%b0%d0%bc%d1%81%d0%ba%d0%b8-%d0%be%d0%b1%d1%83%d0%b2%d0%ba%d0%b8/%d1%81%d0%bf%d0%be%d1%80%d1%82%d0%bd%d0%b8-%d0%be%d0%b1%d1%83%d0%b2%d0%ba%d0%b8/page/'
    async with aiohttp.ClientSession() as session:
        for i in range(5):
            async with session.get(url+str(i+1)) as resp:
                if(resp.status == 200):
                    body = await resp.text()
                    soup = BeautifulSoup(body, 'html.parser')
                    products = soup.select('.product-small.box .box-image .image-fade_in_back a')
                    for k in range(0, len(products)):
                        with open('jenski_sportni.csv','a',encoding='utf8') as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow([products[k]['href']])
                else:
                    break
         
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())