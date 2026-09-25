import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# COLORS - APPOINTMENT THEME
# =========================================================

BG_COLOR = "#F7F3FB"
HEADER_COLOR = "#4A148C"
APPOINTMENT_PURPLE = "#7B1FA2"
DARK_PURPLE = "#4A148C"
LIGHT_PURPLE = "#F3E5F5"

BLUE = "#1976D2"
GREEN = "#2E7D32"
ORANGE = "#EF6C00"
RED = "#C62828"

WHITE = "#FFFFFF"
TEXT_COLOR = "#17324D"
GRAY = "#607D8B"


# =========================================================
# DATABASE
# =========================================================

DB_NAME = "hospital.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


# =========================================================
# LOAD PATIENTS
# =========================================================

def load_patients():

    patient_combo["values"] = ()

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT patient_id, name
            FROM patient
            ORDER BY patient_id
        """)

        rows = cursor.fetchall()

        conn.close()

        patient_list = []

        for row in rows:

            patient_id = row[0]
            patient_name = row[1]

            patient_list.append(
                f"{patient_id} - {patient_name}"
            )

        patient_combo["values"] = patient_list

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# LOAD DOCTORS
# =========================================================

def load_doctors():

    doctor_combo["values"] = ()

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT doctor_id, name
            FROM doctor
            ORDER BY doctor_id
        """)

        rows = cursor.fetchall()

        conn.close()

        doctor_list = []

        for row in rows:

            doctor_id = row[0]
            doctor_name = row[1]

            doctor_list.append(
                f"{doctor_id} - {doctor_name}"
            )

        doctor_combo["values"] = doctor_list

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# ADD APPOINTMENT
# =========================================================

def add_appointment():

    patient = patient_combo.get().strip()
    doctor = doctor_combo.get().strip()
    date = date_entry.get().strip()
    time = time_entry.get().strip()
    reason = reason_entry.get().strip()

    if patient == "":
        messagebox.showerror(
            "Error",
            "Please select a patient"
        )
        return

    if doctor == "":
        messagebox.showerror(
            "Error",
            "Please select a doctor"
        )
        return

    if date == "":
        messagebox.showerror(
            "Error",
            "Please enter appointment date"
        )
        return

    if time == "":
        messagebox.showerror(
            "Error",
            "Please enter appointment time"
        )
        return

    if reason == "":
        messagebox.showerror(
            "Error",
            "Please enter reason"
        )
        return

    try:

        patient_id = patient.split(" - ")[0]
        doctor_id = doctor.split(" - ")[0]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO appointment
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            patient_id,
            doctor_id,
            date,
            time,
            reason
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Appointment added successfully!"
        )

        clear_fields()
        view_appointments()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# VIEW APPOINTMENTS
# =========================================================

def view_appointments():

    for item in appointment_table.get_children():

        appointment_table.delete(item)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.appointment_id,
                p.name,
                d.name,
                a.appointment_date,
                a.appointment_time,
                a.reason
            FROM appointment a
            LEFT JOIN patient p
                ON a.patient_id = p.patient_id
            LEFT JOIN doctor d
                ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_id
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            appointment_table.insert(
                "",
                tk.END,
                values=row
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SEARCH APPOINTMENT
# =========================================================

def search_appointment():

    search_text = search_entry.get().strip()

    if search_text == "":

        view_appointments()

        return

    for item in appointment_table.get_children():

        appointment_table.delete(item)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.appointment_id,
                p.name,
                d.name,
                a.appointment_date,
                a.appointment_time,
                a.reason
            FROM appointment a
            LEFT JOIN patient p
                ON a.patient_id = p.patient_id
            LEFT JOIN doctor d
                ON a.doctor_id = d.doctor_id
            WHERE
                CAST(a.appointment_id AS TEXT) LIKE ?
                OR p.name LIKE ?
                OR d.name LIKE ?
                OR a.appointment_date LIKE ?
                OR a.reason LIKE ?
            ORDER BY a.appointment_id
        """, (
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%"
        ))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            appointment_table.insert(
                "",
                tk.END,
                values=row
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SELECT APPOINTMENT
# =========================================================

def select_appointment(event):

    selected = appointment_table.focus()

    if not selected:
        return

    values = appointment_table.item(
        selected,
        "values"
    )

    if not values:
        return

    appointment_id_entry.delete(
        0,
        tk.END
    )

    appointment_id_entry.insert(
        0,
        values[0]
    )

    # Patient

    patient_name = values[1]

    for item in patient_combo["values"]:

        if " - " in item:

            name = item.split(
                " - ",
                1
            )[1]

            if name == patient_name:

                patient_combo.set(item)

                break

    # Doctor

    doctor_name = values[2]

    for item in doctor_combo["values"]:

        if " - " in item:

            name = item.split(
                " - ",
                1
            )[1]

            if name == doctor_name:

                doctor_combo.set(item)

                break

    date_entry.delete(
        0,
        tk.END
    )

    date_entry.insert(
        0,
        values[3]
    )

    time_entry.delete(
        0,
        tk.END
    )

    time_entry.insert(
        0,
        values[4]
    )

    reason_entry.delete(
        0,
        tk.END
    )

    reason_entry.insert(
        0,
        values[5]
    )


# =========================================================
# UPDATE APPOINTMENT
# =========================================================

def update_appointment():

    appointment_id = appointment_id_entry.get().strip()
    patient = patient_combo.get().strip()
    doctor = doctor_combo.get().strip()
    date = date_entry.get().strip()
    time = time_entry.get().strip()
    reason = reason_entry.get().strip()

    if appointment_id == "":

        messagebox.showerror(
            "Error",
            "Select an appointment first"
        )

        return

    if patient == "" or doctor == "":

        messagebox.showerror(
            "Error",
            "Please select patient and doctor"
        )

        return

    if date == "" or time == "" or reason == "":

        messagebox.showerror(
            "Error",
            "Please fill all fields"
        )

        return

    try:

        patient_id = patient.split(" - ")[0]
        doctor_id = doctor.split(" - ")[0]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE appointment
            SET
                patient_id = ?,
                doctor_id = ?,
                appointment_date = ?,
                appointment_time = ?,
                reason = ?
            WHERE appointment_id = ?
        """, (
            patient_id,
            doctor_id,
            date,
            time,
            reason,
            appointment_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            messagebox.showerror(
                "Error",
                "Appointment not found"
            )

            return

        conn.close()

        messagebox.showinfo(
            "Success",
            "Appointment updated successfully!"
        )

        clear_fields()
        view_appointments()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# DELETE APPOINTMENT
# =========================================================

def delete_appointment():

    appointment_id = appointment_id_entry.get().strip()

    if appointment_id == "":

        messagebox.showerror(
            "Error",
            "Select an appointment first"
        )

        return

    answer = messagebox.askyesno(
        "Delete Appointment",
        "Are you sure you want to delete this appointment?"
    )

    if not answer:
        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM appointment
            WHERE appointment_id = ?
        """, (appointment_id,))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            messagebox.showerror(
                "Error",
                "Appointment not found"
            )

            return

        conn.close()

        messagebox.showinfo(
            "Success",
            "Appointment deleted successfully!"
        )

        clear_fields()
        view_appointments()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# CLEAR FIELDS
# =========================================================

def clear_fields():

    appointment_id_entry.delete(
        0,
        tk.END
    )

    patient_combo.set("")

    doctor_combo.set("")

    date_entry.delete(
        0,
        tk.END
    )

    time_entry.delete(
        0,
        tk.END
    )

    reason_entry.delete(
        0,
        tk.END
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Appointment Management"
)

root.geometry(
    "1200x850"
)

root.minsize(
    1000,
    700
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
    height=90
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


tk.Label(
    header,
    text="🏥",
    font=("Segoe UI Emoji", 30),
    bg=HEADER_COLOR,
    fg=WHITE
).pack(
    side="left",
    padx=(25, 10)
)


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
    text="Healthcare Administration  •  Appointment Management",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#E1BEE7"
).pack(
    anchor="w"
)


# =========================================================
# MAIN CONTENT
# =========================================================

main_container = tk.Frame(
    root,
    bg=BG_COLOR
)

main_container.pack(
    fill="both",
    expand=True
)


# =========================================================
# PAGE TITLE
# =========================================================

tk.Label(
    main_container,
    text="📅  APPOINTMENT MANAGEMENT",
    font=("Segoe UI", 25, "bold"),
    bg=BG_COLOR,
    fg=DARK_PURPLE
).pack(
    pady=(20, 3)
)


tk.Label(
    main_container,
    text="Schedule and manage patient appointments",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=(0, 15)
)


# =========================================================
# FORM CARD
# =========================================================

form_card = tk.Frame(
    main_container,
    bg=WHITE,
    bd=1,
    relief="solid"
)

form_card.pack(
    padx=30,
    pady=5,
    fill="x"
)


tk.Label(
    form_card,
    text="📅  APPOINTMENT DETAILS",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=APPOINTMENT_PURPLE
).grid(
    row=0,
    column=0,
    columnspan=4,
    pady=(15, 12)
)


# =========================================================
# APPOINTMENT ID
# =========================================================

tk.Label(
    form_card,
    text="Appointment ID",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=1,
    column=0,
    padx=12,
    pady=7,
    sticky="e"
)


appointment_id_entry = tk.Entry(
    form_card,
    width=27,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

appointment_id_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# PATIENT
# =========================================================

tk.Label(
    form_card,
    text="Patient",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=1,
    column=2,
    padx=12,
    pady=7,
    sticky="e"
)


patient_combo = ttk.Combobox(
    form_card,
    width=25,
    state="readonly",
    font=("Segoe UI", 10)
)

patient_combo.grid(
    row=1,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# DOCTOR
# =========================================================

tk.Label(
    form_card,
    text="Doctor",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=2,
    column=0,
    padx=12,
    pady=7,
    sticky="e"
)


doctor_combo = ttk.Combobox(
    form_card,
    width=25,
    state="readonly",
    font=("Segoe UI", 10)
)

doctor_combo.grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# DATE
# =========================================================

tk.Label(
    form_card,
    text="Appointment Date",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=2,
    column=2,
    padx=12,
    pady=7,
    sticky="e"
)


date_entry = tk.Entry(
    form_card,
    width=27,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

date_entry.grid(
    row=2,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# TIME
# =========================================================

tk.Label(
    form_card,
    text="Appointment Time",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=3,
    column=0,
    padx=12,
    pady=7,
    sticky="e"
)


time_entry = tk.Entry(
    form_card,
    width=27,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

time_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# REASON
# =========================================================

tk.Label(
    form_card,
    text="Reason",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=3,
    column=2,
    padx=12,
    pady=7,
    sticky="e"
)


reason_entry = tk.Entry(
    form_card,
    width=27,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

reason_entry.grid(
    row=3,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(
    form_card,
    bg=WHITE
)

button_frame.grid(
    row=4,
    column=0,
    columnspan=4,
    pady=18
)


tk.Button(
    button_frame,
    text="➕ ADD",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=APPOINTMENT_PURPLE,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=add_appointment
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    button_frame,
    text="✏️ UPDATE",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=ORANGE,
    fg=WHITE,
    activebackground=ORANGE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=update_appointment
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    button_frame,
    text="🗑️ DELETE",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=RED,
    fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=delete_appointment
).grid(
    row=0,
    column=2,
    padx=5
)


tk.Button(
    button_frame,
    text="🔄 CLEAR",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=GRAY,
    fg=WHITE,
    activebackground=GRAY,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)


tk.Button(
    button_frame,
    text="⟳ REFRESH",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=GREEN,
    fg=WHITE,
    activebackground=GREEN,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=view_appointments
).grid(
    row=0,
    column=4,
    padx=5
)


# =========================================================
# SEARCH CARD
# =========================================================

search_card = tk.Frame(
    main_container,
    bg=WHITE,
    bd=1,
    relief="solid"
)

search_card.pack(
    padx=30,
    pady=10,
    fill="x"
)


tk.Label(
    search_card,
    text="🔍  SEARCH APPOINTMENTS",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=BLUE
).pack(
    side="left",
    padx=20,
    pady=15
)


search_entry = tk.Entry(
    search_card,
    width=35,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

search_entry.pack(
    side="left",
    padx=10,
    pady=15
)


tk.Button(
    search_card,
    text="🔎 SEARCH",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_appointment
).pack(
    side="left",
    padx=10
)


# =========================================================
# TABLE CARD
# =========================================================

table_card = tk.Frame(
    main_container,
    bg=WHITE,
    bd=1,
    relief="solid"
)

table_card.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=5
)


tk.Label(
    table_card,
    text="📋  APPOINTMENT RECORDS",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=APPOINTMENT_PURPLE
).pack(
    anchor="w",
    padx=20,
    pady=(12, 5)
)


# =========================================================
# TABLE FRAME
# =========================================================

table_frame = tk.Frame(
    table_card,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# =========================================================
# TABLE STYLE
# =========================================================

style = ttk.Style()

style.configure(
    "Appointment.Treeview",
    font=("Segoe UI", 10),
    rowheight=32,
    background=WHITE,
    fieldbackground=WHITE
)

style.configure(
    "Appointment.Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=APPOINTMENT_PURPLE,
    foreground=WHITE
)

style.map(
    "Appointment.Treeview",
    background=[
        ("selected", LIGHT_PURPLE)
    ],
    foreground=[
        ("selected", TEXT_COLOR)
    ]
)


# =========================================================
# SCROLLBARS
# =========================================================

vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL
)

vertical_scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.HORIZONTAL
)

horizontal_scrollbar.pack(
    side=tk.BOTTOM,
    fill=tk.X
)


# =========================================================
# APPOINTMENT TABLE
# =========================================================

columns = (
    "ID",
    "Patient",
    "Doctor",
    "Date",
    "Time",
    "Reason"
)


appointment_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    style="Appointment.Treeview",
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


vertical_scrollbar.config(
    command=appointment_table.yview
)

horizontal_scrollbar.config(
    command=appointment_table.xview
)


# =========================================================
# HEADINGS
# =========================================================

appointment_table.heading(
    "ID",
    text="Appointment ID"
)

appointment_table.heading(
    "Patient",
    text="Patient"
)

appointment_table.heading(
    "Doctor",
    text="Doctor"
)

appointment_table.heading(
    "Date",
    text="Appointment Date"
)

appointment_table.heading(
    "Time",
    text="Appointment Time"
)

appointment_table.heading(
    "Reason",
    text="Reason"
)


# =========================================================
# COLUMN WIDTHS
# =========================================================

appointment_table.column(
    "ID",
    width=120,
    anchor="center"
)

appointment_table.column(
    "Patient",
    width=200
)

appointment_table.column(
    "Doctor",
    width=200
)

appointment_table.column(
    "Date",
    width=150,
    anchor="center"
)

appointment_table.column(
    "Time",
    width=150,
    anchor="center"
)

appointment_table.column(
    "Reason",
    width=300
)


appointment_table.pack(
    fill=tk.BOTH,
    expand=True
)


# =========================================================
# TABLE CLICK
# =========================================================

appointment_table.bind(
    "<ButtonRelease-1>",
    select_appointment
)


# =========================================================
# LOAD DATA
# =========================================================

load_patients()

load_doctors()

view_appointments()


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    main_container,
    text="Hospital Management System  •  Appointment Management",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=8
)


# =========================================================
# START
# =========================================================

root.mainloop()