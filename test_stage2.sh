#!/bin/bash

echo "=== Тест 1: Запуск без параметров ==="
echo exit | python3 src/main.py

echo -e "\n=== Тест 2: Только параметр VFS ==="
echo exit | python3 src/main.py --vfs tests/vfs_minimal.csv

echo -e "\n=== Тест 3: Только параметр script ==="
python3 src/main.py --script tests/valid_script.txt

echo -e "\n=== Тест 4: VFS + script ==="
python3 src/main.py --vfs tests/vfs_minimal.csv --script tests/valid_script.txt

echo -e "\n=== Тест 5: Скрипт с ошибкой ==="
echo exit | python3 src/main.py --vfs tests/vfs_minimal.csv --script tests/error_script.txt

echo -e "\n=== Тест 6: conf-dump ==="
printf "conf-dump\nexit\n" | python3 src/main.py --vfs tests/vfs_minimal.csv
