import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==========================================
# DATABASE CONNECTION
# ==========================================

def connect_db():
    return sqlite3.connect("hospital.db")


# ==========================================
# CLEAR ADD PATIENT FIELDS
# ==========================================

def clear_add_fields():

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    blood_entry.delete(0, tk.END)


# ==========================================
# ADD PATIENT
# ==========================================

def add_patient():

    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    blood_group = blood_entry.get()

    if name == "" or age == "":
        messagebox.showerror(
            "Error",
            "Name and Age are required"
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


# ==========================================
# VIEW PATIENTS
# ==========================================

def view_patients():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM patient
        ORDER BY patient_id
    """)

    patients = cursor.fetchall()

    conn.close()

    # New window
    view_window = tk.Toplevel(window)

    view_window.title("Patient Database")

    view_window.geometry("1100x500")

    # Title
    tk.Label(
        view_window,
        text="PATIENT DATABASE",
        font=("Arial", 20, "bold")
    ).pack(pady=10)

    # Frame for table
    table_frame = tk.Frame(view_window)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # Columns
    columns = (
        "ID",
        "Name",
        "Age",
        "Gender",
        "Phone",
        "Address",
        "Blood Group"
    )

    # Create Treeview
    table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    # Column headings
    for column in columns:

        table.heading(
            column,
            text=column
        )

    # Column widths
    table.column(
        "ID",
        width=50,
        anchor="center"
    )

    table.column(
        "Name",
        width=150
    )

    table.column(
        "Age",
        width=60,
        anchor="center"
    )

    table.column(
        "Gender",
        width=80,
        anchor="center"
    )

    table.column(
        "Phone",
        width=120
    )

    table.column(
        "Address",
        width=200
    )

    table.column(
        "Blood Group",
        width=100,
        anchor="center"
    )

    # Vertical scrollbar
    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(
        yscrollcommand=vertical_scrollbar.set
    )

    # Horizontal scrollbar
    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=table.xview
    )

    table.configure(
        xscrollcommand=horizontal_scrollbar.set
    )

    # Put table on screen
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

    # Insert database records
    for patient in patients:

        table.insert(
            "",
            tk.END,
            values=patient
        )

    # No records message
    if not patients:

        messagebox.showinfo(
            "Patient Database",
            "No patients found"
        )


# ==========================================
# SEARCH PATIENT
# ==========================================

def search_patient():

    patient_id = search_entry.get()

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

    conn.close()

    if patient:

        result = (
            f"Patient ID  : {patient[0]}\n"
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


# ==========================================
# UPDATE PATIENT
# ==========================================

def update_patient():

    patient_id = update_id_entry.get()
    name = update_name_entry.get()
    age = update_age_entry.get()
    gender = update_gender_entry.get()
    phone = update_phone_entry.get()
    address = update_address_entry.get()
    blood_group = update_blood_entry.get()

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
        SET name = ?,
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


# ==========================================
# CLEAR UPDATE FIELDS
# ==========================================

def clear_update_fields():

    update_id_entry.delete(0, tk.END)
    update_name_entry.delete(0, tk.END)
    update_age_entry.delete(0, tk.END)
    update_gender_entry.delete(0, tk.END)
    update_phone_entry.delete(0, tk.END)
    update_address_entry.delete(0, tk.END)
    update_blood_entry.delete(0, tk.END)


# ==========================================
# DELETE PATIENT
# ==========================================

def delete_patient():

    patient_id = delete_id_entry.get()

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

    # Find patient
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

    # Confirmation
    answer = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete:\n\n"
        f"ID   : {patient[0]}\n"
        f"Name : {patient[1]}"
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


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title(
    "Hospital Management System - Patient Management"
)

window.geometry("650x700")


# ==========================================
# MAIN SCROLLABLE AREA
# ==========================================

main_frame = tk.Frame(window)

main_frame.pack(
    fill="both",
    expand=True
)

canvas = tk.Canvas(main_frame)

scrollbar = ttk.Scrollbar(
    main_frame,
    orient="vertical",
    command=canvas.yview
)

scrollable_frame = tk.Frame(canvas)


scrollable_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)


canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw",
    width=630
)


canvas.configure(
    yscrollcommand=scrollbar.set
)


canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ==========================================
# TITLE
# ==========================================

tk.Label(
    scrollable_frame,
    text="PATIENT MANAGEMENT",
    font=("Arial", 22, "bold")
).pack(pady=20)


# ==========================================
# ADD PATIENT
# ==========================================

tk.Label(
    scrollable_frame,
    text="ADD PATIENT",
    font=("Arial", 16, "bold")
).pack(pady=10)


tk.Label(
    scrollable_frame,
    text="Patient Name"
).pack()

name_entry = tk.Entry(
    scrollable_frame,
    width=40
)

name_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="Age"
).pack()

age_entry = tk.Entry(
    scrollable_frame,
    width=40
)

age_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="Gender"
).pack()

gender_entry = tk.Entry(
    scrollable_frame,
    width=40
)

gender_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="Phone"
).pack()

phone_entry = tk.Entry(
    scrollable_frame,
    width=40
)

phone_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="Address"
).pack()

address_entry = tk.Entry(
    scrollable_frame,
    width=40
)

address_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="Blood Group"
).pack()

blood_entry = tk.Entry(
    scrollable_frame,
    width=40
)

blood_entry.pack(pady=5)


tk.Button(
    scrollable_frame,
    text="ADD PATIENT",
    command=add_patient,
    width=25
).pack(pady=10)


# ==========================================
# VIEW PATIENTS
# ==========================================

tk.Button(
    scrollable_frame,
    text="VIEW PATIENTS",
    command=view_patients,
    width=25
).pack(pady=10)


# ==========================================
# SEARCH PATIENT
# ==========================================

tk.Label(
    scrollable_frame,
    text="SEARCH PATIENT",
    font=("Arial", 16, "bold")
).pack(pady=15)


tk.Label(
    scrollable_frame,
    text="Patient ID"
).pack()

search_entry = tk.Entry(
    scrollable_frame,
    width=30
)

search_entry.pack(pady=5)


tk.Button(
    scrollable_frame,
    text="SEARCH PATIENT",
    command=search_patient,
    width=25
).pack(pady=10)


# ==========================================
# UPDATE PATIENT
# ==========================================

tk.Label(
    scrollable_frame,
    text="UPDATE PATIENT",
    font=("Arial", 16, "bold")
).pack(pady=15)


tk.Label(
    scrollable_frame,
    text="Patient ID"
).pack()

update_id_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_id_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="New Name"
).pack()

update_name_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_name_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="New Age"
).pack()

update_age_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_age_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="New Gender"
).pack()

update_gender_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_gender_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="New Phone"
).pack()

update_phone_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_phone_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="New Address"
).pack()

update_address_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_address_entry.pack(pady=5)


tk.Label(
    scrollable_frame,
    text="New Blood Group"
).pack()

update_blood_entry = tk.Entry(
    scrollable_frame,
    width=30
)

update_blood_entry.pack(pady=5)


tk.Button(
    scrollable_frame,
    text="UPDATE PATIENT",
    command=update_patient,
    width=25
).pack(pady=10)


# ==========================================
# DELETE PATIENT
# ==========================================

tk.Label(
    scrollable_frame,
    text="DELETE PATIENT",
    font=("Arial", 16, "bold")
).pack(pady=15)


tk.Label(
    scrollable_frame,
    text="Patient ID"
).pack()

delete_id_entry = tk.Entry(
    scrollable_frame,
    width=30
)

delete_id_entry.pack(pady=5)


tk.Button(
    scrollable_frame,
    text="DELETE PATIENT",
    command=delete_patient,
    width=25
).pack(pady=15)


# ==========================================
# START APPLICATION
# ==========================================

window.mainloop()