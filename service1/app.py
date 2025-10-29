from flask import Flask, jsonify
import requests

app = Flask(__name__)

# База данных фруктов
fruits = [
    {"id": 1, "name": "Apple", "color": "red", "price": 1.5},
    {"id": 2, "name": "Banana", "color": "yellow", "price": 0.8},
    {"id": 3, "name": "Orange", "color": "orange", "price": 1.2}
]

@app.route('/fruits', methods=['GET'])
def get_fruits():
    return jsonify(fruits)

@app.route('/fruits/<int:fruit_id>', methods=['GET'])
def get_fruit(fruit_id):
    fruit = next((f for f in fruits if f['id'] == fruit_id), None)
    if fruit:
        return jsonify(fruit)
    return jsonify({"error": "Fruit not found"}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "fruits-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)