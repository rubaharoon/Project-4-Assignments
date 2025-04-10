import sqlite3

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            due_date TEXT,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_task_to_db(text, due_date):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (text, due_date, done) VALUES (?, ?, ?)", (text, due_date, 0))
    conn.commit()
    conn.close()

def get_all_tasks_from_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks ORDER BY due_date ASC")
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task_status(task_id, done):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET done = ? WHERE id = ?", (done, task_id))
    conn.commit()
    conn.close()

def update_task_text_due(task_id, new_text, new_date):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET text = ?, due_date = ? WHERE id = ?", (new_text, new_date, task_id))
    conn.commit()
    conn.close()

def delete_task_from_db(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
