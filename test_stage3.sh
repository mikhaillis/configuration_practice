#!/bin/bash

echo "=== Тест 1: Минимальный VFS ==="
echo exit | python3 src/main.py --vfs tests/vfs_minimal.csv

echo -e "\n=== Тест 2: Несколько файлов ==="
echo exit | python3 src/main.py --vfs tests/vfs_multiple.csv

echo -e "\n=== Тест 3: Глубокая вложенность (3+ уровня) ==="
echo exit | python3 src/main.py --vfs tests/vfs_deep.csv

echo -e "\n=== Тест 4: Файл VFS не найден ==="
echo exit | python3 src/main.py --vfs tests/not_found.csv

echo -e "\n=== Тест 5: Неверный формат CSV ==="
echo exit | python3 src/main.py --vfs tests/vfs_bad_format.csv

echo -e "\n=== Тест 6: Стартовый скрипт ==="
echo exit | python3 src/main.py --vfs tests/vfs_deep.csv --script tests/vfs_script.txt
