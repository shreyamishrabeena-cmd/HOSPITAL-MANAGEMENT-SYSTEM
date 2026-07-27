🏥 Hospital Management System (HMS)

Overview

The Hospital Management System (HMS) is a web-based application developed using Python, Streamlit, and MySQL. It helps manage hospital operations such as patient records, doctor details, and appointment scheduling through an easy-to-use interface.

Features

- 👨‍⚕️ Doctor Management
  - Add, View, Update, and Delete doctor records
- 🧑 Patient Management
  - Add, View, Update, and Delete patient records
- 📅 Appointment Management
  - Book appointments
  - View appointments
  - Search appointments
  - Update appointment status
  - Cancel appointments
- 🔍 Search functionality for patients, doctors, and appointments
- 💾 Secure data storage using MySQL
- 🖥️ User-friendly interface built with Streamlit

Technologies Used

- Python
- Streamlit
- MySQL
- Pandas
- Git & GitHub

Project Structure

Hospital-Management-System/
│── app.py
│── database.py
│── patients.py
│── doctors.py
│── appointments.py
│── requirements.txt
│── README.md

Installation

1. Clone the repository:

git clone https://github.com/YOUR_USERNAME/Hospital-Management-System.git

2. Open the project folder:

cd Hospital-Management-System

3. Install the required packages:

pip install -r requirements.txt

4. Configure the MySQL database in "database.py".

5. Run the application:

streamlit run app.py
    
    **Future Improvements*******

- User authentication
- Billing and payment management
- Medical history management
- Prescription management
- Dashboard with analytics
- Email/SMS appointment reminders


License

This project was developed for educational purposes as a college group project.
