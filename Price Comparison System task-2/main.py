import streamlit as st
import requests

st.set_page_config(page_title="Price Comparison App", page_icon="🛒")

st.title("🛒 E-Commerce Price Comparison System")
st.write("Compare product prices from multiple e-commerce websites")

product_name = st.text_input(
    "Enter product name",
    placeholder="e.g. laptop, shirt, bag"
)

results = []

# ---------------- FakeStore API ----------------
def fetch_fakestore(product):
    url = "https://fakestoreapi.com/products"
    data = requests.get(url).json()
    for item in data:
        if product.lower() in item["title"].lower():
            return {
                "website": "FakeStore",
                "price": item["price"]
            }
    return None

# ---------------- DummyJSON API ----------------
def fetch_dummyjson(product):
    url = f"https://dummyjson.com/products/search?q={product}"
    data = requests.get(url).json()
    if data.get("products"):
        return {
            "website": "DummyShop",
            "price": data["products"][0]["price"]
        }
    return None

# ---------------- Platzi API ----------------
def fetch_platzi(product):
    url = "https://api.escuelajs.co/api/v1/products"
    data = requests.get(url).json()
    for item in data:
        if product.lower() in item["title"].lower():
            return {
                "website": "PlatziStore",
                "price": item["price"]
            }
    return None

# ---------------- Search Button ----------------
if st.button("Search Product"):

    # ✅ FIXED HERE
    if product_name.strip() == "":
        st.warning("Please enter a product name")
        st.stop()

    fs = fetch_fakestore(product_name)
    dj = fetch_dummyjson(product_name)
    ps = fetch_platzi(product_name)

    if fs:
        results.append(fs)
    if dj:
        results.append(dj)
    if ps:
        results.append(ps)

    if not results:
        st.error("No product found on any website")
    else:
        st.subheader("🔎 Price Comparison Results")

        for r in results:
            st.write(f"🛍 **{r['website']}** — 💲 {r['price']}")

        best = min(results, key=lambda x: x["price"])

        st.success(
            f"🏆 BEST PRICE: 💲{best['price']} on {best['website']}"
        )
