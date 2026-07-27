import streamlit as st
import pandas as pd
import numpy as np
from database import connect_db
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard", page_icon="🏥")

st.title("🏥 Hospital Management System")
st.subheader("Dashboard")

# Database Connection
conn = connect_db()

# Read Data
patients = pd.read_sql("SELECT * FROM patients", conn)
doctors = pd.read_sql("SELECT * FROM doctors", conn)
appointments = pd.read_sql("SELECT * FROM appointments", conn)

# -------------------------------
# Summary Cards
# -------------------------------

total_patients = len(patients)
total_doctors = len(doctors)
total_appointments = len(appointments)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👨‍⚕️ Total Doctors", total_doctors)

with col2:
    st.metric("🧑 Total Patients", total_patients)

with col3:
    st.metric("📅 Appointments", total_appointments)

st.divider()

# -------------------------------
# Age Statistics
# -------------------------------

if not patients.empty:

    ages = np.array(patients["age"])

    st.subheader("Patient Age Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric("Average Age", round(np.mean(ages), 2))
    c2.metric("Minimum Age", np.min(ages))
    c3.metric("Maximum Age", np.max(ages))

st.divider()

# -------------------------------
# Gender Distribution
# -------------------------------

if not patients.empty:

    st.subheader("Gender Distribution")

    gender = patients["gender"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        gender.values,
        labels=gender.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

st.divider()

# -------------------------------
# Doctor Specializations
# -------------------------------

if not doctors.empty:

    st.subheader("Doctor Specializations")

    specializations = doctors["specialization"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        specializations.index,
        specializations.values
    )

    ax.set_xlabel("Specialization")
    ax.set_ylabel("Doctors")

    plt.xticks(rotation=30)

    st.pyplot(fig)

st.divider()

# -------------------------------
# Appointments Per Doctor
# -------------------------------

if not appointments.empty:

    st.subheader("Appointments Per Doctor")

    doctor = appointments["doctor_name"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        doctor.index,
        doctor.values
    )

    ax.set_xlabel("Doctor")
    ax.set_ylabel("Appointments")

    plt.xticks(rotation=30)

    st.pyplot(fig)

st.divider()

# -------------------------------
# Recent Patients
# -------------------------------

st.subheader("Recent Patients")

if not patients.empty:
    st.dataframe(
        patients.tail(10),
        use_container_width=True
    )
else:
    st.info("No patient records found.")

st.divider()

# -------------------------------
# Recent Appointments
# -------------------------------

st.subheader("Recent Appointments")

if not appointments.empty:
    st.dataframe(
        appointments.tail(10),
        use_container_width=True
    )
else:
    st.info("No appointment records found.")