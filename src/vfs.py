import csv
import sys

VFS_TREE = {}
CURRENT_PATH = []

def load_vfs(file_path: str) -> dict:
    """Загружает VFS из CSV-файла и строит иерархическое дерево в памяти."""
    root = {"type": "dir", "children": {}}
    
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            
            for row in reader:
                if not row:
                    continue
                
                try:
                    path, obj_type, content = row
                except ValueError:
                    print("Ошибка загрузки VFS: неверный формат строки в CSV.")
                    sys.exit(1)
                
                parts = [p for p in path.split("/") if p]
                current = root
                
                for part in parts:
                    if part not in current["children"]:
                        current["children"][part] = {"type": "dir", "children": {}}
                    current = current["children"][part]
                
                current["type"] = obj_type
                if obj_type == "file":
                    current["content"] = content
                    
    except FileNotFoundError:
        print(f"Ошибка загрузки VFS: файл не найден ({file_path})")
        sys.exit(1)

    return root

def get_node_by_path(target_path: str) -> tuple[dict, list[str]]:
    """
    Вычисляет абсолютный путь и находит соответствующий узел в VFS.
    Возвращает кортеж из целевого узла и вычисленного пути в виде списка.
    Генерирует ValueError при обращении к несуществующему файлу или папке.
    """
    if target_path.startswith("/"):
        calc_path = []
    else:
        calc_path = CURRENT_PATH.copy()

    for part in target_path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if calc_path:
                calc_path.pop()
        else:
            calc_path.append(part)

    current = VFS_TREE
    for segment in calc_path:
        if current.get("type") != "dir":
            raise ValueError(f"Не является директорией: {segment}")
        if segment not in current.get("children", {}):
            raise ValueError(f"Нет такого файла или каталога: {target_path}")
        current = current["children"][segment]

    return current, calc_path