from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    return jsonify(tasks), 200

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid task data'}), 400
    task_text = data['text']
    task_id = random.randint(1, 1000000)

    try:
        with open('tasks.json', 'r') as f:
            existing_tasks = json.load(f)
            print("Existing tasks loaded:", existing_tasks)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_tasks = []

    task = {"id": task_id, "text": task_text, "completed": False}
    existing_tasks.append(task)

    with open('tasks.json', 'w') as f:
        json.dump(existing_tasks, f)

    return jsonify({"message": "Task added successfully", "task": task}), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data or 'completed' not in data:
        return jsonify({'error': 'Invalid task data'}), 400
    completed = data['completed']

    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            print("Existing tasks loaded:", tasks)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'error': 'Task not found'}), 404

    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = completed
            with open('tasks.json', 'w') as f:
                json.dump(tasks, f)
            return jsonify({'message': 'Task updated successfully'}), 200

    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        with open('tasks.json', 'r') as f:
            tasks = json.load(f)
            print("Existing tasks loaded:", tasks)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'error': 'Task not found'}), 404

    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            with open('tasks.json', 'w') as f:
                json.dump(tasks, f)
            return jsonify({'message': 'Task deleted successfully'}), 200

    return jsonify({'error': 'Task not found'}), 404


app.run(debug=True)