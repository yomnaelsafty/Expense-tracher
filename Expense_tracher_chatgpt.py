import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests

# ------------------ Helper Functions ------------------ #

def get_exchange_rate(currency):
    if currency == "USD":
        return 1.0
    try:
        url = f"https://api.exchangerate.host/latest?base={currency}&symbols=USD"
        return requests.get(url).json()["rates"]["USD"]
    except Exception as e:
        messagebox.showerror("Error", f"Currency conversion failed: {e}")
        return 0.0

def validate_inputs():
    try:
        float(amount.get())
    except ValueError:
        messagebox.showwarning("تحذير", "من فضلك أدخل رقمًا صحيحًا في خانة المبلغ.")
        return False

    if not all([currency.get(), category.get(), payment_method.get(), date.get()]):
        messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول.")
        return False

    try:
        datetime.strptime(date.get(), "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("تحذير", "يرجى كتابة التاريخ بالصيغة YYYY-MM-DD.")
        return False

    return True

def clear_inputs():
    amount_entry.delete(0, tk.END)
    currency.set("EGP")
    category.set("Saving")
    payment_method.set("Cash")
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

def calculate_total_usd():
    total = 0
    for item in tree.get_children():
        vals = tree.item(item, "values")
        if vals[0] == "Total":
            continue
        try:
            total += float(vals[1]) * get_exchange_rate(vals[2])
        except:
            continue
    return total

def add_expense():
    if not validate_inputs():
        return

    for item in tree.get_children():
        if tree.item(item, "values")[0] == "Total":
            tree.delete(item)

    tree.insert("", "end", values=(
        len(tree.get_children()) + 1,
        amount.get(),
        currency.get(),
        category.get(),
        payment_method.get(),
        date.get()
    ))

    total = calculate_total_usd()
    tree.insert("", "end", values=("Total", f"{total:.2f}", "USD", "", "", ""), tags=("total",))
    tree.tag_configure("total", background="lightyellow", font=("Arial", 10, "bold"))

    clear_inputs()

# ------------------ GUI Setup ------------------ #

root = tk.Tk()
root.title("💰 Expense Tracker App")
root.geometry("1050x700")
root.configure(bg="#f0f4f7")

# ------- Title ------- #
tk.Label(root, text="Expense Tracker", font=("Arial", 24, "bold"), bg="#f0f4f7", fg="#333").pack(pady=15)

# ------- Main Frame ------- #
form_frame = tk.Frame(root, bg="white", bd=2, relief="ridge", padx=20, pady=20)
form_frame.pack(pady=10)

# -------- Input Fields -------- #
def create_labeled_widget(parent, label_text, widget, row):
    tk.Label(parent, text=label_text, font=("Arial", 12), bg="white").grid(row=row, column=0, sticky="w", pady=8)
    widget.grid(row=row, column=1, pady=8, padx=10, sticky="w")

amount = tk.StringVar()
currency = tk.StringVar(value="EGP")
category = tk.StringVar(value="Saving")
payment_method = tk.StringVar(value="Cash")
date = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))

amount_entry = tk.Entry(form_frame, textvariable=amount, width=30)
create_labeled_widget(form_frame, "💵 Amount (e.g., 100.50):", amount_entry, 0)

currency_menu = ttk.Combobox(form_frame, textvariable=currency, values=["USD", "EUR", "GBP", "EGP", "SAR"], state="readonly", width=28)
create_labeled_widget(form_frame, "💱 Currency:", currency_menu, 1)

category_menu = ttk.Combobox(form_frame, textvariable=category, values=["Saving", "Food", "Transportation", "Education", "Clothes", "House bills", "Charity", "Life Expenses"], state="readonly", width=28)
create_labeled_widget(form_frame, "📂 Category:", category_menu, 2)

payment_menu = ttk.Combobox(form_frame, textvariable=payment_method, values=["Cash", "Credit Card", "Paypal"], state="readonly", width=28)
create_labeled_widget(form_frame, "💳 Payment Method:", payment_menu, 3)

date_entry = tk.Entry(form_frame, textvariable=date, width=30)
create_labeled_widget(form_frame, "📅 Date (YYYY-MM-DD):", date_entry, 4)

# -------- Button -------- #
add_btn = tk.Button(form_frame, text="➕ Add Expense", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, command=add_expense)
add_btn.grid(row=5, column=1, pady=15)

# -------- Treeview Table -------- #
columns = ("#", "amount", "currency", "category", "payment", "date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
style.configure("Treeview", font=("Arial", 10), rowheight=30)

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, width=160 if col != "#" else 50, anchor=tk.CENTER)

tree.pack(pady=20, padx=30)

root.mainloop()
