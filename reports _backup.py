import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ==========================================================
# GLOBAL DATA
# ==========================================================

current_report_name = "Report"
current_columns = []
current_rows = []


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title("Hospital Management System - Reports")

root.geometry("1450x850")

root.configure(bg="white")


# ==========================================================
# TITLE
# ==========================================================

title = tk.Label(
    root,
    text="HOSPITAL REPORTS",
    font=("Arial", 30, "bold"),
    bg="white",
    fg="black"
)

title.pack(pady=20)


# ==========================================================
# SEARCH
# ==========================================================

search_var = tk.StringVar()


search_frame = tk.Frame(
    root,
    bg="white"
)

search_frame.pack(pady=10)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 15, "bold"),
    bg="white"
).grid(
    row=0,
    column=0,
    padx=5
)


search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Arial", 14),
    width=30
)

search_entry.grid(
    row=0,
    column=1,
    padx=5
)


# ==========================================================
# TABLE FRAME
# ==========================================================

table_frame = tk.Frame(
    root,
    bg="white"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


# ==========================================================
# TREEVIEW
# ==========================================================

table = ttk.Treeview(
    table_frame,
    show="headings"
)

table.pack(
    side="left",
    fill="both",
    expand=True
)


# ==========================================================
# SCROLLBARS
# ==========================================================

vertical_scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

vertical_scrollbar.pack(
    side="right",
    fill="y"
)


horizontal_scrollbar = ttk.Scrollbar(
    root,
    orient="horizontal",
    command=table.xview
)

horizontal_scrollbar.pack(
    fill="x",
    padx=20
)


table.configure(
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set
)


# ==========================================================
# CLEAR TABLE
# ==========================================================

def clear_table():

    for item in table.get_children():
        table.delete(item)


# ==========================================================
# DISPLAY DATA
# ==========================================================

def display_data(columns, rows):

    global current_columns
    global current_rows

    current_columns = columns
    current_rows = rows

    clear_table()

    table["columns"] = columns

    for column in columns:

        table.heading(
            column,
            text=column
        )

        table.column(
            column,
            width=160,
            anchor="center"
        )

    for row in rows:

        table.insert(
            "",
            "end",
            values=row
        )


# ==========================================================
# RUN REPORT
# ==========================================================

def run_report(query, report_name):

    global current_report_name

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        conn.close()

        current_report_name = report_name

        display_data(
            columns,
            rows
        )

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ==========================================================
# PATIENT REPORT
# ==========================================================

def patient_report():

    run_report(
        """
        SELECT *
        FROM patient
        ORDER BY patient_id
        """,
        "Patient Report"
    )


# ==========================================================
# DOCTOR REPORT
# ==========================================================

def doctor_report():

    run_report(
        """
        SELECT *
        FROM doctor
        ORDER BY doctor_id
        """,
        "Doctor Report"
    )


# ==========================================================
# APPOINTMENT REPORT
# ==========================================================

def appointment_report():

    run_report(
        """
        SELECT *
        FROM appointment
        ORDER BY appointment_id
        """,
        "Appointment Report"
    )


# ==========================================================
# PRESCRIPTION REPORT
# ==========================================================

def prescription_report():

    run_report(
        """
        SELECT *
        FROM prescription
        ORDER BY prescription_id
        """,
        "Prescription Report"
    )


# ==========================================================
# BILLING REPORT
# ==========================================================

def billing_report():

    run_report(
        """
        SELECT *
        FROM bill
        ORDER BY bill_id
        """,
        "Billing Report"
    )


# ==========================================================
# ROOM REPORT
# ==========================================================

def room_report():

    run_report(
        """
        SELECT *
        FROM room
        ORDER BY room_id
        """,
        "Room Report"
    )


# ==========================================================
# DISCHARGE REPORT
# ==========================================================

def discharge_report():

    run_report(
        """
        SELECT *
        FROM discharge
        ORDER BY discharge_id
        """,
        "Discharge Report"
    )


# ==========================================================
# PATIENT + DOCTOR REPORT
# ==========================================================

def patient_doctor_report():

    run_report(
        """
        SELECT
            p.patient_id AS Patient_ID,
            p.name AS Patient_Name,
            d.doctor_id AS Doctor_ID,
            d.name AS Doctor_Name
        FROM patient p
        LEFT JOIN appointment a
            ON p.patient_id = a.patient_id
        LEFT JOIN doctor d
            ON a.doctor_id = d.doctor_id
        ORDER BY p.patient_id
        """,
        "Patient Doctor Report"
    )


# ==========================================================
# SEARCH
# ==========================================================

def search_report():

    search_text = search_var.get().strip().lower()

    if search_text == "":

        messagebox.showwarning(
            "Search",
            "Please enter something to search."
        )

        return


    found = False


    for item in table.get_children():

        values = table.item(
            item,
            "values"
        )

        match = False

        for value in values:

            if search_text in str(value).lower():

                match = True
                break


        if match:

            table.selection_add(item)

            table.see(item)

            found = True

        else:

            table.selection_remove(item)


    if not found:

        messagebox.showinfo(
            "Search",
            "No matching record found."
        )


# ==========================================================
# CLEAR SEARCH
# ==========================================================

def clear_search():

    search_var.set("")

    for item in table.get_children():

        table.selection_remove(item)


# ==========================================================
# GENERATE PDF
# ==========================================================

def generate_pdf():

    if not current_rows:

        messagebox.showwarning(
            "PDF Report",
            "Please select a report first."
        )

        return


    file_path = filedialog.asksaveasfilename(
        title="Save PDF Report",
        defaultextension=".pdf",
        filetypes=[
            ("PDF Files", "*.pdf")
        ],
        initialfile=current_report_name.replace(
            " ",
            "_"
        ) + ".pdf"
    )


    if not file_path:

        return


    try:

        # Landscape A4 gives more space for columns
        doc = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )


        styles = getSampleStyleSheet()


        title_style = styles["Title"]

        title_style.alignment = TA_CENTER


        normal_style = styles["Normal"]


        elements = []


        # PDF title

        elements.append(
            Paragraph(
                "HOSPITAL MANAGEMENT SYSTEM",
                title_style
            )
        )


        elements.append(
            Spacer(
                1,
                10
            )
        )


        elements.append(
            Paragraph(
                current_report_name,
                styles["Heading2"]
            )
        )


        elements.append(
            Spacer(
                1,
                15
            )
        )


        # Convert data to strings

        pdf_data = []


        header = []

        for column in current_columns:

            header.append(
                Paragraph(
                    str(column),
                    normal_style
                )
            )


        pdf_data.append(header)


        for row in current_rows:

            pdf_row = []

            for value in row:

                text = "" if value is None else str(value)

                pdf_row.append(
                    Paragraph(
                        text,
                        normal_style
                    )
                )

            pdf_data.append(pdf_row)


        # Create table

        pdf_table = Table(
            pdf_data,
            repeatRows=1
        )


        pdf_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.black
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),

                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )
                ]
            )
        )


        elements.append(
            pdf_table
        )


        elements.append(
            Spacer(
                1,
                15
            )
        )


        elements.append(
            Paragraph(
                f"Total Records: {len(current_rows)}",
                normal_style
            )
        )


        # Generate PDF

        doc.build(elements)


        messagebox.showinfo(
            "Success",
            "PDF report created successfully!\n\n"
            + file_path
        )


    except Exception as e:

        messagebox.showerror(
            "PDF Error",
            f"Unable to create PDF:\n{e}"
        )


# ==========================================================
# BUTTON FRAME
# ==========================================================

button_frame = tk.Frame(
    root,
    bg="white"
)

button_frame.pack(
    pady=10
)


# ==========================================================
# REPORT BUTTONS
# ==========================================================

tk.Button(
    button_frame,
    text="PATIENTS",
    font=("Arial", 12, "bold"),
    width=14,
    command=patient_report
).grid(
    row=0,
    column=0,
    padx=4,
    pady=5
)


tk.Button(
    button_frame,
    text="DOCTORS",
    font=("Arial", 12, "bold"),
    width=14,
    command=doctor_report
).grid(
    row=0,
    column=1,
    padx=4,
    pady=5
)


tk.Button(
    button_frame,
    text="APPOINTMENTS",
    font=("Arial", 12, "bold"),
    width=14,
    command=appointment_report
).grid(
    row=0,
    column=2,
    padx=4,
    pady=5
)


tk.Button(
    button_frame,
    text="PRESCRIPTIONS",
    font=("Arial", 12, "bold"),
    width=14,
    command=prescription_report
).grid(
    row=0,
    column=3,
    padx=4,
    pady=5
)


tk.Button(
    button_frame,
    text="BILLING",
    font=("Arial", 12, "bold"),
    width=14,
    command=billing_report
).grid(
    row=0,
    column=4,
    padx=4,
    pady=5
)


tk.Button(
    button_frame,
    text="ROOMS",
    font=("Arial", 12, "bold"),
    width=14,
    command=room_report
).grid(
    row=0,
    column=5,
    padx=4,
    pady=5
)


tk.Button(
    button_frame,
    text="DISCHARGES",
    font=("Arial", 12, "bold"),
    width=14,
    command=discharge_report
).grid(
    row=0,
    column=6,
    padx=4,
    pady=5
)


# ==========================================================
# SECOND BUTTON ROW
# ==========================================================

button_frame2 = tk.Frame(
    root,
    bg="white"
)

button_frame2.pack(
    pady=5
)


tk.Button(
    button_frame2,
    text="PATIENT + DOCTOR",
    font=("Arial", 12, "bold"),
    width=18,
    command=patient_doctor_report
).grid(
    row=0,
    column=0,
    padx=8
)


tk.Button(
    button_frame2,
    text="SEARCH",
    font=("Arial", 12, "bold"),
    width=15,
    command=search_report
).grid(
    row=0,
    column=1,
    padx=8
)


tk.Button(
    button_frame2,
    text="CLEAR SEARCH",
    font=("Arial", 12, "bold"),
    width=15,
    command=clear_search
).grid(
    row=0,
    column=2,
    padx=8
)


# ==========================================================
# PDF BUTTON
# ==========================================================

pdf_button = tk.Button(
    button_frame2,
    text="GENERATE PDF",
    font=("Arial", 13, "bold"),
    width=18,
    command=generate_pdf
)

pdf_button.grid(
    row=0,
    column=3,
    padx=8
)


# ==========================================================
# CLOSE BUTTON
# ==========================================================

tk.Button(
    root,
    text="CLOSE",
    font=("Arial", 13, "bold"),
    width=15,
    command=root.destroy
).pack(
    pady=15
)


# ==========================================================
# START
# ==========================================================

root.mainloop()