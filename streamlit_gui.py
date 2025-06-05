
import streamlit as st
import json
import os
from datetime import datetime

EXPENSES_FILE = "expenses.json"
BUDGET_FILE = "budget.json"

def load_data(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_expense(date, amount, category, note):
    return {"date": date, "amount": amount, "category": category, "note": note}

# 載入資料
expenses = load_data(EXPENSES_FILE)
budget_data = load_data(BUDGET_FILE)

if "records" not in expenses:
    expenses["records"] = []

# Streamlit 介面
st.title("📒 簡易記帳系統")

# 預算設定
st.sidebar.header("💰 預算設定")
budget = st.sidebar.number_input("輸入每月預算", min_value=0.0, value=budget_data.get("monthly_budget", 0.0))
if st.sidebar.button("儲存預算"):
    budget_data["monthly_budget"] = budget
    save_data(budget_data, BUDGET_FILE)
    st.sidebar.success("預算已更新！")

# 新增支出
st.header("➕ 新增支出")
with st.form("add_expense_form"):
    date = st.date_input("日期", value=datetime.today())
    amount = st.number_input("金額", min_value=0.0)
    category = st.text_input("類別（如 餐飲、交通）")
    note = st.text_input("備註")
    submitted = st.form_submit_button("新增")

    if submitted:
        new_record = add_expense(str(date), amount, category, note)
        expenses["records"].append(new_record)
        save_data(expenses, EXPENSES_FILE)
        st.success("支出已新增！")

# 顯示支出紀錄
st.header("📋 支出紀錄")
if expenses["records"]:
    st.dataframe(expenses["records"])
    total_spent = sum(item["amount"] for item in expenses["records"])
    st.metric("💸 總支出", f"{total_spent:.2f} 元")
    if "monthly_budget" in budget_data and budget_data["monthly_budget"] > 0:
        remaining = budget_data["monthly_budget"] - total_spent
        st.metric("📊 剩餘預算", f"{remaining:.2f} 元")
else:
    st.info("尚無任何支出紀錄。")
