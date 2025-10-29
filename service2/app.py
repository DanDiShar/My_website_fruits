from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

cart = []

@app.route('/cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    fruit_id = data.get('fruit_id')
    quantity = data.get('quantity', 1)
    
    # Получаем информацию о фрукте из первого сервиса
    try:
        response = requests.get(f'http://fruits-service:5000/fruits/{fruit_id}')
        if response.status_code == 200:
            fruit = response.json()
            cart_item = {
                "fruit": fruit,
                "quantity": quantity,
                "total_price": fruit['price'] * quantity
            }
            cart.append(cart_item)
            return jsonify(cart_item)
        else:
            return jsonify({"error": "Fruit not found"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Cannot connect to fruits service"}), 503

@app.route('/cart/total', methods=['GET'])
def get_total():
    total = sum(item['total_price'] for item in cart)
    return jsonify({"total_price": total, "items_count": len(cart)})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "cart-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)