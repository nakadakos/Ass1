import os, sqlite3
from flask import Flask, jsonify
app=Flask(__name__)
DB=os.environ.get("DB_PATH","/data/products.db")
os.makedirs(os.path.dirname(DB),exist_ok=True)
PRODUCTS=[
 {"id":1,"name":"Wireless Headphones","price":1499.0,"emoji":"🎧"},
 {"id":2,"name":"Smart Watch","price":2199.0,"emoji":"⌚"},
 {"id":3,"name":"Backpack","price":899.0,"emoji":"🎒"},
 {"id":4,"name":"Bluetooth Speaker","price":1299.0,"emoji":"🔊"}]
def init():
 with sqlite3.connect(DB) as c:
  c.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,name TEXT,price REAL,emoji TEXT)")
  if c.execute("SELECT COUNT(*) FROM products").fetchone()[0]==0:
   c.executemany("INSERT INTO products VALUES(?,?,?,?)",[(p["id"],p["name"],p["price"],p["emoji"]) for p in PRODUCTS])
init()
@app.get("/health")
def health(): return jsonify(status="ok",service="product-service")
@app.get("/products")
def products():
 with sqlite3.connect(DB) as c:
  c.row_factory=sqlite3.Row
  return jsonify([dict(r) for r in c.execute("SELECT * FROM products ORDER BY id")])
@app.get("/products/<int:pid>")
def product(pid):
 with sqlite3.connect(DB) as c:
  c.row_factory=sqlite3.Row
  row=c.execute("SELECT * FROM products WHERE id=?",(pid,)).fetchone()
  return (jsonify(dict(row)),200) if row else (jsonify(error="Product not found"),404)
app.run(host="0.0.0.0",port=5001)
