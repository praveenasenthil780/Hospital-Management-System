import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ============================================================
# FIND TABLE COLUMNS
# ============================================================

def get_columns(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()

    conn.close()

    return [row[1] for row in rows]


def find_column(columns, possible_names):
    for name in possible_names:
        for column in columns:
            if column.lower() == name.lower():
                return column

    return None


# ============================================================
# PATIENT COLUMN INFORMATION
# ============================================================

patient_columns = get_columns("patient")

patient_id_col = find_column(
    patient_columns,
    ["id", "patient_id", "patientid"]
)

patient_name_col = find_column(
    patient_columns,
    ["name", "patient_name", "patientname", "pname"]
)


# ============================================================
# DOCTOR COLUMN INFORMATION
# ============================================================

doctor_columns = get_columns("doctor")

doctor_id_col = find_column(
    doctor_columns,
    ["id", "doctor_id", "doctorid"]
)

doctor_name_col = find_column(
    doctor_columns,
    ["name", "doctor_name", "doctorname", "dname"]
)


# ============================================================
# PRESCRIPTION COLUMN INFORMATION
# ============================================================

prescription_columns = get_columns("prescription")

prescription_id_col = find_column(
    prescription_columns,
    ["id", "prescription_id", "prescriptionid"]
)

prescription_patient_col = find_column(
    prescription_columns,
    ["patient_id", "patientid"]
)

prescription_doctor_col = find_column(
    prescription_columns,
    ["doctor_id", "doctorid"]
)

prescription_medicine_col = find_column(
    prescription_columns,
    ["medicine_name", "medicine", "medicinename"]
)

prescription_dosage_col = find_column(
    prescription_columns,
    ["dosage"]
)

prescription_duration_col = find_column(
    prescription_columns,
    ["duration"]
)

prescription_instructions_col = find_column(
    prescription_columns,
    ["instructions", "instruction"]
)


# ============================================================
# CHECK DATABASE STRUCTURE
# ============================================================

if not patient_id_col or not patient_name_col:
    print("PATIENT TABLE COLUMNS:", patient_columns)

if not doctor_id_col or not doctor_name_col:
    print("DOCTOR TABLE COLUMNS:", doctor_columns)

if not prescription_id_col:
    print("PRESCRIPTION TABLE COLUMNS:", prescription_columns)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Hospital Management System - Prescription")
root.geometry("1500x950")
root.configure(bg="white")


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="PRESCRIPTION MANAGEMENT",
    font=("Arial", 34, "bold"),
    bg="white",
    fg="black"
)

title.pack(pady=35)


# ============================================================
# FORM FRAME
# ============================================================

form_frame = tk.Frame(root, bg="white")
form_frame.pack()


# ============================================================
# VARIABLES
# ============================================================

prescription_id_var = tk.StringVar()
patient_var = tk.StringVar()
doctor_var = tk.StringVar()
medicine_var = tk.StringVar()
dosage_var = tk.StringVar()
duration_var = tk.StringVar()
instructions_var = tk.StringVar()
search_var = tk.StringVar()


# ============================================================
# FORM LABELS
# ============================================================

label_font = ("Arial", 16)

tk.Label(
    form_frame,
    text="Prescription ID",
    font=label_font,
    bg="white"
).grid(row=0, column=0, padx=20, pady=12, sticky="e")

tk.Label(
    form_frame,
    text="Patient",
    font=label_font,
    bg="white"
).grid(row=1, column=0, padx=20, pady=12, sticky="e")

tk.Label(
    form_frame,
    text="Doctor",
    font=label_font,
    bg="white"
).grid(row=2, column=0, padx=20, pady=12, sticky="e")

tk.Label(
    form_frame,
    text="Medicine Name",
    font=label_font,
    bg="white"
).grid(row=3, column=0, padx=20, pady=12, sticky="e")

tk.Label(
    form_frame,
    text="Dosage",
    font=label_font,
    bg="white"
).grid(row=4, column=0, padx=20, pady=12, sticky="e")

tk.Label(
    form_frame,
    text="Duration",
    font=label_font,
    bg="white"
).grid(row=5, column=0, padx=20, pady=12, sticky="e")

tk.Label(
    form_frame,
    text="Instructions",
    font=label_font,
    bg="white"
).grid(row=6, column=0, padx=20, pady=12, sticky="e")


# ============================================================
# INPUTS
# ============================================================

entry_width = 30


prescription_id_entry = tk.Entry(
    form_frame,
    textvariable=prescription_id_var,
    width=entry_width,
    font=("Arial", 15),
    state="readonly"
)

prescription_id_entry.grid(
    row=0,
    column=1,
    padx=20,
    pady=12
)


patient_combo = ttk.Combobox(
    form_frame,
    textvariable=patient_var,
    width=28,
    font=("Arial", 14),
    state="readonly"
)

patient_combo.grid(
    row=1,
    column=1,
    padx=20,
    pady=12
)


doctor_combo = ttk.Combobox(
    form_frame,
    textvariable=doctor_var,
    width=28,
    font=("Arial", 14),
    state="readonly"
)

doctor_combo.grid(
    row=2,
    column=1,
    padx=20,
    pady=12
)


medicine_combo = ttk.Combobox(
    form_frame,
    textvariable=medicine_var,
    width=28,
    font=("Arial", 14),
    state="readonly"
)

medicine_combo.grid(
    row=3,
    column=1,
    padx=20,
    pady=12
)


dosage_entry = tk.Entry(
    form_frame,
    textvariable=dosage_var,
    width=entry_width,
    font=("Arial", 15)
)

dosage_entry.grid(
    row=4,
    column=1,
    padx=20,
    pady=12
)


duration_entry = tk.Entry(
    form_frame,
    textvariable=duration_var,
    width=entry_width,
    font=("Arial", 15)
)

duration_entry.grid(
    row=5,
    column=1,
    padx=20,
    pady=12
)


instructions_entry = tk.Entry(
    form_frame,
    textvariable=instructions_var,
    width=entry_width,
    font=("Arial", 15)
)

instructions_entry.grid(
    row=6,
    column=1,
    padx=20,
    pady=12
)


# ============================================================
# LOAD PATIENTS
# ============================================================

patient_data = {}


def load_patients():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT "{patient_id_col}", "{patient_name_col}"
            FROM patient
            ORDER BY "{patient_id_col}"
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        patient_data.clear()

        values = []

        for patient_id, patient_name in rows:

            display = f"{patient_id} - {patient_name}"

            values.append(display)

            patient_data[display] = patient_id

        patient_combo["values"] = values

        if values:
            patient_combo.current(0)

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load patients:\n{e}"
        )


# ============================================================
# LOAD DOCTORS
# ============================================================

doctor_data = {}


def load_doctors():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT "{doctor_id_col}", "{doctor_name_col}"
            FROM doctor
            ORDER BY "{doctor_id_col}"
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        doctor_data.clear()

        values = []

        for doctor_id, doctor_name in rows:

            display = f"{doctor_id} - {doctor_name}"

            values.append(display)

            doctor_data[display] = doctor_id

        doctor_combo["values"] = values

        if values:
            doctor_combo.current(0)

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load doctors:\n{e}"
        )


# ============================================================
# MEDICINE LIST
# ============================================================

def load_medicines():

    medicines = [
        "Paracetamol",
        "Dolo",
        "Aspirin",
        "Cetirizine",
        "Ibuprofen",
        "Amoxicillin",
        "Azithromycin",
        "Vitamin D",
        "Vitamin B12",
        "Folic Acid",
        "Omeprazole",
        "Pantoprazole",
        "Metformin",
        "Amlodipine",
        "Losartan",
        "Atorvastatin"
    ]

    # Also load medicines already present in database

    try:

        conn = get_connection()
        cursor = conn.cursor()

        if prescription_medicine_col:

            query = f"""
                SELECT DISTINCT "{prescription_medicine_col}"
                FROM prescription
                WHERE "{prescription_medicine_col}" IS NOT NULL
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:

                medicine = row[0]

                if medicine and medicine not in medicines:
                    medicines.append(medicine)

        conn.close()

    except Exception:
        pass

    medicine_combo["values"] = medicines

    if medicines:
        medicine_combo.current(0)


# ============================================================
# NEXT PRESCRIPTION ID
# ============================================================

def get_next_id():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT MAX("{prescription_id_col}")
            FROM prescription
        """

        cursor.execute(query)

        result = cursor.fetchone()

        conn.close()

        if result and result[0] is not None:

            return int(result[0]) + 1

        return 1

    except Exception:

        return 1


def set_next_id():

    prescription_id_var.set(str(get_next_id()))


# ============================================================
# TREEVIEW
# ============================================================

table_frame = tk.Frame(root, bg="white")
table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=25
)


columns = (
    "ID",
    "Patient",
    "Doctor",
    "Medicine Name",
    "Dosage",
    "Duration",
    "Instructions"
)


tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    tree.heading(
        column,
        text=column
    )


tree.column(
    "ID",
    width=80,
    anchor="center"
)

tree.column(
    "Patient",
    width=200,
    anchor="center"
)

tree.column(
    "Doctor",
    width=220,
    anchor="center"
)

tree.column(
    "Medicine Name",
    width=220,
    anchor="center"
)

tree.column(
    "Dosage",
    width=150,
    anchor="center"
)

tree.column(
    "Duration",
    width=150,
    anchor="center"
)

tree.column(
    "Instructions",
    width=300,
    anchor="center"
)


scrollbar_y = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

scrollbar_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=tree.xview
)


tree.configure(
    yscrollcommand=scrollbar_y.set,
    xscrollcommand=scrollbar_x.set
)


tree.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scrollbar_y.grid(
    row=0,
    column=1,
    sticky="ns"
)

scrollbar_x.grid(
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


# ============================================================
# LOAD PRESCRIPTIONS
# ============================================================

def load_data():

    for item in tree.get_children():

        tree.delete(item)

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT
                p."{prescription_id_col}",
                pt."{patient_name_col}",
                d."{doctor_name_col}",
                p."{prescription_medicine_col}",
                p."{prescription_dosage_col}",
                p."{prescription_duration_col}",
                p."{prescription_instructions_col}"

            FROM prescription p

            LEFT JOIN patient pt
                ON p."{prescription_patient_col}"
                = pt."{patient_id_col}"

            LEFT JOIN doctor d
                ON p."{prescription_doctor_col}"
                = d."{doctor_id_col}"

            ORDER BY p."{prescription_id_col}"
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            tree.insert(
                "",
                "end",
                values=row
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load prescriptions:\n{e}"
        )


# ============================================================
# CLEAR FORM
# ============================================================

def clear_form():

    prescription_id_var.set(
        str(get_next_id())
    )

    if patient_combo["values"]:
        patient_combo.current(0)
    else:
        patient_var.set("")

    if doctor_combo["values"]:
        doctor_combo.current(0)
    else:
        doctor_var.set("")

    if medicine_combo["values"]:
        medicine_combo.current(0)
    else:
        medicine_var.set("")

    dosage_var.set("")
    duration_var.set("")
    instructions_var.set("")


# ============================================================
# ADD PRESCRIPTION
# ============================================================

def add_prescription():

    try:

        patient_display = patient_var.get()
        doctor_display = doctor_var.get()
        medicine = medicine_var.get()
        dosage = dosage_var.get()
        duration = duration_var.get()
        instructions = instructions_var.get()

        if not patient_display:

            messagebox.showwarning(
                "Warning",
                "Please select a patient."
            )

            return

        if not doctor_display:

            messagebox.showwarning(
                "Warning",
                "Please select a doctor."
            )

            return

        if not medicine:

            messagebox.showwarning(
                "Warning",
                "Please select a medicine."
            )

            return

        if not dosage:

            messagebox.showwarning(
                "Warning",
                "Please enter dosage."
            )

            return

        if not duration:

            messagebox.showwarning(
                "Warning",
                "Please enter duration."
            )

            return

        patient_id = patient_data[patient_display]

        doctor_id = doctor_data[doctor_display]

        prescription_id = int(
            prescription_id_var.get()
        )

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            INSERT INTO prescription
            (
                "{prescription_id_col}",
                "{prescription_patient_col}",
                "{prescription_doctor_col}",
                "{prescription_medicine_col}",
                "{prescription_dosage_col}",
                "{prescription_duration_col}",
                "{prescription_instructions_col}"
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                prescription_id,
                patient_id,
                doctor_id,
                medicine,
                dosage,
                duration,
                instructions
            )
        )

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            "Prescription added successfully."
        )

        load_data()

        clear_form()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to add prescription:\n{e}"
        )


# ============================================================
# SELECT ROW
# ============================================================

def select_row(event):

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(
        selected,
        "values"
    )

    if not values:
        return

    prescription_id_var.set(
        values[0]
    )

    patient_name = values[1]
    doctor_name = values[2]
    medicine = values[3]

    # Find patient

    for display, patient_id in patient_data.items():

        if display.endswith(
            f" - {patient_name}"
        ):

            patient_var.set(display)
            break

    # Find doctor

    for display, doctor_id in doctor_data.items():

        if display.endswith(
            f" - {doctor_name}"
        ):

            doctor_var.set(display)
            break

    medicine_var.set(medicine)

    dosage_var.set(values[4])

    duration_var.set(values[5])

    instructions_var.set(values[6])


tree.bind(
    "<ButtonRelease-1>",
    select_row
)


# ============================================================
# UPDATE
# ============================================================

def update_prescription():

    try:

        prescription_id = prescription_id_var.get()

        if not prescription_id:

            messagebox.showwarning(
                "Warning",
                "Please select a prescription."
            )

            return

        patient_id = patient_data[
            patient_var.get()
        ]

        doctor_id = doctor_data[
            doctor_var.get()
        ]

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            UPDATE prescription

            SET
                "{prescription_patient_col}" = ?,
                "{prescription_doctor_col}" = ?,
                "{prescription_medicine_col}" = ?,
                "{prescription_dosage_col}" = ?,
                "{prescription_duration_col}" = ?,
                "{prescription_instructions_col}" = ?

            WHERE "{prescription_id_col}" = ?
        """

        cursor.execute(
            query,
            (
                patient_id,
                doctor_id,
                medicine_var.get(),
                dosage_var.get(),
                duration_var.get(),
                instructions_var.get(),
                prescription_id
            )
        )

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            "Prescription updated successfully."
        )

        load_data()

        clear_form()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to update prescription:\n{e}"
        )


# ============================================================
# DELETE
# ============================================================

def delete_prescription():

    try:

        prescription_id = prescription_id_var.get()

        if not prescription_id:

            messagebox.showwarning(
                "Warning",
                "Please select a prescription."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this prescription?"
        )

        if not confirm:
            return

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            DELETE FROM prescription
            WHERE "{prescription_id_col}" = ?
        """

        cursor.execute(
            query,
            (prescription_id,)
        )

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            "Prescription deleted successfully."
        )

        load_data()

        clear_form()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to delete prescription:\n{e}"
        )


# ============================================================
# SEARCH
# ============================================================

def search_prescription():

    search_text = search_var.get().strip()

    for item in tree.get_children():

        tree.delete(item)

    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = f"""
            SELECT
                p."{prescription_id_col}",
                pt."{patient_name_col}",
                d."{doctor_name_col}",
                p."{prescription_medicine_col}",
                p."{prescription_dosage_col}",
                p."{prescription_duration_col}",
                p."{prescription_instructions_col}"

            FROM prescription p

            LEFT JOIN patient pt
                ON p."{prescription_patient_col}"
                = pt."{patient_id_col}"

            LEFT JOIN doctor d
                ON p."{prescription_doctor_col}"
                = d."{doctor_id_col}"

            WHERE
                CAST(p."{prescription_id_col}" AS TEXT) LIKE ?
                OR pt."{patient_name_col}" LIKE ?
                OR d."{doctor_name_col}" LIKE ?
                OR p."{prescription_medicine_col}" LIKE ?

            ORDER BY p."{prescription_id_col}"
        """

        value = f"%{search_text}%"

        cursor.execute(
            query,
            (
                value,
                value,
                value,
                value
            )
        )

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            tree.insert(
                "",
                "end",
                values=row
            )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to search prescriptions:\n{e}"
        )


# ============================================================
# BUTTONS
# ============================================================

button_frame = tk.Frame(
    root,
    bg="white"
)

button_frame.pack(
    pady=10
)


button_font = (
    "Arial",
    13
)


tk.Button(
    button_frame,
    text="ADD",
    width=12,
    font=button_font,
    command=add_prescription
).grid(
    row=0,
    column=0,
    padx=8
)


tk.Button(
    button_frame,
    text="UPDATE",
    width=12,
    font=button_font,
    command=update_prescription
).grid(
    row=0,
    column=1,
    padx=8
)


tk.Button(
    button_frame,
    text="DELETE",
    width=12,
    font=button_font,
    command=delete_prescription
).grid(
    row=0,
    column=2,
    padx=8
)


tk.Button(
    button_frame,
    text="CLEAR",
    width=12,
    font=button_font,
    command=clear_form
).grid(
    row=0,
    column=3,
    padx=8
)


tk.Button(
    button_frame,
    text="REFRESH",
    width=12,
    font=button_font,
    command=lambda: load_data()
).grid(
    row=0,
    column=4,
    padx=8
)


# ============================================================
# SEARCH FRAME
# ============================================================

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
    font=("Arial", 16),
    bg="white"
).grid(
    row=0,
    column=0,
    padx=10
)


search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    width=30,
    font=("Arial", 14)
)

search_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Button(
    search_frame,
    text="SEARCH",
    width=12,
    font=("Arial", 13),
    command=search_prescription
).grid(
    row=0,
    column=2,
    padx=10
)


# ============================================================
# INITIAL LOAD
# ============================================================

load_patients()

load_doctors()

load_medicines()

set_next_id()

load_data()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()