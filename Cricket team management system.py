import tkinter as tk
from tkinter import messagebox

players = []

def add_player():
    name, role, age = e1.get(), e2.get(), e3.get()
    if not name or not role or not age:
        messagebox.showerror("Error", "All fields required")
        return
    players.append(f"{name} - {role} - {age}")
    listbox.insert(tk.END, players[-1])
    e1.delete(0,'end'); e2.delete(0,'end'); e3.delete(0,'end')

def delete_player():
    try:
        idx = listbox.curselection()[0]
        listbox.delete(idx); players.pop(idx)
    except:
        messagebox.showwarning("Select a player")

root = tk.Tk()
root.title("Cricket Team Manager")

tk.Label(root, text="Name").pack()
e1 = tk.Entry(root); e1.pack()

tk.Label(root, text="Role").pack()
e2 = tk.Entry(root); e2.pack()

tk.Label(root, text="Age").pack()
e3 = tk.Entry(root); e3.pack()

tk.Button(root, text="Add Player", command=add_player).pack(pady=5)
listbox = tk.Listbox(root, width=40, height=8); listbox.pack()

tk.Button(root, text="Delete Player", command=delete_player).pack(pady=5)

root.mainloop()
