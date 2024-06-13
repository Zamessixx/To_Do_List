
import sqlite3

DB_NAME = 'task.db'

def init_db():
    conn= sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                      (id INTEGER PRIMARY KEY, user_id INTEGER, username TEXT, task TEXT)''')

    conn.commit()
    conn.close()

def add_task(user_id, username, task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, username, task) VALUES(?,?,?)", (user_id, username, task))
    conn.commit()
    conn.close()

def get_task():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, username, task FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


