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

root.title("Hospital Management System - Discharge")
root.geometry("1500x900")
root.configure(bg="#F4F7FB")


# ==========================================================
# COLORS
# ==========================================================

BG_COLOR = "#F4F7FB"
HEADER_COLOR = "#173F5F"
TITLE_COLOR = "#173F5F"

CARD_COLOR = "#FFFFFF"

LABEL_COLOR = "#34495E"

ENTRY_BG = "#F8FAFC"

ADD_COLOR = "#27AE60"
UPDATE_COLOR = "#2980B9"
DELETE_COLOR = "#E74C3C"
CLEAR_COLOR = "#F39C12"
REFRESH_COLOR = "#8E44AD"
SEARCH_COLOR = "#16A085"

WHITE = "#FFFFFF"


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

patient_dict = {}


# ==========================================================
# TITLE
# ==========================================================

header_frame = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=90
)

header_frame.pack(
    fill="x"
)

header_frame.pack_propagate(False)


tk.Label(
    header_frame,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 26, "bold"),
    bg=HEADER_COLOR,
    fg=WHITE
).pack(pady=(12, 2))


tk.Label(
    header_frame,
    text="DISCHARGE MANAGEMENT",
    font=("Arial", 15, "bold"),
    bg=HEADER_COLOR,
    fg="#D6EAF8"
).pack()


# ==========================================================
# FORM CARD
# ==========================================================

form_card = tk.Frame(
    root,
    bg=CARD_COLOR,
    bd=1,
    relief="solid"
)

form_card.pack(
    padx=30,
    pady=20,
    fill="x"
)


tk.Label(
    form_card,
    text="Discharge Details",
    font=("Arial", 20, "bold"),
    bg=CARD_COLOR,
    fg=TITLE_COLOR
).grid(
    row=0,
    column=0,
    columnspan=4,
    pady=(18, 15)
)


# ==========================================================
# FORM STYLE FUNCTION
# ==========================================================

def create_label(text, row, column):

    tk.Label(
        form_card,
        text=text,
        font=("Arial", 12, "bold"),
        bg=CARD_COLOR,
        fg=LABEL_COLOR
    ).grid(
        row=row,
        column=column,
        padx=15,
        pady=9,
        sticky="e"
    )


# ==========================================================
# DISCHARGE ID
# ==========================================================

create_label(
    "Discharge ID",
    1,
    0
)


tk.Entry(
    form_card,
    textvariable=discharge_id_var,
    font=("Arial", 12),
    width=27,
    state="readonly",
    readonlybackground="#EAECEE"
).grid(
    row=1,
    column=1,
    padx=15,
    pady=9
)


# ==========================================================
# PATIENT
# ==========================================================

create_label(
    "Patient",
    2,
    0
)


patient_combo = ttk.Combobox(
    form_card,
    textvariable=patient_var,
    font=("Arial", 12),
    width=25,
    state="readonly"
)

patient_combo.grid(
    row=2,
    column=1,
    padx=15,
    pady=9
)


# ==========================================================
# ADMISSION DATE
# ==========================================================

create_label(
    "Admission Date",
    3,
    0
)


tk.Entry(
    form_card,
    textvariable=admission_date_var,
    font=("Arial", 12),
    width=27,
    bg=ENTRY_BG
).grid(
    row=3,
    column=1,
    padx=15,
    pady=9
)


# ==========================================================
# DISCHARGE DATE
# ==========================================================

create_label(
    "Discharge Date",
    4,
    0
)


tk.Entry(
    form_card,
    textvariable=discharge_date_var,
    font=("Arial", 12),
    width=27,
    bg=ENTRY_BG
).grid(
    row=4,
    column=1,
    padx=15,
    pady=9
)


# ==========================================================
# ROOM
# ==========================================================

create_label(
    "Room Number",
    5,
    0
)


room_combo = ttk.Combobox(
    form_card,
    textvariable=room_number_var,
    font=("Arial", 12),
    width=25
)

room_combo.grid(
    row=5,
    column=1,
    padx=15,
    pady=9
)


# ==========================================================
# DIAGNOSIS
# ==========================================================

create_label(
    "Diagnosis",
    6,
    0
)


tk.Entry(
    form_card,
    textvariable=diagnosis_var,
    font=("Arial", 12),
    width=27,
    bg=ENTRY_BG
).grid(
    row=6,
    column=1,
    padx=15,
    pady=9
)


# ==========================================================
# TREATMENT SUMMARY
# ==========================================================

tk.Label(
    form_card,
    text="Treatment Summary",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=LABEL_COLOR
).grid(
    row=1,
    column=2,
    padx=15,
    pady=9,
    sticky="ne"
)


treatment_text = tk.Text(
    form_card,
    width=38,
    height=6,
    font=("Arial", 11),
    bg=ENTRY_BG,
    relief="solid",
    bd=1
)

treatment_text.grid(
    row=1,
    column=3,
    rowspan=3,
    padx=15,
    pady=9
)


# ==========================================================
# DISCHARGE INSTRUCTIONS
# ==========================================================

tk.Label(
    form_card,
    text="Discharge Instructions",
    font=("Arial", 12, "bold"),
    bg=CARD_COLOR,
    fg=LABEL_COLOR
).grid(
    row=4,
    column=2,
    padx=15,
    pady=9,
    sticky="ne"
)


instructions_text = tk.Text(
    form_card,
    width=38,
    height=6,
    font=("Arial", 11),
    bg=ENTRY_BG,
    relief="solid",
    bd=1
)

instructions_text.grid(
    row=4,
    column=3,
    rowspan=3,
    padx=15,
    pady=9
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

        # Make room available

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
# LOAD DATA
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

    admission_date_var.set(values[2])
    discharge_date_var.set(values[3])
    room_number_var.set(values[4])
    diagnosis_var.set(values[5])

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
# BUTTON FUNCTION
# ==========================================================

def create_button(
    parent,
    text,
    color,
    command,
    column
):

    button = tk.Button(
        parent,
        text=text,
        font=("Arial", 11, "bold"),
        width=13,
        height=2,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        command=command
    )

    button.grid(
        row=0,
        column=column,
        padx=7
    )

    return button


# ==========================================================
# BUTTON FRAME
# ==========================================================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(
    pady=5
)


create_button(
    button_frame,
    "ADD",
    ADD_COLOR,
    add_discharge,
    0
)


create_button(
    button_frame,
    "UPDATE",
    UPDATE_COLOR,
    update_discharge,
    1
)


create_button(
    button_frame,
    "DELETE",
    DELETE_COLOR,
    delete_discharge,
    2
)


create_button(
    button_frame,
    "CLEAR",
    CLEAR_COLOR,
    clear_form,
    3
)


create_button(
    button_frame,
    "REFRESH",
    REFRESH_COLOR,
    load_data,
    4
)


# ==========================================================
# SEARCH FRAME
# ==========================================================

search_card = tk.Frame(
    root,
    bg=CARD_COLOR,
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
    text="Search Discharge",
    font=("Arial", 14, "bold"),
    bg=CARD_COLOR,
    fg=LABEL_COLOR
).grid(
    row=0,
    column=0,
    padx=15,
    pady=12
)


search_entry = tk.Entry(
    search_card,
    textvariable=search_var,
    font=("Arial", 12),
    width=40,
    bg=ENTRY_BG
)

search_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=12
)


tk.Button(
    search_card,
    text="SEARCH",
    font=("Arial", 11, "bold"),
    width=12,
    height=2,
    bg=SEARCH_COLOR,
    fg=WHITE,
    activebackground=SEARCH_COLOR,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_discharge
).grid(
    row=0,
    column=2,
    padx=10
)


# ==========================================================
# TABLE CARD
# ==========================================================

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
    table_card,
    columns=columns,
    show="headings",
    selectmode="browse"
)


# ==========================================================
# TABLE HEADINGS
# ==========================================================

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
    width=280,
    anchor="w"
)

table.column(
    "Instructions",
    width=280,
    anchor="w"
)


# ==========================================================
# TABLE STYLE
# ==========================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="#FFFFFF",
    foreground="#2C3E50",
    rowheight=35,
    fieldbackground="#FFFFFF",
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background=HEADER_COLOR,
    foreground=WHITE,
    font=("Arial", 11, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#D6EAF8")
    ],
    foreground=[
        ("selected", "#173F5F")
    ]
)


# ==========================================================
# SCROLLBARS
# ==========================================================

vertical_scrollbar = ttk.Scrollbar(
    table_card,
    orient="vertical",
    command=table.yview
)


horizontal_scrollbar = ttk.Scrollbar(
    table_card,
    orient="horizontal",
    command=table.xview
)


table.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


table.pack(
    side="left",
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
# FOOTER
# ==========================================================

tk.Label(
    root,
    text="Hospital Management System | Discharge Module",
    font=("Arial", 10),
    bg=BG_COLOR,
    fg="#7F8C8D"
).pack(
    pady=8
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