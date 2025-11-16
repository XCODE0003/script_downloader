from bs4 import BeautifulSoup

def replace_links(input_file_path, new_url):
    # Читаем HTML файл
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Находим все теги <a> с атрибутом href
    links = soup.find_all('a', href=True)
    
    # Заменяем все ссылки на новый URL
    for link in links:
        link['href'] = new_url
    
    # Сохраняем измененный HTML в тот же файл
    with open(input_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

# Пример использования
if __name__ == "__main__":
    file_path = input("Введите путь к HTML файлу: ")
    new_url = input("Введите новую ссылку для замены: ")
    replace_links(file_path, new_url)
    print("Замена ссылок выполнена успешно!") 

