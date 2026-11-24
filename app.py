import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


# Helper function to connect to the SQL database
def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn


# 1. Create the SQL table when the app starts
with get_db() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')


# 2. Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')


# 3. API Route: Get all tasks from SQL (GET)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    rows = conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


# 4. API Route: Add a new task to SQL (POST)
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Task cannot be empty'}), 400

    conn = get_db()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added!'}), 201

# 5. API Route: Delete a task from SQL (DELETE)
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted!'})



if __name__ == '__main__':
    app.run(debug=True)
