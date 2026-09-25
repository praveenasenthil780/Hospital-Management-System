import tkinter as tk
from tkinter import messagebox
import sqlite3


# ==========================================================
# COLORS
# ==========================================================

BG_COLOR = "#EAF4F8"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#1976D2"
PRIMARY_DARK = "#0D47A1"
TEXT_COLOR = "#263238"
LABEL_COLOR = "#455A64"
ENTRY_BG = "#F5F9FC"
BORDER_COLOR = "#B0BEC5"
SUCCESS_COLOR = "#2E7D32"
CLOSE_COLOR = "#D32F2F"


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================================
# REGISTER USER
# ==========================================================

def register_user():

    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm_password = confirm_entry.get().strip()

    # Check empty fields
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror(
            "Error",
            "Please fill all fields."
        )
        return

    # Check password
    if password != confirm_password:
        messagebox.showerror(
            "Error",
            "Passwords do not match."
        )
        return

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # Make sure users table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
        """, (username, password))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Registration Successful",
            "User registered successfully!"
        )

        # Clear fields
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        confirm_entry.delete(0, tk.END)

        username_entry.focus()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Registration Error",
            "Username already exists."
        )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Database error:\n\n{e}"
        )


# ==========================================================
# CLOSE WINDOW
# ==========================================================

def close_window():

    answer = messagebox.askyesno(
        "Close",
        "Are you sure you want to close?"
    )

    if answer:
        root.destroy()


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Register"
)

root.geometry(
    "650x650"
)

root.resizable(
    False,
    False
)

root.configure(
    bg=BG_COLOR
)


# ==========================================================
# TOP HEADER
# ==========================================================

header = tk.Frame(
    root,
    bg=PRIMARY_DARK,
    height=100
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


# Hospital icon
tk.Label(
    header,
    text="🏥",
    font=("Arial", 35),
    bg=PRIMARY_DARK,
    fg="white"
).pack(
    side="left",
    padx=35
)


# Hospital title
tk.Label(
    header,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg=PRIMARY_DARK,
    fg="white"
).pack(
    side="left"
)


# ==========================================================
# MAIN CARD
# ==========================================================

card = tk.Frame(
    root,
    bg=CARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

card.place(
    x=100,
    y=130,
    width=450,
    height=470
)


# ==========================================================
# REGISTER TITLE
# ==========================================================

tk.Label(
    card,
    text="CREATE NEW USER",
    font=("Arial", 22, "bold"),
    bg=CARD_COLOR,
    fg=PRIMARY_DARK
).pack(
    pady=(30, 5)
)


tk.Label(
    card,
    text="Register an account to access the system",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=LABEL_COLOR
).pack(
    pady=(0, 25)
)


# ==========================================================
# USERNAME LABEL
# ==========================================================

tk.Label(
    card,
    text="Username",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


# ==========================================================
# USERNAME ENTRY
# ==========================================================

username_entry = tk.Entry(
    card,
    width=32,
    font=("Arial", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1
)

username_entry.pack(
    padx=55,
    pady=(6, 15),
    ipady=8
)


# ==========================================================
# PASSWORD LABEL
# ==========================================================

tk.Label(
    card,
    text="Password",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


# ==========================================================
# PASSWORD ENTRY
# ==========================================================

password_entry = tk.Entry(
    card,
    width=32,
    font=("Arial", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    show="*"
)

password_entry.pack(
    padx=55,
    pady=(6, 15),
    ipady=8
)


# ==========================================================
# CONFIRM PASSWORD LABEL
# ==========================================================

tk.Label(
    card,
    text="Confirm Password",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


# ==========================================================
# CONFIRM PASSWORD ENTRY
# ==========================================================

confirm_entry = tk.Entry(
    card,
    width=32,
    font=("Arial", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    show="*"
)

confirm_entry.pack(
    padx=55,
    pady=(6, 20),
    ipady=8
)


# ==========================================================
# REGISTER BUTTON
# ==========================================================

register_button = tk.Button(
    card,
    text="REGISTER",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground=PRIMARY_DARK,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=register_user
)

register_button.pack(
    pady=5
)


# ==========================================================
# CLOSE BUTTON
# ==========================================================

close_button = tk.Button(
    card,
    text="CLOSE",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg=CLOSE_COLOR,
    fg="white",
    activebackground="#B71C1C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=close_window
)

close_button.pack(
    pady=8
)


# ==========================================================
# FOOTER
# ==========================================================

tk.Label(
    root,
    text="© Hospital Management System",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg=LABEL_COLOR
).pack(
    side="bottom",
    pady=12
)


# ==========================================================
# ENTER KEY
# ==========================================================

root.bind(
    "<Return>",
    lambda event: register_user()
)


# ==========================================================
# START
# ==========================================================

username_entry.focus()

root.mainloop()