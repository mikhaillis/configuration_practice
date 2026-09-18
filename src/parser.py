def parse_command(string: str) -> list[str]:
    """
    Разделяет введенную строку на команду и аргументы.
    Поддерживает аргументы внутри двойных и одинарных кавычек.
    """
    if not string:
        return

    tokens = []
    cur_token = []
    quote_char = None

    for char in string:
        if quote_char:
            if char == quote_char:
                quote_char = None
            else:
                cur_token.append(char)
        else:
            if char in ("'", '"'):
                quote_char = char
            elif char == " ":
                if cur_token:
                    tokens.append("".join(cur_token))
                    cur_token = []
            else:
                cur_token.append(char)

    if quote_char:
        raise ValueError(f"Синтаксическая ошибка: незакрытая кавычка {quote_char}")

    if cur_token:
        tokens.append("".join(cur_token))

    return tokens