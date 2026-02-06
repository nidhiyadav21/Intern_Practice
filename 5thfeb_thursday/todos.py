from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Mock database (in-memory list)
todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Practice Postman", "done": True}
]

# GET all tasks
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# GET single task
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        abort(404, description="Task not found")
    return jsonify(todo), 200

# CREATE new task
@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.json or 'task' not in request.json:
        abort(400, description="Invalid data")
    new_todo = {
        "id": todos[-1]["id"] + 1,
        "task": request.json['task'],
        "done": False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# UPDATE task status
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        abort(404, description="Task not found")
    if not request.json or 'done' not in request.json:
        abort(400, description="Invalid data")
    todo['done'] = request.json['done']
    return jsonify(todo), 200

# DELETE task
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"result": True}), 200

if __name__ == "__main__":
    app.run(debug=True)
