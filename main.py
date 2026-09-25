import tkinter as tk
from tkinter import messagebox
import subprocess
import sys


# ==========================================================
# COLORS
# ==========================================================

BG_COLOR = "#EAF4F8"
HEADER_COLOR = "#0D47A1"
PRIMARY_COLOR = "#1976D2"
PRIMARY_DARK = "#1565C0"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#263238"
DANGER_COLOR = "#D32F2F"
GREEN_COLOR = "#2E7D32"
PURPLE_COLOR = "#6A1B9A"
ORANGE_COLOR = "#EF6C00"


# ==========================================================
# OPEN MODULE
# ==========================================================

def open_module(filename):

    try:

        subprocess.Popen(
            [sys.executable, filename]
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Unable to open {filename}\n\n{e}"
        )


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:

        root.destroy()

        try:

            subprocess.Popen(
                [sys.executable, "login.py"]
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


# ==========================================================
# EXIT
# ==========================================================

def exit_program():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:

        root.destroy()


# ==========================================================
# HOVER EFFECT
# ==========================================================

def button_enter(button, color):

    button.configure(
        bg=color
    )


def button_leave(button, color):

    button.configure(
        bg=color
    )


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Dashboard"
)

root.geometry(
    "1250x750"
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
    bg=HEADER_COLOR,
    height=110
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


# Hospital icon

tk.Label(
    header,
    text="🏥",
    font=("Arial", 38),
    bg=HEADER_COLOR,
    fg="white"
).pack(
    side="left",
    padx=35
)


# Hospital title

title_frame = tk.Frame(
    header,
    bg=HEADER_COLOR
)

title_frame.pack(
    side="left"
)


tk.Label(
    title_frame,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold"),
    bg=HEADER_COLOR,
    fg="white"
).pack(
    anchor="w"
)


tk.Label(
    title_frame,
    text="Hospital Administration Dashboard",
    font=("Arial", 11),
    bg=HEADER_COLOR,
    fg="#BBDEFB"
).pack(
    anchor="w"
)


# Logout button

logout_button = tk.Button(
    header,
    text="LOGOUT",
    font=("Arial", 11, "bold"),
    width=12,
    bg=DANGER_COLOR,
    fg="white",
    activebackground="#B71C1C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=logout
)

logout_button.pack(
    side="right",
    padx=30
)


# ==========================================================
# WELCOME
# ==========================================================

welcome = tk.Label(
    root,
    text="Welcome to Hospital Management System",
    font=("Arial", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

welcome.pack(
    pady=(25, 5)
)


subtitle = tk.Label(
    root,
    text="Select a module to continue",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg="#607D8B"
)

subtitle.pack(
    pady=(0, 20)
)


# ==========================================================
# MODULE FRAME
# ==========================================================

module_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

module_frame.pack(
    padx=40
)


# ==========================================================
# CREATE MODULE BUTTON
# ==========================================================

def create_module_button(
    parent,
    text,
    icon,
    filename,
    row,
    column,
    color
):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        highlightbackground="#CFD8DC",
        highlightthickness=1,
        width=250,
        height=135
    )

    card.grid(
        row=row,
        column=column,
        padx=12,
        pady=12
    )

    card.grid_propagate(False)


    button = tk.Button(
        card,
        text=f"{icon}\n{text}",
        font=("Arial", 14, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        height=5,
        command=lambda: open_module(filename)
    )

    button.pack(
        fill="both",
        expand=True,
        padx=8,
        pady=8
    )

    return button


# ==========================================================
# ROW 1
# ==========================================================

create_module_button(
    module_frame,
    "PATIENTS",
    "👤",
    "patient.py",
    0,
    0,
    PRIMARY_COLOR
)


create_module_button(
    module_frame,
    "DOCTORS",
    "👨‍⚕️",
    "doctor.py",
    0,
    1,
    GREEN_COLOR
)


create_module_button(
    module_frame,
    "APPOINTMENTS",
    "📅",
    "appointment.py",
    0,
    2,
    PURPLE_COLOR
)


create_module_button(
    module_frame,
    "PRESCRIPTIONS",
    "💊",
    "prescription.py",
    0,
    3,
    ORANGE_COLOR
)


# ==========================================================
# ROW 2
# ==========================================================

create_module_button(
    module_frame,
    "ROOMS",
    "🛏️",
    "room.py",
    1,
    0,
    "#00838F"
)


create_module_button(
    module_frame,
    "BILLING",
    "💰",
    "billing.py",
    1,
    1,
    "#558B2F"
)


create_module_button(
    module_frame,
    "DISCHARGE",
    "🚪",
    "discharge.py",
    1,
    2,
    "#5E35B1"
)


create_module_button(
    module_frame,
    "REPORTS",
    "📊",
    "reports.py",
    1,
    3,
    "#C62828"
)


# ==========================================================
# ROW 3
# ==========================================================

create_module_button(
    module_frame,
    "CHANGE PASSWORD",
    "🔑",
    "change_password.py",
    2,
    0,
    "#455A64"
)


# ==========================================================
# DATABASE STATUS
# ==========================================================

status_frame = tk.Frame(
    root,
    bg=CARD_COLOR,
    highlightbackground="#CFD8DC",
    highlightthickness=1
)

status_frame.pack(
    fill="x",
    padx=60,
    pady=(20, 10)
)


tk.Label(
    status_frame,
    text="●",
    font=("Arial", 16),
    bg=CARD_COLOR,
    fg=GREEN_COLOR
).pack(
    side="left",
    padx=(20, 5),
    pady=8
)


tk.Label(
    status_frame,
    text="Database Connected",
    font=("Arial", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    pady=8
)


tk.Label(
    status_frame,
    text="SQLite Database: hospital.db",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg="#607D8B"
).pack(
    side="right",
    padx=20
)


# ==========================================================
# EXIT BUTTON
# ==========================================================

exit_button = tk.Button(
    root,
    text="EXIT APPLICATION",
    font=("Arial", 11, "bold"),
    width=20,
    height=2,
    bg=DANGER_COLOR,
    fg="white",
    activebackground="#B71C1C",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=exit_program
)

exit_button.pack(
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
    fg="#78909C"
).pack(
    side="bottom",
    pady=8
)


# ==========================================================
# START
# ==========================================================

root.mainloop()