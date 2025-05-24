import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import requests


total_usd = 0.0

def get_exchange_rate(from_currency):

    if from_currency == "USD":
        return 1.0

    try:
        url = f"https://api.exchangerate.host/latest?base={from_currency}&symbols=USD"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"]["USD"]
        return rate
    except Exception as e:
        messagebox.showerror("Error", f"Currency conversion failed: {e}")
        return 0.0


def add_expense():

    amount_value = amount.get()
    currency_value = currency.get()
    category_value = category.get()
    payment_value = payment_method.get()
    date_value = date.get()

    try:
        float(amount_value)
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid number in Amount.")
        return

    if not currency_value or not category_value or not payment_value  or not date_value:
        messagebox.showwarning("Warning", "Please fill in all the fields.")
        return
    
    try:
        datetime.strptime(date_value,  "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Warning", "Please enter a valid date in YYYY-MM-DD format.")
        return
    
    for item in tree.get_children():
        if tree.item(item, "values")[0] == "Total":
            tree.delete(item)

    tree.insert("", "end", values=(len(tree.get_children())+1, amount_value, currency_value, category_value, payment_value, date_value))

    total_usd = 0

    for item in tree.get_children():
        values = tree.item(item, "values")
        if values[0] == "Total":
            continue
        try:
            amt = float(values[1])
            curr = values[2]
            rate = get_exchange_rate(curr)
            total_usd += amt * rate
        except:
            continue

    tree.insert("", "end", values=("Total", f"{total_usd:.2f}", "USD", "", "", ""), tags=("total",))
    tree.tag_configure("total", background="yellow", font=("Arial", 10, "bold"))

    amount.delete(0, tk.END)
    currency.set("EGP")
    category.set("Saving")
    payment_method.set("Cash")
    date.delete(0, tk.END)
    date.insert(0, datetime.today().strftime("%Y-%m-%d"))



root = tk.Tk()
root.title("Expense Tracker app")
root.geometry("1000x650")

tk.Label(root, text="Amount:", font=("Arial",12)).grid(column=0, row=0,padx=20,pady=5,sticky="ew")
amount =tk.Entry(root,width=30)
amount.grid(column=1, row=0, padx=0, pady=5, sticky="w")

tk.Label(root, text="Currency:", font=("Arial",12)).grid(column=0, row=1,padx=20,pady=5,sticky="ew")
currency_options = ["USD", "EUR", "GBP", "EGP", "SAR"]
currency = ttk.Combobox(root,values=currency_options,state="readonly",width=28)
currency.grid(column=1, row=1, padx=0, pady=5, sticky="w")
currency.set("EGP")

tk.Label(root, text="Category", font=("Arial",12)).grid(column=0, row=2,padx=20,pady=5,sticky="ew")
category_options =["Saving", "Food", "Transportation","Education","Clothes", "House bills","Charity","Life Expenses"]
category = ttk.Combobox(root,values=category_options,state="readonly",width=28 )
category.grid(column=1, row=2, padx=0, pady=5, sticky="w")
category.set("Saving")

tk.Label(root, text="Payment Method", font=("Arial",12)).grid(column=0, row=3,padx=20,pady=5,sticky="ew")
payment_options = ["Cash", "Credit Card", "Paypal"]
payment_method = ttk.Combobox(root,values=payment_options,state="readonly",width=28 )
payment_method.grid(column=1, row=3, padx=0, pady=5, sticky="w")
payment_method.set("Cash")

tk.Label(root, text="Date", font=("Arial",12)).grid(column=0, row=4,padx=20,pady=5,sticky="ew")
date =tk.Entry(root, width=30)
date.grid(column=1, row=4, padx=0, pady=5, sticky="w")
date.insert(0, datetime.today().strftime("%Y-%m-%d"))


style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial",10, "bold"))

columns =  ("#" ,"amount", "currency", "category", "payment", "date")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("amount", text="Amount")
tree.heading("currency", text="Currency")
tree.heading("category", text="Category")
tree.heading("payment", text="Payment")
tree.heading("date", text="Date")
tree.column("#", width=50, anchor=tk.CENTER)
tree.column("amount", width=180, anchor=tk.CENTER)
tree.column("currency", width=180, anchor=tk.CENTER)
tree.column("category", width=200, anchor=tk.CENTER)
tree.column("payment", width=200, anchor=tk.CENTER)
tree.column("date", width=200, anchor=tk.CENTER)
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)


add_btn = tk.Button(root, text="Add Expense",font=("Arial",12), command=add_expense)
add_btn.grid(column=1, row=5, padx=30, pady=5, sticky="w")


root.mainloop()