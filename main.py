from flask import Flask, render_template, redirect, session, url_for
import pymysql 
from dotenv import load_dotenv
import os

load_dotenv()
db_config = {
    "host": os.getenv('db_host'),
    "user": os.getenv('db_user'),
    "password": os.getenv('db_password'),
    "database": os.getenv('db_db')
}

def connect_to_db(config):
    try:
        conn=pymysql.connect(**config)
        print("success")
        return conn
    except pymysql.Error as e:
        print(f"failledi {e}")


conn = connect_to_db(db_config)



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
    totalprice = sum(item['price'] for item in cart_items)
    return render_template('index.html', products=PRODUCTS, cart_items=cart_items,totalprice=totalprice)


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

@app.route('/checkout', methods=['POST'])
def checkout():
    cart_items = session.get('cart', [])

    if not cart_items:
        return redirect(url_for('index'))
    
    totalprice = sum(item['price'] for item in cart_items)

    order_names = ", ".join([item['name'] for item in cart_items])

    if len(order_names) > 100:
        order_names = order_names[:97] + "..."

    cursor = conn.cursor()
    sql = "INSERT INTO final_order (name, totalprice) VALUES (%s, %s)"
    cursor.execute(sql, (order_names, totalprice))

    conn.commit()

    session.pop('cart', None)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)