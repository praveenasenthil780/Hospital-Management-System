import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


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
        messagebox.showerror("Error", "Enter doctor name")
        return

    if age == "":
        messagebox.showerror("Error", "Enter age")
        return

    if gender == "":
        messagebox.showerror("Error", "Enter gender")
        return

    if specialization == "":
        messagebox.showerror("Error", "Enter specialization")
        return

    if phone == "":
        messagebox.showerror("Error", "Enter phone")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number")
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

    # IMPORTANT:
    # Do NOT use SELECT *
    # We specify the exact order.

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
    window.title("Doctor Database")
    window.geometry("1200x650")

    title = tk.Label(
        window,
        text="DOCTOR DATABASE",
        font=("Arial", 24, "bold")
    )

    title.pack(pady=20)

    frame = tk.Frame(window)
    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # Vertical scrollbar
    y_scroll = ttk.Scrollbar(
        frame,
        orient="vertical"
    )

    y_scroll.pack(
        side="right",
        fill="y"
    )

    # Horizontal scrollbar
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

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )

    y_scroll.config(
        command=table.yview
    )

    x_scroll.config(
        command=table.xview
    )

    # Headings

    table.heading(
        "ID",
        text="ID"
    )

    table.heading(
        "Name",
        text="Name"
    )

    table.heading(
        "Age",
        text="Age"
    )

    table.heading(
        "Gender",
        text="Gender"
    )

    table.heading(
        "Specialization",
        text="Specialization"
    )

    table.heading(
        "Phone",
        text="Phone"
    )

    table.heading(
        "Email",
        text="Email"
    )

    # Column widths

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

    # Insert rows

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
        f"Doctor ID: {doctor[0]}\n"
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

root.geometry("700x850")

root.configure(
    bg="white"
)


# =========================================================
# SCROLLABLE MAIN WINDOW
# =========================================================

canvas = tk.Canvas(
    root,
    bg="white"
)

scrollbar = ttk.Scrollbar(
    root,
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
    bg="white"
)

canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


def update_scroll(event):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


main_frame.bind(
    "<Configure>",
    update_scroll
)


# =========================================================
# TITLE
# =========================================================

tk.Label(
    main_frame,
    text="DOCTOR MANAGEMENT",
    font=("Arial", 24, "bold"),
    bg="white"
).pack(pady=20)


# =========================================================
# ADD DOCTOR
# =========================================================

tk.Label(
    main_frame,
    text="ADD DOCTOR",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=10)


# Name

tk.Label(
    main_frame,
    text="Doctor Name",
    bg="white"
).pack()

name_entry = tk.Entry(
    main_frame,
    width=35
)

name_entry.pack(pady=5)


# Age

tk.Label(
    main_frame,
    text="Age",
    bg="white"
).pack()

age_entry = tk.Entry(
    main_frame,
    width=35
)

age_entry.pack(pady=5)


# Gender

tk.Label(
    main_frame,
    text="Gender",
    bg="white"
).pack()

gender_entry = tk.Entry(
    main_frame,
    width=35
)

gender_entry.pack(pady=5)


# Specialization

tk.Label(
    main_frame,
    text="Specialization",
    bg="white"
).pack()

specialization_entry = tk.Entry(
    main_frame,
    width=35
)

specialization_entry.pack(pady=5)


# Phone

tk.Label(
    main_frame,
    text="Phone",
    bg="white"
).pack()

phone_entry = tk.Entry(
    main_frame,
    width=35
)

phone_entry.pack(pady=5)


# Email

tk.Label(
    main_frame,
    text="Email",
    bg="white"
).pack()

email_entry = tk.Entry(
    main_frame,
    width=35
)

email_entry.pack(pady=5)


# Add Button

tk.Button(
    main_frame,
    text="ADD DOCTOR",
    width=25,
    command=add_doctor
).pack(pady=10)


# View Button

tk.Button(
    main_frame,
    text="VIEW DOCTORS",
    width=25,
    command=view_doctors
).pack(pady=5)


# =========================================================
# SEARCH
# =========================================================

tk.Label(
    main_frame,
    text="SEARCH DOCTOR",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=25)


tk.Label(
    main_frame,
    text="Doctor ID",
    bg="white"
).pack()

search_entry = tk.Entry(
    main_frame,
    width=35
)

search_entry.pack(pady=5)


tk.Button(
    main_frame,
    text="SEARCH DOCTOR",
    width=25,
    command=search_doctor
).pack(pady=10)


# =========================================================
# UPDATE
# =========================================================

tk.Label(
    main_frame,
    text="UPDATE DOCTOR",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=25)


# ID

tk.Label(
    main_frame,
    text="Doctor ID",
    bg="white"
).pack()

update_id_entry = tk.Entry(
    main_frame,
    width=35
)

update_id_entry.pack(pady=5)


# Name

tk.Label(
    main_frame,
    text="New Name",
    bg="white"
).pack()

update_name_entry = tk.Entry(
    main_frame,
    width=35
)

update_name_entry.pack(pady=5)


# Age

tk.Label(
    main_frame,
    text="New Age",
    bg="white"
).pack()

update_age_entry = tk.Entry(
    main_frame,
    width=35
)

update_age_entry.pack(pady=5)


# Gender

tk.Label(
    main_frame,
    text="New Gender",
    bg="white"
).pack()

update_gender_entry = tk.Entry(
    main_frame,
    width=35
)

update_gender_entry.pack(pady=5)


# Specialization

tk.Label(
    main_frame,
    text="New Specialization",
    bg="white"
).pack()

update_specialization_entry = tk.Entry(
    main_frame,
    width=35
)

update_specialization_entry.pack(pady=5)


# Phone

tk.Label(
    main_frame,
    text="New Phone",
    bg="white"
).pack()

update_phone_entry = tk.Entry(
    main_frame,
    width=35
)

update_phone_entry.pack(pady=5)


# Email

tk.Label(
    main_frame,
    text="New Email",
    bg="white"
).pack()

update_email_entry = tk.Entry(
    main_frame,
    width=35
)

update_email_entry.pack(pady=5)


tk.Button(
    main_frame,
    text="UPDATE DOCTOR",
    width=25,
    command=update_doctor
).pack(pady=10)


# =========================================================
# DELETE
# =========================================================

tk.Label(
    main_frame,
    text="DELETE DOCTOR",
    font=("Arial", 20, "bold"),
    bg="white"
).pack(pady=25)


tk.Label(
    main_frame,
    text="Doctor ID",
    bg="white"
).pack()

delete_id_entry = tk.Entry(
    main_frame,
    width=35
)

delete_id_entry.pack(pady=5)


tk.Button(
    main_frame,
    text="DELETE DOCTOR",
    width=25,
    command=delete_doctor
).pack(pady=15)


# =========================================================
# START
# =========================================================

root.mainloop()