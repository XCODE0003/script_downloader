import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor

def extract_real_url(url):
    """
    Извлекает реальный URL из сложных URL-адресов CDN
    """
    # Проверяем, содержит ли URL путь CDN с вложенным URL
    cdn_pattern = r'cdn-cgi/image/.*?/(https://.*)'
    match = re.search(cdn_pattern, url)
    if match:
        return match.group(1)
    return url

def download_file(url, base_dir='downloads'):
    """
    Функция для скачивания файла по указанному URL и его сохранения в указанный путь,
    сохраняя структуру директорий из URL.
    """
    try:
        # Извлекаем реальный URL, если это CDN-ссылка
        real_url = extract_real_url(url)

        path_from_url = real_url.split('//')[1]  # Удаление схемы (http, https)
        save_path = os.path.join(base_dir, path_from_url)

        # Проверка, существует ли уже этот файл
        if os.path.exists(save_path):
            print(f"Файл {os.path.basename(save_path)} уже существует. Пропуск...")
            return

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        # Используем оригинальный URL для запроса
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as f:
            f.write(response.content)
        return f"Файл {os.path.basename(save_path)} успешно скачан."
    except requests.RequestException as e:
        return f"Ошибка при скачивании файла {url}: {e}"

def download_files_from_file(file_path, num_threads=3):
    """
    Функция для скачивания файлов в несколько потоков.
    """
    with open(file_path, 'r') as file:
        urls = file.readlines()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Запускаем загрузку в несколько потоков
        results = executor.map(download_file, (url.strip() for url in urls if url.strip()))

        # Вывод результатов
        for result in results:
            if result:
                print(result)

if __name__ == "__main__":
    file_path = 'found_links.txt'
    download_files_from_file(file_path)