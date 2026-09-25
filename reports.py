import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


# ==========================================================
# DATABASE
# ==========================================================

DB_NAME = "hospital.db"


def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10)


# ==========================================================
# GLOBAL REPORT DATA
# ==========================================================

current_report_name = "Hospital Report"
current_columns = []
current_rows = []


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()

root.title("Hospital Management System - Reports")
root.geometry("1450x850")
root.configure(bg="#F3F8FC")


# ==========================================================
# COLORS
# ==========================================================

HEADER_COLOR = "#006064"
DARK_BLUE = "#01579B"
BLUE = "#0277BD"
GREEN = "#2E7D32"
ORANGE = "#EF6C00"
RED = "#C62828"
PURPLE = "#6A1B9A"
GRAY = "#607D8B"
WHITE = "#FFFFFF"


# ==========================================================
# HEADER
# ==========================================================

header = tk.Frame(
    root,
    bg=HEADER_COLOR,
    height=90
)

header.pack(fill="x")
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

header_text.pack(side="left")


tk.Label(
    header_text,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Segoe UI", 22, "bold"),
    bg=HEADER_COLOR,
    fg=WHITE
).pack(anchor="w")


tk.Label(
    header_text,
    text="Healthcare Administration  •  Reports",
    font=("Segoe UI", 11),
    bg=HEADER_COLOR,
    fg="#B2EBF2"
).pack(anchor="w")


# ==========================================================
# PAGE TITLE
# ==========================================================

tk.Label(
    root,
    text="📊 HOSPITAL REPORTS",
    font=("Segoe UI", 27, "bold"),
    bg="#F3F8FC",
    fg=DARK_BLUE
).pack(pady=(20, 3))


tk.Label(
    root,
    text="View hospital records and generate PDF reports",
    font=("Segoe UI", 11),
    bg="#F3F8FC",
    fg=GRAY
).pack(pady=(0, 15))


# ==========================================================
# SEARCH FRAME
# ==========================================================

search_frame = tk.Frame(
    root,
    bg=WHITE,
    bd=1,
    relief="solid"
)

search_frame.pack(
    padx=30,
    pady=5,
    fill="x"
)


tk.Label(
    search_frame,
    text="🔍 Search",
    font=("Segoe UI", 12, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
).pack(
    side="left",
    padx=15,
    pady=12
)


search_var = tk.StringVar()


search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Segoe UI", 11),
    width=35
)

search_entry.pack(
    side="left",
    padx=10
)


# ==========================================================
# TABLE FRAME
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


tk.Label(
    table_card,
    text="📋 REPORT DATA",
    font=("Segoe UI", 16, "bold"),
    bg=WHITE,
    fg=BLUE
).pack(
    anchor="w",
    padx=15,
    pady=10
)


table_frame = tk.Frame(
    table_card,
    bg=WHITE
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# ==========================================================
# TREEVIEW STYLE
# ==========================================================

style = ttk.Style()

style.configure(
    "Report.Treeview",
    font=("Segoe UI", 10),
    rowheight=32,
    background=WHITE,
    fieldbackground=WHITE
)

style.configure(
    "Report.Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)


# ==========================================================
# TABLE
# ==========================================================

table = ttk.Treeview(
    table_frame,
    show="headings",
    style="Report.Treeview"
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
    table_card,
    orient="horizontal",
    command=table.xview
)

horizontal_scrollbar.pack(
    fill="x",
    padx=15
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

        formatted_row = []

        for value in row:

            if value is None:
                formatted_row.append("")
            else:
                formatted_row.append(value)

        table.insert(
            "",
            "end",
            values=formatted_row
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

    except sqlite3.Error as e:

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
        SELECT
            b.bill_id AS Bill_ID,
            p.name AS Patient_Name,
            b.consultation_fee AS Consultation,
            b.medicine_fee AS Medicine,
            b.room_charges AS Room_Charges,
            b.other_charges AS Other_Charges,
            b.total_amount AS Total
        FROM bill b
        LEFT JOIN patient p
            ON b.patient_id = p.patient_id
        ORDER BY b.bill_id
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
# SEARCH REPORT
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

    if not current_columns:

        messagebox.showwarning(
            "PDF Report",
            "Please select a report first."
        )

        return

    file_path = filedialog.asksaveasfilename(
        title="Save Hospital PDF Report",
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

        # ==================================================
        # PDF DOCUMENT
        # ==================================================

        doc = SimpleDocTemplate(
            file_path,
            pagesize=landscape(A4),
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "HospitalTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=8
        )

        report_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=8
        )

        normal_style = ParagraphStyle(
            "NormalText",
            parent=styles["Normal"],
            fontSize=8
        )

        header_style = ParagraphStyle(
            "HeaderText",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8
        )


        elements = []


        # ==================================================
        # HOSPITAL TITLE
        # ==================================================

        elements.append(
            Paragraph(
                "HOSPITAL MANAGEMENT SYSTEM",
                title_style
            )
        )


        # ==================================================
        # REPORT NAME
        # ==================================================

        elements.append(
            Paragraph(
                current_report_name,
                report_style
            )
        )


        # ==================================================
        # DATE
        # ==================================================

        current_date = datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

        elements.append(
            Paragraph(
                "Generated On: " + current_date,
                normal_style
            )
        )


        elements.append(
            Spacer(
                1,
                15
            )
        )


        # ==================================================
        # PDF TABLE DATA
        # ==================================================

        pdf_data = []


        # HEADER

        header = []

        for column in current_columns:

            header.append(
                Paragraph(
                    str(column),
                    header_style
                )
            )

        pdf_data.append(header)


        # ROWS

        for row in current_rows:

            pdf_row = []

            for value in row:

                if value is None:

                    text = ""

                else:

                    text = str(value)

                pdf_row.append(
                    Paragraph(
                        text,
                        normal_style
                    )
                )

            pdf_data.append(pdf_row)


        # ==================================================
        # CREATE PDF TABLE
        # ==================================================

        pdf_table = Table(
            pdf_data,
            repeatRows=1
        )


        pdf_table.setStyle(
            TableStyle(
                [

                    # Header
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#006064")
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    ),

                    # Grid
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),

                    # Alignment
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE"
                    ),

                    # Padding
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
                    ),

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


        # ==================================================
        # TOTAL RECORDS
        # ==================================================

        elements.append(
            Paragraph(
                f"Total Records: {len(current_rows)}",
                normal_style
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
                "Hospital Management System",
                normal_style
            )
        )


        # ==================================================
        # CREATE PDF
        # ==================================================

        doc.build(elements)


        messagebox.showinfo(
            "PDF Created",
            "PDF report created successfully!\n\n"
            + file_path
        )


    except Exception as e:

        messagebox.showerror(
            "PDF Error",
            f"Unable to create PDF:\n\n{e}"
        )


# ==========================================================
# BUTTON FRAME
# ==========================================================

button_frame = tk.Frame(
    root,
    bg="#F3F8FC"
)

button_frame.pack(
    pady=8
)


# ==========================================================
# REPORT BUTTONS
# ==========================================================

tk.Button(
    button_frame,
    text="👤 PATIENTS",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=BLUE,
    fg=WHITE,
    command=patient_report
).grid(
    row=0,
    column=0,
    padx=4
)


tk.Button(
    button_frame,
    text="👨‍⚕️ DOCTORS",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=GREEN,
    fg=WHITE,
    command=doctor_report
).grid(
    row=0,
    column=1,
    padx=4
)


tk.Button(
    button_frame,
    text="📅 APPOINTMENTS",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=ORANGE,
    fg=WHITE,
    command=appointment_report
).grid(
    row=0,
    column=2,
    padx=4
)


tk.Button(
    button_frame,
    text="💊 PRESCRIPTIONS",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=PURPLE,
    fg=WHITE,
    command=prescription_report
).grid(
    row=0,
    column=3,
    padx=4
)


tk.Button(
    button_frame,
    text="💰 BILLING",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=RED,
    fg=WHITE,
    command=billing_report
).grid(
    row=0,
    column=4,
    padx=4
)


tk.Button(
    button_frame,
    text="🛏️ ROOMS",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=DARK_BLUE,
    fg=WHITE,
    command=room_report
).grid(
    row=0,
    column=5,
    padx=4
)


tk.Button(
    button_frame,
    text="🚪 DISCHARGES",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=GRAY,
    fg=WHITE,
    command=discharge_report
).grid(
    row=0,
    column=6,
    padx=4
)


# ==========================================================
# SECOND BUTTON ROW
# ==========================================================

button_frame2 = tk.Frame(
    root,
    bg="#F3F8FC"
)

button_frame2.pack(
    pady=5
)


tk.Button(
    button_frame2,
    text="👨‍⚕️ PATIENT + DOCTOR",
    font=("Segoe UI", 10, "bold"),
    width=20,
    bg=DARK_BLUE,
    fg=WHITE,
    command=patient_doctor_report
).grid(
    row=0,
    column=0,
    padx=6
)


tk.Button(
    button_frame2,
    text="🔍 SEARCH",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=BLUE,
    fg=WHITE,
    command=search_report
).grid(
    row=0,
    column=1,
    padx=6
)


tk.Button(
    button_frame2,
    text="CLEAR SEARCH",
    font=("Segoe UI", 10, "bold"),
    width=15,
    bg=GRAY,
    fg=WHITE,
    command=clear_search
).grid(
    row=0,
    column=2,
    padx=6
)


tk.Button(
    button_frame2,
    text="📄 GENERATE PDF",
    font=("Segoe UI", 11, "bold"),
    width=20,
    bg=GREEN,
    fg=WHITE,
    command=generate_pdf
).grid(
    row=0,
    column=3,
    padx=6
)


# ==========================================================
# CLOSE BUTTON
# ==========================================================

tk.Button(
    root,
    text="CLOSE",
    font=("Segoe UI", 11, "bold"),
    width=15,
    bg=RED,
    fg=WHITE,
    command=root.destroy
).pack(
    pady=10
)


# ==========================================================
# START
# ==========================================================

root.mainloop()