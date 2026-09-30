import argparse
import sys
from parser import parse_command
from commands import execute_command, set_config
from vfs import load_vfs, VFS_TREE, CURRENT_PATH

def get_prompt() -> str:
    path_str = "/" + "/".join(CURRENT_PATH)
    return f"vfs:{path_str}> "

parser = argparse.ArgumentParser(description="Эмулятор командной строки ОС")
parser.add_argument("--vfs", type=str, help="Путь к физическому расположению VFS")
parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
args = parser.parse_args()
args_dict = vars(args)

print(f"стартовые аргументы:\n {args_dict}")
set_config(args_dict)

if args_dict.get("vfs"):
    VFS_TREE.update(load_vfs(args_dict["vfs"]))
else:
    VFS_TREE.update({"type": "dir", "children": {}})

script_path = args_dict.get("script")

if script_path:
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue

                print(f"{get_prompt()}{line}")

                try:
                    tokens = parse_command(line)
                    if not tokens:
                        continue
                    execute_command(tokens[0], tokens[1:])
                except ValueError as err:
                    print(f"Ошибка в скрипте: {err}")
                    break

    except FileNotFoundError:
        print(f"Ошибка: файл стартового скрипта не найден: {script_path}")
    except OSError as err:
        print(f"Ошибка доступа к файлу: {err}")

while True:
    try:
        comand = input(get_prompt())
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из эмулятора.")
        sys.exit(0)

    try:
        tokens = parse_command(comand)
        if not tokens:
            continue
        execute_command(tokens[0], tokens[1:])
    except ValueError as e:
        print(f"ошибка ввода: {e}")
        continue