import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime
import os

# ================= CONFIG =================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
DATA_FILE = "expenses.csv"

# ================= FUNCTIONS =================
def extract_text(image):
    return pytesseract.image_to_string(image)

def extract_amount(text):
    amounts = re.findall(r'\d+\.\d{2}', text)
    return max(map(float, amounts)) if amounts else 0.0

def extract_category(text):
    text = text.lower()
    if "food" in text or "restaurant" in text:
        return "Food"
    elif "uber" in text or "fuel" in text:
        return "Transport"
    elif "mart" in text or "store" in text:
        return "Groceries"
    elif "electric" in text or "bill" in text:
        return "Utilities"
    return "Others"

def save_expense(date, amount, category):
    df = pd.DataFrame([[date, amount, category]], columns=["Date", "Amount", "Category"])
    if os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_FILE, index=False)

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, parse_dates=["Date"])
    return pd.DataFrame(columns=["Date", "Amount", "Category"])

# ================= UI =================
st.set_page_config(page_title="Receipt Expense Analyzer", layout="wide")
st.title("🧾 Smart Receipt Scanner & Expense Analyzer")

# ================= RECEIPT SCAN =================
st.header("📸 Scan Receipt")
uploaded_file = st.file_uploader("Upload Receipt Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=300)

    text = extract_text(image)
    amount = extract_amount(text)
    category = extract_category(text)

    st.subheader("📝 Extracted Data")
    st.write("**Detected Amount:** Rs", amount)
    st.write("**Category:**", category)

    if st.button("Save Expense"):
        save_expense(datetime.now(), amount, category)
        st.success("Expense Saved Successfully!")

# ================= ANALYTICS =================
st.header("📊 Monthly Expense Summary")

df = load_data()

if not df.empty:
    df["Month"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("Month")["Amount"].sum()

    st.subheader("💰 Total Monthly Spending")
    st.dataframe(monthly)

    # ================= CHART =================
    st.subheader("📈 Expense Visualization")
    fig, ax = plt.subplots()
    monthly.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount (Rs)")
    ax.set_xlabel("Month")
    st.pyplot(fig)

    # ================= CATEGORY ANALYTICS =================
    st.subheader("🧠 Spending Analytics")
    category_sum = df.groupby("Category")["Amount"].sum()

    fig2, ax2 = plt.subplots()
    category_sum.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

    # ================= ALERT SYSTEM =================
    st.subheader("🚨 Alerts")
    threshold = st.slider("Set Monthly Spending Alert (Rs)", 5000, 100000, 30000)

    if monthly.iloc[-1] > threshold:
        st.error("⚠️ Alert! You have exceeded your monthly budget.")
    else:
        st.success("✅ Spending is within budget.")

else:
    st.info("No expense data available yet.")
