#!/bin/bash

echo "=== Этап 5: полный прогон cp через стартовый скрипт ==="
echo exit | python3 src/main.py --vfs tests/vfs_deep.csv --script tests/stage5_script.txt

echo -e "\n=== Этап 5: режимы cp (файл-файл, в каталог, перезапись) ==="
printf "ls\ncp file1.txt copy_a.txt\nls\ncp alpha.txt docs/\nls docs\ncp file1.txt alpha.txt\nwc alpha.txt\nexit\n" \
  | python3 src/main.py --vfs tests/vfs_deep.csv

echo -e "\n=== Этап 5: ошибки cp ==="
printf "cp\ncp only_one\ncp missing.txt out.txt\ncp docs out.txt\nexit\n" \
  | python3 src/main.py --vfs tests/vfs_deep.csv
