import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Database Setup
conn = sqlite3.connect("crm_gui.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    interaction_type TEXT,
    interaction_date TEXT,
    notes TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
""")
conn.commit()

# Functions for Customer Management
def add_customer():
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()

    if not name or not email:
        messagebox.showerror("Input Error", "Name and Email are required.")
        return

    cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    conn.commit()
    messagebox.showinfo("Success", "Customer added successfully.")
    view_customers()

def view_customers():
    for row in customer_tree.get_children():
        customer_tree.delete(row)
    cursor.execute("SELECT * FROM customers")
    for customer in cursor.fetchall():
        customer_tree.insert("", "end", values=customer)

def delete_customer():
    selected = customer_tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "No customer selected.")
        return

    customer_id = customer_tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    messagebox.showinfo("Success", "Customer deleted successfully.")
    view_customers()

# Functions for Interaction Management
def add_interaction():
    customer_id = customer_id_var.get()
    interaction_type = interaction_type_var.get()
    interaction_date = interaction_date_var.get()
    notes = notes_var.get()

    if not customer_id or not interaction_type:
        messagebox.showerror("Input Error", "Customer ID and Interaction Type are required.")
        return

    cursor.execute("INSERT INTO interactions (customer_id, interaction_type, interaction_date, notes) VALUES (?, ?, ?, ?)",
                   (customer_id, interaction_type, interaction_date, notes))
    conn.commit()
    messagebox.showinfo("Success", "Interaction added successfully.")
    view_interactions()

def view_interactions():
    for row in interaction_tree.get_children():
        interaction_tree.delete(row)
    cursor.execute("SELECT * FROM interactions")
    for interaction in cursor.fetchall():
        interaction_tree.insert("", "end", values=interaction)

# CRM Summary
def crm_summary():
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM interactions")
    interaction_count = cursor.fetchone()[0]

    messagebox.showinfo("CRM Summary", f"Total Customers: {customer_count}\nTotal Interactions: {interaction_count}")

# GUI Setup
root = tk.Tk()
img=PhotoImage(file='C:/Users/91830/Desktop/INTERNSHIP/pic.png')
root.iconphoto(False,img)

root.title("Customer Relationship Management System")
root.geometry("1100x850")

# Variables
name_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
customer_id_var = tk.StringVar()
interaction_type_var = tk.StringVar()
interaction_date_var = tk.StringVar()
notes_var = tk.StringVar()

# Customer Management Frame
customer_frame = tk.LabelFrame(root, text="Customer Management", padx=10, pady=10)
customer_frame.pack(fill="both", expand="yes", padx=20, pady=8)

tk.Label(customer_frame, text="Name").grid(row=0, column=0)
tk.Entry(customer_frame, textvariable=name_var).grid(row=0, column=1)

tk.Label(customer_frame, text="Email").grid(row=1, column=0)
tk.Entry(customer_frame, textvariable=email_var).grid(row=1, column=1)

tk.Label(customer_frame, text="Phone").grid(row=2, column=0)
tk.Entry(customer_frame, textvariable=phone_var).grid(row=2, column=1)

tk.Button(customer_frame, text="Add Customer", command=add_customer).grid(row=3, column=0, columnspan=2)
tk.Button(customer_frame, text="Delete Selected Customer", command=delete_customer).grid(row=4, column=0, columnspan=2)

# Customer TreeView
customer_tree = ttk.Treeview(customer_frame, columns=("ID", "Name", "Email", "Phone"), show="headings")
customer_tree.heading("ID", text="ID")
customer_tree.heading("Name", text="Name")
customer_tree.heading("Email", text="Email")
customer_tree.heading("Phone", text="Phone")
customer_tree.grid(row=5, column=0, columnspan=2)

# Interaction Management Frame
interaction_frame = tk.LabelFrame(root, text="Interaction Management", padx=10, pady=10)
interaction_frame.pack(fill="both", expand="yes", padx=20, pady=8)

tk.Label(interaction_frame, text="Customer ID").grid(row=0, column=0)
tk.Entry(interaction_frame, textvariable=customer_id_var).grid(row=0, column=1)

tk.Label(interaction_frame, text="Interaction Type").grid(row=1, column=0)
tk.Entry(interaction_frame, textvariable=interaction_type_var).grid(row=1, column=1)

tk.Label(interaction_frame, text="Date").grid(row=2, column=0)
tk.Entry(interaction_frame, textvariable=interaction_date_var).grid(row=2, column=1)

tk.Label(interaction_frame, text="Notes").grid(row=3, column=0)
tk.Entry(interaction_frame, textvariable=notes_var).grid(row=3, column=1)

tk.Button(interaction_frame, text="Add Interaction", command=add_interaction).grid(row=4, column=0, columnspan=2)

# Interaction TreeView
interaction_tree = ttk.Treeview(interaction_frame, columns=("ID", "Customer ID", "Type", "Date", "Notes"), show="headings")
interaction_tree.heading("ID", text="ID")
interaction_tree.heading("Customer ID", text="Customer ID")
interaction_tree.heading("Type", text="Type")
interaction_tree.heading("Date", text="Date")
interaction_tree.heading("Notes", text="Notes")
interaction_tree.grid(row=5, column=0, columnspan=2)

# CRM Summary Button
tk.Button(root, text="Show CRM Summary", command=crm_summary).pack(pady=10)

# Initial view load
view_customers()
view_interactions()

# Run the application
root.mainloop()
conn.close()
