import streamlit as st
import pandas as pd
import numpy as np
from database import connect_db
import matplotlib.pyplot as plt

st.set_page_config(page_title="Reports")

st.title("📊 Hospital Reports")

conn = connect_db()

# Load Data
patients = pd.read_sql("SELECT * FROM patients", conn)
doctors = pd.read_sql("SELECT * FROM doctors", conn)
appointments = pd.read_sql("SELECT * FROM appointments", conn)

# -------------------------------
# Summary Cards
# -------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Patients", len(patients))

with col2:
    st.metric("Total Doctors", len(doctors))

with col3:
    st.metric("Appointments", len(appointments))

st.divider()

# -------------------------------
# Age Statistics using NumPy
# -------------------------------

if not patients.empty:

    ages = np.array(patients["age"])

    st.subheader("Age Statistics")

    c1, c2, c3 = st.columns(3)

    c1.metric("Average Age", round(np.mean(ages), 2))
    c2.metric("Youngest Patient", np.min(ages))
    c3.metric("Oldest Patient", np.max(ages))

st.divider()

# -------------------------------
# Gender Distribution
# -------------------------------

if not patients.empty:

    st.subheader("Gender Distribution")

    gender_count = patients["gender"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        gender_count,
        labels=gender_count.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

st.divider()

# -------------------------------
# Patients by Age
# -------------------------------

if not patients.empty:

    st.subheader("Patient Age Distribution")

    fig, ax = plt.subplots()

    ax.hist(
        patients["age"],
        bins=10
    )

    ax.set_xlabel("Age")
    ax.set_ylabel("Number of Patients")

    st.pyplot(fig)

st.divider()

# -------------------------------
# Doctor-wise Appointments
# -------------------------------

if not appointments.empty:

    st.subheader("Appointments per Doctor")

    doctor_data = appointments["doctor_name"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        doctor_data.index,
        doctor_data.values
    )

    ax.set_xlabel("Doctor")
    ax.set_ylabel("Appointments")

    plt.xticks(rotation=30)

    st.pyplot(fig)

st.divider()

# -------------------------------
# Patient Records
# -------------------------------

st.subheader("Patient Records")

st.dataframe(
    patients,
    use_container_width=True
)

# -------------------------------
# Download Report
# -------------------------------

csv = patients.to_csv(index=False)

st.download_button(
    label="Download Patient Report",
    data=csv,
    file_name="patient_report.csv",
    mime="text/csv"
)