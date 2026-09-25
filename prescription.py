import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F3F8FC"
HEADER_COLOR = "#006064"
PRESCRIPTION_COLOR = "#6A1B9A"
DARK_PURPLE = "#4A148C"

WHITE = "#FFFFFF"
TEXT_COLOR = "#263238"
GRAY = "#607D8B"

GREEN = "#2E7D32"
ORANGE = "#EF6C00"
RED = "#C62828"


# =========================================================
# DATABASE
# =========================================================

DB_NAME = "hospital.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


# =========================================================
# CREATE TABLE
# =========================================================

def create_prescription_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescription (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            doctor_name TEXT NOT NULL,
            medicine TEXT NOT NULL,
            dosage TEXT NOT NULL,
            duration TEXT NOT NULL,
            prescription_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# CLEAR FIELDS
# =========================================================

def clear_fields():

    prescription_id_entry.config(state="normal")
    prescription_id_entry.delete(0, tk.END)
    prescription_id_entry.config(state="readonly")

    patient_entry.delete(0, tk.END)
    doctor_entry.delete(0, tk.END)
    medicine_entry.delete(0, tk.END)
    dosage_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


# =========================================================
# ADD PRESCRIPTION
# =========================================================

def add_prescription():

    patient = patient_entry.get().strip()
    doctor = doctor_entry.get().strip()
    medicine = medicine_entry.get().strip()
    dosage = dosage_entry.get().strip()
    duration = duration_entry.get().strip()
    prescription_date = date_entry.get().strip()

    if patient == "":
        messagebox.showerror(
            "Error",
            "Please enter Patient Name"
        )
        return

    if doctor == "":
        messagebox.showerror(
            "Error",
            "Please enter Doctor Name"
        )
        return

    if medicine == "":
        messagebox.showerror(
            "Error",
            "Please enter Medicine"
        )
        return

    if dosage == "":
        messagebox.showerror(
            "Error",
            "Please enter Dosage"
        )
        return

    if duration == "":
        messagebox.showerror(
            "Error",
            "Please enter Duration"
        )
        return

    if prescription_date == "":
        messagebox.showerror(
            "Error",
            "Please enter Prescription Date"
        )
        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO prescription
            (
                patient_name,
                doctor_name,
                medicine,
                dosage,
                duration,
                prescription_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient,
            doctor,
            medicine,
            dosage,
            duration,
            prescription_date
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Prescription added successfully!"
        )

        clear_fields()
        view_prescriptions()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# VIEW PRESCRIPTIONS
# =========================================================

def view_prescriptions():

    for item in prescription_table.get_children():
        prescription_table.delete(item)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                prescription_id,
                patient_name,
                doctor_name,
                medicine,
                dosage,
                duration,
                prescription_date
            FROM prescription
            ORDER BY prescription_id DESC
        """)

        prescriptions = cursor.fetchall()

        conn.close()

        for prescription in prescriptions:

            prescription_table.insert(
                "",
                tk.END,
                values=prescription
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SELECT PRESCRIPTION
# =========================================================

def select_prescription(event):

    selected = prescription_table.focus()

    if not selected:
        return

    values = prescription_table.item(
        selected,
        "values"
    )

    if not values:
        return

    clear_fields()

    prescription_id_entry.config(
        state="normal"
    )

    prescription_id_entry.insert(
        0,
        values[0]
    )

    prescription_id_entry.config(
        state="readonly"
    )

    patient_entry.insert(
        0,
        values[1]
    )

    doctor_entry.insert(
        0,
        values[2]
    )

    medicine_entry.insert(
        0,
        values[3]
    )

    dosage_entry.insert(
        0,
        values[4]
    )

    duration_entry.insert(
        0,
        values[5]
    )

    date_entry.insert(
        0,
        values[6]
    )


# =========================================================
# UPDATE PRESCRIPTION
# =========================================================

def update_prescription():

    prescription_id = prescription_id_entry.get().strip()
    patient = patient_entry.get().strip()
    doctor = doctor_entry.get().strip()
    medicine = medicine_entry.get().strip()
    dosage = dosage_entry.get().strip()
    duration = duration_entry.get().strip()
    prescription_date = date_entry.get().strip()

    if prescription_id == "":
        messagebox.showerror(
            "Error",
            "Please select a prescription from the table"
        )
        return

    if patient == "" or doctor == "" or medicine == "":
        messagebox.showerror(
            "Error",
            "Please fill all required fields"
        )
        return

    if dosage == "" or duration == "" or prescription_date == "":
        messagebox.showerror(
            "Error",
            "Please fill all required fields"
        )
        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE prescription
            SET
                patient_name = ?,
                doctor_name = ?,
                medicine = ?,
                dosage = ?,
                duration = ?,
                prescription_date = ?
            WHERE prescription_id = ?
        """, (
            patient,
            doctor,
            medicine,
            dosage,
            duration,
            prescription_date,
            prescription_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            messagebox.showerror(
                "Error",
                "Prescription not found"
            )

            return

        conn.close()

        messagebox.showinfo(
            "Success",
            "Prescription updated successfully!"
        )

        clear_fields()
        view_prescriptions()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# DELETE PRESCRIPTION
# =========================================================

def delete_prescription():

    prescription_id = prescription_id_entry.get().strip()

    if prescription_id == "":
        messagebox.showerror(
            "Error",
            "Please select a prescription"
        )
        return

    confirm = messagebox.askyesno(
        "Delete Prescription",
        "Are you sure you want to delete this prescription?"
    )

    if not confirm:
        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM prescription
            WHERE prescription_id = ?
        """, (prescription_id,))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            messagebox.showerror(
                "Error",
                "Prescription not found"
            )

            return

        conn.close()

        messagebox.showinfo(
            "Success",
            "Prescription deleted successfully!"
        )

        clear_fields()
        view_prescriptions()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SEARCH PRESCRIPTION
# =========================================================

def search_prescription():

    search_text = search_entry.get().strip()

    if search_text == "":
        view_prescriptions()
        return

    for item in prescription_table.get_children():
        prescription_table.delete(item)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                prescription_id,
                patient_name,
                doctor_name,
                medicine,
                dosage,
                duration,
                prescription_date
            FROM prescription
            WHERE
                CAST(prescription_id AS TEXT) LIKE ?
                OR patient_name LIKE ?
                OR doctor_name LIKE ?
                OR medicine LIKE ?
                OR dosage LIKE ?
                OR duration LIKE ?
                OR prescription_date LIKE ?
            ORDER BY prescription_id DESC
        """, (
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%"
        ))

        prescriptions = cursor.fetchall()

        conn.close()

        for prescription in prescriptions:

            prescription_table.insert(
                "",
                tk.END,
                values=prescription
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Prescription Management"
)

root.geometry(
    "1350x850"
)

root.minsize(
    1050,
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
    text="Healthcare Administration  •  Prescription Management",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#B2EBF2"
).pack(
    anchor="w"
)


# =========================================================
# PAGE TITLE
# =========================================================

tk.Label(
    root,
    text="💊  PRESCRIPTION MANAGEMENT",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=DARK_PURPLE
).pack(
    pady=(20, 3)
)


tk.Label(
    root,
    text="Create and manage patient prescriptions",
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
    root,
    bg=WHITE,
    bd=1,
    relief="solid"
)

form_card.pack(
    padx=30,
    fill="x"
)


tk.Label(
    form_card,
    text="💊  PRESCRIPTION DETAILS",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=PRESCRIPTION_COLOR
).grid(
    row=0,
    column=0,
    columnspan=4,
    pady=(15, 12)
)


# =========================================================
# PRESCRIPTION ID
# =========================================================

tk.Label(
    form_card,
    text="Prescription ID",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=1,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


prescription_id_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    state="readonly"
)

prescription_id_entry.grid(
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
    text="Patient Name",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=1,
    column=2,
    padx=15,
    pady=7,
    sticky="e"
)


patient_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

patient_entry.grid(
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
    text="Doctor Name",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=2,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


doctor_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

doctor_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# MEDICINE
# =========================================================

tk.Label(
    form_card,
    text="Medicine",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=2,
    column=2,
    padx=15,
    pady=7,
    sticky="e"
)


medicine_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

medicine_entry.grid(
    row=2,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# DOSAGE
# =========================================================

tk.Label(
    form_card,
    text="Dosage",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=3,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


dosage_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

dosage_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# DURATION
# =========================================================

tk.Label(
    form_card,
    text="Duration",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=3,
    column=2,
    padx=15,
    pady=7,
    sticky="e"
)


duration_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

duration_entry.grid(
    row=3,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# DATE
# =========================================================

tk.Label(
    form_card,
    text="Prescription Date",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=4,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


date_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

date_entry.grid(
    row=4,
    column=1,
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
    row=5,
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
    bg=PRESCRIPTION_COLOR,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=add_prescription
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
    relief="flat",
    cursor="hand2",
    command=update_prescription
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
    relief="flat",
    cursor="hand2",
    command=delete_prescription
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
    relief="flat",
    cursor="hand2",
    command=view_prescriptions
).grid(
    row=0,
    column=4,
    padx=5
)


# =========================================================
# SEARCH
# =========================================================

search_card = tk.Frame(
    root,
    bg=WHITE,
    bd=1,
    relief="solid"
)

search_card.pack(
    padx=30,
    pady=12,
    fill="x"
)


tk.Label(
    search_card,
    text="🔍 SEARCH PRESCRIPTION",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE,
    fg=PRESCRIPTION_COLOR
).pack(
    side="left",
    padx=20,
    pady=14
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
    padx=10
)


tk.Button(
    search_card,
    text="🔎 SEARCH",
    width=15,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=PRESCRIPTION_COLOR,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_prescription
).pack(
    side="left",
    padx=10
)


# =========================================================
# TABLE CARD
# =========================================================

table_card = tk.Frame(
    root,
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
    text="📋  PRESCRIPTION RECORDS",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=PRESCRIPTION_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(12, 5)
)


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
# TREEVIEW STYLE
# =========================================================

style = ttk.Style()

style.configure(
    "Prescription.Treeview",
    font=("Segoe UI", 10),
    rowheight=32,
    background=WHITE,
    fieldbackground=WHITE
)

style.configure(
    "Prescription.Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=PRESCRIPTION_COLOR,
    foreground=WHITE
)

style.map(
    "Prescription.Treeview",
    background=[
        ("selected", "#E1BEE7")
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
    orient="vertical"
)

vertical_scrollbar.pack(
    side="right",
    fill="y"
)


horizontal_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="horizontal"
)

horizontal_scrollbar.pack(
    side="bottom",
    fill="x"
)


# =========================================================
# TABLE
# =========================================================

columns = (
    "ID",
    "Patient",
    "Doctor",
    "Medicine",
    "Dosage",
    "Duration",
    "Date"
)


prescription_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    style="Prescription.Treeview",
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


vertical_scrollbar.config(
    command=prescription_table.yview
)

horizontal_scrollbar.config(
    command=prescription_table.xview
)


prescription_table.heading(
    "ID",
    text="Prescription ID"
)

prescription_table.heading(
    "Patient",
    text="Patient Name"
)

prescription_table.heading(
    "Doctor",
    text="Doctor Name"
)

prescription_table.heading(
    "Medicine",
    text="Medicine"
)

prescription_table.heading(
    "Dosage",
    text="Dosage"
)

prescription_table.heading(
    "Duration",
    text="Duration"
)

prescription_table.heading(
    "Date",
    text="Prescription Date"
)


prescription_table.column(
    "ID",
    width=130,
    anchor="center"
)

prescription_table.column(
    "Patient",
    width=200,
    anchor="center"
)

prescription_table.column(
    "Doctor",
    width=200,
    anchor="center"
)

prescription_table.column(
    "Medicine",
    width=200,
    anchor="center"
)

prescription_table.column(
    "Dosage",
    width=150,
    anchor="center"
)

prescription_table.column(
    "Duration",
    width=150,
    anchor="center"
)

prescription_table.column(
    "Date",
    width=180,
    anchor="center"
)


prescription_table.pack(
    fill="both",
    expand=True
)


# =========================================================
# SELECT RECORD
# =========================================================

prescription_table.bind(
    "<ButtonRelease-1>",
    select_prescription
)


# =========================================================
# START
# =========================================================

create_prescription_table()

view_prescriptions()

root.mainloop()