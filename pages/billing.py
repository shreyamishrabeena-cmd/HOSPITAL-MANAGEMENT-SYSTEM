import streamlit as st
import pandas as pd
from database import connect_db

st.title("💳 Billing Management")

conn = connect_db()
cursor = conn.cursor()

# Create bills table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS bills(
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100),
    doctor_name VARCHAR(100),
    consultation_fee DECIMAL(10,2),
    medicine_fee DECIMAL(10,2),
    test_fee DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_mode VARCHAR(30),
    bill_date DATE
)
""")
conn.commit()

menu = st.sidebar.selectbox(
    "Billing Menu",
    [
        "Generate Bill",
        "View Bills",
        "Search Bill",
        "Delete Bill"
    ]
)

# -------------------------------------------------
# GENERATE BILL
# -------------------------------------------------

if menu == "Generate Bill":

    st.subheader("Generate New Bill")

    patient_name = st.text_input("Patient Name")
    doctor_name = st.text_input("Doctor Name")

    consultation = st.number_input(
        "Consultation Fee",
        min_value=0.0,
        step=100.0
    )

    medicine = st.number_input(
        "Medicine Fee",
        min_value=0.0,
        step=100.0
    )

    tests = st.number_input(
        "Test Fee",
        min_value=0.0,
        step=100.0
    )

    payment = st.selectbox(
        "Payment Mode",
        ["Cash","UPI","Card"]
    )

    bill_date = st.date_input("Bill Date")

    total = consultation + medicine + tests

    st.info(f"Total Amount : ₹ {total:.2f}")

    if st.button("Save Bill"):

        cursor.execute("""
        INSERT INTO bills(
            patient_name,
            doctor_name,
            consultation_fee,
            medicine_fee,
            test_fee,
            total_amount,
            payment_mode,
            bill_date
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            patient_name,
            doctor_name,
            consultation,
            medicine,
            tests,
            total,
            payment,
            bill_date
        ))

        conn.commit()

        st.success("Bill Generated Successfully")

# -------------------------------------------------
# VIEW BILLS
# -------------------------------------------------

elif menu == "View Bills":

    st.subheader("Bill Records")

    df = pd.read_sql("SELECT * FROM bills", conn)

    st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# SEARCH BILL
# -------------------------------------------------

elif menu == "Search Bill":

    st.subheader("Search Bill")

    patient = st.text_input("Patient Name")

    if st.button("Search"):
        if not patient:
            st.warning("Please enter a patient name to search.")
        else:
            query = """
            SELECT * FROM bills
            WHERE patient_name LIKE %s
            """

            df = pd.read_sql(
                query,
                conn,
                params=(f"%{patient}%",)
            )

            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No bills found for that patient.")
            