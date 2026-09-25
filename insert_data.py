import sqlite3


conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()


# ==========================================
# PATIENT DATA
# ==========================================

patients = [
    ("Arun Kumar", 35, "Male", "9876543210", "Chennai", "O+"),
    ("Priya Sharma", 28, "Female", "9876543211", "Bangalore", "A+"),
    ("Ravi Kumar", 45, "Male", "9876543212", "Hyderabad", "B+"),
    ("Sneha Patel", 32, "Female", "9876543213", "Mumbai", "AB+"),
    ("Karthik Raj", 52, "Male", "9876543214", "Coimbatore", "O-"),
    ("Divya Singh", 24, "Female", "9876543215", "Delhi", "A-"),
    ("Manoj Kumar", 40, "Male", "9876543216", "Kochi", "B+"),
    ("Anitha Devi", 30, "Female", "9876543217", "Madurai", "O+"),
    ("Suresh Babu", 60, "Male", "9876543218", "Salem", "AB+"),
    ("Meena Ravi", 38, "Female", "9876543219", "Trichy", "A+")
]


cursor.executemany("""
    INSERT INTO patient
    (name, age, gender, phone, address, blood_group)
    VALUES (?, ?, ?, ?, ?, ?)
""", patients)

print("Patient data inserted.")


# ==========================================
# DOCTOR DATA
# ==========================================

doctors = [
    ("Dr. Rajesh Kumar", 45, "Male", "Cardiology",
     "9000000001", "rajesh@gmail.com"),

    ("Dr. Priya Devi", 38, "Female", "Dermatology",
     "9000000002", "priya@gmail.com"),

    ("Dr. Arun Sharma", 50, "Male", "Neurology",
     "9000000003", "arun@gmail.com"),

    ("Dr. Kavitha Rao", 42, "Female", "Pediatrics",
     "9000000004", "kavitha@gmail.com"),

    ("Dr. Suresh Patel", 48, "Male", "Orthopedics",
     "9000000005", "suresh@gmail.com"),

    ("Dr. Divya Singh", 36, "Female", "Gynecology",
     "9000000006", "divya@gmail.com"),

    ("Dr. Manoj Kumar", 44, "Male", "General Medicine",
     "9000000007", "manoj@gmail.com"),

    ("Dr. Anitha Raj", 40, "Female", "ENT",
     "9000000008", "anitha@gmail.com")
]


cursor.executemany("""
    INSERT INTO doctor
    (name, age, gender, specialization, phone, email)
    VALUES (?, ?, ?, ?, ?, ?)
""", doctors)

print("Doctor data inserted.")


# ==========================================
# APPOINTMENT DATA
# ==========================================

appointments = [
    (1, 1, "23-09-2026", "10:00 AM", "Chest pain"),
    (2, 2, "23-09-2026", "11:00 AM", "Skin allergy"),
    (3, 3, "24-09-2026", "09:30 AM", "Headache"),
    (4, 4, "24-09-2026", "10:30 AM", "Child checkup"),
    (5, 5, "25-09-2026", "11:30 AM", "Knee pain"),
    (6, 6, "25-09-2026", "02:00 PM", "Regular checkup"),
    (7, 7, "26-09-2026", "09:00 AM", "Fever"),
    (8, 8, "26-09-2026", "03:00 PM", "Ear pain")
]


cursor.executemany("""
    INSERT INTO appointment
    (patient_id, doctor_id, appointment_date,
     appointment_time, reason)
    VALUES (?, ?, ?, ?, ?)
""", appointments)

print("Appointment data inserted.")


# ==========================================
# BILL DATA
# ==========================================

bills = [
    (1, 1, 500, 300, 700, 1500, "Paid"),
    (2, 2, 400, 250, 500, 1150, "Paid"),
    (3, 3, 600, 400, 800, 1800, "Pending"),
    (4, 4, 400, 200, 300, 900, "Paid"),
    (5, 5, 550, 350, 600, 1500, "Pending"),
    (6, 6, 500, 300, 400, 1200, "Paid"),
    (7, 7, 300, 150, 250, 700, "Paid"),
    (8, 8, 450, 250, 350, 1050, "Pending")
]


cursor.executemany("""
    INSERT INTO bill
    (patient_id, doctor_id, consultation_fee,
     medicine_fee, test_fee, total_amount,
     payment_status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", bills)

print("Bill data inserted.")


# ==========================================
# PRESCRIPTION DATA
# ==========================================

prescriptions = [
    (1, 1, "Aspirin", "75mg", "5 days",
     "Take after food"),

    (2, 2, "Cetirizine", "10mg", "7 days",
     "Take at night"),

    (3, 3, "Paracetamol", "500mg", "5 days",
     "Take after food"),

    (4, 4, "Vitamin D", "1000 IU", "30 days",
     "Take after breakfast"),

    (5, 5, "Ibuprofen", "400mg", "5 days",
     "Take after food"),

    (6, 6, "Folic Acid", "5mg", "30 days",
     "Take once daily"),

    (7, 7, "Paracetamol", "500mg", "3 days",
     "Take when needed"),

    (8, 8, "Amoxicillin", "500mg", "7 days",
     "Follow prescribed schedule")
]


cursor.executemany("""
    INSERT INTO prescription
    (patient_id, doctor_id, medicine_name,
     dosage, duration, instructions)
    VALUES (?, ?, ?, ?, ?, ?)
""", prescriptions)

print("Prescription data inserted.")


# ==========================================
# SAVE
# ==========================================

conn.commit()
conn.close()


print("--------------------------------------")
print("ALL SAMPLE DATA INSERTED SUCCESSFULLY!")
print("--------------------------------------")