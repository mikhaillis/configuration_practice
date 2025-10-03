#!/bin/bash

echo "=== Этап 1: интерактивный прототип ==="
python3 src/main.py --script tests/stage1_script.txt

echo -e "\n=== Этап 1: проверка кавычек и неизвестной команды ==="
printf 'ls "my folder"\ncd "path with spaces"\nbadcmd\nexit\n' | python3 src/main.py
