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
CLOSE_COLOR = "#D32F2F"


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

def change_password():

    username = username_entry.get().strip()
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check empty fields
    if (
        username == ""
        or old_password == ""
        or new_password == ""
        or confirm_password == ""
    ):
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    # Check new password
    if new_password != confirm_password:

        messagebox.showerror(
            "Error",
            "New password and confirm password do not match."
        )

        return

    # Check password length
    if len(new_password) < 4:

        messagebox.showwarning(
            "Warning",
            "Password must contain at least 4 characters."
        )

        return

    try:

        conn = get_connection()
        cursor = conn.cursor()

        # Check username and current password
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, old_password)
        )

        user = cursor.fetchone()

        if user is None:

            conn.close()

            messagebox.showerror(
                "Error",
                "Username or current password is incorrect."
            )

            return

        # Update password
        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE username = ?
            """,
            (new_password, username)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Password changed successfully!"
        )

        # Clear fields
        username_entry.delete(0, tk.END)
        old_password_entry.delete(0, tk.END)
        new_password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)

        username_entry.focus()

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
    "Hospital Management System - Change Password"
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


# ==========================================================
# HEADER
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
    height=520
)


# ==========================================================
# TITLE
# ==========================================================

tk.Label(
    card,
    text="CHANGE PASSWORD",
    font=("Arial", 22, "bold"),
    bg=CARD_COLOR,
    fg=PRIMARY_DARK
).pack(
    pady=(30, 5)
)


tk.Label(
    card,
    text="Update your account password",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=LABEL_COLOR
).pack(
    pady=(0, 25)
)


# ==========================================================
# USERNAME
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
# CURRENT PASSWORD
# ==========================================================

tk.Label(
    card,
    text="Current Password",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


old_password_entry = tk.Entry(
    card,
    width=32,
    font=("Arial", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    show="*"
)

old_password_entry.pack(
    padx=55,
    pady=(6, 15),
    ipady=8
)


# ==========================================================
# NEW PASSWORD
# ==========================================================

tk.Label(
    card,
    text="New Password",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


new_password_entry = tk.Entry(
    card,
    width=32,
    font=("Arial", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    show="*"
)

new_password_entry.pack(
    padx=55,
    pady=(6, 15),
    ipady=8
)


# ==========================================================
# CONFIRM PASSWORD
# ==========================================================

tk.Label(
    card,
    text="Confirm New Password",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


confirm_password_entry = tk.Entry(
    card,
    width=32,
    font=("Arial", 12),
    bg=ENTRY_BG,
    fg=TEXT_COLOR,
    relief="solid",
    bd=1,
    show="*"
)

confirm_password_entry.pack(
    padx=55,
    pady=(6, 20),
    ipady=8
)


# ==========================================================
# CHANGE PASSWORD BUTTON
# ==========================================================

change_button = tk.Button(
    card,
    text="CHANGE PASSWORD",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg=PRIMARY_COLOR,
    fg="white",
    activebackground=PRIMARY_DARK,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=change_password
)

change_button.pack(
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
    lambda event: change_password()
)


# ==========================================================
# START
# ==========================================================

username_entry.focus()

root.mainloop()