@echo off
chcp 65001 > nul
echo === Тест 1: Запуск без параметров ===

@echo off
echo === Тест 1: Запуск без параметров ===
echo exit | python src/main.py

echo.
echo === Тест 2: Только параметр VFS ===
echo exit | python src/main.py --vfs test.csv

echo.
echo === Тест 3: Запуск с корректным скриптом ===
python src/main.py --script tests\valid_script.txt

echo.
echo === Тест 4: Запуск со скриптом, содержащим синтаксическую ошибку ===
echo exit | python src\main.py --vfs test.csv --script tests\error_script.txt
pause