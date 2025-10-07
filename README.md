# Эмулятор командной строки ОС

## 1. Общее описание
Эмулятор языка оболочки ОС, имитирующий работу в командной строке
UNIX-подобной ОС. Программа работает с виртуальной файловой системой (VFS),
загружаемой из CSV-файла в оперативную память, и поддерживает выполнение
скриптов и базовых файловых операций без реальной модификации файловой
системы хоста.

Вариант 9: `wc`, `who`, `tail` (этап 4), `cp` (этап 5).

## 2. Описание всех функций и настроек
**Параметры командной строки:**
- `--vfs` — путь к физическому расположению VFS (CSV-файл).
- `--script` — путь к стартовому скрипту.

**Поддерживаемые команды:**
- `ls [-l] [-h] [-a] [путь]` — содержимое директории
  (`-l` длинный формат, `-h` человекочитаемый размер, `-a` скрытые файлы).
- `cd [путь]` — переход в директорию.
- `exit` — завершение работы.
- `wc <файл>` — строки, слова и байты файла.
- `who` — информация о текущем пользователе.
- `tail [-n N] <файл>` — последние N строк (по умолчанию 10).
- `cp <источник> <приемник>` — копирование файла внутри VFS (только в памяти).
- `conf-dump` — вывод параметров эмулятора (ключ = значение).

## 3. Запуск и тесты по этапам

```bat
python src\main.py --vfs tests\vfs_deep.csv
python src\main.py --vfs tests\vfs_deep.csv --script tests\stage5_script.txt

test_stage1.bat
test_stage2.bat
test_stage3.bat
test_stage4.bat
test_stage5.bat
```

Аналогичные `.sh` скрипты есть для Linux/macOS.

## 4. Примеры использования

**Приглашение содержит имя VFS:**
```text
vfs:/> ls
vfs:/docs> cd work
```

**Парсер кавычек и ошибки:**
```text
vfs:/> ls "my folder"
ls: Нет такого файла или каталога: my folder
vfs:/> unknown
ошибка ввода: Команда не найдена: unknown
```

**Флаги ls:**
```text
vfs:/> ls -a
.  ..  .config  .hidden  alpha.txt  docs  file1.txt  images
vfs:/> ls -lh
-rw-r--r--  1 user  user       82B  file1.txt
```

**Команды этапа 4:**
```text
vfs:/> who
misha	pts/0	console
vfs:/> wc file1.txt
5	17	82	file1.txt
vfs:/> tail -n 2 file1.txt
of text content
for wc and tail
```

**Команда этапа 5 (`cp`, только в памяти):**
```text
vfs:/> cp file1.txt file1_copy.txt
vfs:/> ls
alpha.txt  docs  file1.txt  file1_copy.txt  images
vfs:/> cp alpha.txt docs/personal/
vfs:/> ls docs/personal
alpha.txt  notes.txt
vfs:/> cp missing.txt out.txt
Ошибка в скрипте: cp: Нет такого файла или каталога: missing.txt
```

**Стартовый скрипт** печатает и ввод, и вывод; останавливается на первой
ошибке выполнения.
