@echo off
chcp 65001 > nul

echo === Тест 1: Минимальный VFS ===
echo exit | python src\main.py --vfs tests\vfs_minimal.csv

echo.
echo === Тест 2: Несколько файлов ===
echo exit | python src\main.py --vfs tests\vfs_multiple.csv

echo.
echo === Тест 3: Глубокая вложенность (3+ уровня) ===
echo exit | python src\main.py --vfs tests\vfs_deep.csv

echo.
echo === Тест 4: Файл VFS не найден ===
echo exit | python src\main.py --vfs tests\not_found.csv

echo.
echo === Тест 5: Неверный формат CSV ===
echo exit | python src\main.py --vfs tests\vfs_bad_format.csv

echo.
echo === Тест 6: Стартовый скрипт (команды прошлых этапов + VFS + ошибки) ===
echo exit | python src\main.py --vfs tests\vfs_deep.csv --script tests\vfs_script.txt

pause
