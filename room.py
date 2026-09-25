import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F3F8FC"
HEADER_COLOR = "#006064"
ROOM_COLOR = "#0277BD"
DARK_BLUE = "#01579B"

WHITE = "#FFFFFF"
TEXT_COLOR = "#17324D"
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
# CREATE ROOM TABLE
# =========================================================

def create_room_table():

    conn = connect_db()
    cursor = conn.cursor()

    # Create room table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL UNIQUE,
            room_type TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(room)")
    columns = [row[1] for row in cursor.fetchall()]

    # Add patient_name if it is missing
    if "patient_name" not in columns:
        cursor.execute("""
            ALTER TABLE room
            ADD COLUMN patient_name TEXT
        """)

    conn.commit()
    conn.close()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS room (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL UNIQUE,
            room_type TEXT NOT NULL,
            status TEXT NOT NULL,
            patient_name TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# LOAD PATIENTS
# =========================================================

def load_patients():

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT patient_id, name
            FROM patient
            ORDER BY name
        """)

        patients = cursor.fetchall()

        conn.close()

        patient_entry["values"] = [
            f"{patient[0]} - {patient[1]}"
            for patient in patients
        ]

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            f"Unable to load patients.\n\n{e}"
        )


# =========================================================
# GET PATIENT NAME
# =========================================================

def get_patient_name():

    selected = patient_entry.get().strip()

    if selected == "":
        return ""

    if " - " in selected:

        return selected.split(
            " - ",
            1
        )[1]

    return selected


# =========================================================
# CLEAR FIELDS
# =========================================================

def clear_fields():

    room_id_entry.config(
        state="normal"
    )

    room_id_entry.delete(
        0,
        tk.END
    )

    room_id_entry.config(
        state="readonly"
    )

    room_number_entry.delete(
        0,
        tk.END
    )

    room_type_combo.set("")

    status_combo.set("Available")

    patient_entry.set("")


# =========================================================
# ADD ROOM
# =========================================================

def add_room():

    room_number = room_number_entry.get().strip()
    room_type = room_type_combo.get().strip()
    status = status_combo.get().strip()
    patient_name = get_patient_name()

    if room_number == "":

        messagebox.showerror(
            "Error",
            "Please enter Room Number"
        )

        return

    if room_type == "":

        messagebox.showerror(
            "Error",
            "Please select Room Type"
        )

        return

    if status == "":

        messagebox.showerror(
            "Error",
            "Please select Room Status"
        )

        return

    # Available room should not have a patient
    if status == "Available":

        patient_name = ""

    # Occupied room should have a patient
    if status == "Occupied" and patient_name == "":

        messagebox.showerror(
            "Error",
            "Please select Patient Name for an occupied room"
        )

        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO room
            (
                room_number,
                room_type,
                status,
                patient_name
            )
            VALUES (?, ?, ?, ?)
        """, (
            room_number,
            room_type,
            status,
            patient_name
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Room added successfully!"
        )

        clear_fields()
        view_rooms()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Room number already exists"
        )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# VIEW ROOMS
# =========================================================

def view_rooms():

    for item in room_table.get_children():

        room_table.delete(item)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                room_id,
                room_number,
                room_type,
                status,
                patient_name
            FROM room
            ORDER BY room_id
        """)

        rooms = cursor.fetchall()

        conn.close()

        for room in rooms:

            room_table.insert(
                "",
                tk.END,
                values=room
            )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SELECT ROOM
# =========================================================

def select_room(event):

    selected = room_table.focus()

    if not selected:
        return

    values = room_table.item(
        selected,
        "values"
    )

    if not values:
        return

    clear_fields()

    room_id_entry.config(
        state="normal"
    )

    room_id_entry.insert(
        0,
        values[0]
    )

    room_id_entry.config(
        state="readonly"
    )

    room_number_entry.insert(
        0,
        values[1]
    )

    room_type_combo.set(
        values[2]
    )

    status_combo.set(
        values[3]
    )

    patient_name = values[4]

    if patient_name:

        # Find matching patient in dropdown
        found = False

        for patient in patient_entry["values"]:

            if patient.endswith(
                f" - {patient_name}"
            ):

                patient_entry.set(
                    patient
                )

                found = True
                break

        # If patient is not found in database,
        # display the stored name
        if not found:

            patient_entry.set(
                patient_name
            )


# =========================================================
# UPDATE ROOM
# =========================================================

def update_room():

    room_id = room_id_entry.get().strip()
    room_number = room_number_entry.get().strip()
    room_type = room_type_combo.get().strip()
    status = status_combo.get().strip()
    patient_name = get_patient_name()

    if room_id == "":

        messagebox.showerror(
            "Error",
            "Please select a room from the table"
        )

        return

    if room_number == "":

        messagebox.showerror(
            "Error",
            "Please enter Room Number"
        )

        return

    if room_type == "":

        messagebox.showerror(
            "Error",
            "Please select Room Type"
        )

        return

    if status == "":

        messagebox.showerror(
            "Error",
            "Please select Room Status"
        )

        return

    if status == "Available":

        patient_name = ""

    if status == "Occupied" and patient_name == "":

        messagebox.showerror(
            "Error",
            "Please select Patient Name for an occupied room"
        )

        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE room
            SET
                room_number = ?,
                room_type = ?,
                status = ?,
                patient_name = ?
            WHERE room_id = ?
        """, (
            room_number,
            room_type,
            status,
            patient_name,
            room_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            messagebox.showerror(
                "Error",
                "Room not found"
            )

            return

        conn.close()

        messagebox.showinfo(
            "Success",
            "Room updated successfully!"
        )

        clear_fields()
        view_rooms()

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Room number already exists"
        )

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# DELETE ROOM
# =========================================================

def delete_room():

    room_id = room_id_entry.get().strip()

    if room_id == "":

        messagebox.showerror(
            "Error",
            "Please select a room"
        )

        return

    confirm = messagebox.askyesno(
        "Delete Room",
        "Are you sure you want to delete this room?"
    )

    if not confirm:
        return

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM room
            WHERE room_id = ?
        """, (
            room_id,
        ))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            messagebox.showerror(
                "Error",
                "Room not found"
            )

            return

        conn.close()

        messagebox.showinfo(
            "Success",
            "Room deleted successfully!"
        )

        clear_fields()
        view_rooms()

    except sqlite3.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# =========================================================
# SEARCH ROOM
# =========================================================

def search_room():

    search_text = search_entry.get().strip()

    if search_text == "":

        view_rooms()

        return

    for item in room_table.get_children():

        room_table.delete(item)

    try:

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                room_id,
                room_number,
                room_type,
                status,
                patient_name

            FROM room

            WHERE
                CAST(room_id AS TEXT) LIKE ?
                OR room_number LIKE ?
                OR room_type LIKE ?
                OR status LIKE ?
                OR patient_name LIKE ?

            ORDER BY room_id
        """, (
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%",
            "%" + search_text + "%"
        ))

        rooms = cursor.fetchall()

        conn.close()

        for room in rooms:

            room_table.insert(
                "",
                tk.END,
                values=room
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
    "Hospital Management System - Room Management"
)

root.geometry(
    "1250x850"
)

root.minsize(
    1000,
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
    text="Healthcare Administration  •  Room Management",
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
    text="🛏️  ROOM MANAGEMENT",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=DARK_BLUE
).pack(
    pady=(20, 3)
)


tk.Label(
    root,
    text="Manage hospital rooms and their availability",
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
    text="🛏️  ROOM DETAILS",
    font=("Segoe UI", 17, "bold"),
    bg=WHITE,
    fg=ROOM_COLOR
).grid(
    row=0,
    column=0,
    columnspan=4,
    pady=(15, 12)
)


# =========================================================
# ROOM ID
# =========================================================

tk.Label(
    form_card,
    text="Room ID",
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


room_id_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    state="readonly"
)

room_id_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# ROOM NUMBER
# =========================================================

tk.Label(
    form_card,
    text="Room Number",
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


room_number_entry = tk.Entry(
    form_card,
    width=28,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1
)

room_number_entry.grid(
    row=1,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# ROOM TYPE
# =========================================================

tk.Label(
    form_card,
    text="Room Type",
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


room_type_combo = ttk.Combobox(
    form_card,
    values=[
        "General Ward",
        "Private Room",
        "Semi Private",
        "ICU",
        "Emergency",
        "Operation Theatre"
    ],
    state="readonly",
    width=26,
    font=("Segoe UI", 10)
)

room_type_combo.grid(
    row=2,
    column=1,
    padx=10,
    pady=7
)


# =========================================================
# STATUS
# =========================================================

tk.Label(
    form_card,
    text="Room Status",
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


status_combo = ttk.Combobox(
    form_card,
    values=[
        "Available",
        "Occupied",
        "Maintenance"
    ],
    state="readonly",
    width=26,
    font=("Segoe UI", 10)
)

status_combo.set(
    "Available"
)

status_combo.grid(
    row=2,
    column=3,
    padx=10,
    pady=7
)


# =========================================================
# PATIENT NAME DROPDOWN
# =========================================================

tk.Label(
    form_card,
    text="Patient Name",
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


patient_entry = ttk.Combobox(
    form_card,
    width=26,
    font=("Segoe UI", 10),
    state="readonly"
)

patient_entry.grid(
    row=3,
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
    row=4,
    column=0,
    columnspan=4,
    pady=18
)


tk.Button(
    button_frame,
    text="➕ ADD ROOM",
    width=16,
    height=2,
    font=("Segoe UI", 10, "bold"),
    bg=ROOM_COLOR,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=add_room
).grid(
    row=0,
    column=0,
    padx=5
)


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
    command=update_room
).grid(
    row=0,
    column=1,
    padx=5
)


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
    command=delete_room
).grid(
    row=0,
    column=2,
    padx=5
)


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
    command=clear_fields
).grid(
    row=0,
    column=3,
    padx=5
)


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
    command=view_rooms
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
    text="🔍 SEARCH ROOM",
    font=("Segoe UI", 15, "bold"),
    bg=WHITE,
    fg=ROOM_COLOR
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
    bg=ROOM_COLOR,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    command=search_room
).pack(
    side="left",
    padx=10
)


# =========================================================
# TABLE
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
    text="📋  ROOM RECORDS",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=ROOM_COLOR
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
    "Room.Treeview",
    font=("Segoe UI", 10),
    rowheight=32,
    background=WHITE,
    fieldbackground=WHITE
)

style.configure(
    "Room.Treeview.Heading",
    font=("Segoe UI", 10, "bold"),
    background=ROOM_COLOR,
    foreground=WHITE
)

style.map(
    "Room.Treeview",
    background=[
        ("selected", "#BBDEFB")
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
    "Room Number",
    "Room Type",
    "Status",
    "Patient"
)


room_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    style="Room.Treeview",
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


vertical_scrollbar.config(
    command=room_table.yview
)

horizontal_scrollbar.config(
    command=room_table.xview
)


room_table.heading(
    "ID",
    text="Room ID"
)

room_table.heading(
    "Room Number",
    text="Room Number"
)

room_table.heading(
    "Room Type",
    text="Room Type"
)

room_table.heading(
    "Status",
    text="Status"
)

room_table.heading(
    "Patient",
    text="Patient Name"
)


room_table.column(
    "ID",
    width=100,
    anchor="center"
)

room_table.column(
    "Room Number",
    width=180,
    anchor="center"
)

room_table.column(
    "Room Type",
    width=220,
    anchor="center"
)

room_table.column(
    "Status",
    width=180,
    anchor="center"
)

room_table.column(
    "Patient",
    width=250,
    anchor="center"
)


room_table.pack(
    fill="both",
    expand=True
)


# =========================================================
# SELECT RECORD
# =========================================================

room_table.bind(
    "<ButtonRelease-1>",
    select_room
)


# =========================================================
# START
# =========================================================

create_room_table()

load_patients()

view_rooms()

root.mainloop()