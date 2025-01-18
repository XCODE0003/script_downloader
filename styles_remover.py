import re

def extract_classes_from_selector(selector):
    """Возвращает список классов, найденных в селекторе."""
    # ищем классы в селекторе, примеры: .class, .class:hover, .class::before, .class.otherClass
    return re.findall(r'\.([^\s\.\:#>\[\]]+)', selector)

def read_classes(file_path):
    """Чтение списка классов из файла."""
    with open(file_path, "r") as file:
        return file.read().splitlines()

def css_contains_class(selector, class_list):
    """Проверяем, содержит ли селектор хоть один класс из списка."""
    selector_classes = extract_classes_from_selector(selector)
    return any(cls in class_list for cls in selector_classes)

def extract_relevant_css(source_css_path, class_list, output_css_path):
    """Извлекает стили, относящиеся к заданным классам."""
    with open(source_css_path, "r") as file:
        source_css = file.read()
    
    # Используем non-greedy matching для блоков стилей, чтобы извлекать их корректно
    pattern = re.compile(r'(.+?)\{(.+?)\}', re.DOTALL)
    relevant_css = ""

    for selector, body in pattern.findall(source_css):
        # Очищаем селектор от пробелов и переносов строк для более точного сопоставления
        selector = " ".join(selector.split())
        if css_contains_class(selector, class_list):
            relevant_css += f"{selector} {{{body}}}\n"
    
    with open(output_css_path, "w") as file:
        file.write(relevant_css)

# Список классов, полученный из HTML
class_list = read_classes("classes_output.txt")
# Извлекаем стили, относящиеся к классам, в новый CSS файл
extract_relevant_css("source.css", class_list, "result.css")

print("Извлечение завершено.")