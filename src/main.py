import argparse
import sys

from commands import execute_command, set_config
from parser import parse_command
from vfs import CURRENT_PATH, VFS_TREE, load_vfs


def get_prompt() -> str:
    path_str = "/" + "/".join(CURRENT_PATH)
    return f"vfs:{path_str}> "


def run_script(script_path: str) -> None:
    """Выполняет стартовый скрипт; останавливается на ошибке."""
    try:
        with open(script_path, "r", encoding="utf-8-sig") as file:
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
        print(f"Ошибка: файл скрипта не найден: {script_path}")
    except OSError as err:
        print(f"Ошибка доступа к файлу: {err}")


def run_repl() -> None:
    """Интерактивный цикл ввода команд."""
    while True:
        try:
            command = input(get_prompt())
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из эмулятора.")
            sys.exit(0)

        try:
            tokens = parse_command(command)
            if not tokens:
                continue
            execute_command(tokens[0], tokens[1:])
        except ValueError as err:
            print(f"ошибка ввода: {err}")


def parse_args() -> dict:
    parser = argparse.ArgumentParser(
        description="Эмулятор командной строки ОС"
    )
    parser.add_argument(
        "--vfs",
        type=str,
        help="Путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        type=str,
        help="Путь к стартовому скрипту",
    )
    return vars(parser.parse_args())


def main() -> None:
    args_dict = parse_args()

    print(f"стартовые аргументы:\n {args_dict}")
    set_config(args_dict)

    if args_dict.get("vfs"):
        VFS_TREE.update(load_vfs(args_dict["vfs"]))
    else:
        VFS_TREE.update({"type": "dir", "children": {}})

    script_path = args_dict.get("script")
    if script_path:
        run_script(script_path)

    run_repl()


if __name__ == "__main__":
    main()
