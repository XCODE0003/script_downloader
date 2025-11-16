import os

def rename_files(directory_path):
    # Проходим по всем файлам и директориям
    for root, dirs, files in os.walk(directory_path):
        # Сначала переименовываем файлы
        for filename in files:
            if '﹖' in filename:
                old_path = os.path.join(root, filename)
                new_filename = filename.replace('﹖', '_')
                new_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_path, new_path)
                    print(f'Переименован файл: {old_path} -> {new_path}')
                except Exception as e:
                    print(f'Ошибка при переименовании {old_path}: {str(e)}')

        # Затем переименовываем директории
        for dirname in dirs:
            if '﹖' in dirname:
                old_path = os.path.join(root, dirname)
                new_dirname = dirname.replace('﹖', '_')
                new_path = os.path.join(root, new_dirname)
                try:
                    os.rename(old_path, new_path)
                    print(f'Переименована директория: {old_path} -> {new_path}')
                except Exception as e:
                    print(f'Ошибка при переименовании {old_path}: {str(e)}')

if __name__ == "__main__":
    # Укажите абсолютный путь к директории
    directory_path = "/Users/nikita/Downloads/us.sitesucker.mac.sitesucker-pro/oberig.ua"
    
    # Проверяем существование директории
    if not os.path.exists(directory_path):
        print(f"Директория {directory_path} не существует")
    else:
        print(f"Начинаем переименование файлов в {directory_path}")
        rename_files(directory_path)
        print("Переименование завершено")