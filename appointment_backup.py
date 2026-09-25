import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# DATABASE CONNECTION
# =========================================================

DB_NAME = "hospital.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


# =========================================================
# GET PATIENTS
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
# GET DOCTORS
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

    appointment_id_entry.delete(0, tk.END)
    appointment_id_entry.insert(0, values[0])

    # Select patient
    patient_name = values[1]

    for item in patient_combo["values"]:

        if " - " in item:

            name = item.split(" - ", 1)[1]

            if name == patient_name:

                patient_combo.set(item)
                break

    # Select doctor
    doctor_name = values[2]

    for item in doctor_combo["values"]:

        if " - " in item:

            name = item.split(" - ", 1)[1]

            if name == doctor_name:

                doctor_combo.set(item)
                break

    date_entry.delete(0, tk.END)
    date_entry.insert(0, values[3])

    time_entry.delete(0, tk.END)
    time_entry.insert(0, values[4])

    reason_entry.delete(0, tk.END)
    reason_entry.insert(0, values[5])


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
        "Delete",
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
    "Hospital Management System - Appointment"
)

root.geometry(
    "1100x700"
)

root.configure(
    bg="white"
)


# =========================================================
# TITLE
# =========================================================

tk.Label(
    root,
    text="APPOINTMENT MANAGEMENT",
    font=("Arial", 24, "bold"),
    bg="white"
).pack(pady=15)


# =========================================================
# FORM FRAME
# =========================================================

form_frame = tk.Frame(
    root,
    bg="white"
)

form_frame.pack(
    pady=5
)


# =========================================================
# APPOINTMENT ID
# =========================================================

tk.Label(
    form_frame,
    text="Appointment ID",
    font=("Arial", 11),
    bg="white"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

appointment_id_entry = tk.Entry(
    form_frame,
    width=30,
    font=("Arial", 11)
)

appointment_id_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# PATIENT
# =========================================================

tk.Label(
    form_frame,
    text="Patient",
    font=("Arial", 11),
    bg="white"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

patient_combo = ttk.Combobox(
    form_frame,
    width=28,
    state="readonly",
    font=("Arial", 11)
)

patient_combo.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# DOCTOR
# =========================================================

tk.Label(
    form_frame,
    text="Doctor",
    font=("Arial", 11),
    bg="white"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

doctor_combo = ttk.Combobox(
    form_frame,
    width=28,
    state="readonly",
    font=("Arial", 11)
)

doctor_combo.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# DATE
# =========================================================

tk.Label(
    form_frame,
    text="Appointment Date",
    font=("Arial", 11),
    bg="white"
).grid(
    row=3,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

date_entry = tk.Entry(
    form_frame,
    width=30,
    font=("Arial", 11)
)

date_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# TIME
# =========================================================

tk.Label(
    form_frame,
    text="Appointment Time",
    font=("Arial", 11),
    bg="white"
).grid(
    row=4,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

time_entry = tk.Entry(
    form_frame,
    width=30,
    font=("Arial", 11)
)

time_entry.grid(
    row=4,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# REASON
# =========================================================

tk.Label(
    form_frame,
    text="Reason",
    font=("Arial", 11),
    bg="white"
).grid(
    row=5,
    column=0,
    padx=10,
    pady=8,
    sticky="w"
)

reason_entry = tk.Entry(
    form_frame,
    width=30,
    font=("Arial", 11)
)

reason_entry.grid(
    row=5,
    column=1,
    padx=10,
    pady=8
)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(
    root,
    bg="white"
)

button_frame.pack(
    pady=10
)


tk.Button(
    button_frame,
    text="ADD",
    width=12,
    command=add_appointment
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    button_frame,
    text="UPDATE",
    width=12,
    command=update_appointment
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    button_frame,
    text="DELETE",
    width=12,
    command=delete_appointment
).grid(
    row=0,
    column=2,
    padx=5
)


tk.Button(
    button_frame,
    text="CLEAR",
    width=12,
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)


tk.Button(
    button_frame,
    text="REFRESH",
    width=12,
    command=view_appointments
).grid(
    row=0,
    column=4,
    padx=5
)


# =========================================================
# SEARCH
# =========================================================

search_frame = tk.Frame(
    root,
    bg="white"
)

search_frame.pack(
    pady=10
)


tk.Label(
    search_frame,
    text="Search",
    font=("Arial", 11),
    bg="white"
).pack(
    side=tk.LEFT,
    padx=5
)


search_entry = tk.Entry(
    search_frame,
    width=35,
    font=("Arial", 11)
)

search_entry.pack(
    side=tk.LEFT,
    padx=5
)


tk.Button(
    search_frame,
    text="SEARCH",
    width=12,
    command=search_appointment
).pack(
    side=tk.LEFT,
    padx=5
)


# =========================================================
# TABLE FRAME
# =========================================================

table_frame = tk.Frame(
    root,
    bg="white"
)

table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)


# =========================================================
# SCROLLBAR
# =========================================================

scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
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
    yscrollcommand=scrollbar.set
)

scrollbar.config(
    command=appointment_table.yview
)


appointment_table.heading(
    "ID",
    text="ID"
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
    text="Date"
)

appointment_table.heading(
    "Time",
    text="Time"
)

appointment_table.heading(
    "Reason",
    text="Reason"
)


appointment_table.column(
    "ID",
    width=60
)

appointment_table.column(
    "Patient",
    width=180
)

appointment_table.column(
    "Doctor",
    width=180
)

appointment_table.column(
    "Date",
    width=120
)

appointment_table.column(
    "Time",
    width=120
)

appointment_table.column(
    "Reason",
    width=250
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
# START
# =========================================================

root.mainloop()