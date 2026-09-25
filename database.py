import sqlite3
import os

# ============================================================
# DATABASE FILE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "hospital.db")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ============================================================
# ADD COLUMN IF IT DOES NOT EXIST
# ============================================================

def add_column_if_missing(cursor, table_name, column_name, column_definition):

    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = [row[1] for row in cursor.fetchall()]

    if column_name not in columns:
        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN "
            f"{column_name} {column_definition}"
        )


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ========================================================
    # USERS TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # ========================================================
    # PATIENT TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT,
            blood_group TEXT,
            email TEXT,
            emergency_contact TEXT
        )
    """)

    # Add missing patient columns to old database
    add_column_if_missing(
        cursor, "patient", "name", "TEXT"
    )

    add_column_if_missing(
        cursor, "patient", "age", "INTEGER"
    )

    add_column_if_missing(
        cursor, "patient", "gender", "TEXT"
    )

    add_column_if_missing(
        cursor, "patient", "phone", "TEXT"
    )

    add_column_if_missing(
        cursor, "patient", "address", "TEXT"
    )

    add_column_if_missing(
        cursor, "patient", "blood_group", "TEXT"
    )

    add_column_if_missing(
        cursor, "patient", "email", "TEXT"
    )

    add_column_if_missing(
        cursor, "patient", "emergency_contact", "TEXT"
    )

    # ========================================================
    # DOCTOR TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            phone TEXT,
            address TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT
        )
    """)

    # Add missing doctor columns
    add_column_if_missing(
        cursor, "doctor", "name", "TEXT"
    )

    add_column_if_missing(
        cursor, "doctor", "specialization", "TEXT"
    )

    add_column_if_missing(
        cursor, "doctor", "phone", "TEXT"
    )

    add_column_if_missing(
        cursor, "doctor", "address", "TEXT"
    )

    add_column_if_missing(
        cursor, "doctor", "age", "INTEGER"
    )

    add_column_if_missing(
        cursor, "doctor", "gender", "TEXT"
    )

    add_column_if_missing(
        cursor, "doctor", "email", "TEXT"
    )

    # ========================================================
    # APPOINTMENT TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            appointment_date TEXT,
            appointment_time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled',

            FOREIGN KEY(patient_id)
            REFERENCES patient(id)
            ON DELETE CASCADE,

            FOREIGN KEY(doctor_id)
            REFERENCES doctor(id)
            ON DELETE CASCADE
        )
    """)

    # Important for your previous error:
    # "table appointment has no column named reason"

    add_column_if_missing(
        cursor, "appointment", "patient_id", "INTEGER"
    )

    add_column_if_missing(
        cursor, "appointment", "doctor_id", "INTEGER"
    )

    add_column_if_missing(
        cursor, "appointment", "appointment_date", "TEXT"
    )

    add_column_if_missing(
        cursor, "appointment", "appointment_time", "TEXT"
    )

    add_column_if_missing(
        cursor, "appointment", "reason", "TEXT"
    )

    add_column_if_missing(
        cursor, "appointment", "status", "TEXT"
    )

    # ========================================================
    # PRESCRIPTION TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescription (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            medicine_name TEXT,
            dosage TEXT,
            duration TEXT,
            instructions TEXT,

            FOREIGN KEY(patient_id)
            REFERENCES patient(id)
            ON DELETE CASCADE,

            FOREIGN KEY(doctor_id)
            REFERENCES doctor(id)
            ON DELETE CASCADE
        )
    """)

    # Important for your previous errors:
    # medicine column / medicine_name column

    add_column_if_missing(
        cursor, "prescription", "patient_id", "INTEGER"
    )

    add_column_if_missing(
        cursor, "prescription", "doctor_id", "INTEGER"
    )

    add_column_if_missing(
        cursor, "prescription", "medicine_name", "TEXT"
    )

    add_column_if_missing(
        cursor, "prescription", "dosage", "TEXT"
    )

    add_column_if_missing(
        cursor, "prescription", "duration", "TEXT"
    )

    add_column_if_missing(
        cursor, "prescription", "instructions", "TEXT"
    )

    # ========================================================
    # BILLING TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            consultation_fee REAL DEFAULT 0,
            medicine_fee REAL DEFAULT 0,
            room_charges REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,

            FOREIGN KEY(patient_id)
            REFERENCES patient(id)
            ON DELETE CASCADE
        )
    """)

    add_column_if_missing(
        cursor, "billing", "patient_id", "INTEGER"
    )

    add_column_if_missing(
        cursor, "billing", "consultation_fee", "REAL"
    )

    add_column_if_missing(
        cursor, "billing", "medicine_fee", "REAL"
    )

    add_column_if_missing(
        cursor, "billing", "room_charges", "REAL"
    )

    add_column_if_missing(
        cursor, "billing", "total_amount", "REAL"
    )

    # ========================================================
    # MEDICINE TABLE
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            category TEXT,
            dosage TEXT,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0
        )
    """)

    add_column_if_missing(
        cursor, "medicine", "medicine_name", "TEXT"
    )

    add_column_if_missing(
        cursor, "medicine", "category", "TEXT"
    )

    add_column_if_missing(
        cursor, "medicine", "dosage", "TEXT"
    )

    add_column_if_missing(
        cursor, "medicine", "quantity", "INTEGER"
    )

    add_column_if_missing(
        cursor, "medicine", "price", "REAL"
    )

    # ========================================================
    # SAVE CHANGES
    # ========================================================

    conn.commit()

    # ========================================================
    # CREATE DEFAULT ADMIN USER
    # ========================================================

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password)
        VALUES (?, ?)
    """, ("admin", "1234"))

    conn.commit()

    # ========================================================
    # CLOSE DATABASE
    # ========================================================

    conn.close()

    print("----------------------------------------")
    print("Hospital Management System Database")
    print("----------------------------------------")
    print("Database:", DB_NAME)
    print("Users table       : Ready")
    print("Patient table     : Ready")
    print("Doctor table      : Ready")
    print("Appointment table : Ready")
    print("Prescription table: Ready")
    print("Billing table     : Ready")
    print("Medicine table    : Ready")
    print("----------------------------------------")
    print("Database setup completed successfully.")
    print("----------------------------------------")


# ============================================================
# TEST DATABASE
# ============================================================

def show_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    print("\nDATABASE TABLES:")

    for table in tables:
        print("-", table[0])

    conn.close()


# ============================================================
# RUN DATABASE
# ============================================================

if __name__ == "__main__":

    create_database()
    show_tables()