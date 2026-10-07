@echo off
chcp 65001 > nul

echo === Этап 4: полный прогон ls/cd/wc/who/tail (+ флаги ls) ===
echo exit | python src\main.py --vfs tests\vfs_deep.csv --script tests\stage4_script.txt

echo.
echo === Этап 4: флаги ls -l -h -a ===
(
echo ls
echo ls -a
echo ls -l
echo ls -lh
echo ls -lah
echo exit
) | python src\main.py --vfs tests\vfs_deep.csv

echo.
echo === Этап 4: wc / who / tail ===
(
echo who
echo wc file1.txt
echo tail -n 2 file1.txt
echo exit
) | python src\main.py --vfs tests\vfs_deep.csv

pause
