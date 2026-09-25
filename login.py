import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F3F8FC"
HEADER_COLOR = "#006064"
DARK_BLUE = "#01579B"
BLUE = "#0277BD"

WHITE = "#FFFFFF"
TEXT_COLOR = "#17324D"
GRAY = "#607D8B"

GREEN = "#2E7D32"
RED = "#C62828"


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # Check empty fields
    if username == "" or password == "":
        messagebox.showerror(
            "Login Error",
            "Please enter username and password."
        )
        return

    try:

        conn = sqlite3.connect(
            "hospital.db",
            timeout=10
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, username
            FROM users
            WHERE username = ? AND password = ?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        # =================================================
        # LOGIN SUCCESS
        # =================================================

        if user:

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {username}!\n\n"
                "Hospital Management System"
            )

            root.destroy()

            subprocess.Popen(
                [sys.executable, "main.py"]
            )

        # =================================================
        # LOGIN FAILED
        # =================================================

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )

            password_entry.delete(
                0,
                tk.END
            )

            password_entry.focus()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Could not connect to database.\n\n{e}"
        )


# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(show="")
        show_password_button.config(text="🙈 Hide")

    else:

        password_entry.config(show="*")
        show_password_button.config(text="👁 Show")


# =========================================================
# OPEN REGISTER
# =========================================================

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


# =========================================================
# OPEN CHANGE PASSWORD
# =========================================================

def open_change_password():

    try:

        subprocess.Popen(
            [sys.executable, "change_password.py"]
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Could not open Change Password window.\n\n{e}"
        )


# =========================================================
# EXIT PROGRAM
# =========================================================

def exit_program():

    answer = messagebox.askyesno(
        "Exit Application",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Login"
)

root.geometry(
    "650x700"
)

root.resizable(
    False,
    False
)

root.configure(
    bg=BG_COLOR
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=120
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


# Hospital icon

tk.Label(
    header,
    text="🏥",
    font=("Segoe UI Emoji", 42),
    bg=HEADER_COLOR,
    fg=WHITE
).pack(
    side="left",
    padx=(45, 18)
)


# Header text

header_text = tk.Frame(
    header,
    bg=HEADER_COLOR
)

header_text.pack(
    side="left"
)


tk.Label(
    header_text,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Segoe UI", 20, "bold"),
    bg=HEADER_COLOR,
    fg=WHITE
).pack(
    anchor="w"
)


tk.Label(
    header_text,
    text="Healthcare Administration System",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#B2EBF2"
).pack(
    anchor="w",
    pady=(3, 0)
)


# =========================================================
# LOGIN CARD
# =========================================================

login_card = tk.Frame(
    root,
    bg=WHITE,
    bd=1,
    relief="solid"
)

login_card.place(
    x=105,
    y=155,
    width=440,
    height=450
)


# =========================================================
# LOGIN ICON
# =========================================================

tk.Label(
    login_card,
    text="🔐",
    font=("Segoe UI Emoji", 42),
    bg=WHITE,
    fg=DARK_BLUE
).pack(
    pady=(25, 5)
)


# =========================================================
# LOGIN TITLE
# =========================================================

tk.Label(
    login_card,
    text="USER LOGIN",
    font=("Segoe UI", 23, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
).pack(
    pady=(0, 5)
)


tk.Label(
    login_card,
    text="Sign in to access the hospital dashboard",
    font=("Segoe UI", 9),
    bg=WHITE,
    fg=GRAY
).pack(
    pady=(0, 20)
)


# =========================================================
# USERNAME
# =========================================================

tk.Label(
    login_card,
    text="👤  Username",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


username_entry = tk.Entry(
    login_card,
    width=30,
    font=("Segoe UI", 11),
    relief="solid",
    bd=1
)

username_entry.pack(
    padx=55,
    pady=(5, 15),
    ipady=7
)


# =========================================================
# PASSWORD
# =========================================================

tk.Label(
    login_card,
    text="🔒  Password",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


password_frame = tk.Frame(
    login_card,
    bg=WHITE
)

password_frame.pack(
    padx=55,
    pady=(5, 5)
)


password_entry = tk.Entry(
    password_frame,
    width=24,
    font=("Segoe UI", 11),
    relief="solid",
    bd=1,
    show="*"
)

password_entry.pack(
    side="left",
    ipady=7
)


show_password_button = tk.Button(
    password_frame,
    text="👁 Show",
    font=("Segoe UI", 8, "bold"),
    bg=WHITE,
    fg=BLUE,
    relief="flat",
    cursor="hand2",
    command=toggle_password
)

show_password_button.pack(
    side="left",
    padx=(5, 0)
)


# =========================================================
# LOGIN BUTTON
# =========================================================

login_button = tk.Button(
    login_card,
    text="🔐  LOGIN",
    width=30,
    height=2,
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=login
)

login_button.pack(
    pady=(15, 8)
)


# =========================================================
# REGISTER + CHANGE PASSWORD
# =========================================================

small_button_frame = tk.Frame(
    login_card,
    bg=WHITE
)

small_button_frame.pack(
    pady=5
)


register_button = tk.Button(
    small_button_frame,
    text="📝 Register User",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=GREEN,
    relief="flat",
    cursor="hand2",
    command=open_register
)

register_button.grid(
    row=0,
    column=0,
    padx=10
)


change_password_button = tk.Button(
    small_button_frame,
    text="🔑 Change Password",
    font=("Segoe UI", 9, "bold"),
    bg=WHITE,
    fg=DARK_BLUE,
    relief="flat",
    cursor="hand2",
    command=open_change_password
)

change_password_button.grid(
    row=0,
    column=1,
    padx=10
)


# =========================================================
# EXIT BUTTON
# =========================================================

exit_button = tk.Button(
    login_card,
    text="❌ EXIT",
    width=20,
    height=1,
    font=("Segoe UI", 9, "bold"),
    bg=RED,
    fg=WHITE,
    activebackground="#8E0000",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=exit_program
)

exit_button.pack(
    pady=(8, 5)
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    root,
    text="Hospital Management System  •  Secure Healthcare Administration",
    font=("Segoe UI", 8),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    side="bottom",
    pady=15
)


# =========================================================
# ENTER KEY = LOGIN
# =========================================================

root.bind(
    "<Return>",
    lambda event: login()
)


# =========================================================
# START
# =========================================================

username_entry.focus()

root.mainloop()