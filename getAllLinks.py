import requests
from bs4 import BeautifulSoup

def get_https_links(url):
    # Запрос страницы
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный ответ
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []

    # Парсинг HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Инициализируем список для сбора ссылок
    links = []

    # Фильтр для тегов <img>, <script>, и <link> и соответствующих атрибутов
    for img_tag in soup.find_all('img', src=True):
        src = img_tag['src']
        if src.startswith('https'):
            links.append(src)
    
    for script_tag in soup.find_all('script', src=True):
        src = script_tag['src']
        if src and src.startswith('https'):  # проверка наличия src, т.к. могут быть скрипты без src
            links.append(src)

    for link_tag in soup.find_all('link', href=True):
        href = link_tag['href']
        if href.startswith('https'):
            links.append(href)

    return links

# Пример использования:
url = "http://127.0.0.1:5501"
https_links = get_https_links(url)
for link in https_links:
    print(link)