import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# Предопределённые цитаты
quotes = [
    {"text": "Будь лучше, чем ты был вчера.", "author": "Неизвестный", "topic": "Мотивация"},
    {"text": "Жизнь — это то, что происходит, пока вы строите планы.", "author": "Джон Леннон", "topic": "Философия"},
    {"text": "Тот, кто не рискует, не пьет шампанское.", "author": "Неизвестный", "topic": "Ирония"},
    # Добавьте больше цитат по желанию
]

history = []

DATA_FILE = "history.json"

# Загрузка истории из файла
def load_history():
    global history
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

# Сохранение истории
def save_history():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Генерация случайной цитаты
def generate_quote():
    quote = random.choice(quotes)
    display_quote(quote)
    # Добавляем в историю
    history.append(quote)
    save_history()
    update_history_list()

# Отобразить выбранную цитату
def display_quote(quote):
    quote_text_var.set(f'"{quote["text"]}"\n— {quote["author"]} ({quote["topic"]})')

# Обновление списка истории
def update_history_list(filtered_quotes=None):
    listbox.delete(0, tk.END)
    quotes_to_show = filtered_quotes if filtered_quotes is not None else history
    for q in quotes_to_show:
        listbox.insert(tk.END, f'"{q["text"]}" — {q["author"]} ({q["topic"]})')

# Фильтрация по автору и теме
def apply_filter():
    author_filter = entry_author.get().strip().lower()
    topic_filter = entry_topic.get().strip().lower()

    filtered = []
    for q in history:
        if author_filter and author_filter not in q["author"].lower():
            continue
        if topic_filter and topic_filter not in q["topic"].lower():
            continue
        filtered.append(q)
    update_history_list(filtered)

# Добавление новой цитаты
def add_quote():
    text = simpledialog.askstring("Добавить цитату", "Введите текст цитаты:")
    author = simpledialog.askstring("Добавить цитату", "Введите автора:")
    topic = simpledialog.askstring("Добавить цитату", "Введите тему:")

    if not text or not author or not topic:
        messagebox.showerror("Ошибка", "Поля не должны быть пустыми.")
        return

    new_quote = {"text": text.strip(), "author": author.strip(), "topic": topic.strip()}
    quotes.append(new_quote)
    # Можно сразу добавить в историю
    history.append(new_quote)
    save_history()
    update_history_list()

# Создаем GUI
root = tk.Tk()
root.title("Random Quote Generator")

# Цитата
quote_text_var = tk.StringVar()
label_quote = tk.Label(root, textvariable=quote_text_var, wraplength=400, justify=tk.LEFT)
label_quote.pack(padx=10, pady=10)

# Кнопка "Сгенерировать цитату"
btn_generate = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(pady=5)

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
entry_author = tk.Entry(filter_frame)
entry_author.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
entry_topic = tk.Entry(filter_frame)
entry_topic.grid(row=0, column=3, padx=5)

btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=5)

btn_clear_filter = tk.Button(filter_frame, text="Сбросить", command=update_history_list)
btn_clear_filter.grid(row=0, column=5, padx=5)

# История
tk.Label(root, text="История:").pack()
listbox = tk.Listbox(root, width=70, height=10)
listbox.pack(padx=10, pady=5)

# Добавить цитату вручную
btn_add = tk.Button(root, text="Добавить цитату", command=add_quote)
btn_add.pack(pady=5)

# Загружаем историю при запуске
load_history()
update_history_list()

root.mainloop()
