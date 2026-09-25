import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
import os


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================================
# GET TABLE COUNT
# ==========================================================

def get_count(table_name):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        count = cursor.fetchone()[0]

        conn.close()

        return count

    except Exception:
        return 0


# ==========================================================
# OPEN MODULE
# ==========================================================

def open_module(filename):

    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )

    if not os.path.exists(path):

        messagebox.showerror(
            "File Not Found",
            f"{filename} was not found."
        )

        return

    try:

        subprocess.Popen(
            [sys.executable, path]
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ==========================================================
# UPDATE DASHBOARD COUNTS
# ==========================================================

def update_counts():

    patient_count.config(
        text=str(get_count("patient"))
    )

    doctor_count.config(
        text=str(get_count("doctor"))
    )

    appointment_count.config(
        text=str(get_count("appointment"))
    )

    prescription_count.config(
        text=str(get_count("prescription"))
    )

    billing_count.config(
        text=str(get_count("bill"))
    )

    room_count.config(
        text=str(get_count("room"))
    )

    discharge_count.config(
        text=str(get_count("discharge"))
    )

    root.after(
        5000,
        update_counts
    )


# ==========================================================
# LOGOUT
# ==========================================================

def logout():

    result = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if result:

        root.destroy()


# ==========================================================
# CREATE STATISTICS CARD
# ==========================================================

def create_card(
    parent,
    title,
    row,
    column
):

    frame = tk.Frame(
        parent,
        bg="white",
        bd=2,
        relief="groove",
        width=250,
        height=120
    )

    frame.grid(
        row=row,
        column=column,
        padx=15,
        pady=10
    )

    frame.grid_propagate(False)

    title_label = tk.Label(
        frame,
        text=title,
        font=("Arial", 15, "bold"),
        bg="white",
        fg="black"
    )

    title_label.pack(
        pady=(15, 5)
    )

    count_label = tk.Label(
        frame,
        text="0",
        font=("Arial", 28, "bold"),
        bg="white",
        fg="black"
    )

    count_label.pack()

    return count_label


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title(
    "Hospital Management System"
)

root.geometry(
    "1250x900"
)

root.configure(
    bg="white"
)


# ==========================================================
# TITLE
# ==========================================================

title = tk.Label(
    root,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 30, "bold"),
    bg="white",
    fg="black"
)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(
    root,
    text="Admin Dashboard",
    font=("Arial", 18),
    bg="white",
    fg="black"
)

subtitle.pack(
    pady=5
)


# ==========================================================
# STATISTICS FRAME
# ==========================================================

stats_frame = tk.Frame(
    root,
    bg="white"
)

stats_frame.pack(
    pady=10
)


# ==========================================================
# STATISTICS CARDS
# ==========================================================

patient_count = create_card(
    stats_frame,
    "Total Patients",
    0,
    0
)

doctor_count = create_card(
    stats_frame,
    "Total Doctors",
    0,
    1
)

appointment_count = create_card(
    stats_frame,
    "Appointments",
    0,
    2
)

prescription_count = create_card(
    stats_frame,
    "Prescriptions",
    1,
    0
)

billing_count = create_card(
    stats_frame,
    "Bills",
    1,
    1
)

room_count = create_card(
    stats_frame,
    "Rooms",
    1,
    2
)

discharge_count = create_card(
    stats_frame,
    "Discharges",
    2,
    1
)


# ==========================================================
# MODULE BUTTON FRAME
# ==========================================================

button_frame = tk.Frame(
    root,
    bg="white"
)

button_frame.pack(
    pady=10
)


# ==========================================================
# CREATE MODULE BUTTON
# ==========================================================

def create_button(
    text,
    filename,
    row,
    column
):

    button = tk.Button(
        button_frame,
        text=text,
        font=("Arial", 13, "bold"),
        width=24,
        height=2,
        command=lambda: open_module(filename)
    )

    button.grid(
        row=row,
        column=column,
        padx=10,
        pady=6
    )


# ==========================================================
# MODULE BUTTONS
# ==========================================================

create_button(
    "Patient Management",
    "patient.py",
    0,
    0
)

create_button(
    "Doctor Management",
    "doctor.py",
    0,
    1
)

create_button(
    "Appointment Management",
    "appointment.py",
    1,
    0
)

create_button(
    "Prescription Management",
    "prescription.py",
    1,
    1
)

create_button(
    "Billing Management",
    "billing.py",
    2,
    0
)

create_button(
    "Room Management",
    "room.py",
    2,
    1
)

create_button(
    "Discharge Management",
    "discharge.py",
    3,
    0
)

create_button(
    "Reports",
    "reports.py",
    3,
    1
)

create_button(
    "User Management",
    "create_user.py",
    4,
    0
)


# ==========================================================
# REFRESH BUTTON
# ==========================================================

refresh_button = tk.Button(
    root,
    text="REFRESH DASHBOARD",
    font=("Arial", 13, "bold"),
    width=25,
    height=2,
    command=update_counts
)

refresh_button.pack(
    pady=8
)


# ==========================================================
# LOGOUT BUTTON
# ==========================================================

logout_button = tk.Button(
    root,
    text="LOGOUT",
    font=("Arial", 13, "bold"),
    width=25,
    height=2,
    command=logout
)

logout_button.pack(
    pady=5
)


# ==========================================================
# FOOTER
# ==========================================================

footer = tk.Label(
    root,
    text="Hospital Management System",
    font=("Arial", 11),
    bg="white",
    fg="black"
)

footer.pack(
    side="bottom",
    pady=10
)


# ==========================================================
# START DASHBOARD
# ==========================================================

update_counts()

root.mainloop()