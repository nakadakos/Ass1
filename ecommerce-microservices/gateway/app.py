import os, requests
from flask import Flask, jsonify, render_template, request
app=Flask(__name__)
PRODUCT=os.getenv("PRODUCT_URL","http://product-service:5001")
CART=os.getenv("CART_URL","http://cart-service:5002")
ORDER=os.getenv("ORDER_URL","http://order-service:5003")
TIMEOUT=4
@app.get("/")
def home(): return render_template("index.html")
@app.get("/health")
def health(): return jsonify(status="ok",service="gateway")
@app.get("/api/products")
def products():
 try:
  r=requests.get(PRODUCT+"/products",timeout=TIMEOUT); return (r.json(),r.status_code)
 except requests.RequestException: return jsonify(error="Product service unavailable"),502
@app.get("/api/cart/<session_id>")
def cart(session_id):
 try:
  r=requests.get(CART+"/cart/"+session_id,timeout=TIMEOUT); return (r.json(),r.status_code)
 except requests.RequestException: return jsonify(error="Cart service unavailable"),502
@app.post("/api/cart/<session_id>")
def update_cart(session_id):
 try:
  r=requests.post(CART+"/cart/"+session_id,json=request.get_json(silent=True) or {},timeout=TIMEOUT); return (r.json(),r.status_code)
 except requests.RequestException: return jsonify(error="Cart service unavailable"),502
@app.delete("/api/cart/<session_id>")
def clear_cart(session_id):
 try:
  r=requests.delete(CART+"/cart/"+session_id,timeout=TIMEOUT); return (r.json(),r.status_code)
 except requests.RequestException: return jsonify(error="Cart service unavailable"),502
@app.post("/api/orders")
def create_order():
 d=request.get_json(silent=True) or {}
 try:
  r=requests.post(ORDER+"/orders",json=d,timeout=TIMEOUT); return (r.json(),r.status_code)
 except requests.RequestException: return jsonify(error="Order service unavailable"),502
@app.get("/api/orders")
def orders():
 try:
  r=requests.get(ORDER+"/orders",timeout=TIMEOUT); return (r.json(),r.status_code)
 except requests.RequestException: return jsonify(error="Order service unavailable"),502
if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
