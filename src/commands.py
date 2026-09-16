import sys
commands_handlers = {}

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
    


@register("ls")
def ls(args: list[str]):
    print(f"ls: {args}")

@register("cd")
def cd(args: list[str]):
    print(f"cd: {args}")

@register("exit")
def exit(args: list[str]):
    sys.exit()