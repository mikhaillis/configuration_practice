@echo off
chcp 65001 > nul

echo === Этап 1: интерактивный прототип (парсер, заглушки через VFS, ошибки) ===
python src\main.py --script tests\stage1_script.txt

echo.
echo === Этап 1: проверка кавычек и неизвестной команды ===
(
echo ls "my folder"
echo cd "path with spaces"
echo badcmd
echo exit
) | python src\main.py

pause
