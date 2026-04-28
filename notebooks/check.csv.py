# Просто читаем первые 3 строки файла как текст
with open("../data/raw/part_ayaulym_done.csv", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        print(f"Rows{i}: {line[:200]}")
        if i >= 2:
            break