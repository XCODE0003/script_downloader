import re

# Исходный текст с URL
text = """
http://localhost:8881/_next/image?url=/_next/static/media/1.f4dba256.webp
http://localhost:8881/_next/image?url=/_next/static/media/2.55201be7.png
http://localhost:8881/_next/image?url=/_next/static/media/1.6d4bac96.png
http://localhost:8881/_next/image?url=/_next/static/media/4.2ba59c8b.png
http://localhost:8881/_next/image?url=/_next/static/media/6.6361c9ba.png
http://localhost:8881/_next/image?url=/_next/static/media/1.b0e3b1fb.png
http://localhost:8881/_next/image?url=/_next/static/media/3.493688a5.png
http://localhost:8881/_next/image?url=/_next/static/media/2.1e63dcda.png


"""

# Регулярное выражение для поиска URL-адресов в тексте, учитывая потенциальные переносы строк
# Обрабатываем GET запросы и HTTP ответы в многострочном тексте
# Используем non-capturing group (?:...), lazy quantifiers и lookaheads для точного захвата URL
regex_pattern = r"http://localhost:8881/_next/image\?url=[^\s]+?\.(?:png|jpg|jpeg|webp|gif|bmp|tiff)"

# Удаление переносов строк и лишних пробелов из найденных совпадений
matches = [re.sub(r"\s+", "", match) for match in re.findall(regex_pattern, text)]

# Путь и имя файла для сохранения результатов
output_file_path = "found_links.txt"

# Сохранение найденных ссылок в файл
with open(output_file_path, "w") as file:
    for match in matches:
        match = match.replace('http://localhost:8881/_next/image?url=', 'https://amlbot.com')
        file.write(match + "\n")

print(f"Ссылки были успешно сохранены в файл {output_file_path}")