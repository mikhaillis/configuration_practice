from parser import parse_command
from commands import execute_command
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





    



    

        