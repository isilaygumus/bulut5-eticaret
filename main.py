from flask import Flask, render_template, redirect, session, url_for
import mysql.connector 
from dotenv import load_dotenv
import os

load_dotenv()
db_config = {
    "host": os.getenv('db_host'),
    "user": os.getenv('db_user'),
    "password": os.getenv('db_password'),
    "database": os.getenv('db_db')
}

app = Flask(__name__)

app.secret_key = 'bulut5-sirri'

PRODUCTS = [
    {"id": 1, "name": "bulut bilişim kitabı", "price": 150, "image": "https://picsum.photos/200"},
    {"id": 2, "name": "kablosuz mouse", "price": 350, "image": "https://picsum.photos/200"},
    {"id": 3, "name": "mekanik klavye", "price": 1200, "image": "https://picsum.photos/200"},
]


@app.route('/')
def index():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('index.html', products=PRODUCTS, cart_items=cart_items,total_price=total_price)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    for product in PRODUCTS:
        if product['id'] == product_id:
            session['cart'].append(product)
            session.modified = True
            break
    return redirect(url_for('index'))


@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)