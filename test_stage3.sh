#!/bin/bash

echo "=== Тест 1: Минимальный VFS ==="
echo "exit" | python3 src/main.py --vfs tests/vfs_minimal.csv

echo -e "\n=== Тест 2: Несколько файлов ==="
echo "exit" | python3 src/main.py --vfs tests/vfs_multiple.csv

echo -e "\n=== Тест 3: Глубокая вложенность (3+ уровня) ==="
echo "exit" | python3 src/main.py --vfs tests/vfs_deep.csv

echo -e "\n=== Тест 4: Проверка ошибки загрузки (файл не найден) ==="
echo "exit" | python3 src/main.py --vfs tests/not_found.csv

echo -e "\n=== Тест 5: Полный прогон через стартовый скрипт ==="
python3 src/main.py --vfs tests/vfs_deep.csv --script tests/vfs_script.txt