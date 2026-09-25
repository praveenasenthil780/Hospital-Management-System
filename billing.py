import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10)


# ==========================================================
# CREATE BILL TABLE
# ==========================================================

def create_bill_table():

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bill (
                bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                consultation_fee REAL DEFAULT 0,
                medicine_fee REAL DEFAULT 0,
                room_charges REAL DEFAULT 0,
                other_charges REAL DEFAULT 0,
                total_amount REAL DEFAULT 0
            )
        """)

        conn.commit()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to create bill table:\n\n{e}"
        )

    finally:

        if conn:
            conn.close()


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title(
    "Hospital Management System - Billing"
)

root.geometry(
    "1500x900"
)

root.minsize(
    1100,
    700
)

root.configure(
    bg="#F3F8FC"
)


# ==========================================================
# COLORS
# ==========================================================

BG_COLOR = "#F3F8FC"

HEADER_COLOR = "#006064"

BILL_COLOR = "#0277BD"

DARK_BLUE = "#01579B"

WHITE = "#FFFFFF"

TEXT_COLOR = "#17324D"

GRAY = "#607D8B"

GREEN = "#2E7D32"

ORANGE = "#EF6C00"

RED = "#C62828"

LIGHT_BLUE = "#E3F2FD"


# ==========================================================
# VARIABLES
# ==========================================================

bill_id_var = tk.StringVar(
    master=root
)

patient_var = tk.StringVar(
    master=root
)

consultation_var = tk.StringVar(
    master=root
)

medicine_var = tk.StringVar(
    master=root
)

room_var = tk.StringVar(
    master=root
)

other_var = tk.StringVar(
    master=root
)

total_var = tk.StringVar(
    master=root
)

search_var = tk.StringVar(
    master=root
)


# Store patient IDs
patient_dict = {}


# ==========================================================
# HEADER
# ==========================================================

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
    text="Healthcare Administration  •  Billing Management",
    font=("Segoe UI", 10),
    bg=HEADER_COLOR,
    fg="#B2EBF2"
).pack(
    anchor="w"
)


# ==========================================================
# PAGE TITLE
# ==========================================================

tk.Label(
    root,
    text="💳  BILLING MANAGEMENT",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=DARK_BLUE
).pack(
    pady=(20, 3)
)


tk.Label(
    root,
    text="Manage patient bills, charges and payment records",
    font=("Segoe UI", 10),
    bg=BG_COLOR,
    fg=GRAY
).pack(
    pady=(0, 15)
)


# ==========================================================
# FORM CARD
# ==========================================================

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
    text="💰  BILL DETAILS",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=BILL_COLOR
).grid(
    row=0,
    column=0,
    columnspan=4,
    pady=(15, 12)
)


# ==========================================================
# BILL ID
# ==========================================================

tk.Label(
    form_card,
    text="Bill ID",
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


bill_id_entry = tk.Entry(
    form_card,
    textvariable=bill_id_var,
    width=28,
    font=("Segoe UI", 10),
    state="readonly"
)

bill_id_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# ==========================================================
# PATIENT
# ==========================================================

tk.Label(
    form_card,
    text="Patient",
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


patient_combo = ttk.Combobox(
    form_card,
    textvariable=patient_var,
    state="readonly",
    width=26,
    font=("Segoe UI", 10)
)

patient_combo.grid(
    row=1,
    column=3,
    padx=10,
    pady=7
)


# ==========================================================
# CONSULTATION FEE
# ==========================================================

tk.Label(
    form_card,
    text="Consultation Fee",
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


consultation_entry = tk.Entry(
    form_card,
    textvariable=consultation_var,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

consultation_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


# ==========================================================
# MEDICINE FEE
# ==========================================================

tk.Label(
    form_card,
    text="Medicine Fee",
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
    textvariable=medicine_var,
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


# ==========================================================
# ROOM CHARGES
# ==========================================================

tk.Label(
    form_card,
    text="Room Charges",
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


room_entry = tk.Entry(
    form_card,
    textvariable=room_var,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

room_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=7
)


# ==========================================================
# OTHER CHARGES
# ==========================================================

tk.Label(
    form_card,
    text="Other Charges",
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


other_entry = tk.Entry(
    form_card,
    textvariable=other_var,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

other_entry.grid(
    row=3,
    column=3,
    padx=10,
    pady=7
)


# ==========================================================
# TOTAL
# ==========================================================

tk.Label(
    form_card,
    text="Total Amount",
    font=("Segoe UI", 11, "bold"),
    bg=WHITE,
    fg=GREEN
).grid(
    row=4,
    column=0,
    padx=15,
    pady=10,
    sticky="e"
)


total_entry = tk.Entry(
    form_card,
    textvariable=total_var,
    width=28,
    font=("Segoe UI", 12, "bold"),
    state="readonly",
    readonlybackground="#E8F5E9",
    fg=GREEN
)

total_entry.grid(
    row=4,
    column=1,
    padx=10,
    pady=10
)


# ==========================================================
# CALCULATE TOTAL
# ==========================================================

def calculate_total(*args):

    try:
        consultation = float(
            consultation_var.get() or 0
        )
    except ValueError:
        consultation = 0

    try:
        medicine = float(
            medicine_var.get() or 0
        )
    except ValueError:
        medicine = 0

    try:
        room = float(
            room_var.get() or 0
        )
    except ValueError:
        room = 0

    try:
        other = float(
            other_var.get() or 0
        )
    except ValueError:
        other = 0

    total = (
        consultation
        + medicine
        + room
        + other
    )

    total_var.set(
        f"{total:.2f}"
    )


consultation_var.trace_add(
    "write",
    calculate_total
)

medicine_var.trace_add(
    "write",
    calculate_total
)

room_var.trace_add(
    "write",
    calculate_total
)

other_var.trace_add(
    "write",
    calculate_total
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

            display_value = (
                f"{patient_id} - {name}"
            )

            patient_dict[
                display_value
            ] = patient_id

            patient_values.append(
                display_value
            )

        patient_combo["values"] = patient_values

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load patients:\n\n{e}"
        )


# ==========================================================
# NEXT BILL ID
# ==========================================================

def get_next_bill_id():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(
                MAX(bill_id), 0
            ) + 1
            FROM bill
        """)

        next_id = cursor.fetchone()[0]

        conn.close()

        bill_id_var.set(
            str(next_id)
        )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to get Bill ID:\n\n{e}"
        )


# ==========================================================
# ADD BILL
# ==========================================================

def add_bill():

    patient = patient_var.get().strip()

    if not patient:

        messagebox.showwarning(
            "Warning",
            "Please select a patient."
        )

        return

    patient_id = patient_dict.get(
        patient
    )

    if patient_id is None:

        messagebox.showwarning(
            "Warning",
            "Invalid patient selected."
        )

        return

    try:

        consultation = float(
            consultation_var.get() or 0
        )

        medicine = float(
            medicine_var.get() or 0
        )

        room = float(
            room_var.get() or 0
        )

        other = float(
            other_var.get() or 0
        )

    except ValueError:

        messagebox.showwarning(
            "Warning",
            "Please enter valid numbers for all charges."
        )

        return

    if (
        consultation < 0
        or medicine < 0
        or room < 0
        or other < 0
    ):

        messagebox.showwarning(
            "Warning",
            "Charges cannot be negative."
        )

        return

    total = (
        consultation
        + medicine
        + room
        + other
    )

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bill
            (
                patient_id,
                consultation_fee,
                medicine_fee,
                room_charges,
                other_charges,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            consultation,
            medicine,
            room,
            other,
            total
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Bill added successfully."
        )

        clear_form()
        load_data()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if conn:
            conn.close()


# ==========================================================
# LOAD BILL DATA
# ==========================================================

def load_data():

    for item in table.get_children():

        table.delete(item)

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                b.bill_id,
                p.name,
                b.consultation_fee,
                b.medicine_fee,
                b.room_charges,
                b.other_charges,
                b.total_amount
            FROM bill b
            LEFT JOIN patient p
                ON b.patient_id = p.patient_id
            ORDER BY b.bill_id
        """)

        rows = cursor.fetchall()

        for row in rows:

            table.insert(
                "",
                "end",
                values=row
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load bills:\n\n{e}"
        )

    finally:

        if conn:
            conn.close()


# ==========================================================
# SELECT TABLE ROW
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

    bill_id_var.set(
        values[0]
    )

    patient_name = str(
        values[1]
    )

    # Find patient ID/name combination
    for display_value in patient_dict:

        if display_value.endswith(
            f" - {patient_name}"
        ):

            patient_var.set(
                display_value
            )

            break

    consultation_var.set(
        values[2]
    )

    medicine_var.set(
        values[3]
    )

    room_var.set(
        values[4]
    )

    other_var.set(
        values[5]
    )

    total_var.set(
        values[6]
    )


# ==========================================================
# UPDATE BILL
# ==========================================================

def update_bill():

    bill_id = bill_id_var.get().strip()

    if not bill_id:

        messagebox.showwarning(
            "Warning",
            "Please select a bill."
        )

        return

    patient = patient_var.get().strip()

    if not patient:

        messagebox.showwarning(
            "Warning",
            "Please select a patient."
        )

        return

    patient_id = patient_dict.get(
        patient
    )

    if patient_id is None:

        messagebox.showwarning(
            "Warning",
            "Invalid patient selected."
        )

        return

    try:

        consultation = float(
            consultation_var.get() or 0
        )

        medicine = float(
            medicine_var.get() or 0
        )

        room = float(
            room_var.get() or 0
        )

        other = float(
            other_var.get() or 0
        )

    except ValueError:

        messagebox.showwarning(
            "Warning",
            "Please enter valid amounts."
        )

        return

    total = (
        consultation
        + medicine
        + room
        + other
    )

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE bill
            SET
                patient_id = ?,
                consultation_fee = ?,
                medicine_fee = ?,
                room_charges = ?,
                other_charges = ?,
                total_amount = ?
            WHERE bill_id = ?
        """, (
            patient_id,
            consultation,
            medicine,
            room,
            other,
            total,
            bill_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            messagebox.showerror(
                "Error",
                "Bill not found."
            )

            return

        messagebox.showinfo(
            "Success",
            "Bill updated successfully."
        )

        clear_form()
        load_data()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if conn:
            conn.close()


# ==========================================================
# DELETE BILL
# ==========================================================

def delete_bill():

    bill_id = bill_id_var.get().strip()

    if not bill_id:

        messagebox.showwarning(
            "Warning",
            "Please select a bill."
        )

        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this bill?"
    )

    if not confirm:
        return

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM bill
            WHERE bill_id = ?
            """,
            (bill_id,)
        )

        conn.commit()

        if cursor.rowcount == 0:

            messagebox.showerror(
                "Error",
                "Bill not found."
            )

            return

        messagebox.showinfo(
            "Success",
            "Bill deleted successfully."
        )

        clear_form()
        load_data()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        if conn:
            conn.close()


# ==========================================================
# CLEAR FORM
# ==========================================================

def clear_form():

    patient_var.set("")

    consultation_var.set("")

    medicine_var.set("")

    room_var.set("")

    other_var.set("")

    total_var.set("")

    get_next_bill_id()


# ==========================================================
# SEARCH BILL
# ==========================================================

def search_bill():

    search_text = (
        search_var.get()
        .strip()
    )

    for item in table.get_children():

        table.delete(item)

    conn = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        if search_text == "":

            cursor.execute("""
                SELECT
                    b.bill_id,
                    p.name,
                    b.consultation_fee,
                    b.medicine_fee,
                    b.room_charges,
                    b.other_charges,
                    b.total_amount
                FROM bill b
                LEFT JOIN patient p
                    ON b.patient_id = p.patient_id
                ORDER BY b.bill_id
            """)

        else:

            cursor.execute("""
                SELECT
                    b.bill_id,
                    p.name,
                    b.consultation_fee,
                    b.medicine_fee,
                    b.room_charges,
                    b.other_charges,
                    b.total_amount
                FROM bill b
                LEFT JOIN patient p
                    ON b.patient_id = p.patient_id
                WHERE
                    CAST(
                        b.bill_id AS TEXT
                    ) LIKE ?
                    OR p.name LIKE ?
                ORDER BY b.bill_id
            """, (
                "%" + search_text + "%",
                "%" + search_text + "%"
            ))

        rows = cursor.fetchall()

        for row in rows:

            table.insert(
                "",
                "end",
                values=row
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to search:\n\n{e}"
        )

    finally:

        if conn:
            conn.close()


# ==========================================================
# BUTTON FRAME
# ==========================================================

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


# ==========================================================
# ADD BUTTON
# ==========================================================

tk.Button(
    button_frame,
    text="➕ ADD BILL",
    width=16,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=BILL_COLOR,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=add_bill
).grid(
    row=0,
    column=0,
    padx=5
)


# ==========================================================
# UPDATE BUTTON
# ==========================================================

tk.Button(
    button_frame,
    text="✏️ UPDATE",
    width=16,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=ORANGE,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=update_bill
).grid(
    row=0,
    column=1,
    padx=5
)


# ==========================================================
# DELETE BUTTON
# ==========================================================

tk.Button(
    button_frame,
    text="🗑️ DELETE",
    width=16,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=RED,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=delete_bill
).grid(
    row=0,
    column=2,
    padx=5
)


# ==========================================================
# CLEAR BUTTON
# ==========================================================

tk.Button(
    button_frame,
    text="🔄 CLEAR",
    width=16,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=GRAY,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=clear_form
).grid(
    row=0,
    column=3,
    padx=5
)


# ==========================================================
# REFRESH BUTTON
# ==========================================================

tk.Button(
    button_frame,
    text="⟳ REFRESH",
    width=16,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=GREEN,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=lambda: (
        load_patients(),
        load_data(),
        get_next_bill_id()
    )
).grid(
    row=0,
    column=4,
    padx=5
)


# ==========================================================
# SEARCH CARD
# ==========================================================

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
    text="🔍 SEARCH BILL",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE,
    fg=BILL_COLOR
).pack(
    side="left",
    padx=20,
    pady=14
)


search_entry = tk.Entry(
    search_card,
    textvariable=search_var,
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
    bg=BILL_COLOR,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_bill
).pack(
    side="left",
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
    pady=5
)


tk.Label(
    table_card,
    text="📋  BILL RECORDS",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=BILL_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(12, 5)
)


# ==========================================================
# TABLE FRAME
# ==========================================================

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


# ==========================================================
# TREEVIEW STYLE
# ==========================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except:
    pass


style.configure(
    "Bill.Treeview",
    font=("Segoe UI", 10),
    rowheight=32,
    background=WHITE,
    fieldbackground=WHITE,
    foreground=TEXT_COLOR
)


style.configure(
    "Bill.Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=BILL_COLOR,
    foreground=WHITE
)


style.map(
    "Bill.Treeview",
    background=[
        ("selected", "#BBDEFB")
    ],
    foreground=[
        ("selected", TEXT_COLOR)
    ]
)


# ==========================================================
# SCROLLBAR
# ==========================================================

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


# ==========================================================
# TABLE
# ==========================================================

columns = (
    "Bill ID",
    "Patient",
    "Consultation",
    "Medicine Fee",
    "Room Charges",
    "Other Charges",
    "Total"
)


table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    style="Bill.Treeview",
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


vertical_scrollbar.config(
    command=table.yview
)


horizontal_scrollbar.config(
    command=table.xview
)


# ==========================================================
# HEADINGS
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
    "Bill ID",
    width=100,
    anchor="center"
)

table.column(
    "Patient",
    width=240,
    anchor="center"
)

table.column(
    "Consultation",
    width=170,
    anchor="center"
)

table.column(
    "Medicine Fee",
    width=170,
    anchor="center"
)

table.column(
    "Room Charges",
    width=170,
    anchor="center"
)

table.column(
    "Other Charges",
    width=170,
    anchor="center"
)

table.column(
    "Total",
    width=170,
    anchor="center"
)


table.pack(
    fill="both",
    expand=True
)


# ==========================================================
# SELECT ROW
# ==========================================================

table.bind(
    "<ButtonRelease-1>",
    select_row
)


# ==========================================================
# ENTER KEY SEARCH
# ==========================================================

search_entry.bind(
    "<Return>",
    lambda event: search_bill()
)


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

create_bill_table()

load_patients()

get_next_bill_id()

load_data()


# ==========================================================
# START PROGRAM
# ==========================================================

root.mainloop()