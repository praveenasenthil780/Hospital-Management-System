import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================================
# CREATE DISCHARGE TABLE
# ==========================================================

def create_discharge_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discharge (
            discharge_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            admission_date TEXT,
            discharge_date TEXT,
            room_number TEXT,
            diagnosis TEXT,
            treatment_summary TEXT,
            discharge_instructions TEXT
        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title("Hospital Management System - Discharge Management")
root.geometry("1500x900")
root.configure(bg="white")


# ==========================================================
# VARIABLES
# ==========================================================

discharge_id_var = tk.StringVar()
patient_var = tk.StringVar()
admission_date_var = tk.StringVar()
discharge_date_var = tk.StringVar()
room_number_var = tk.StringVar()
diagnosis_var = tk.StringVar()
search_var = tk.StringVar()


# Patient dictionary
patient_dict = {}


# ==========================================================
# TITLE
# ==========================================================

title = tk.Label(
    root,
    text="DISCHARGE MANAGEMENT",
    font=("Arial", 30, "bold"),
    bg="white",
    fg="black"
)

title.pack(pady=20)


# ==========================================================
# FORM FRAME
# ==========================================================

form_frame = tk.Frame(
    root,
    bg="white"
)

form_frame.pack(pady=5)


# ==========================================================
# DISCHARGE ID
# ==========================================================

tk.Label(
    form_frame,
    text="Discharge ID",
    font=("Arial", 17),
    bg="white"
).grid(
    row=0,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


tk.Entry(
    form_frame,
    textvariable=discharge_id_var,
    font=("Arial", 15),
    width=28,
    state="readonly"
).grid(
    row=0,
    column=1,
    padx=15,
    pady=7
)


# ==========================================================
# PATIENT
# ==========================================================

tk.Label(
    form_frame,
    text="Patient",
    font=("Arial", 17),
    bg="white"
).grid(
    row=1,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


patient_combo = ttk.Combobox(
    form_frame,
    textvariable=patient_var,
    font=("Arial", 15),
    width=27,
    state="readonly"
)

patient_combo.grid(
    row=1,
    column=1,
    padx=15,
    pady=7
)


# ==========================================================
# ADMISSION DATE
# ==========================================================

tk.Label(
    form_frame,
    text="Admission Date",
    font=("Arial", 17),
    bg="white"
).grid(
    row=2,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


tk.Entry(
    form_frame,
    textvariable=admission_date_var,
    font=("Arial", 15),
    width=28
).grid(
    row=2,
    column=1,
    padx=15,
    pady=7
)


# ==========================================================
# DISCHARGE DATE
# ==========================================================

tk.Label(
    form_frame,
    text="Discharge Date",
    font=("Arial", 17),
    bg="white"
).grid(
    row=3,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


tk.Entry(
    form_frame,
    textvariable=discharge_date_var,
    font=("Arial", 15),
    width=28
).grid(
    row=3,
    column=1,
    padx=15,
    pady=7
)


# ==========================================================
# ROOM NUMBER
# ==========================================================

tk.Label(
    form_frame,
    text="Room Number",
    font=("Arial", 17),
    bg="white"
).grid(
    row=4,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


room_combo = ttk.Combobox(
    form_frame,
    textvariable=room_number_var,
    font=("Arial", 15),
    width=27
)

room_combo.grid(
    row=4,
    column=1,
    padx=15,
    pady=7
)


# ==========================================================
# DIAGNOSIS
# ==========================================================

tk.Label(
    form_frame,
    text="Diagnosis",
    font=("Arial", 17),
    bg="white"
).grid(
    row=5,
    column=0,
    padx=15,
    pady=7,
    sticky="e"
)


tk.Entry(
    form_frame,
    textvariable=diagnosis_var,
    font=("Arial", 15),
    width=28
).grid(
    row=5,
    column=1,
    padx=15,
    pady=7
)


# ==========================================================
# TREATMENT SUMMARY
# ==========================================================

tk.Label(
    form_frame,
    text="Treatment Summary",
    font=("Arial", 17),
    bg="white"
).grid(
    row=0,
    column=2,
    padx=15,
    pady=7,
    sticky="ne"
)


treatment_text = tk.Text(
    form_frame,
    width=32,
    height=4,
    font=("Arial", 14)
)

treatment_text.grid(
    row=0,
    column=3,
    rowspan=3,
    padx=15,
    pady=7
)


# ==========================================================
# DISCHARGE INSTRUCTIONS
# ==========================================================

tk.Label(
    form_frame,
    text="Discharge Instructions",
    font=("Arial", 17),
    bg="white"
).grid(
    row=3,
    column=2,
    padx=15,
    pady=7,
    sticky="ne"
)


instructions_text = tk.Text(
    form_frame,
    width=32,
    height=4,
    font=("Arial", 14)
)

instructions_text.grid(
    row=3,
    column=3,
    rowspan=3,
    padx=15,
    pady=7
)


# ==========================================================
# LOAD PATIENTS
# ==========================================================

def load_patients():

    global patient_dict

    patient_dict = {}

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT patient_id, name
            FROM patient
            ORDER BY patient_id
        """)

        rows = cursor.fetchall()

        conn.close()

        patient_values = []

        for patient_id, name in rows:

            display_value = f"{patient_id} - {name}"

            patient_dict[display_value] = patient_id

            patient_values.append(display_value)

        patient_combo["values"] = patient_values

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load patients:\n{e}"
        )


# ==========================================================
# LOAD ROOMS
# ==========================================================

def load_rooms():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT room_number
            FROM room
            ORDER BY room_id
        """)

        rows = cursor.fetchall()

        conn.close()

        room_values = []

        for row in rows:

            room_values.append(str(row[0]))

        room_combo["values"] = room_values

    except Exception as e:

        # Room table may not exist yet
        room_combo["values"] = []

        print("Unable to load rooms:", e)


# ==========================================================
# NEXT DISCHARGE ID
# ==========================================================

def get_next_discharge_id():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(MAX(discharge_id), 0) + 1
            FROM discharge
        """)

        next_id = cursor.fetchone()[0]

        conn.close()

        discharge_id_var.set(str(next_id))

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to get Discharge ID:\n{e}"
        )


# ==========================================================
# ADD DISCHARGE
# ==========================================================

def add_discharge():

    patient = patient_var.get()
    admission_date = admission_date_var.get().strip()
    discharge_date = discharge_date_var.get().strip()
    room_number = room_number_var.get().strip()
    diagnosis = diagnosis_var.get().strip()

    treatment_summary = treatment_text.get(
        "1.0",
        tk.END
    ).strip()

    discharge_instructions = instructions_text.get(
        "1.0",
        tk.END
    ).strip()


    # Validation

    if not patient:

        messagebox.showwarning(
            "Warning",
            "Please select a patient."
        )

        return


    if admission_date == "":

        messagebox.showwarning(
            "Warning",
            "Please enter admission date."
        )

        return


    if discharge_date == "":

        messagebox.showwarning(
            "Warning",
            "Please enter discharge date."
        )

        return


    if diagnosis == "":

        messagebox.showwarning(
            "Warning",
            "Please enter diagnosis."
        )

        return


    patient_id = patient_dict.get(patient)


    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO discharge
            (
                patient_id,
                admission_date,
                discharge_date,
                room_number,
                diagnosis,
                treatment_summary,
                discharge_instructions
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            admission_date,
            discharge_date,
            room_number,
            diagnosis,
            treatment_summary,
            discharge_instructions
        ))

        conn.commit()
        conn.close()


        # Make room available after discharge

        if room_number:

            try:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE room
                    SET
                        status = 'Available',
                        patient_id = NULL
                    WHERE room_number = ?
                """, (room_number,))

                conn.commit()
                conn.close()

            except Exception:
                pass


        messagebox.showinfo(
            "Success",
            "Patient discharged successfully."
        )


        clear_form()
        load_data()
        load_rooms()


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==========================================================
# LOAD DISCHARGE DATA
# ==========================================================

def load_data():

    for item in table.get_children():

        table.delete(item)


    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                d.discharge_id,
                p.name,
                d.admission_date,
                d.discharge_date,
                d.room_number,
                d.diagnosis,
                d.treatment_summary,
                d.discharge_instructions
            FROM discharge d
            LEFT JOIN patient p
                ON d.patient_id = p.patient_id
            ORDER BY d.discharge_id
        """)

        rows = cursor.fetchall()

        conn.close()


        for row in rows:

            table.insert(
                "",
                "end",
                values=row
            )


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load discharge records:\n{e}"
        )


# ==========================================================
# SELECT ROW
# ==========================================================

def select_row(event):

    selected = table.focus()

    if not selected:
        return


    values = table.item(
        selected,
        "values"
    )


    if not values:
        return


    discharge_id_var.set(values[0])


    patient_name = values[1]

    patient_var.set("")


    if patient_name:

        for display_value in patient_dict:

            if display_value.endswith(
                f" - {patient_name}"
            ):

                patient_var.set(
                    display_value
                )

                break


    admission_date_var.set(
        values[2]
    )

    discharge_date_var.set(
        values[3]
    )

    room_number_var.set(
        values[4]
    )

    diagnosis_var.set(
        values[5]
    )


    treatment_text.delete(
        "1.0",
        tk.END
    )

    treatment_text.insert(
        "1.0",
        values[6] if values[6] else ""
    )


    instructions_text.delete(
        "1.0",
        tk.END
    )

    instructions_text.insert(
        "1.0",
        values[7] if values[7] else ""
    )


# ==========================================================
# UPDATE DISCHARGE
# ==========================================================

def update_discharge():

    discharge_id = discharge_id_var.get()


    if not discharge_id:

        messagebox.showwarning(
            "Warning",
            "Please select a discharge record."
        )

        return


    patient = patient_var.get()

    if not patient:

        messagebox.showwarning(
            "Warning",
            "Please select a patient."
        )

        return


    patient_id = patient_dict.get(patient)


    admission_date = admission_date_var.get().strip()
    discharge_date = discharge_date_var.get().strip()
    room_number = room_number_var.get().strip()
    diagnosis = diagnosis_var.get().strip()


    treatment_summary = treatment_text.get(
        "1.0",
        tk.END
    ).strip()


    discharge_instructions = instructions_text.get(
        "1.0",
        tk.END
    ).strip()


    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE discharge
            SET
                patient_id = ?,
                admission_date = ?,
                discharge_date = ?,
                room_number = ?,
                diagnosis = ?,
                treatment_summary = ?,
                discharge_instructions = ?
            WHERE discharge_id = ?
        """, (
            patient_id,
            admission_date,
            discharge_date,
            room_number,
            diagnosis,
            treatment_summary,
            discharge_instructions,
            discharge_id
        ))

        conn.commit()
        conn.close()


        messagebox.showinfo(
            "Success",
            "Discharge record updated successfully."
        )


        clear_form()
        load_data()


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==========================================================
# DELETE DISCHARGE
# ==========================================================

def delete_discharge():

    discharge_id = discharge_id_var.get()


    if not discharge_id:

        messagebox.showwarning(
            "Warning",
            "Please select a discharge record."
        )

        return


    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this discharge record?"
    )


    if not confirm:
        return


    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM discharge
            WHERE discharge_id = ?
            """,
            (discharge_id,)
        )

        conn.commit()
        conn.close()


        messagebox.showinfo(
            "Success",
            "Discharge record deleted successfully."
        )


        clear_form()
        load_data()


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==========================================================
# CLEAR FORM
# ==========================================================

def clear_form():

    patient_var.set("")

    admission_date_var.set("")

    discharge_date_var.set("")

    room_number_var.set("")

    diagnosis_var.set("")


    treatment_text.delete(
        "1.0",
        tk.END
    )


    instructions_text.delete(
        "1.0",
        tk.END
    )


    get_next_discharge_id()


# ==========================================================
# SEARCH
# ==========================================================

def search_discharge():

    search_text = search_var.get().strip()


    for item in table.get_children():

        table.delete(item)


    try:

        conn = get_connection()
        cursor = conn.cursor()


        if search_text == "":

            cursor.execute("""
                SELECT
                    d.discharge_id,
                    p.name,
                    d.admission_date,
                    d.discharge_date,
                    d.room_number,
                    d.diagnosis,
                    d.treatment_summary,
                    d.discharge_instructions
                FROM discharge d
                LEFT JOIN patient p
                    ON d.patient_id = p.patient_id
                ORDER BY d.discharge_id
            """)


        else:

            cursor.execute("""
                SELECT
                    d.discharge_id,
                    p.name,
                    d.admission_date,
                    d.discharge_date,
                    d.room_number,
                    d.diagnosis,
                    d.treatment_summary,
                    d.discharge_instructions
                FROM discharge d
                LEFT JOIN patient p
                    ON d.patient_id = p.patient_id
                WHERE
                    CAST(d.discharge_id AS TEXT) LIKE ?
                    OR p.name LIKE ?
                    OR d.room_number LIKE ?
                    OR d.diagnosis LIKE ?
                ORDER BY d.discharge_id
            """, (
                "%" + search_text + "%",
                "%" + search_text + "%",
                "%" + search_text + "%",
                "%" + search_text + "%"
            ))


        rows = cursor.fetchall()

        conn.close()


        for row in rows:

            table.insert(
                "",
                "end",
                values=row
            )


    except Exception as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to search:\n{e}"
        )


# ==========================================================
# BUTTON FRAME
# ==========================================================

button_frame = tk.Frame(
    root,
    bg="white"
)

button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="ADD",
    font=("Arial", 14),
    width=12,
    command=add_discharge
).grid(
    row=0,
    column=0,
    padx=8
)


tk.Button(
    button_frame,
    text="UPDATE",
    font=("Arial", 14),
    width=12,
    command=update_discharge
).grid(
    row=0,
    column=1,
    padx=8
)


tk.Button(
    button_frame,
    text="DELETE",
    font=("Arial", 14),
    width=12,
    command=delete_discharge
).grid(
    row=0,
    column=2,
    padx=8
)


tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 14),
    width=12,
    command=clear_form
).grid(
    row=0,
    column=3,
    padx=8
)


tk.Button(
    button_frame,
    text="REFRESH",
    font=("Arial", 14),
    width=12,
    command=load_data
).grid(
    row=0,
    column=4,
    padx=8
)


# ==========================================================
# SEARCH FRAME
# ==========================================================

search_frame = tk.Frame(
    root,
    bg="white"
)

search_frame.pack(pady=8)


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


tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Arial", 15),
    width=30
).grid(
    row=0,
    column=1,
    padx=10
)


tk.Button(
    search_frame,
    text="SEARCH",
    font=("Arial", 14),
    width=12,
    command=search_discharge
).grid(
    row=0,
    column=2,
    padx=10
)


# ==========================================================
# TABLE FRAME
# ==========================================================

table_frame = tk.Frame(
    root
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ==========================================================
# TABLE
# ==========================================================

columns = (
    "Discharge ID",
    "Patient",
    "Admission Date",
    "Discharge Date",
    "Room",
    "Diagnosis",
    "Treatment Summary",
    "Instructions"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    table.heading(
        column,
        text=column
    )


# ==========================================================
# COLUMN WIDTHS
# ==========================================================

table.column(
    "Discharge ID",
    width=100,
    anchor="center"
)

table.column(
    "Patient",
    width=180,
    anchor="center"
)

table.column(
    "Admission Date",
    width=130,
    anchor="center"
)

table.column(
    "Discharge Date",
    width=130,
    anchor="center"
)

table.column(
    "Room",
    width=100,
    anchor="center"
)

table.column(
    "Diagnosis",
    width=180,
    anchor="center"
)

table.column(
    "Treatment Summary",
    width=250,
    anchor="center"
)

table.column(
    "Instructions",
    width=250,
    anchor="center"
)


# ==========================================================
# SCROLLBARS
# ==========================================================

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


table.pack(
    side="top",
    fill="both",
    expand=True
)


vertical_scrollbar.pack(
    side="right",
    fill="y"
)


horizontal_scrollbar.pack(
    side="bottom",
    fill="x"
)


# ==========================================================
# TABLE CLICK
# ==========================================================

table.bind(
    "<ButtonRelease-1>",
    select_row
)


# ==========================================================
# START PROGRAM
# ==========================================================

create_discharge_table()

load_patients()

load_rooms()

get_next_discharge_id()

load_data()

root.mainloop()