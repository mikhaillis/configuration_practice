@echo off
chcp 65001 > nul

echo === Этап 5: полный прогон cp через стартовый скрипт ===
echo exit | python src\main.py --vfs tests\vfs_deep.csv --script tests\stage5_script.txt

echo.
echo === Этап 5: режимы cp (файл-файл, в каталог, перезапись) ===
(
echo ls
echo cp file1.txt copy_a.txt
echo ls
echo cp alpha.txt docs/
echo ls docs
echo cp file1.txt alpha.txt
echo wc alpha.txt
echo exit
) | python src\main.py --vfs tests\vfs_deep.csv

echo.
echo === Этап 5: ошибки cp ===
(
echo cp
echo cp only_one
echo cp missing.txt out.txt
echo cp docs out.txt
echo exit
) | python src\main.py --vfs tests\vfs_deep.csv

pause
