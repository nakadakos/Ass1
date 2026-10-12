import os, sqlite3
from flask import Flask, jsonify, request
app=Flask(__name__)
DB=os.environ.get("DB_PATH","/data/cart.db")
os.makedirs(os.path.dirname(DB),exist_ok=True)
def conn():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with conn() as c:
 c.execute("CREATE TABLE IF NOT EXISTS cart_items(id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, UNIQUE(session_id,product_id))")
@app.get("/health")
def health(): return jsonify(status="ok",service="cart-service")
@app.get("/cart/<session_id>")
def get_cart(session_id):
 with conn() as c: rows=c.execute("SELECT product_id,quantity FROM cart_items WHERE session_id=?",(session_id,)).fetchall()
 return jsonify([dict(r) for r in rows])
@app.post("/cart/<session_id>")
def update_cart(session_id):
 data=request.get_json(silent=True) or {}
 try: pid=int(data.get("product_id")); qty=int(data.get("quantity"))
 except (TypeError,ValueError): return jsonify(error="product_id and quantity must be integers"),400
 if pid<1 or qty<0 or qty>50: return jsonify(error="Invalid product or quantity"),400
 with conn() as c:
  if qty==0: c.execute("DELETE FROM cart_items WHERE session_id=? AND product_id=?",(session_id,pid))
  else: c.execute("INSERT INTO cart_items(session_id,product_id,quantity) VALUES(?,?,?) ON CONFLICT(session_id,product_id) DO UPDATE SET quantity=excluded.quantity",(session_id,pid,qty))
 return jsonify(message="Cart updated",product_id=pid,quantity=qty)
@app.delete("/cart/<session_id>")
def clear_cart(session_id):
 with conn() as c: c.execute("DELETE FROM cart_items WHERE session_id=?",(session_id,))
 return jsonify(message="Cart cleared")
app.run(host="0.0.0.0",port=5002)
