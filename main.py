import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


window = tk.Tk()

window.title("Expense Tracker")
window.geometry("800x500")

notebook = ttk.Notebook(window)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1,text="Transaction")
notebook.add(tab2,text="Report")
notebook.pack(expand=True,fill="both")

tk.Label(tab1,text="Transaction Table").pack(pady=10)

columns = ("Date", "Category", "Amount", "Description")
treeview = ttk.Treeview(tab1, columns=columns, show="headings")
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=200)

treeview.pack(expand=True,fill="both")

input_frame = ttk.Frame(tab1)
input_frame.pack(pady=50)


ttk.Label(input_frame,text="Date: ").grid(row=0,column=0)
date_entry = ttk.Entry(input_frame)
date_entry.grid(row=0,column=1)

ttk.Label(input_frame,text="Category: ").grid(row=1,column=0)
category_entry = ttk.Entry(input_frame)
category_entry.grid(row=1,column=1)

ttk.Label(input_frame,text="Amount: ").grid(row=2,column=0)
amount_entry = ttk.Entry(input_frame)
amount_entry.grid(row=2,column=1)

ttk.Label(input_frame,text="Description: ").grid(row=3,column=0)
description_entry = ttk.Entry(input_frame)
description_entry.grid(row=3,column=1)

def add_transaction():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()
    
    treeview.insert("","end",values=(date,category,amount,description)) 

def on_item_select(event):
    selected_item = treeview.selection()
    if selected_item:
        item_data = treeview.item(selected_item[0],"values")
        date_entry.delete(0,tk.END)
        date_entry.insert(0,item_data[0])

        category_entry.delete(0,tk.END)
        category_entry.insert(0,item_data[1])

        amount_entry.delete(0,tk.END)
        amount_entry.insert(0,item_data[2])

        description_entry.delete(0,tk.END)
        description_entry.insert(0,item_data[3])

def update_transaction():
    selected_item = treeview.selection()
    if selected_item:
        new_date = date_entry.get()
        new_category = category_entry.get()
        new_amount = amount_entry.get()
        new_description = description_entry.get()

        if new_date and new_category and new_amount and new_description:
            treeview.item(selected_item[0], values=(new_date, new_category, new_amount, new_description))
        else:
            messagebox.showwarning("Invalid input, all fields must be filled.")
    else:
        messagebox.showwarning("No selection, please select a row to update.")

submit = ttk.Button(input_frame,text="Add Expenses",command=add_transaction)
submit.grid(row=4,columnspan=2,pady=10)

update = ttk.Button(input_frame,text="Update Expenses",command=update_transaction)
update.grid(row=5,columnspan=3,pady=10)

treeview.bind("<ButtonRelease-1>", on_item_select)

window.mainloop()