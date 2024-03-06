import sqlite3
from datetime import datetime

# Create SQLite database and tasks table
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        priority TEXT,
        due_date DATE,
        completed BOOLEAN
    )
''')
conn.commit()

class ToDoList:
    def add_task(self, task, priority='medium', due_date=None):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task, priority, due_date, completed) VALUES (?, ?, ?, ?)',
                       (task, priority, due_date, 0))
        conn.commit()
        conn.close()

    def remove_task(self, task_id):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

    def mark_completed(self, task_id):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

    def display_tasks(self):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        conn.close()

        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                task_id, task_desc, priority, due_date, completed = task
                status = "Completed" if completed else "Not Completed"
                print(f"{task_id}. {task_desc} - Priority: {priority} - Due Date: {due_date} - {status}")

# Example usage:
todo_list = ToDoList()

while True:
    print("\nCommand Options:")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Completed")
    print("4. Display Tasks")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        task = input("Enter task: ")
        priority = input("Enter priority (high/medium/low): ")
        due_date_str = input("Enter due date (YYYY-MM-DD), or leave empty: ")
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
        todo_list.add_task(task, priority, due_date)

    elif choice == '2':
        task_id = int(input("Enter the task ID to remove: "))
        todo_list.remove_task(task_id)

    elif choice == '3':
        task_id = int(input("Enter the task ID to mark as completed: "))
        todo_list.mark_completed(task_id)

    elif choice == '4':
        todo_list.display_tasks()

    elif choice == '5':
        print("Exiting. Your tasks are saved in the database.")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
