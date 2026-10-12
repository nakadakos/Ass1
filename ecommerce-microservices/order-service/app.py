import os, sqlite3, json
from flask import Flask, jsonify, request
app=Flask(__name__)
DB=os.environ.get("DB_PATH","/data/orders.db")
os.makedirs(os.path.dirname(DB),exist_ok=True)
def conn():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
with conn() as c:
 c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, customer TEXT NOT NULL, items TEXT NOT NULL, total REAL NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
@app.get("/health")
def health(): return jsonify(status="ok",service="order-service")
@app.post("/orders")
def create_order():
 d=request.get_json(silent=True) or {}
 customer=str(d.get("customer","")).strip(); items=d.get("items",[])
 if not customer or not isinstance(items,list) or not items: return jsonify(error="Enter your name and add at least one product."),400
 normalized=[]; total=0.0
 for item in items:
  try: pid=int(item["id"]); qty=int(item["qty"]); name=str(item["name"]); price=float(item["price"])
  except (KeyError,TypeError,ValueError): return jsonify(error="Invalid cart item."),400
  if pid<1 or qty<1 or qty>50 or price<0: return jsonify(error="Invalid product or quantity."),400
  total+=price*qty; normalized.append({"id":pid,"name":name,"qty":qty,"price":price})
 with conn() as c:
  cur=c.execute("INSERT INTO orders(customer,items,total) VALUES(?,?,?)",(customer,json.dumps(normalized),total))
 return jsonify(message="Order placed successfully!",order_id=cur.lastrowid,total=round(total,2)),201
@app.get("/orders")
def orders():
 with conn() as c: rows=c.execute("SELECT id,customer,total,created_at FROM orders ORDER BY id DESC").fetchall()
 return jsonify([dict(r) for r in rows])
app.run(host="0.0.0.0",port=5003)
