# Farmer Management System (with CSV storage)
# Simple GUI project using Tkinter

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

CSV_FILE = "farmers.csv"

# List to store farmer records (acts like a temporary database)
farmer_list = []

# ---------------- CSV Functions ----------------

def load_from_csv():
    """Read existing records from the CSV file into farmer_list and the table."""
    if not os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header row
        for row in reader:
            if row:
                farmer = tuple(row)
                farmer_list.append(farmer)
                table.insert("", "end", values=farmer)


def save_to_csv():
    """Write the entire farmer_list to the CSV file (overwrites old file)."""
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Age", "Crop", "Contact"])  # header row
        writer.writerows(farmer_list)


# ---------------- Functions ----------------

def add_farmer():
    name = name_entry.get()
    age = age_entry.get()
    crop = crop_combo.get()
    contact = contact_entry.get()

    if name == "" or age == "" or crop == "" or contact == "":
        messagebox.showwarning("Missing Info", "Please fill all fields!")
        return

    farmer = (name, age, crop, contact)
    farmer_list.append(farmer)
    table.insert("", "end", values=farmer)
    save_to_csv()  # save immediately to the CSV file

    messagebox.showinfo("Success", "Farmer Added Successfully!")
    clear_fields()


def search_farmer():
    name = name_entry.get()
    found = False

    for row in table.get_children():
        table.delete(row)

    for farmer in farmer_list:
        if name.lower() in farmer[0].lower():
            table.insert("", "end", values=farmer)
            found = True

    if not found:
        messagebox.showerror("Not Found", "No farmer found with that name!")


def delete_farmer():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("No Selection", "Please select a farmer to delete!")
        return

    for item in selected:
        values = table.item(item, "values")
        farmer_list.remove(tuple(values))
        table.delete(item)

    save_to_csv()  # update the CSV file after deleting
    messagebox.showinfo("Deleted", "Farmer Deleted Successfully!")


def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    crop_combo.set("")
    contact_entry.delete(0, tk.END)


# ---------------- GUI Setup ----------------

window = tk.Tk()
window.title("Farmer Management System")
window.geometry("600x450")

# Labels and Entry Fields
tk.Label(window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1)

tk.Label(window, text="Age:").grid(row=1, column=0, padx=10, pady=10)
age_entry = tk.Entry(window)
age_entry.grid(row=1, column=1)

tk.Label(window, text="Crop:").grid(row=2, column=0, padx=10, pady=10)
crop_combo = ttk.Combobox(window, values=["Wheat", "Rice", "Sugarcane", "Cotton", "Maize", "Soybean", "Vegetables"])
crop_combo.grid(row=2, column=1)

tk.Label(window, text="Contact No:").grid(row=3, column=0, padx=10, pady=10)
contact_entry = tk.Entry(window)
contact_entry.grid(row=3, column=1)

# Buttons
tk.Button(window, text="Add Farmer", command=add_farmer, bg="lightgreen").grid(row=4, column=0, pady=10)
tk.Button(window, text="Search", command=search_farmer, bg="lightblue").grid(row=4, column=1)
tk.Button(window, text="Delete", command=delete_farmer, bg="salmon").grid(row=5, column=0)
tk.Button(window, text="Clear", command=clear_fields, bg="khaki").grid(row=5, column=1)

# Table to display farmers
table = ttk.Treeview(window, columns=("Name", "Age", "Crop", "Contact"), show="headings")
table.heading("Name", text="Name")
table.heading("Age", text="Age")
table.heading("Crop", text="Crop")
table.heading("Contact", text="Contact No")
table.grid(row=6, column=0, columnspan=2, padx=10, pady=20)

# Load any existing records from farmers.csv when the app starts
load_from_csv()

window.mainloop()
