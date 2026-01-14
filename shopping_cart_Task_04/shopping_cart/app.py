from flask import Flask, render_template, session, redirect, url_for, request
import requests

app = Flask(__name__)
app.secret_key = "secret123"   # session ke liye

PRODUCT_API = "https://fakestoreapi.com/products"


# ---------------- HOME PAGE (Product List) ----------------
@app.route("/")
def index():
    products = requests.get(PRODUCT_API).json()

    if "cart" not in session:
        session["cart"] = {}

    return render_template("index.html", products=products, cart=session["cart"])


# ---------------- ADD TO CART ----------------
@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["qty"] += 1
    else:
        product = requests.get(f"{PRODUCT_API}/{product_id}").json()
        cart[str(product_id)] = {
            "title": product["title"],
            "price": product["price"],
            "qty": 1
        }

    session["cart"] = cart
    return redirect(url_for("index"))


# ---------------- REMOVE FROM CART ----------------
@app.route("/remove/<product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(product_id, None)
    session["cart"] = cart
    return redirect(url_for("cart"))


# ---------------- UPDATE QUANTITY ----------------
@app.route("/update", methods=["POST"])
def update_quantity():
    cart = session.get("cart", {})
    for pid in cart:
        qty = int(request.form.get(pid))
        if qty <= 0:
            cart.pop(pid)
        else:
            cart[pid]["qty"] = qty

    session["cart"] = cart
    return redirect(url_for("cart"))


# ---------------- CART PAGE ----------------
@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    total = sum(item["price"] * item["qty"] for item in cart.values())
    return render_template("cart.html", cart=cart, total=total)


if __name__ == "__main__":
    app.run(debug=True)
