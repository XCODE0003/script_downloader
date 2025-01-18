import requests
from bs4 import BeautifulSoup
from mysql.connector import connect, Error
import json
import os

db_host = '127.0.0.1'
db_port = '3307'
db_user = 'root'
db_password = ''
db_name = 'hermes'

category_id = 1
categories = [1, 2, 3, 4, 5, 6, 7, 8]
# for category_id in categories:
    
site_url = 'https://hermesoriginalbag.com/'

html = requests.get(site_url).text

soup = BeautifulSoup(html, 'html.parser')

products = {}
def download_images(images):
    for img_url in images:
        path_parts = img_url.split('/')
        directory = os.path.join('images', *path_parts[:-1])
        file_name = path_parts[-1]

        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, file_name)
        img_url = 'https://hermesoriginalbag.com' + img_url
        img = requests.get(img_url).content
        with open(file_path, 'wb') as f:
            f.write(img)
            
            
categories = []
for category in soup.find_all('div', class_='categoryBox'):
    onclick_attr = category.get('onclick')
    if onclick_attr and onclick_attr.startswith('window.location'):
        category_id = onclick_attr.split('=')[-1]
        category_id = category_id.replace("'", "")
        image = category.find('img').get('src')
        category_name = category.find('div').text.strip()
        download_images([image])
        try:
            with connect(
                host=db_host,
                user=db_user,
                port=db_port,
                password=db_password,
                database=db_name
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO categories (id,name, image) VALUES (%s ,%s, %s)', (category_id,category_name, image))
                    connection.commit()
                    
        except Error as e:
            print(e)
        
    

# Get all product links
# product_links = []
# for product_div in soup.find_all('div', class_='mainItem'):
#     onclick_attr = product_div.get('onclick')
#     if onclick_attr and onclick_attr.startswith('window.location'):
#         link = onclick_attr.split("'")[1]
#         product_links.append(link)
#         products[link] = {
#             'image_hover': product_div.find('img', class_='itemImageHover').get('data-src'),
#             'sold': product_div.find('div', class_='itemSold') is not None,
#         }

# for link in product_links:
#     full_link = 'https://hermesoriginalbag.com' + link

#     product_html = requests.get(full_link).text
#     product_soup = BeautifulSoup(product_html, 'html.parser')
    
#     product_name = product_soup.find('div', class_='productTitle').text.strip()
#     product_description = product_soup.find('div', class_='productDesc').text.strip()
#     images = []
#     for img in product_soup.find_all('div', class_='photoSlideWrap'):
#         img_url = img.find('img').get('src')
#         images.append(img_url)
    
#     products[link]['product_name'] = product_name
#     products[link]['product_description'] = product_description
#     products[link]['images'] = images
#     download_images([products[link]['image_hover']])
#     download_images(images)
    
#     try:
#         with connect(
#             host=db_host,
#             user=db_user,
#             port=db_port,
#             password=db_password,
#             database=db_name
#         ) as connection:
#             with connection.cursor() as cursor:
#                 images_json = json.dumps(images)
#                 cursor.execute('INSERT INTO products (name, description, images, category_id, image_hover, sold) VALUES (%s, %s, %s, %s, %s, %s)', (product_name, product_description, images_json, category_id,  products[link]['image_hover'], products[link]['sold']))
#                 connection.commit()
                
#     except Error as e:
#         print(e)
    


