import copy
import getpass
import sys

CONSTANT1 = 1024
CONSTANT2 = 2

from vfs import (
    CURRENT_PATH,
    basename,
    decode_file_content,
    get_file_size,
    get_node_by_path,
    get_parent_and_name,
    path_to_str,
)

commands_handlers = {}
pre_arguments = {}


def register(name: str):
    """Декоратор добавления функции в dict хэндлеров."""

    def decorator(func):
        commands_handlers[name] = func
        return func

    return decorator


def execute_command(name: str, args: list[str]):
    """Вызывает обработчик команды из реестра по ее имени."""
    func = commands_handlers.get(name)
    if not func:
        raise ValueError(f"Команда не найдена: {name}")
    func(args)


def set_config(args: dict):
    for arg in args:
        pre_arguments[arg] = args[arg]


def human_size(num: int) -> str:
    """Форматирует размер в человекочитаемый вид (-h)."""
    units = ["B", "K", "M", "G", "T"]
    size = float(num)
    for unit in units:
        if size < CONSTANT1 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)}B"
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{int(num)}B"


def apply_ls_flag(flag: str, state: dict) -> None:
    """Применяет один символ флага ls к состоянию."""
    if flag == "l":
        state["long"] = True
    elif flag == "h":
        state["human"] = True
    elif flag == "a":
        state["all"] = True
    else:
        raise ValueError(f"ls: неизвестный флаг: -{flag}")


def apply_ls_flag_group(arg: str, state: dict) -> None:
    """Применяет группу флагов вида -lah."""
    for ch in arg[1:]:
        apply_ls_flag(ch, state)


def parse_ls_args(args: list[str]) -> tuple[dict, list[str]]:
    """Разбирает флаги ls: -l, -h, -a и пути."""
    state = {"long": False, "human": False, "all": False}
    targets = []

    for arg in args:
        is_flag = (
            arg.startswith("-")
            and len(arg) > 1
            and not arg.startswith("--")
        )
        if is_flag:
            apply_ls_flag_group(arg, state)
        else:
            targets.append(arg)

    return state, targets


def format_ls_entry(name: str, node: dict, state: dict) -> str:
    """Форматирует одну запись ls."""
    if not state["long"]:
        return name

    if node.get("type") == "dir":
        mode = "drwxr-xr-x"
        size = 0
    else:
        mode = "-rw-r--r--"
        size = get_file_size(node)

    if state["human"]:
        size_str = human_size(size)
    else:
        size_str = str(size)

    return f"{mode}  1 user  user  {size_str:>8}  {name}"


def collect_ls_entries(node: dict, state: dict) -> list[tuple[str, dict]]:
    """Собирает список имен для вывода ls."""
    children = node.get("children", {})
    names = sorted(children.keys())
    entries = []

    if state["all"]:
        entries.append((".", node))
        entries.append(("..", node))

    for name in names:
        if state["all"] or not name.startswith("."):
            entries.append((name, children[name]))

    return entries


def print_ls_entries(entries: list[tuple[str, dict]], state: dict) -> None:
    """Печатает собранные записи ls."""
    if state["long"]:
        for name, child in entries:
            print(format_ls_entry(name, child, state))
        return

    visible = [name for name, _ in entries]
    print("  ".join(visible) if visible else "")


def print_ls_target(
    target: str,
    state: dict,
    show_header: bool,
    blank_before: bool,
) -> None:
    """Печатает результат ls для одного пути."""
    try:
        node, path_parts = get_node_by_path(target)
    except ValueError as err:
        print(f"ls: {err}")
        return

    if node.get("type") == "file":
        name = path_parts[-1] if path_parts else target
        print(format_ls_entry(name, node, state))
        return

    if show_header:
        if blank_before:
            print()
        print(f"{path_to_str(path_parts)}:")

    entries = collect_ls_entries(node, state)
    print_ls_entries(entries, state)


@register("conf-dump")
def init_config(args) -> None:
    print("стартовые аргументы:")
    for arg in pre_arguments:
        print(f"{arg} = {pre_arguments[arg]}")


@register("ls")
def ls(args: list[str]):
    state, targets = parse_ls_args(args)
    if not targets:
        targets = ["."]

    multi = len(targets) > 1
    for idx, target in enumerate(targets):
        print_ls_target(target, state, multi, idx > 0)


@register("cd")
def cd(args: list[str]):
    target = args[0] if args else "/"

    if len(args) > 1:
        raise ValueError("cd: слишком много аргументов")

    try:
        node, path_parts = get_node_by_path(target)
    except ValueError as err:
        print(f"cd: {err}")
        return

    if node.get("type") != "dir":
        print(f"cd: не является директорией: {target}")
        return

    CURRENT_PATH.clear()
    CURRENT_PATH.extend(path_parts)


@register("exit")
def exit_cmd(args: list[str]):
    sys.exit(0)


def count_wc_stats(text: str) -> tuple[int, int, int]:
    """Считает строки, слова и байты текста."""
    lines = text.count("\n")
    if text and not text.endswith("\n"):
        lines += 1
    words = len(text.split())
    bytes_count = len(text.encode("utf-8"))
    return lines, words, bytes_count


@register("wc")
def wc(args: list[str]):
    """Подсчет строк, слов и байт в файле."""
    if not args:
        raise ValueError("wc: укажите файл")

    for target in args:
        try:
            node, path_parts = get_node_by_path(target)
        except ValueError as err:
            print(f"wc: {err}")
            continue

        if node.get("type") != "file":
            print(f"wc: {target}: это каталог")
            continue

        text = decode_file_content(node)
        lines, words, bytes_count = count_wc_stats(text)
        name = path_parts[-1] if path_parts else target
        print(f"{lines}\t{words}\t{bytes_count}\t{name}")


@register("who")
def who(args: list[str]):
    """Вывод информации о текущем пользователе."""
    if args:
        raise ValueError("who: команда не принимает аргументы")

    try:
        username = getpass.getuser()
    except Exception:
        username = "user"

    print(f"{username}\tpts/0\tconsole")


def parse_tail_n(token: str) -> int:
    """Преобразует строку в число строк для tail."""
    try:
        return int(token)
    except ValueError as err:
        raise ValueError("tail: неверное число строк") from err


def parse_tail_args(args: list[str]) -> tuple[int, list[str]]:
    """Разбирает аргументы tail: -n N и список файлов."""
    n = 10
    files = []
    i = 0

    while i < len(args):
        arg = args[i]
        if arg == "-n" and i + 1 < len(args):
            n = parse_tail_n(args[i + 1])
            i += CONSTANT2
        elif arg.startswith("-n") and len(arg) > 2:
            n = parse_tail_n(arg[2:])
            i += 1
        elif arg.startswith("-") and arg[1:].isdigit():
            n = int(arg[1:])
            i += 1
        else:
            files.append(arg)
            i += 1

    return n, files


def print_tail_file(target: str, n: int) -> None:
    """Печатает последние n строк одного файла."""
    try:
        node, _ = get_node_by_path(target)
    except ValueError as err:
        print(f"tail: {err}")
        return

    if node.get("type") != "file":
        print(f"tail: {target}: это каталог")
        return

    text = decode_file_content(node)
    for line in text.splitlines()[-n:]:
        print(line)


@register("tail")
def tail(args: list[str]):
    """Вывод последних строк файла. По умолчанию 10 строк."""
    n, files = parse_tail_args(args)
    if not files:
        raise ValueError("tail: укажите файл")

    for target in files:
        print_tail_file(target, n)


def resolve_cp_destination(src: str, dst: str) -> str:
    """Если dst — каталог, копируем внутрь с именем источника."""
    try:
        dst_node, _ = get_node_by_path(dst)
    except ValueError:
        return dst

    if dst_node.get("type") == "dir":
        return dst.rstrip("/") + "/" + basename(src)
    return dst


def copy_file_in_vfs(src: str, dst: str) -> None:
    """Копирует файл внутри VFS только в оперативной памяти."""
    try:
        src_node, _ = get_node_by_path(src)
    except ValueError as err:
        raise ValueError(f"cp: {err}") from err

    if src_node.get("type") != "file":
        raise ValueError(
            f"cp: {src}: копирование каталогов не поддерживается"
        )

    dst = resolve_cp_destination(src, dst)

    try:
        parent, name, _ = get_parent_and_name(dst)
    except ValueError as err:
        raise ValueError(f"cp: {err}") from err

    existing = parent.get("children", {}).get(name)
    if existing is not None and existing.get("type") == "dir":
        raise ValueError(
            f"cp: {dst}: нельзя перезаписать каталог файлом"
        )

    parent.setdefault("children", {})[name] = copy.deepcopy(src_node)


@register("cp")
def cp(args: list[str]):
    """Копирование файла внутри VFS (только в памяти)."""
    if len(args) != 2:
        raise ValueError(
            "cp: использование: cp <источник> <приемник>"
        )

    copy_file_in_vfs(args[0], args[1])
