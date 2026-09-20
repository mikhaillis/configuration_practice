import sys
commands_handlers = {}
pre_arguments = {}

def register(name: str):
    """декоратор добавления функции в dict хэндлеров"""

    def decorator(func):
        commands_handlers[name] = func
        return func

    return decorator

def execute_command(name:str, args: list[str]):
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
    print(f"ls: {args}")

@register("cd")
def cd(args: list[str]):
    print(f"cd: {args}")

@register("exit")
def exit(args: list[str]):
    sys.exit()