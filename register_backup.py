import tkinter as tk
from tkinter import messagebox
import sqlite3


# ==========================================
# REGISTER USER
# ==========================================

def register_user():

    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm_password = confirm_entry.get().strip()

    # Check empty fields
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields"
        )
        return

    # Check password
    if password != confirm_password:
        messagebox.showerror(
            "Error",
            "Passwords do not match"
        )
        return

    # Connect database
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
        """, (username, password))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "User registered successfully!"
        )

        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        confirm_entry.delete(0, tk.END)

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Username already exists"
        )

    finally:

        conn.close()


# ==========================================
# CLOSE
# ==========================================

def close_window():
    root.destroy()


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Hospital Management System - Register"
)

root.geometry(
    "500x500"
)

root.configure(
    bg="white"
)


# ==========================================
# TITLE
# ==========================================

tk.Label(
    root,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="white"
).pack(pady=35)


tk.Label(
    root,
    text="CREATE NEW USER",
    font=("Arial", 18, "bold"),
    bg="white"
).pack(pady=10)


# ==========================================
# USERNAME
# ==========================================

tk.Label(
    root,
    text="Username",
    font=("Arial", 12),
    bg="white"
).pack(pady=5)

username_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)

username_entry.pack(pady=5)


# ==========================================
# PASSWORD
# ==========================================

tk.Label(
    root,
    text="Password",
    font=("Arial", 12),
    bg="white"
).pack(pady=5)

password_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12),
    show="*"
)

password_entry.pack(pady=5)


# ==========================================
# CONFIRM PASSWORD
# ==========================================

tk.Label(
    root,
    text="Confirm Password",
    font=("Arial", 12),
    bg="white"
).pack(pady=5)

confirm_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12),
    show="*"
)

confirm_entry.pack(pady=5)


# ==========================================
# REGISTER BUTTON
# ==========================================

tk.Button(
    root,
    text="REGISTER",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    command=register_user
).pack(pady=20)


# ==========================================
# CLOSE BUTTON
# ==========================================

tk.Button(
    root,
    text="CLOSE",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    command=close_window
).pack()


# ==========================================
# START
# ==========================================

root.mainloop()