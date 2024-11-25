from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def load_data():
    with open('rate.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('rate.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/get/<module_name>', methods=['GET'])
def get_stats(module_name):
    data = load_data()
    if module_name in data:
        return jsonify(data[module_name])
    else:
        return jsonify({'error': 'Нету такого ебырь'}), 404

@app.route('/rate/<user_id>/<module_name>/<action>', methods=['POST'])
def rate_module(user_id, module_name, action):
    data = load_data()

    if module_name not in data:
        data[module_name] = {"likes": 0, "dislikes": 0}

    if action == 'like':
        data[module_name]["likes"] += 1
    elif action == 'dislike':
        data[module_name]["dislikes"] += 1
    else:
        return jsonify({'error': 'Плаке плаке щовил анскил пашел атсуда'}), 400
    
    save_data(data)
    return jsonify({'message': 'СЭР ДА СЭР!'})

if __name__ == '__main__':
    app.run(debug=True)
