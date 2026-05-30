

import tkinter as tk
from tkinter import messagebox
from tkinter import END
from datetime import datetime
import sqlite3

def connect_db():
    return sqlite3.connect("EXPENSES.db")

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL)''')  # Added date column
    conn.commit()
    conn.close()

def add_expenses(description, category, amount, date):
    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a numeric value for amount.")
        return
    
    # Validate the date format
    try:
        datetime.strptime(date, '%Y-%m-%d')  # Check if the date is in the correct format
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid date (YYYY-MM-DD).")
        return
    
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses (description, category, amount, date) VALUES (?, ?, ?, ?)", 
                (description, category, amount, date))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Expense added successfully.")
    desc_entry.delete(0, END)
    cat_entry.delete(0, END)
    amt_entry.delete(0, END)
    date_entry.delete(0, END)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Reset to default date
    expenses_list()
    update_amount()

def expenses_list():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    
    listbox.delete(0, tk.END)
    if not expenses:
        listbox.insert(tk.END, "No expenses recorded.")
        return
    for expense in expenses:
        listbox.insert(tk.END, f"ID: {expense[0]}, {expense[1]}, {expense[2]}, Amount: ${expense[3]:.2f}, Date: {expense[4]}")

def delete_expense():
    try:
        expense_id = int(entry_delete_id.get())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            messagebox.showerror("Error", f"No expense found with ID {expense_id}.")
        else:
            messagebox.showinfo("Success", f"Expense with ID {expense_id} deleted.")
        conn.close()
        expenses_list()
        update_amount()
        entry_delete_id.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric ID.")

def update_expense():
    try:
        expense_id = int(entry_update_id.get())
        description = update_desc_entry.get()
        category = update_cat_entry.get()
        amount = float(update_amt_entry.get())
        date = update_date_entry.get()
        
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero.")
            return

        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date (YYYY-MM-DD).")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE expenses SET description=?, category=?, amount=?, date=? WHERE id=?", 
                       (description, category, amount, date, expense_id))
        conn.commit()
        
        if cursor.rowcount == 0:
            messagebox.showerror("Error", f"No expense found with ID {expense_id}.")
        else:
            messagebox.showinfo("Success", f"Expense ID {expense_id} updated.")
        
        conn.close()
        expenses_list()
        update_amount()

        # Clear fields
        entry_update_id.delete(0, tk.END)
        update_desc_entry.delete(0, tk.END)
        update_cat_entry.delete(0, tk.END)
        update_amt_entry.delete(0, tk.END)
        update_date_entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid values.")

def update_amount():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]
    conn.close()
    
    total = total if total else 0.0
    total_entry.config(state="normal")
    total_entry.delete(0, tk.END)
    total_entry.insert(0, f"${total:.2f}")
    total_entry.config(state="readonly")

# GUI setup
root = tk.Tk()
root.geometry('800x1200')
root.title("Expense Tracker")
root.configure(bg='Skyblue')  
create_table()

head = tk.Label(root, text="Expense Tracker", font=("italic", 25, "bold"),background="skyblue")
head.pack()

# Add Expense Section
add_frame = tk.LabelFrame(root, text="Add Expense", font=("arial", 10),background="skyblue")
add_frame.pack(padx=10, pady=10, fill="x")

desc_label = tk.Label(add_frame, text="Description:")
desc_label.grid(row=0, column=0, padx=5, pady=5)
desc_entry = tk.Entry(add_frame)
desc_entry.grid(row=0, column=1, padx=5, pady=5)

cat_label = tk.Label(add_frame, text="Category:")
cat_label.grid(row=1, column=0, padx=5, pady=5)
cat_entry = tk.Entry(add_frame)
cat_entry.grid(row=1, column=1, padx=5, pady=5)

amt_label = tk.Label(add_frame, text="Amount:")
amt_label.grid(row=2, column=0, padx=5, pady=5)
amt_entry = tk.Entry(add_frame)
amt_entry.grid(row=2, column=1, padx=5, pady=5)

date_label = tk.Label(add_frame, text="Date (YYYY-MM-DD):")
date_label.grid(row=3, column=0, padx=5, pady=5)
date_entry = tk.Entry(add_frame)
date_entry.grid(row=3, column=1, padx=5, pady=5)

# Set the default date to today's date if no input is given
default_date = datetime.today().strftime('%Y-%m-%d')
date_entry.insert(0, default_date)

add_btn = tk.Button(add_frame, text="Add Expense", bg="green", fg="white", 
                    command=lambda: add_expenses(desc_entry.get(), cat_entry.get(), amt_entry.get(), date_entry.get()))
add_btn.grid(row=4, columnspan=2, padx=20, pady=10)

# List Expenses Section
list_frame = tk.LabelFrame(root, text="List Expenses", font=("arial", 10),background="skyblue")
list_frame.pack(padx=10, pady=10, fill="x")

listbox = tk.Listbox(list_frame, width=100, height=5)
listbox.pack(padx=5, pady=5)

total_label = tk.Label(list_frame, text="Total:")
total_label.pack()
total_entry = tk.Entry(list_frame, state="readonly")
total_entry.pack(padx=5, pady=5)

list_btn = tk.Button(list_frame, text="Refresh List", bg="yellow", fg="black", command=expenses_list)
list_btn.pack(pady=5)

# Delete Expense Section
delete_frame = tk.LabelFrame(root, text="Delete Expense", font=("arial", 10),background="skyblue")
delete_frame.pack(padx=10, pady=10, fill="x")

delete_id = tk.Label(delete_frame, text="Enter Expense ID to delete:")
delete_id.grid(row=0, column=0, padx=5, pady=5)
entry_delete_id = tk.Entry(delete_frame)
entry_delete_id.grid(row=0, column=1, padx=5, pady=5)

delete_btn = tk.Button(delete_frame, text="Delete Expense", bg="red", fg="white", command=delete_expense)
delete_btn.grid(row=1, columnspan=2, pady=5)

# Update Expense Section
update_frame = tk.LabelFrame(root, text="Update Expense", font=("arial", 10),background="skyblue")
update_frame.pack(padx=10, pady=10, fill="x")

tk.Label(update_frame, text="ID to Update:").grid(row=0, column=0, padx=5, pady=5)
entry_update_id = tk.Entry(update_frame)
entry_update_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(update_frame, text="New Description:").grid(row=1, column=0, padx=5, pady=5)
update_desc_entry = tk.Entry(update_frame)
update_desc_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(update_frame, text="New Category:").grid(row=2, column=0, padx=5, pady=5)
update_cat_entry = tk.Entry(update_frame)
update_cat_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(update_frame, text="New Amount:").grid(row=3, column=0, padx=5, pady=5)
update_amt_entry = tk.Entry(update_frame)
update_amt_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(update_frame, text="New Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
update_date_entry = tk.Entry(update_frame)
update_date_entry.grid(row=4, column=1, padx=5, pady=5)

update_btn = tk.Button(update_frame, text="Update Expense", bg="blue", fg="white", command=update_expense)
update_btn.grid(row=5, columnspan=2, pady=5)

root.mainloop()
