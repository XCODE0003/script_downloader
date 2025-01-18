import aiohttp
import asyncio
from bs4 import BeautifulSoup
import aiomysql
import json
import os

db_host = '127.0.0.1'
db_port = 3307
db_user = 'root'
db_password = ''
db_name = 'hermes'

categories = [1, 2, 3, 4, 5, 6, 7, 8]
def parse_categories():
    

async def download_image(session, img_url):
    path_parts = img_url.split('/')
    directory = os.path.join('images', *path_parts[:-1])
    file_name = path_parts[-1]

    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, file_name)
    img_url = 'https://hermesoriginalbag.com' + img_url

    async with session.get(img_url) as response:
        img = await response.read()
        with open(file_path, 'wb') as f:
            f.write(img)

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_category(session, pool, category_id):
    site_url = f'https://hermesoriginalbag.com/catalog?cat={category_id}'
    html = await fetch_html(session, site_url)
    soup = BeautifulSoup(html, 'html.parser')

    products = {}
    product_links = []

    for product_div in soup.find_all('div', class_='mainItem'):
        onclick_attr = product_div.get('onclick')
        if onclick_attr and onclick_attr.startswith('window.location'):
            link = onclick_attr.split("'")[1]
            product_links.append(link)
            products[link] = {
                'image_hover': product_div.find('img', class_='itemImageHover').get('data-src'),
                'sold': product_div.find('div', class_='itemSold') is not None,
            }

    for link in product_links:
        full_link = 'https://hermesoriginalbag.com' + link
        product_html = await fetch_html(session, full_link)
        product_soup = BeautifulSoup(product_html, 'html.parser')

        product_name = product_soup.find('div', class_='productTitle').text.strip()
        product_description = product_soup.find('div', class_='productDesc').text.strip()
        images = [img.find('img').get('src') for img in product_soup.find_all('div', class_='photoSlideWrap')]

        products[link]['product_name'] = product_name
        products[link]['product_description'] = product_description
        products[link]['images'] = images

        await download_image(session, products[link]['image_hover'])
        await asyncio.gather(*[download_image(session, img_url) for img_url in images])

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                images_json = json.dumps(images)
                await cursor.execute(
                    'INSERT INTO products (name, description, images, category_id, image_hover, sold) VALUES (%s, %s, %s, %s, %s, %s)',
                    (product_name, product_description, images_json, category_id, products[link]['image_hover'], products[link]['sold'])
                )
                await conn.commit()

async def main():
    async with aiohttp.ClientSession() as session:
        pool = await aiomysql.create_pool(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db=db_name,
            autocommit=True
        )

        tasks = [process_category(session, pool, category_id) for category_id in categories]
        await asyncio.gather(*tasks)

        pool.close()
        await pool.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())