import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Budget & Expense Tracker", page_icon="💰", layout="centered")

# --- App Title
st.title("💰 Budget & Expense Tracker")

# --- Session State for storing transactions
if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

# --- Input Form
with st.form("transaction_form"):
    col1, col2 = st.columns(2)
    with col1:
        t_type = st.selectbox("Type", ["Income", "Expense"])
        amount = st.number_input("Amount", min_value=0.0, step=100.0, format="%.2f")
    with col2:
        category = st.selectbox("Category", ["Food", "Transport", "Rent", "Entertainment", "Salary", "Other"])
        note = st.text_input("Note")
    submitted = st.form_submit_button("➕ Add Transaction")

if submitted and amount > 0:
    st.session_state["transactions"].append({
        "Type": t_type,
        "Amount": amount,
        "Category": category,
        "Note": note
    })
    st.success("Transaction added!")

# --- Display Data
if st.session_state["transactions"]:
    df = pd.DataFrame(st.session_state["transactions"])
    st.subheader("📋 Transactions")
    st.dataframe(df)

    # --- Balance
    income = df[df["Type"]=="Income"]["Amount"].sum()
    expense = df[df["Type"]=="Expense"]["Amount"].sum()
    balance = income - expense
    st.metric("💵 Balance", f"${balance:,.2f}", delta=f"{income-expense:.2f}")

    # --- Charts
    st.subheader("📊 Expense Breakdown")
    expense_df = df[df["Type"]=="Expense"].groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    if not expense_df.empty:
        expense_df.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)
    else:
        st.info("No expenses yet!")
else:
    st.info("No transactions yet. Add one above!")
