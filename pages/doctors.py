import streamlit as st
import pandas as pd
from database import connect_db

st.title("👨‍⚕️ Doctor Management")

conn = connect_db()
cursor = conn.cursor()

menu = st.sidebar.selectbox(
    "Select Option",
    ["Add Doctor", "View Doctors", "Search Doctor", "Update Doctor", "Delete Doctor"]
)

# ------------------- ADD DOCTOR -------------------

if menu == "Add Doctor":

    st.subheader("Add New Doctor")

    name = st.text_input("Doctor Name")
    specialization = st.text_input("Specialization")
    phone = st.text_input("Phone Number")

    if st.button("Save Doctor"):

        query = """
        INSERT INTO doctors(name, specialization, phone)
        VALUES(%s, %s, %s)
        """

        cursor.execute(query, (name, specialization, phone))
        conn.commit()

        st.success("Doctor Added Successfully!")

# ------------------- VIEW DOCTORS -------------------

elif menu == "View Doctors":

    st.subheader("Doctor List")

    df = pd.read_sql("SELECT * FROM doctors", conn)

    st.dataframe(df, use_container_width=True)

# ------------------- SEARCH DOCTOR -------------------

elif menu == "Search Doctor":

    st.subheader("Search Doctor")

    keyword = st.text_input("Enter Doctor Name")

    if st.button("Search"):

        query = """
        SELECT * FROM doctors
        WHERE name LIKE %s
        """

        df = pd.read_sql(query, conn, params=(f"%{keyword}%",))

        if len(df) > 0:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Doctor Not Found")

# ------------------- UPDATE DOCTOR -------------------

elif menu == "Update Doctor":

    st.subheader("Update Doctor")

    doctor_id = st.number_input("Doctor ID", min_value=1)

    if st.button("Load Details"):

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id=%s",
            (doctor_id,)
        )

        data = cursor.fetchone()

        if data:

            st.session_state.name = data[1]
            st.session_state.specialization = data[2]
            st.session_state.phone = data[3]

        else:
            st.error("Doctor Not Found")

    if "name" in st.session_state:

        new_name = st.text_input(
            "Doctor Name",
            value=st.session_state.name
        )

        new_specialization = st.text_input(
            "Specialization",
            value=st.session_state.specialization
        )

        new_phone = st.text_input(
            "Phone",
            value=st.session_state.phone
        )

        if st.button("Update"):

            cursor.execute(
                """
                UPDATE doctors
                SET name=%s,
                    specialization=%s,
                    phone=%s
                WHERE doctor_id=%s
                """,
                (
                    new_name,
                    new_specialization,
                    new_phone,
                    doctor_id
                )
            )

            conn.commit()

            st.success("Doctor Updated Successfully")

# ------------------- DELETE DOCTOR -------------------

elif menu == "Delete Doctor":

    st.subheader("Delete Doctor")

    doctor_id = st.number_input(
        "Doctor ID",
        min_value=1,
        key="delete"
    )

    if st.button("Delete"):

        cursor.execute(
            "DELETE FROM doctors WHERE doctor_id=%s",
            (doctor_id,)
        )

        conn.commit()

        st.success("Doctor Deleted Successfully")