import sys
from vfs import get_node_by_path, CURRENT_PATH

commands_handlers = {}
pre_arguments = {}

def register(name: str):
    """Декоратор добавления функции в dict хэндлеров."""
    def decorator(func):
        commands_handlers[name] = func
        return func
    return decorator

def execute_command(name: str, args: list[str]):
    """Вызывает обработчик команды из реестра по ее имени.
    Выводит ошибку, если команда не зарегистрирована."""
    func = commands_handlers.get(name, None)
    if not func:
        raise ValueError(f"Команда не найдена: {name}")
    else:
        func(args)

def set_config(args: dict):
    for arg in args:
        pre_arguments[arg] = args[arg]

@register("conf-dump")
def init_config(args) -> None:
    print("стартовые аргументы:")
    for arg in pre_arguments:
        print(f"аргумент {arg}: {pre_arguments[arg]}")

@register("ls")
def ls(args: list[str]):
    target = args[0] if args else "."
    node, _ = get_node_by_path(target)
    
    if node["type"] == "file":
        print(target)
    else:
        children = list(node.get("children", {}).keys())
        print(" ".join(children))

@register("cd")
def cd(args: list[str]):
    target = args[0] if args else "/"
    node, calc_path = get_node_by_path(target)
    
    if node.get("type") != "dir":
        raise ValueError(f"Не является директорией: {target}")
    
    CURRENT_PATH.clear()
    CURRENT_PATH.extend(calc_path)

@register("exit")
def exit(args: list[str]):
    sys.exit(0)