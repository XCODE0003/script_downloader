import requests
import os

def download_file(url, base_dir='downloads'):
    """
    Функция для скачивания файла по указанному URL и его сохранения в указанный путь,
    сохраняя структуру директорий из URL.   
    """
    try:
        
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP.
        
        # Построение пути сохранения файла с учетом его URL.
        path_from_url = url.split('//')[1]  # Удаление схемы (http, https).
        save_path = os.path.join(base_dir, path_from_url)
        
        # Создание директорий для файла, если они не существуют.
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Файл {os.path.basename(save_path)} успешно скачан.")
    except requests.RequestException as e:
        print(f"Ошибка при скачивании файла {url}: {e}")

def download_files_from_file(file_path):
    """
    Функция для скачивания файлов, ссылки на которые содержатся в указанном файле.
    Сохраняет файлы с учетом их путей в URL.
    """
    with open(file_path, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()  # Удаляем пробельные символы с начала и конца строки.
        if url:  # Проверяем, что строка не пустая.
            download_file(url)

if __name__ == "__main__":
    # Путь к файлу со ссылками.
    file_path = 'found_links.txt'
    
    # Запускаем процесс скачивания.
    download_files_from_file(file_path)