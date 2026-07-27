import streamlit as st
import pandas as pd
from database import connect_db

st.title("Patient Management")

conn = connect_db()
cursor = conn.cursor()

name = st.text_input("Patient Name")
age = st.number_input("Age", 1, 120)
gender = st.selectbox("Gender", ["Male", "Female"])
phone = st.text_input("Phone")
address = st.text_area("Address")

if st.button("Add Patient"):
    sql = """
    INSERT INTO patients(name,age,gender,phone,address)
    VALUES(%s,%s,%s,%s,%s)
    """
    cursor.execute(sql, (name, age, gender, phone, address))
    conn.commit()
    st.success("Patient Added Successfully")

df = pd.read_sql("SELECT * FROM patients", conn)

st.subheader("Patient Records")
st.dataframe(df)