import psycopg2
from psycopg2.extras import execute_values

# Insert list for patients 
Patients = [
    ("Alice Thomas", "1980-04-15", "F"),
    ("Bob Kumar", "1992-07-30", "M"),
    ("Cathy Nguyen", "1975-12-05", "F")
]

# Insert list for doctors
Doctors = [
    ("Dr. Smith", "Cardiology"),
    ("Dr. Patel", "Dermatology"),
    ("Dr. Rivera", "General Medicine")
]

# Insert list appointments
Appointments = [
    (1, 1, "2025-08-01", "Scheduled"),
    (2, 3, "2025-08-03", "Completed"),
    (3, 2, "2025-08-04", "Cancelled")
]

try:
    conn = psycopg2.connect(     # Define Connection
        dbname="DB3810",
        user="postgres",
        password="Trooper_501",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()        # Define cursor


    try:
        # Table for patients
        cur.execute("""     
        CREATE TABLE IF NOT EXISTS patients (  
            patient_id SERIAL PRIMARY KEY,
            full_name VARCHAR(100),
            dob DATE,
            gender VARCHAR(10)
        )
        """)
        print("Patient table created") 

        # Table for doctors
        cur.execute("""     
        CREATE TABLE IF NOT EXISTS doctors (  
            doctor_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            specialty VARCHAR(50)
        )
        """)
        print("Doctors table created")

        # Table for appointments
        cur.execute("""     
        CREATE TABLE IF NOT EXISTS appointments (  
            appointment_id SERIAL PRIMARY KEY,
            patient_id INT,
            doctor_id INT,
            appointment_date DATE,
            status VARCHAR(20) CHECK (status = 'Scheduled' OR status = 'Completed' OR status = 'Cancelled'), 
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                    ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                    ON DELETE CASCADE
        )
        """)
        print("Appointments table created")

        # Resets data in tables
        cur.execute("DELETE FROM appointments")
        cur.execute("DELETE FROM doctors")
        cur.execute("DELETE FROM patients")

        # Restarts ID sequences from 1
        cur.execute("ALTER SEQUENCE patients_patient_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE doctors_doctor_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE appointments_appointment_id_seq RESTART WITH 1")

        # Inserts for patients table
        execute_values( 
            cur,
            "INSERT INTO patients (full_name, dob, gender) VALUES %s",
            Patients
        )
        print("Patients inserted")

        # Inserts for doctor table
        execute_values( 
            cur,
            "INSERT INTO doctors (name, specialty) VALUES %s",
            Doctors
        )
        print("Doctors inserted")

        # Inserts for appointments table
        execute_values( 
            cur,
            "INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES %s",
            Appointments
        )
        print("Appointments inserted")

        # Table before deletion
        print("\nAppointments before doctor deletion:")
        cur.execute("SELECT * FROM appointments")
        for row in cur.fetchall():
            print(row)

        # Deletes doctor with rows affected listed
        cur.execute("DELETE FROM doctors WHERE doctor_id = %s", (2,))
        print("Rows deleted:", cur.rowcount)

        # Table after deletion
        print("\nAppointments after doctor deletion:")
        cur.execute("SELECT * FROM appointments")
        for row in cur.fetchall():
            print(row)

        # Prints view of scheduled appointments
        print("\nUpcoming appointments:")
        cur.execute("SELECT * FROM v_upcoming_appointments")
        for row in cur.fetchall():
            print(row)

        # Calls procedure to add a new appointment
        cur.callproc('schedule_appointment', (2,1,"2025-08-02"))

        # Shows new listed appointment in table
        print("\nListed Appointments:")
        cur.execute("SELECT * FROM appointments")
        for row in cur.fetchall():
            print(row)

        # Changes the status of appointment and prints table
        cur.callproc('mark_appointment_completed', (1,))

        # Shows updated appointment status
        print("\nListed Appointments:")
        cur.execute("SELECT * FROM appointments")
        for row in cur.fetchall():
            print(row)

        # Calls procedure to show appointments by category input
        specialty_input = 'Cardiology'  # or input("Enter specialty: ") if you want it interactive
        cur.execute("SELECT * FROM appointments_by_specialty(%s)", (specialty_input,))
        rows = cur.fetchall()

        # Shows appointments by specialty category
        print(f"\nAppointments for specialty: {specialty_input}")
        for row in rows:
            print(row)

        conn.commit()       # Commit SQL
        print ("\nAll operations completed")

    except psycopg2.Error as e: # Error if cannot access database correclty
            conn.rollback()
            print("Database error occurred:", e.pgerror)

    finally: # Finishes all opertations and closes connections at the end
        cur.close()
        conn.close()

except psycopg2.OperationalError as conn_err: # Error if connection is bugged or not working
    print("Connection error:", conn_err)