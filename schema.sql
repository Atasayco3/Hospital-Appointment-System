DROP FUNCTION IF EXISTS appointments_by_specialty(VARCHAR);
DROP PROCEDURE IF EXISTS mark_appointment_completed;
DROP PROCEDURE IF EXISTS schedule_appointment;

-- Schedule procedure
CREATE OR REPLACE PROCEDURE schedule_appointment(p_patient_id INT, p_doctor_id INT, p_appt_date DATE)
LANGUAGE plpgsql
AS $$
BEGIN 
    -- Check if patient exists
    IF NOT EXISTS (SELECT 1 FROM patients WHERE patient_id = p_patient_id) THEN
        RAISE EXCEPTION 'Patient ID % does not exist', p_patient_id;
    END IF;

    -- Check if doctor exists
    IF NOT EXISTS (SELECT 1 FROM doctors WHERE doctor_id = p_doctor_id) THEN
        RAISE EXCEPTION 'Doctor ID % does not exist', p_doctor_id;
    END IF;

    -- Inserts into appointments
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, status)
    VALUES (p_patient_id, p_doctor_id, p_appt_date, 'Scheduled');
END;
$$;


-- Mark appointment
CREATE OR REPLACE PROCEDURE mark_appointment_completed(p_appointment_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_rows INT;
BEGIN 
    -- Checks if appointment exists
    IF NOT EXISTS (SELECT 1 FROM appointments WHERE appointment_id = p_appointment_id) THEN
        RAISE EXCEPTION 'Appointment ID % does not exist', p_appointment_id;
    END IF;

    -- Updates status
    UPDATE appointments SET status = 'Completed' WHERE appointment_id = p_appointment_id;

    -- Shows count of rows updated
    GET DIAGNOSTICS v_rows = ROW_COUNT;
    RAISE NOTICE '% row(s) updated.', v_rows;
END;
$$;

-- Returns scheduled appointments filtered by doctor specialty
CREATE OR REPLACE FUNCTION appointments_by_specialty(p_specialty VARCHAR)
RETURNS TABLE (
    appointment_id INT,
    patient_name VARCHAR,
    doctor_name VARCHAR,
    appointment_date DATE,
    status VARCHAR
) AS $$
BEGIN 
	RETURN QUERY
	SELECT 
        a.appointment_id,
        p.full_name AS patient_name,
        d.name AS doctor_name,
        a.appointment_date,
        a.status
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN doctors d ON a.doctor_id = d.doctor_id
    WHERE a.status = 'Scheduled'
      AND d.specialty = p_specialty
    ORDER BY a.appointment_date;
END;
$$ LANGUAGE plpgsql;


DROP VIEW IF EXISTS v_upcoming_appointments;

-- View of appointments scheduled in the next 30 days
CREATE OR REPLACE VIEW v_upcoming_appointments AS
SELECT 
	a.appointment_id,
    p.full_name,
    d.name,
    d.specialty,
	a.appointment_date
FROM 
    appointments a
JOIN 
    patients p ON a.patient_id = p.patient_id
JOIN 
    doctors d ON a.doctor_id = d.doctor_id
WHERE 
    a.status = 'Scheduled'
    AND a.appointment_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '30 days'
ORDER BY 
    a.appointment_date;

SELECT * FROM v_upcoming_appointments;

SElECT * FROM patients;
SElECT * FROM doctors;
SElECT * FROM appointments;
