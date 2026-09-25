import sqlite3

DB_NAME = "hospital.db"


def create_discharge_table():

    conn = sqlite3.connect(DB_NAME)
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

    print("Discharge table created successfully.")


if __name__ == "__main__":
    create_discharge_table()