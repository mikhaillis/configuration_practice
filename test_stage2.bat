@echo off
chcp 65001 > nul

echo === Тест 1: Запуск без параметров ===
echo exit | python src\main.py

echo.
echo === Тест 2: Только параметр VFS ===
echo exit | python src\main.py --vfs tests\vfs_minimal.csv

echo.
echo === Тест 3: Только параметр script ===
python src\main.py --script tests\valid_script.txt

echo.
echo === Тест 4: VFS + script ===
python src\main.py --vfs tests\vfs_minimal.csv --script tests\valid_script.txt

echo.
echo === Тест 5: Скрипт с ошибкой (остановка на первой ошибке) ===
echo exit | python src\main.py --vfs tests\vfs_minimal.csv --script tests\error_script.txt

echo.
echo === Тест 6: conf-dump ===
(
echo conf-dump
echo exit
) | python src\main.py --vfs tests\vfs_minimal.csv --script tests\valid_script.txt

pause
