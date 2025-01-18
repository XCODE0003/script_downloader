import os

def rename_files(root_folder):
    # Проходим по всем папкам и файлам в указанной директории рекурсивно
    for root_dir, dirs, files in os.walk(root_folder):
        for filename in files:
            # Проверяем, содержит ли имя файла символ, который нужно удалить
            if '﹖' in filename:
                # Формируем новое имя файла без этого символа
                new_filename = filename.replace('﹖', '')
                # Формируем полный путь к текущему файлу и к файлу с новым именем
                old_file_path = os.path.join(root_dir, filename)
                new_file_path = os.path.join(root_dir, new_filename)
                # Переименовываем файл
                os.rename(old_file_path, new_file_path)
                print(f'Renamed "{old_file_path}" to "{new_file_path}"')

if __name__ == "__main__":
    # Укажите путь к корневой папке, в которой нужно искать и переименовывать файлы
    root_folder_path = '/Users/nikita/Downloads/us.sitesucker.mac.sitesucker-pro/fragment.com/'
    rename_files(root_folder_path)