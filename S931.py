import tkinter as tk
from tkinter import ttk, messagebox
import csv, os

file = "farmers.csv"
farmers = []
def show(data=farmers):
    table.delete(*table.get_children())
    for i, f in enumerate(data, 1):
        table.insert("", "end", iid=str(i-1), values=(i, *f))

def save():
    with open(file, "w", newline="") as f:
        csv.writer(f).writerows([["Name","Age","Crop","Contact"]] + farmers)

def add():
    f = [name.get(), age.get(), crop.get(), contact.get()]
    if "" in f:
        messagebox.showwarning("Warning", "Fill all fields!")
    else:
        farmers.append(f); save(); show(); clear()

def search():
    word = name.get().lower()
    if word == "all":
        show()
    else:
        show([f for f in farmers if word in f[0].lower()])

def delete():
    x = table.selection()
    if x:
        farmers.pop(int(x[0])); save(); show()

def update():
    x = table.selection()
    if x:
        farmers[int(x[0])] = [name.get(), age.get(), crop.get(), contact.get()]
        save(); show()

def clear():
    name.delete(0,"end"); age.delete(0,"end"); crop.set(""); contact.delete(0,"end")

def count():
    messagebox.showinfo("Farmers", "Total Farmers: " + str(len(farmers)))

def load():
    if os.path.exists(file):
        with open(file) as f: farmers.extend(list(csv.reader(f))[1:])
    show()

# ---------- UI ----------

win = tk.Tk() 
win.title("🌾 Farmer Management System")
win.geometry("800x520")
win.configure(bg="#E8F5E9")

tk.Label(win, text="🌾 FARMER MANAGEMENT SYSTEM 🌾",
         font=("Arial",20,"bold"), bg="#2E7D32", fg="white").pack(fill="x",pady=10)

box = tk.Frame(win,bg="#E8F5E9")
box.pack(pady=10)

for i,text in enumerate(["Name","Age","Crop","Contact"]):
    tk.Label(box,text=text,bg="#E8F5E9",
             font=("Arial",11,"bold")).grid(row=i,column=0,pady=6)

name = tk.Entry(box,width=25)
age = tk.Entry(box,width=25)
crop = ttk.Combobox(box,values=["Rice","Wheat","Cotton","Maize","Sugarcane","Vegetables"],width=22)
contact = tk.Entry(box,width=25)

name.grid(row=0,column=1); age.grid(row=1,column=1)
crop.grid(row=2,column=1); contact.grid(row=3,column=1)

btn = tk.Frame(win,bg="#E8F5E9")
btn.pack(pady=8)

for text,command,color in [
    ("➕ Add",add,"#81C784"),("🔍 Search",search,"#64B5F6"),
    ("✏ Update",update,"#FFD54F"),("🗑 Delete",delete,"#EF9A9A"),
    ("🧹 Clear",clear,"#BDBDBD"),("🔢 Count",count,"#A5D6A7")]:
    tk.Button(btn,text=text,command=command,bg=color,
              width=10,font=("Arial",9,"bold")).pack(side="left",padx=3)

table = ttk.Treeview(win,columns=("ID","Name","Age","Crop","Contact"),
                     show="headings",height=10)

for c in ("ID","Name","Age","Crop","Contact"):
    table.heading(c,text=c)
    table.column(c,width=140)

table.pack(fill="both",expand=True,padx=20,pady=10)

load()
win.mainloop()
