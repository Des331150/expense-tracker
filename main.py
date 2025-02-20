
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import os
from tkinter import filedialog

def openfile():
    file_open = filedialog.askopenfilename(filetypes=[("Text file",".txt"),("CSV",".csv"),("All files",".*")],title="Open File")
    if not file_open:
        return
    try:
        if file_open.endswith(".csv"):
            with open(file_open,"r",newline="") as file:
                reader = csv.reader(file)
                header = next(reader)
                treeview.delete(*treeview.get_children())
                for row in reader:
                    treeview.insert("","end",values=(row))

        else:
            with open(file_open,"r") as file:
                treeview.delete(*treeview.get_children())
                for line in file:
                    data = line.strip().split("\t")
                    treeview.insert("","end",values=(data))

            print("File has been opened successfully")
    
    except Exception as e:
            print("Error opening file:",e)
               

def savefile():
    file_path = filedialog.asksaveasfilename(defaultextension=" .txt",filetypes=[("Text file",".txt"),("CSV",".csv"),("All files",".*")])
    if not file_path:
        return
    try:
        all_rows = []
        for item in treeview.get_children():
            row_values = treeview.item(item,"values")
            all_rows.append(row_values)

        if file_path.endswith(".csv"):
            with open(file_path,"w",newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date","Category","Amount","Description"])
                writer.writerows(all_rows)

        else:
            with open(file_path,"w") as file:
                for row in all_rows:
                    file.write("\t".join(row) + "\n")

        print("File has been saved successfully.")

    except Exception as e:
        print("Error saving file:",e)

CSV_FILE = "expenses.csv"

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date","Category","Amount","Description"])


def load_expenses():
    treeview.delete(*treeview.get_children())
    with open(CSV_FILE,"r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            treeview.insert("","end",values=row)


window = tk.Tk()

window.title("Expense Tracker")
window.geometry("800x500")

menubar = tk.Menu(window)
window.config(menu=menubar)

fileMenu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=fileMenu)
fileMenu.add_command(label="Open",command=openfile)
fileMenu.add_separator()
fileMenu.add_command(label="Save",command=savefile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=quit)


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
    
    if not date or not category or not amount or not description:
        messagebox.showerror("Error","Date, Category and Amount are required")
        return
    
    with open(CSV_FILE,"a",newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date,category,amount,description])

    treeview.insert("","end",values=(date,category,amount,description))
    clear_entries()


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
    clear_entries()


def delete_transaction():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error","Please select a row to delete.")
        return
    
    values = treeview.item(selected_item[0],"values")
      
    treeview.delete(selected_item[0])

    rows = []
    with open(CSV_FILE,"r") as file:
        reader = csv.reader(file)
        rows = [row for row in reader if row != list(values)]
        
    with open(CSV_FILE,"w",newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    clear_entries()


def clear_entries():
    date_entry.delete(0,tk.END)
    category_entry.delete(0,tk.END)
    amount_entry.delete(0,tk.END)
    description_entry.delete(0,tk.END)


submit = ttk.Button(input_frame,text="Add Expenses",command=add_transaction)
submit.grid(row=4,columnspan=2,pady=10)

update = ttk.Button(input_frame,text="Update Expenses",command=update_transaction)
update.grid(row=5,columnspan=3,pady=5)

update = ttk.Button(input_frame,text="Delete Expenses",command=delete_transaction)
update.grid(row=6,columnspan=4,pady=5)

treeview.bind("<ButtonRelease-1>", on_item_select)

initialize_csv()
load_expenses()

window.mainloop()