import argparse
from parser import parse_command
from commands import execute_command, init_config, set_config

parser = argparse.ArgumentParser(description="Эмулятор командной строки ОС")
parser.add_argument("--vfs", type=str, help="Путь к физическому расположению VFS")
parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
args = parser.parse_args()
args = vars(args)
print(f"стартовые аргументы:\n {args}")

set_config(args)

script_path = args["script"]
if script_path:
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue

                print(f"vfs> {line}")

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
    vfs = "vfs>"
    comand = input(vfs)

    try:
        tokens = parse_command(comand)
        if not tokens:
            continue
        execute_command(tokens[0], tokens[1:])
    except ValueError as e:
        print(f"ошибка ввода: {e}")
        continue
