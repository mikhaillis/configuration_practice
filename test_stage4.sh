#!/bin/bash

echo "=== Этап 4: полный прогон ls/cd/wc/who/tail (+ флаги ls) ==="
echo exit | python3 src/main.py --vfs tests/vfs_deep.csv --script tests/stage4_script.txt

echo -e "\n=== Этап 4: флаги ls -l -h -a ==="
printf "ls\nls -a\nls -l\nls -lh\nls -lah\nexit\n" | python3 src/main.py --vfs tests/vfs_deep.csv

echo -e "\n=== Этап 4: wc / who / tail ==="
printf "who\nwc file1.txt\ntail -n 2 file1.txt\nexit\n" | python3 src/main.py --vfs tests/vfs_deep.csv
