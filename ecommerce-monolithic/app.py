import os
import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "/data/monolith.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 1499.0, "emoji": "🎧"},
    {"id": 2, "name": "Smart Watch", "price": 2199.0, "emoji": "⌚"},
    {"id": 3, "name": "Backpack", "price": 899.0, "emoji": "🎒"},
    {"id": 4, "name": "Bluetooth Speaker", "price": 1299.0, "emoji": "🔊"},
]

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

init_db()

@app.get("/")
def home():
    return render_template("index.html", architecture="Monolithic Architecture")

@app.get("/health")
def health():
    return jsonify(status="ok", service="monolith")

@app.get("/api/products")
def products():
    return jsonify(PRODUCTS)

@app.post("/api/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    customer = str(data.get("customer", "")).strip()
    items = data.get("items", [])
    if not customer or not isinstance(items, list) or not items:
        return jsonify(error="Enter your name and add at least one product."), 400
    lookup = {p["id"]: p for p in PRODUCTS}
    total = 0.0
    normalized = []
    for item in items:
        try:
            pid, qty = int(item["id"]), int(item["qty"])
        except (KeyError, TypeError, ValueError):
            return jsonify(error="Invalid cart item."), 400
        if pid not in lookup or qty < 1 or qty > 50:
            return jsonify(error="Invalid product or quantity."), 400
        p = lookup[pid]
        total += p["price"] * qty
        normalized.append({"id": pid, "name": p["name"], "qty": qty, "price": p["price"]})
    with connect() as con:
        cur = con.execute("INSERT INTO orders(customer, items, total) VALUES (?, ?, ?)",
                          (customer, __import__("json").dumps(normalized), total))
        order_id = cur.lastrowid
    return jsonify(message="Order placed successfully!", order_id=order_id, total=round(total, 2)), 201

@app.get("/api/orders")
def list_orders():
    with connect() as con:
        rows = con.execute("SELECT id, customer, total, created_at FROM orders ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
