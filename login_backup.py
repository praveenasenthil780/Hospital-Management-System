import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys


# ==========================================
# LOGIN FUNCTION
# ==========================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # Check empty fields
    if username == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please enter username and password"
        )
        return

    try:

        # Connect to database
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        # Check username and password
        cursor.execute("""
            SELECT user_id, username
            FROM users
            WHERE username = ? AND password = ?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        # ==========================================
        # LOGIN SUCCESS
        # ==========================================

        if user:

            messagebox.showinfo(
                "Login Successful",
                "Welcome to Hospital Management System"
            )

            root.destroy()

            subprocess.Popen(
                [sys.executable, "main.py"]
            )

        # ==========================================
        # LOGIN FAILED
        # ==========================================

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password"
            )

            password_entry.delete(
                0,
                tk.END
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Could not connect to database.\n\n{e}"
        )


# ==========================================
# OPEN REGISTER
# ==========================================

def open_register():

    try:

        subprocess.Popen(
            [sys.executable, "register.py"]
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Could not open Register window.\n\n{e}"
        )


# ==========================================
# EXIT PROGRAM
# ==========================================

def exit_program():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:

        root.destroy()


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title(
    "Hospital Management System - Login"
)

root.geometry(
    "500x520"
)

root.resizable(
    False,
    False
)

root.configure(
    bg="white"
)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    root,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="white"
)

title_label.pack(
    pady=35
)


# ==========================================
# LOGIN HEADING
# ==========================================

login_label = tk.Label(
    root,
    text="LOGIN",
    font=("Arial", 18, "bold"),
    bg="white"
)

login_label.pack(
    pady=10
)


# ==========================================
# USERNAME LABEL
# ==========================================

username_label = tk.Label(
    root,
    text="Username",
    font=("Arial", 12),
    bg="white"
)

username_label.pack(
    pady=5
)


# ==========================================
# USERNAME ENTRY
# ==========================================

username_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12)
)

username_entry.pack(
    pady=5
)


# ==========================================
# PASSWORD LABEL
# ==========================================

password_label = tk.Label(
    root,
    text="Password",
    font=("Arial", 12),
    bg="white"
)

password_label.pack(
    pady=5
)


# ==========================================
# PASSWORD ENTRY
# ==========================================

password_entry = tk.Entry(
    root,
    width=30,
    font=("Arial", 12),
    show="*"
)

password_entry.pack(
    pady=5
)


# ==========================================
# LOGIN BUTTON
# ==========================================

login_button = tk.Button(
    root,
    text="LOGIN",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    command=login
)

login_button.pack(
    pady=20
)


# ==========================================
# REGISTER BUTTON
# ==========================================

register_button = tk.Button(
    root,
    text="REGISTER NEW USER",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    command=open_register
)

register_button.pack(
    pady=5
)


# ==========================================
# EXIT BUTTON
# ==========================================

exit_button = tk.Button(
    root,
    text="EXIT",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    command=exit_program
)

exit_button.pack(
    pady=5
)


# ==========================================
# ENTER KEY = LOGIN
# ==========================================

root.bind(
    "<Return>",
    lambda event: login()
)


# ==========================================
# START APPLICATION
# ==========================================

username_entry.focus()

root.mainloop()