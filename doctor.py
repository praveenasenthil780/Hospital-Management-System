import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F3F8F6"
HEADER_COLOR = "#1B5E20"
DOCTOR_GREEN = "#2E7D32"
LIGHT_GREEN = "#E8F5E9"
DARK_GREEN = "#1B5E20"

BLUE = "#1976D2"
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
# ADD DOCTOR
# =========================================================

def add_doctor():

    name = name_entry.get().strip()
    age = age_entry.get().strip()
    gender = gender_entry.get().strip()
    specialization = specialization_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "":
        messagebox.showerror(
            "Error",
            "Enter doctor name"
        )
        return

    if age == "":
        messagebox.showerror(
            "Error",
            "Enter age"
        )
        return

    if gender == "":
        messagebox.showerror(
            "Error",
            "Enter gender"
        )
        return

    if specialization == "":
        messagebox.showerror(
            "Error",
            "Enter specialization"
        )
        return

    if phone == "":
        messagebox.showerror(
            "Error",
            "Enter phone"
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
        INSERT INTO doctor
        (name, age, gender, specialization, phone, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        age,
        gender,
        specialization,
        phone,
        email
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Doctor added successfully!"
    )

    clear_add_fields()


# =========================================================
# CLEAR ADD FIELDS
# =========================================================

def clear_add_fields():

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    specialization_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


# =========================================================
# VIEW DOCTORS
# =========================================================

def view_doctors():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            doctor_id,
            name,
            age,
            gender,
            specialization,
            phone,
            email
        FROM doctor
        ORDER BY doctor_id
    """)

    doctors = cursor.fetchall()

    conn.close()

    window = tk.Toplevel(root)

    window.title(
        "Doctor Database"
    )

    window.geometry(
        "1200x650"
    )

    window.configure(
        bg=BG_COLOR
    )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    header = tk.Frame(
        window,
        bg=HEADER_COLOR,
        height=75
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    tk.Label(
        header,
        text="👨‍⚕️  DOCTOR DATABASE",
        font=("Segoe UI", 22, "bold"),
        bg=HEADER_COLOR,
        fg=WHITE
    ).pack(
        pady=18
    )

    # -----------------------------------------------------
    # TABLE FRAME
    # -----------------------------------------------------

    frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    y_scroll = ttk.Scrollbar(
        frame,
        orient="vertical"
    )

    y_scroll.pack(
        side="right",
        fill="y"
    )

    x_scroll = ttk.Scrollbar(
        frame,
        orient="horizontal"
    )

    x_scroll.pack(
        side="bottom",
        fill="x"
    )

    columns = (
        "ID",
        "Name",
        "Age",
        "Gender",
        "Specialization",
        "Phone",
        "Email"
    )

    style = ttk.Style()

    style.configure(
        "Doctor.Treeview",
        font=("Segoe UI", 10),
        rowheight=32,
        background=WHITE,
        fieldbackground=WHITE
    )

    style.configure(
        "Doctor.Treeview.Heading",
        font=("Segoe UI", 10, "bold"),
        background=DOCTOR_GREEN,
        foreground=WHITE
    )

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        style="Doctor.Treeview",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )

    y_scroll.config(
        command=table.yview
    )

    x_scroll.config(
        command=table.xview
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
        width=80,
        anchor="center"
    )

    table.column(
        "Gender",
        width=120
    )

    table.column(
        "Specialization",
        width=200
    )

    table.column(
        "Phone",
        width=160
    )

    table.column(
        "Email",
        width=250
    )

    # -----------------------------------------------------
    # INSERT DATA
    # -----------------------------------------------------

    for doctor in doctors:

        table.insert(
            "",
            tk.END,
            values=doctor
        )

    table.pack(
        fill="both",
        expand=True
    )


# =========================================================
# SEARCH DOCTOR
# =========================================================

def search_doctor():

    doctor_id = search_entry.get().strip()

    if doctor_id == "":
        messagebox.showerror(
            "Error",
            "Enter Doctor ID"
        )
        return

    try:
        doctor_id = int(doctor_id)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Doctor ID must be a number"
        )
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            doctor_id,
            name,
            age,
            gender,
            specialization,
            phone,
            email
        FROM doctor
        WHERE doctor_id = ?
    """, (doctor_id,))

    doctor = cursor.fetchone()

    conn.close()

    if doctor is None:

        messagebox.showinfo(
            "Search",
            "Doctor not found"
        )

        return

    messagebox.showinfo(
        "Doctor Found",
        f"Doctor ID: {doctor[0]}\n\n"
        f"Name: {doctor[1]}\n"
        f"Age: {doctor[2]}\n"
        f"Gender: {doctor[3]}\n"
        f"Specialization: {doctor[4]}\n"
        f"Phone: {doctor[5]}\n"
        f"Email: {doctor[6]}"
    )


# =========================================================
# UPDATE DOCTOR
# =========================================================

def update_doctor():

    doctor_id = update_id_entry.get().strip()
    name = update_name_entry.get().strip()
    age = update_age_entry.get().strip()
    gender = update_gender_entry.get().strip()
    specialization = update_specialization_entry.get().strip()
    phone = update_phone_entry.get().strip()
    email = update_email_entry.get().strip()

    if doctor_id == "":
        messagebox.showerror(
            "Error",
            "Enter Doctor ID"
        )
        return

    try:
        doctor_id = int(doctor_id)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Doctor ID must be a number"
        )
        return

    if age != "":

        try:
            age = int(age)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Age must be a number"
            )
            return

    else:
        age = None

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE doctor
        SET
            name = ?,
            age = ?,
            gender = ?,
            specialization = ?,
            phone = ?,
            email = ?
        WHERE doctor_id = ?
    """, (
        name,
        age,
        gender,
        specialization,
        phone,
        email,
        doctor_id
    ))

    if cursor.rowcount == 0:

        conn.close()

        messagebox.showinfo(
            "Update",
            "Doctor ID not found"
        )

        return

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Doctor updated successfully!"
    )

    clear_update_fields()


# =========================================================
# CLEAR UPDATE FIELDS
# =========================================================

def clear_update_fields():

    update_id_entry.delete(0, tk.END)
    update_name_entry.delete(0, tk.END)
    update_age_entry.delete(0, tk.END)
    update_gender_entry.delete(0, tk.END)
    update_specialization_entry.delete(0, tk.END)
    update_phone_entry.delete(0, tk.END)
    update_email_entry.delete(0, tk.END)


# =========================================================
# DELETE DOCTOR
# =========================================================

def delete_doctor():

    doctor_id = delete_id_entry.get().strip()

    if doctor_id == "":
        messagebox.showerror(
            "Error",
            "Enter Doctor ID"
        )
        return

    try:
        doctor_id = int(doctor_id)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Doctor ID must be a number"
        )
        return

    confirm = messagebox.askyesno(
        "Delete Doctor",
        "Are you sure you want to delete this doctor?"
    )

    if not confirm:
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM doctor
        WHERE doctor_id = ?
    """, (doctor_id,))

    if cursor.rowcount == 0:

        conn.close()

        messagebox.showinfo(
            "Delete",
            "Doctor ID not found"
        )

        return

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Doctor deleted successfully!"
    )

    delete_id_entry.delete(
        0,
        tk.END
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Doctor Management"
)

root.geometry(
    "850x900"
)

root.minsize(
    750,
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
    text="Healthcare Administration  •  Doctor Management",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#D5EEF5"
).pack(
    anchor="w"
)


# =========================================================
# SCROLLABLE MAIN WINDOW
# =========================================================

container = tk.Frame(
    root,
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


main_frame = tk.Frame(
    canvas,
    bg=BG_COLOR
)

canvas_window = canvas.create_window(
    (0, 0),
    window=main_frame,
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


main_frame.bind(
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
    main_frame,
    text="👨‍⚕️  DOCTOR MANAGEMENT",
    font=("Segoe UI", 25, "bold"),
    bg=BG_COLOR,
    fg=DARK_GREEN
).pack(
    pady=(25, 5)
)


tk.Label(
    main_frame,
    text="Manage doctor information and hospital medical staff",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=(0, 20)
)


# =========================================================
# ADD DOCTOR SECTION
# =========================================================

add_section = tk.Frame(
    main_frame,
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
    text="ADD DOCTOR",
    font=("Segoe UI", 18, "bold"),
    bg=WHITE,
    fg=DOCTOR_GREEN
).pack(
    pady=(18, 12)
)


# ---------------------------------------------------------
# FORM FRAME
# ---------------------------------------------------------

form_frame = tk.Frame(
    add_section,
    bg=WHITE
)

form_frame.pack(
    padx=30,
    pady=5
)


def create_label(parent, text, row):

    tk.Label(
        parent,
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


def create_entry(parent, row):

    entry = tk.Entry(
        parent,
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


create_label(
    form_frame,
    "Doctor Name",
    0
)

name_entry = create_entry(
    form_frame,
    0
)


create_label(
    form_frame,
    "Age",
    1
)

age_entry = create_entry(
    form_frame,
    1
)


create_label(
    form_frame,
    "Gender",
    2
)

gender_entry = create_entry(
    form_frame,
    2
)


create_label(
    form_frame,
    "Specialization",
    3
)

specialization_entry = create_entry(
    form_frame,
    3
)


create_label(
    form_frame,
    "Phone",
    4
)

phone_entry = create_entry(
    form_frame,
    4
)


create_label(
    form_frame,
    "Email",
    5
)

email_entry = create_entry(
    form_frame,
    5
)


# ---------------------------------------------------------
# ADD / VIEW BUTTONS
# ---------------------------------------------------------

button_frame = tk.Frame(
    add_section,
    bg=WHITE
)

button_frame.pack(
    pady=18
)


tk.Button(
    button_frame,
    text="➕  ADD DOCTOR",
    font=("Segoe UI", 10, "bold"),
    width=20,
    height=2,
    bg=DOCTOR_GREEN,
    fg=WHITE,
    activebackground=DARK_GREEN,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=add_doctor
).grid(
    row=0,
    column=0,
    padx=6
)


tk.Button(
    button_frame,
    text="📋  VIEW DOCTORS",
    font=("Segoe UI", 10, "bold"),
    width=20,
    height=2,
    bg=BLUE,
    fg=WHITE,
    activebackground=BLUE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=view_doctors
).grid(
    row=0,
    column=1,
    padx=6
)


# =========================================================
# SEARCH DOCTOR
# =========================================================

search_section = tk.Frame(
    main_frame,
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
    text="🔍  SEARCH DOCTOR",
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
    text="Doctor ID",
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
    text="🔎  SEARCH DOCTOR",
    font=("Segoe UI", 10, "bold"),
    width=22,
    height=2,
    bg=PURPLE,
    fg=WHITE,
    activebackground=PURPLE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_doctor
).pack(
    pady=15
)


# =========================================================
# UPDATE DOCTOR
# =========================================================

update_section = tk.Frame(
    main_frame,
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
    text="✏️  UPDATE DOCTOR",
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


def create_update_label(text, row):

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


def create_update_entry(row):

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


create_update_label(
    "Doctor ID",
    0
)

update_id_entry = create_update_entry(0)


create_update_label(
    "New Name",
    1
)

update_name_entry = create_update_entry(1)


create_update_label(
    "New Age",
    2
)

update_age_entry = create_update_entry(2)


create_update_label(
    "New Gender",
    3
)

update_gender_entry = create_update_entry(3)


create_update_label(
    "New Specialization",
    4
)

update_specialization_entry = create_update_entry(4)


create_update_label(
    "New Phone",
    5
)

update_phone_entry = create_update_entry(5)


create_update_label(
    "New Email",
    6
)

update_email_entry = create_update_entry(6)


tk.Button(
    update_section,
    text="✏️  UPDATE DOCTOR",
    font=("Segoe UI", 10, "bold"),
    width=22,
    height=2,
    bg=ORANGE,
    fg=WHITE,
    activebackground=ORANGE,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=update_doctor
).pack(
    pady=18
)


# =========================================================
# DELETE DOCTOR
# =========================================================

delete_section = tk.Frame(
    main_frame,
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
    text="🗑️  DELETE DOCTOR",
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
    text="Doctor ID",
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
    text="🗑️  DELETE DOCTOR",
    font=("Segoe UI", 10, "bold"),
    width=22,
    height=2,
    bg=RED,
    fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=delete_doctor
).pack(
    pady=18
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    main_frame,
    text="Hospital Management System  •  Doctor Management",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=20
)


# =========================================================
# START
# =========================================================

root.mainloop()