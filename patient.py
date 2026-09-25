import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# COLORS - PATIENT THEME
# =========================================================

BG_COLOR = "#F3F8FC"
HEADER_COLOR = "#0D47A1"
PATIENT_BLUE = "#1976D2"
DARK_BLUE = "#0D47A1"
LIGHT_BLUE = "#E3F2FD"

GREEN = "#2E7D32"
PURPLE = "#7B1FA2"
ORANGE = "#EF6C00"
RED = "#C62828"

WHITE = "#FFFFFF"
TEXT_COLOR = "#17324D"
GRAY = "#607D8B"


# =========================================================
# DATABASE
# =========================================================

def connect_db():
    return sqlite3.connect("hospital.db")


# =========================================================
# CLEAR ADD FIELDS
# =========================================================

def clear_add_fields():

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    blood_entry.delete(0, tk.END)


# =========================================================
# ADD PATIENT
# =========================================================

def add_patient():

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_entry.get().strip()
    phone = phone_entry.get().strip()
    address = address_entry.get().strip()
    blood_group = blood_entry.get().strip()

    if name == "":
        messagebox.showerror(
            "Error",
            "Please enter patient name"
        )
        return

    if age == "":
        messagebox.showerror(
            "Error",
            "Please enter age"
        )
        return

    try:
        age = int(age)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Age must be a number"
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO patient
        (name, age, gender, phone, address, blood_group)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        phone,
        address,
        blood_group
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Patient added successfully!"
    )

    clear_add_fields()


# =========================================================
# VIEW PATIENTS
# =========================================================

def view_patients():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            name,
            age,
            gender,
            phone,
            address,
            blood_group
        FROM patient
        ORDER BY patient_id
    """)

    patients = cursor.fetchall()

    conn.close()

    view_window = tk.Toplevel(window)

    view_window.title(
        "Hospital Management System - Patient Database"
    )

    view_window.geometry(
        "1150x600"
    )

    view_window.configure(
        bg=BG_COLOR
    )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    header = tk.Frame(
        view_window,
        bg=HEADER_COLOR,
        height=75
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    tk.Label(
        header,
        text="👤  PATIENT DATABASE",
        font=("Segoe UI", 21, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(
        pady=18
    )

    # -----------------------------------------------------
    # TABLE
    # -----------------------------------------------------

    table_frame = tk.Frame(
        view_window,
        bg=BG_COLOR
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    columns = (
        "ID",
        "Name",
        "Age",
        "Gender",
        "Phone",
        "Address",
        "Blood Group"
    )

    style = ttk.Style()

    style.configure(
        "Patient.Treeview",
        font=("Segoe UI", 10),
        rowheight=32,
        background=WHITE,
        fieldbackground=WHITE
    )

    style.configure(
        "Patient.Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background=PATIENT_BLUE,
        foreground=WHITE
    )

    style.map(
        "Patient.Treeview",
        background=[
            ("selected", LIGHT_BLUE)
        ],
        foreground=[
            ("selected", TEXT_COLOR)
        ]
    )

    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Patient.Treeview"
    )

    # -----------------------------------------------------
    # HEADINGS
    # -----------------------------------------------------

    for column in columns:

        table.heading(
            column,
            text=column
        )

    # -----------------------------------------------------
    # COLUMN WIDTHS
    # -----------------------------------------------------

    table.column(
        "ID",
        width=70,
        anchor="center"
    )

    table.column(
        "Name",
        width=180
    )

    table.column(
        "Age",
        width=70,
        anchor="center"
    )

    table.column(
        "Gender",
        width=100,
        anchor="center"
    )

    table.column(
        "Phone",
        width=150
    )

    table.column(
        "Address",
        width=300
    )

    table.column(
        "Blood Group",
        width=120,
        anchor="center"
    )

    # -----------------------------------------------------
    # SCROLLBARS
    # -----------------------------------------------------

    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=table.xview
    )

    table.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set
    )

    table.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )

    # -----------------------------------------------------
    # INSERT PATIENT DATA
    # -----------------------------------------------------

    for patient in patients:

        table.insert(
            "",
            tk.END,
            values=patient
        )

    if not patients:

        messagebox.showinfo(
            "Patient Database",
            "No patients found"
        )


# =========================================================
# SEARCH PATIENT
# =========================================================

def search_patient():

    patient_id = search_entry.get().strip()

    if patient_id == "":
        messagebox.showerror(
            "Error",
            "Please enter Patient ID"
        )
        return

    try:
        patient_id = int(patient_id)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Patient ID must be a number"
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            name,
            age,
            gender,
            phone,
            address,
            blood_group
        FROM patient
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    conn.close()

    if patient:

        result = (
            f"Patient ID  : {patient[0]}\n\n"
            f"Name        : {patient[1]}\n"
            f"Age         : {patient[2]}\n"
            f"Gender      : {patient[3]}\n"
            f"Phone       : {patient[4]}\n"
            f"Address     : {patient[5]}\n"
            f"Blood Group : {patient[6]}"
        )

        messagebox.showinfo(
            "Patient Found",
            result
        )

    else:

        messagebox.showerror(
            "Not Found",
            "Patient not found"
        )


# =========================================================
# UPDATE PATIENT
# =========================================================

def update_patient():

    patient_id = update_id_entry.get().strip()
    name = update_name_entry.get().strip()
    age = update_age_entry.get().strip()
    gender = update_gender_entry.get().strip()
    phone = update_phone_entry.get().strip()
    address = update_address_entry.get().strip()
    blood_group = update_blood_entry.get().strip()

    if patient_id == "":
        messagebox.showerror(
            "Error",
            "Please enter Patient ID"
        )
        return

    if name == "" or age == "":
        messagebox.showerror(
            "Error",
            "Name and Age are required"
        )
        return

    try:

        patient_id = int(patient_id)
        age = int(age)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Patient ID and Age must be numbers"
        )

        return

    conn = connect_db()
    cursor = conn.cursor()

    # Check patient exists

    cursor.execute("""
        SELECT *
        FROM patient
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    if patient is None:

        conn.close()

        messagebox.showerror(
            "Error",
            "Patient not found"
        )

        return

    # Update patient

    cursor.execute("""
        UPDATE patient
        SET
            name = ?,
            age = ?,
            gender = ?,
            phone = ?,
            address = ?,
            blood_group = ?
        WHERE patient_id = ?
    """, (
        name,
        age,
        gender,
        phone,
        address,
        blood_group,
        patient_id
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Patient updated successfully!"
    )

    clear_update_fields()


# =========================================================
# CLEAR UPDATE FIELDS
# =========================================================

def clear_update_fields():

    update_id_entry.delete(
        0,
        tk.END
    )

    update_name_entry.delete(
        0,
        tk.END
    )

    update_age_entry.delete(
        0,
        tk.END
    )

    update_gender_entry.delete(
        0,
        tk.END
    )

    update_phone_entry.delete(
        0,
        tk.END
    )

    update_address_entry.delete(
        0,
        tk.END
    )

    update_blood_entry.delete(
        0,
        tk.END
    )


# =========================================================
# DELETE PATIENT
# =========================================================

def delete_patient():

    patient_id = delete_id_entry.get().strip()

    if patient_id == "":
        messagebox.showerror(
            "Error",
            "Please enter Patient ID"
        )
        return

    try:

        patient_id = int(patient_id)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Patient ID must be a number"
        )

        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM patient
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    if patient is None:

        conn.close()

        messagebox.showerror(
            "Error",
            "Patient not found"
        )

        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete this patient?\n\n"
        f"Patient ID : {patient[0]}\n"
        f"Name       : {patient[1]}"
    )

    if answer:

        cursor.execute("""
            DELETE FROM patient
            WHERE patient_id = ?
        """, (patient_id,))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Patient deleted successfully!"
        )

        delete_id_entry.delete(
            0,
            tk.END
        )

    conn.close()


# =========================================================
# MAIN WINDOW
# =========================================================

window = tk.Tk()

window.title(
    "Hospital Management System - Patient Management"
)

window.geometry(
    "850x900"
)

window.minsize(
    750,
    700
)

window.configure(
    bg=BG_COLOR
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    window,
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
    text="Healthcare Administration  •  Patient Management",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#D5EEF5"
).pack(
    anchor="w"
)


# =========================================================
# SCROLLABLE AREA
# =========================================================

container = tk.Frame(
    window,
    bg=BG_COLOR
)

container.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    container,
    bg=BG_COLOR,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    container,
    orient="vertical",
    command=canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

canvas.configure(
    yscrollcommand=scrollbar.set
)


scrollable_frame = tk.Frame(
    canvas,
    bg=BG_COLOR
)

canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)


def update_scroll(event):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_frame(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


scrollable_frame.bind(
    "<Configure>",
    update_scroll
)

canvas.bind(
    "<Configure>",
    resize_frame
)


# =========================================================
# PAGE TITLE
# =========================================================

tk.Label(
    scrollable_frame,
    text="👤  PATIENT MANAGEMENT",
    font=("Segoe UI", 25, "bold"),
    bg=BG_COLOR,
    fg=DARK_BLUE
).pack(
    pady=(25, 5)
)


tk.Label(
    scrollable_frame,
    text="Manage patient information and hospital records",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=(0, 20)
)


# =========================================================
# ADD PATIENT SECTION
# =========================================================

add_section = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    bd=1,
    relief="solid"
)

add_section.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    add_section,
    text="➕  ADD PATIENT",
    font=("Segoe UI", 18, "bold"),
    bg=WHITE,
    fg=PATIENT_BLUE
).pack(
    pady=(18, 12)
)


add_form = tk.Frame(
    add_section,
    bg=WHITE
)

add_form.pack(
    padx=30,
    pady=5
)


def add_label(text, row):

    tk.Label(
        add_form,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).grid(
        row=row,
        column=0,
        sticky="e",
        padx=10,
        pady=7
    )


def add_entry(row):

    entry = tk.Entry(
        add_form,
        width=38,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )

    entry.grid(
        row=row,
        column=1,
        padx=10,
        pady=7
    )

    return entry


add_label(
    "Patient Name",
    0
)

name_entry = add_entry(0)


add_label(
    "Age",
    1
)

age_entry = add_entry(1)


add_label(
    "Gender",
    2
)

gender_entry = add_entry(2)


add_label(
    "Phone",
    3
)

phone_entry = add_entry(3)


add_label(
    "Address",
    4
)

address_entry = add_entry(4)


add_label(
    "Blood Group",
    5
)

blood_entry = add_entry(5)


# ---------------------------------------------------------
# ADD BUTTON
# ---------------------------------------------------------

tk.Button(
    add_section,
    text="➕  ADD PATIENT",
    font=("Segoe UI", 10, "bold"),
    width=24,
    height=2,
    bg=PATIENT_BLUE,
    fg=WHITE,
    activebackground=DARK_BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=add_patient
).pack(
    pady=12
)


# =========================================================
# VIEW PATIENTS
# =========================================================

view_section = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    bd=1,
    relief="solid"
)

view_section.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    view_section,
    text="📋  PATIENT RECORDS",
    font=("Segoe UI", 18, "bold"),
    bg=WHITE,
    fg=GREEN
).pack(
    pady=(18, 10)
)


tk.Label(
    view_section,
    text="View all registered patients",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg=GRAY
).pack(
    pady=2
)


tk.Button(
    view_section,
    text="📋  VIEW PATIENTS",
    font=("Segoe UI", 10, "bold"),
    width=24,
    height=2,
    bg=GREEN,
    fg=WHITE,
    activebackground=GREEN,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=view_patients
).pack(
    pady=15
)


# =========================================================
# SEARCH PATIENT
# =========================================================

search_section = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    bd=1,
    relief="solid"
)

search_section.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    search_section,
    text="🔍  SEARCH PATIENT",
    font=("Segoe UI", 18, "bold"),
    bg=WHITE,
    fg=PURPLE
).pack(
    pady=(18, 10)
)


search_form = tk.Frame(
    search_section,
    bg=WHITE
)

search_form.pack(
    pady=5
)


tk.Label(
    search_form,
    text="Patient ID",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=0,
    padx=10
)


search_entry = tk.Entry(
    search_form,
    width=35,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

search_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Button(
    search_section,
    text="🔎  SEARCH PATIENT",
    font=("Segoe UI", 10, "bold"),
    width=24,
    height=2,
    bg=PURPLE,
    fg=WHITE,
    activebackground=PURPLE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_patient
).pack(
    pady=15
)


# =========================================================
# UPDATE PATIENT
# =========================================================

update_section = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    bd=1,
    relief="solid"
)

update_section.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    update_section,
    text="✏️  UPDATE PATIENT",
    font=("Segoe UI", 18, "bold"),
    bg=WHITE,
    fg=ORANGE
).pack(
    pady=(18, 12)
)


update_form = tk.Frame(
    update_section,
    bg=WHITE
)

update_form.pack(
    padx=30,
    pady=5
)


def update_label(text, row):

    tk.Label(
        update_form,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).grid(
        row=row,
        column=0,
        sticky="e",
        padx=10,
        pady=7
    )


def update_entry(row):

    entry = tk.Entry(
        update_form,
        width=38,
        font=("Segoe UI", 10),
        relief="solid",
        bd=1
    )

    entry.grid(
        row=row,
        column=1,
        padx=10,
        pady=7
    )

    return entry


update_label(
    "Patient ID",
    0
)

update_id_entry = update_entry(0)


update_label(
    "New Name",
    1
)

update_name_entry = update_entry(1)


update_label(
    "New Age",
    2
)

update_age_entry = update_entry(2)


update_label(
    "New Gender",
    3
)

update_gender_entry = update_entry(3)


update_label(
    "New Phone",
    4
)

update_phone_entry = update_entry(4)


update_label(
    "New Address",
    5
)

update_address_entry = update_entry(5)


update_label(
    "New Blood Group",
    6
)

update_blood_entry = update_entry(6)


tk.Button(
    update_section,
    text="✏️  UPDATE PATIENT",
    font=("Segoe UI", 10, "bold"),
    width=24,
    height=2,
    bg=ORANGE,
    fg=WHITE,
    activebackground=ORANGE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=update_patient
).pack(
    pady=18
)


# =========================================================
# DELETE PATIENT
# =========================================================

delete_section = tk.Frame(
    scrollable_frame,
    bg=WHITE,
    bd=1,
    relief="solid"
)

delete_section.pack(
    padx=40,
    pady=10,
    fill="x"
)


tk.Label(
    delete_section,
    text="🗑️  DELETE PATIENT",
    font=("Segoe UI", 18, "bold"),
    bg=WHITE,
    fg=RED
).pack(
    pady=(18, 10)
)


delete_form = tk.Frame(
    delete_section,
    bg=WHITE
)

delete_form.pack(
    pady=5
)


tk.Label(
    delete_form,
    text="Patient ID",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=0,
    padx=10
)


delete_id_entry = tk.Entry(
    delete_form,
    width=35,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

delete_id_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Button(
    delete_section,
    text="🗑️  DELETE PATIENT",
    font=("Segoe UI", 10, "bold"),
    width=24,
    height=2,
    bg=RED,
    fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=delete_patient
).pack(
    pady=18
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    scrollable_frame,
    text="Hospital Management System  •  Patient Management",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=20
)


# =========================================================
# START
# =========================================================

window.mainloop()