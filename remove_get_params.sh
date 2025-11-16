#!/bin/bash

# Скрипт для удаления GET параметров из имен файлов
# Удаляет все что идет после знака "?" в названии файла

# Функция для логирования
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Проверяем, передан ли путь к директории как аргумент
if [ $# -eq 0 ]; then
    DIRECTORY="."
    log "Директория не указана, используется текущая директория: $(pwd)"
else
    DIRECTORY="$1"
    log "Обрабатываем директорию: $DIRECTORY"
fi

# Проверяем, существует ли директория
if [ ! -d "$DIRECTORY" ]; then
    log "ОШИБКА: Директория '$DIRECTORY' не существует!"
    exit 1
fi

# Переходим в указанную директорию
cd "$DIRECTORY" || {
    log "ОШИБКА: Не удалось перейти в директорию '$DIRECTORY'"
    exit 1
}

# Счетчики
renamed_count=0
total_files=0

log "Начинаем обработку файлов..."

# Обрабатываем все файлы в текущей директории
for file in *; do
    # Пропускаем директории
    if [ -d "$file" ]; then
        continue
    fi

    total_files=$((total_files + 1))

    # Проверяем, содержит ли имя файла знак "?"
    if [[ "$file" == *"?"* ]]; then
        # Извлекаем часть до знака "?"
        new_name="${file%%\?*}"

        # Получаем расширение из оригинального имени (если есть)
        if [[ "$file" == *.* ]]; then
            # Если в новом имени нет расширения, пытаемся его восстановить
            if [[ "$new_name" != *.* ]]; then
                # Ищем расширение в оригинальном имени до GET параметров
                original_without_params="${file%%\?*}"
                if [[ "$original_without_params" == *.* ]]; then
                    extension="${original_without_params##*.}"
                    new_name="${new_name}.${extension}"
                fi
            fi
        fi

        # Проверяем, не существует ли уже файл с таким именем
        if [ -e "$new_name" ] && [ "$new_name" != "$file" ]; then
            log "ПРЕДУПРЕЖДЕНИЕ: Файл '$new_name' уже существует, пропускаем '$file'"
            continue
        fi

        # Переименовываем файл
        if mv "$file" "$new_name" 2>/dev/null; then
            log "✓ '$file' -> '$new_name'"
            renamed_count=$((renamed_count + 1))
        else
            log "ОШИБКА: Не удалось переименовать '$file'"
        fi
    fi
done

log "Обработка завершена!"
log "Всего файлов обработано: $total_files"
log "Файлов переименовано: $renamed_count"

# Показываем результат
if [ $renamed_count -gt 0 ]; then
    log "Файлы успешно переименованы!"
else
    log "Файлы с GET параметрами не найдены."
fi