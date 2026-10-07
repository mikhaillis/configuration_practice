import base64
import csv
import sys

VFS_TREE = {}
CURRENT_PATH = []
CONST = 3


def ensure_dir_node(node: dict, name: str) -> dict:
    """Возвращает дочерний каталог, создавая его при необходимости."""
    children = node["children"]
    if name not in children:
        children[name] = {"type": "dir", "children": {}}
    return children[name]


def apply_node_type(node: dict, obj_type: str, content: str) -> None:
    """Задает тип узла и содержимое файла."""
    node["type"] = obj_type
    if obj_type == "file":
        node["content"] = content
        node.pop("children", None)
    else:
        node.setdefault("children", {})


def insert_path(root: dict, path: str, obj_type: str, content: str) -> None:
    """Вставляет путь path в дерево VFS."""
    parts = [p for p in path.split("/") if p]
    current = root

    for part in parts:
        current = ensure_dir_node(current, part)

    apply_node_type(current, obj_type, content)


def parse_vfs_row(row: list[str]) -> tuple[str, str, str]:
    """Проверяет строку CSV и возвращает path, type, content."""
    if len(row) != CONST:
        print("Ошибка загрузки VFS: неверный формат строки в CSV.")
        sys.exit(1)

    path, obj_type, content = row
    if obj_type not in ("file", "dir"):
        print(
            "Ошибка загрузки VFS: "
            f"неизвестный тип '{obj_type}'."
        )
        sys.exit(1)

    return path, obj_type, content


def load_vfs(file_path: str) -> dict:
    """Загружает VFS из CSV-файла и строит дерево в памяти."""
    root = {"type": "dir", "children": {}}

    try:
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if not row:
                    continue
                path, obj_type, content = parse_vfs_row(row)
                insert_path(root, path, obj_type, content)
    except FileNotFoundError:
        print(
            "Ошибка загрузки VFS: "
            f"файл не найден ({file_path})"
        )
        sys.exit(1)

    return root


def resolve_path(target_path: str) -> list[str]:
    """Вычисляет абсолютный путь без проверки существования."""
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

    return calc_path


def get_node_by_path(target_path: str) -> tuple[dict, list[str]]:
    """
    Находит узел VFS по пути.
    Возвращает узел и путь в виде списка сегментов.
    """
    calc_path = resolve_path(target_path)
    current = VFS_TREE

    for segment in calc_path:
        if current.get("type") != "dir":
            raise ValueError(f"Не является директорией: {segment}")
        if segment not in current.get("children", {}):
            raise ValueError(
                f"Нет такого файла или каталога: {target_path}"
            )
        current = current["children"][segment]

    return current, calc_path


def decode_file_bytes(node: dict) -> bytes:
    """Декодирует base64-содержимое файла VFS в байты."""
    if node.get("type") != "file":
        raise ValueError("Не является файлом")

    raw = node.get("content", "") or ""
    if not raw:
        return b""

    try:
        return base64.b64decode(raw, validate=False)
    except Exception:
        return raw.encode("utf-8")


def decode_file_content(node: dict) -> str:
    """Декодирует base64-содержимое файла VFS в текст."""
    data = decode_file_bytes(node)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def get_file_size(node: dict) -> int:
    """Размер файла в байтах (после декодирования)."""
    if node.get("type") != "file":
        return 0
    return len(decode_file_bytes(node))


def path_to_str(path_parts: list[str]) -> str:
    if path_parts:
        return "/" + "/".join(path_parts)
    return "/"


def get_parent_and_name(
    target_path: str,
) -> tuple[dict, str, list[str]]:
    """
    Возвращает родительский каталог, имя узла и полный путь.
    Нужен для создания и копирования файлов в памяти.
    """
    calc_path = resolve_path(target_path)
    if not calc_path:
        raise ValueError(f"Некорректный путь: {target_path}")

    name = calc_path[-1]
    parent_path = calc_path[:-1]
    parent = VFS_TREE

    for segment in parent_path:
        if parent.get("type") != "dir":
            raise ValueError(f"Не является директорией: {segment}")
        children = parent.get("children", {})
        if segment not in children:
            raise ValueError(
                f"Нет такого файла или каталога: {target_path}"
            )
        parent = children[segment]

    if parent.get("type") != "dir":
        joined = "/".join(parent_path)
        raise ValueError(f"Не является директорией: {joined}")

    return parent, name, calc_path


def basename(path: str) -> str:
    """Возвращает имя файла из пути."""
    parts = [p for p in path.split("/") if p]
    if parts:
        return parts[-1]
    return path
