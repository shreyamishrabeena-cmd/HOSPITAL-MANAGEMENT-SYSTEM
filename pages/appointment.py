import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from database import connect_db


def normalize_date(value):
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return None
    return None


def normalize_time(value):
    if isinstance(value, time):
        return value
    if isinstance(value, datetime):
        return value.time()
    if isinstance(value, timedelta):
        return (datetime.min + value).time()
    if isinstance(value, str):
        for fmt in ("%H:%M:%S", "%H:%M", "%H:%M:%S.%f"):
            try:
                return datetime.strptime(value, fmt).time()
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(value).time()
        except ValueError:
            return None
    return None

st.title("📅 Appointment Management")

conn = connect_db()
cursor = conn.cursor()

# ==========================
# BOOK APPOINTMENT
# ==========================
st.subheader("➕ Book Appointment")

# Fetch Patients
cursor.execute("SELECT patient_id, name FROM patients")
patients = cursor.fetchall()

# Fetch Doctors
cursor.execute("SELECT doctor_id, name FROM doctors")
doctors = cursor.fetchall()

if patients and doctors:

    patient_options = {
        f"{p[0]} - {p[1]}": (p[0], p[1])
        for p in patients
    }

    doctor_options = {
        f"{d[0]} - {d[1]}": (d[0], d[1])
        for d in doctors
    }

    selected_patient = st.selectbox(
        "Select Patient",
        list(patient_options.keys())
    )

    selected_doctor = st.selectbox(
        "Select Doctor",
        list(doctor_options.keys())
    )

    appointment_date = st.date_input("Appointment Date")

    appointment_time = st.time_input("Appointment Time")

    status = st.selectbox(
        "Status",
        [
            "Scheduled",
            "Completed",
            "Cancelled"
        ]
    )

    if st.button("Book Appointment"):

        patient_id, patient_name = patient_options[selected_patient]
        doctor_id, doctor_name = doctor_options[selected_doctor]

        cursor.execute("""
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status,
                patient_name,
                doctor_name
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            status,
            patient_name,
            doctor_name
        ))

        conn.commit()

        st.success("✅ Appointment booked successfully!")

else:
    st.warning("Please add patients and doctors first.")



    # ==========================
# VIEW APPOINTMENTS
# ==========================

st.subheader("📋 View Appointments")

if st.button("View All Appointments"):

    cursor.execute("""
        SELECT
            appointment_id,
            patient_id,
            patient_name,
            doctor_id,
            doctor_name,
            appointment_date,
            appointment_time,
            status
        FROM appointments
        ORDER BY appointment_date, appointment_time
    """)

    appointments = cursor.fetchall()

    if appointments:

        df = pd.DataFrame(
            appointments,
            columns=[
                "Appointment ID",
                "Patient ID",
                "Patient Name",
                "Doctor ID",
                "Doctor Name",
                "Appointment Date",
                "Appointment Time",
                "Status"
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.info("No appointments found.")


# ==========================
# SEARCH APPOINTMENT
# ==========================

st.subheader("🔍 Search Appointment")

search_id = st.number_input(
    "Enter Appointment ID",
    min_value=1,
    step=1
)

if st.button("Search Appointment"):

    cursor.execute("""
        SELECT
            appointment_id,
            patient_id,
            patient_name,
            doctor_id,
            doctor_name,
            appointment_date,
            appointment_time,
            status
        FROM appointments
        WHERE appointment_id=%s
    """, (search_id,))

    appointment = cursor.fetchone()

    if appointment:

        result = pd.DataFrame(
            [appointment],
            columns=[
                "Appointment ID",
                "Patient ID",
                "Patient Name",
                "Doctor ID",
                "Doctor Name",
                "Appointment Date",
                "Appointment Time",
                "Status"
            ]
        )

        st.dataframe(result, use_container_width=True)

    else:
        st.error("Appointment not found.")


        # ==========================
# UPDATE APPOINTMENT
# ==========================

st.subheader("✏️ Update Appointment")

update_id = st.number_input(
    "Appointment ID to Update",
    min_value=1,
    step=1,
    key="update_id"
)

if st.button("Load Appointment"):

    cursor.execute("""
        SELECT patient_id, doctor_id, appointment_date,
               appointment_time, status
        FROM appointments
        WHERE appointment_id=%s
    """, (update_id,))

    record = cursor.fetchone()

    if record:

        st.session_state["update_loaded"] = True
        st.session_state["patient_id"] = record[0]
        st.session_state["doctor_id"] = record[1]
        st.session_state["appointment_date"] = record[2]
        st.session_state["appointment_time"] = record[3]
        st.session_state["status"] = record[4]

    else:
        st.error("Appointment not found.")

if st.session_state.get("update_loaded", False):

    appt_date = normalize_date(st.session_state["appointment_date"])
    appt_time = normalize_time(st.session_state["appointment_time"])

    if appt_date is None:
        appt_date = date.today()
    if appt_time is None:
        appt_time = datetime.now().time()

    new_date = st.date_input(
        "New Appointment Date",
        value=appt_date,
        key="new_date"
    )

    new_time = st.time_input(
        "New Appointment Time",
        value=appt_time,
        key="new_time"
    )

    status_options = ["Scheduled", "Completed", "Cancelled"]
    current_status = st.session_state.get("status", "Scheduled")
    status_index = status_options.index(current_status) if current_status in status_options else 0

    new_status = st.selectbox(
        "Status",
        status_options,
        index=status_index,
        key="update_status"
    )

    if st.button("Update Appointment"):
        cursor.execute("""
            UPDATE appointments
            SET appointment_date=%s,
                appointment_time=%s,
                status=%s
            WHERE appointment_id=%s
        """,
        (
            new_date,
            new_time,
            new_status,
            update_id
        ))

        conn.commit()

        st.success("✅ Appointment updated successfully!")

# ==========================
# CANCEL APPOINTMENT
# ==========================

st.subheader("❌ Cancel Appointment")

cancel_id = st.number_input(
    "Appointment ID to Cancel",
    min_value=1,
    step=1,
    key="cancel_id"
)

if st.button("Cancel Appointment"):

    cursor.execute("""
        UPDATE appointments
        SET status='Cancelled'
        WHERE appointment_id=%s
    """, (cancel_id,))

    conn.commit()

    if cursor.rowcount > 0:
        st.success("✅ Appointment cancelled successfully!")
    else:
        st.error("Appointment not found.")

# ==========================
# CLOSE DATABASE CONNECTION
# ==========================

cursor.close()
conn.close()