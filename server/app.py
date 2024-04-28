# Store this code in 'app.py' file
from flask import *
import sqlite3
import re
import random
app = Flask(__name__)

DATABASE_FILE = 'var/data.sqlite3'

@app.route('/patients', methods=['POST'])
def create_patient():
    # Get the request data
    data = request.get_json()

    # Extract the patient details from the request data
    health_id = generate_unique_id()
    first_name = data['FirstName']
    last_name = data['LastName']
    date_of_birth = data['DateOfBirth']
    gender = data['Gender']
    address = data['Address']
    phone_number = data['PhoneNumber']
    email = data['Email']
    emergency_contact_id = generate_unique_id()
    emergency_contact_healthID = health_id
    emergencycontactfirstname = data['EmergencyContact']['Name']
    emergencycontactlastname = data['EmergencyContact']['LastName']
    emergencycontactrelationship = data['EmergencyContact']['Relationship']
    emergency_contact_phone_number = data['EmergencyContact']['PhoneNumber']
    emergency_contact_email = data['EmergencyContact']['Email']

    # Generate a unique patient ID
    # You can use a library like uuid to generate a unique ID

    # Insert the patient details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Patient (HealthID, FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber, Email, EmergencyContactID) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)", ( health_id, first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact_id))
    cursor.execute("INSERT INTO EmergencyContact (EmergencyContactID, FirstName, LastName, Relationship, PhoneNumber, Email, HealthID) VALUES ( ?, ?, ?, ?, ?, ?, ?)", ( emergency_contact_id, emergencycontactfirstname, emergencycontactlastname, emergencycontactrelationship, emergency_contact_phone_number, emergency_contact_email, emergency_contact_healthID))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Patient created successfully'}), 201

@app.route('/emergency_contacts', methods=['POST'])
def create_emergency_contact():
    # Get the request data
    data = request.get_json()

    # Extract the emergency contact details from the request data
    name = data['Name']
    phone_number = data['PhoneNumber']
    email = data['Email']

    # Generate a unique emergency contact ID
    # You can use a library like uuid to generate a unique ID
    emergency_contact_id = generate_unique_id()

    # Insert the emergency contact details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO EmergencyContact (EmergencyContactID, Name, PhoneNumber, Email) VALUES ( ?, ?, ?, ?)", ( emergency_contact_id, name, phone_number, email))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Emergency contact created successfully'}), 201

@app.route('/updateEmergencyContact', methods=['PUT'])
def update_emergency_contact():
    # Get the request data
    data = request.get_json()

    # Extract the emergency contact details from the request data
    emergency_contact_id = data['EmergencyContactID']
    first_name = data['FirstName']
    last_name = data['LastName']
    phone_number = data['PhoneNumber']
    email = data['Email']

    # Update the emergency contact details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE EmergencyContact SET FirstName = ?, LastName = ?, PhoneNumber = ?, Email = ? WHERE EmergencyContactID = ?", (first_name, last_name, phone_number, email, emergency_contact_id))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Emergency contact updated successfully'}), 200

@app.route('/getPatients', methods=['GET'])
def get_patients():
    # Get all the patients from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patient")
    patients = cursor.fetchall()
    conn.close()

    # Return the patients as a JSON response
    return jsonify({'patients': patients}), 200

@app.route('/getPatient/<healthid>', methods=['GET'])
def get_patient(healthid):
    # Get the patient with the specified health ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Patient WHERE HealthID = ?", (healthid,))
    patient = cursor.fetchone()
    cursor.execute("SELECT * FROM EmergencyContact WHERE HealthID = ?", (healthid,))
    emer = cursor.fetchone()
    conn.close()

    # Return the patient as a JSON response
    return jsonify({'patient': patient,
                    'emergencyContact': emer}), 200

@app.route('/deletePatient/<healthid>', methods=['DELETE'])
def delete_patient(healthid):
    # Delete the patient with the specified health ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Patient WHERE HealthID = ?", (healthid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Patient deleted successfully'}), 200

@app.route('/deleteEmergencyContact/<emergencycontactid>', methods=['DELETE'])
def delete_emergency_contact(emergencycontactid):
    # Delete the emergency contact with the specified ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM EmergencyContact WHERE EmergencyContactID = ?", (emergencycontactid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Emergency contact deleted successfully'}), 200

@app.route('/updatePatient/<healthid>', methods=['PUT'])
def update_patient(healthid):
    # Get the request data
    data = request.get_json()

    # Extract the patient details from the request data
    first_name = data['FirstName']
    last_name = data['LastName']
    date_of_birth = data['DateOfBirth']
    address = data['Address']
    phone_number = data['PhoneNumber']
    email = data['Email']

    # Update the patient details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Patient SET FirstName = ?, LastName = ?, DateOfBirth = ?, Address = ?, PhoneNumber = ?, Email = ? WHERE HealthID = ?", (first_name, last_name, date_of_birth, address, phone_number, email, healthid))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Patient updated successfully'}), 200

@app.route('/addHospital', methods=['POST'])
def create_hospital():
    # Get the request data
    data = request.get_json()

    # Extract the hospital details from the request data
    name = data['Name']
    address = data['Address']
    phone_number = data['PhoneNumber']
    email = data['Email']

    # Generate a unique hospital ID
    # You can use a library like uuid to generate a unique ID
    hospital_id = generate_unique_id('Hospital')

    # Insert the hospital details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Hospital (HospitalID, Name, Address, PhoneNumber, Email) VALUES ( ?, ?, ?, ?, ?)", ( hospital_id, name, address, phone_number, email))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Hospital created successfully'}), 201

@app.route('/getHospitals', methods=['GET'])
def get_hospitals():
    # Get all the hospitals from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Hospital")
    hospitals = cursor.fetchall()
    conn.close()

    # Return the hospitals as a JSON response
    return jsonify({'hospitals': hospitals}), 200

@app.route('/getHospital/<hospitalid>', methods=['GET'])
def get_hospital(hospitalid):
    # Get the hospital with the specified hospital ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Hospital WHERE HospitalID = ?", (hospitalid,))
    hospital = cursor.fetchone()
    conn.close()

    # Return the hospital as a JSON response
    return jsonify({'hospital': hospital}), 200

@app.route('/deleteHospital/<hospitalid>', methods=['DELETE'])
def delete_hospital(hospitalid):
    # Delete the hospital with the specified hospital ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Hospital WHERE HospitalID = ?", (hospitalid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Hospital deleted successfully'}), 200

@app.route('/updateHospital/<hospitalid>', methods=['PUT'])
def update_hospital(hospitalid):
    # Get the request data
    data = request.get_json()

    # Extract the hospital details from the request data
    name = data['Name']
    address = data['Address']
    phone_number = data['PhoneNumber']
    email = data['Email']

    # Update the hospital details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Hospital SET Name = ?, Address = ?, PhoneNumber = ?, Email = ? WHERE HospitalID = ?", (name, address, phone_number, email, hospitalid))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Hospital updated successfully'}), 200

@app.route('/addDoctor', methods=['POST'])
def create_doctor():
    # Get the request data
    data = request.get_json()

    # Extract the doctor details from the request data
    first_name = data['FirstName']
    last_name = data['LastName']
    specializations = data['Specialization']
    phone_number = data['PhoneNumber']
    email = data['Email']
    hospital_id = data['HospitalID']

    # Generate a unique doctor ID
    # You can use a library like uuid to generate a unique ID
    doctor_id = generate_unique_id("Doctor")

    # Insert the doctor details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Doctor (DoctorID, FirstName, LastName, Specialization, HospitalID,PhoneNumber, Email) VALUES ( ?, ?, ?, ?, ? ,?, ?)", ( doctor_id, first_name, last_name, specializations, hospital_id,  phone_number, email, ))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Doctor created successfully'}), 201

@app.route('/getDoctors', methods=['GET'])
def get_doctors():
    # Get all the doctors from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor")
    doctors = cursor.fetchall()
    conn.close()

    # Return the doctors as a JSON response
    return jsonify({'doctors': doctors}), 200

@app.route('/getDoctor/<doctorid>', methods=['GET'])
def get_doctor(doctorid):
    # Get the doctor with the specified doctor ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor WHERE DoctorID = ?", (doctorid,))
    doctor = cursor.fetchone()
    conn.close()

    # Return the doctor as a JSON response
    return jsonify({'doctor': doctor}), 200

@app.route('/deleteDoctor/<doctorid>', methods=['DELETE'])
def delete_doctor(doctorid):
    # Delete the doctor with the specified doctor ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Doctor WHERE DoctorID = ?", (doctorid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Doctor deleted successfully'}), 200

@app.route('/updateDoctor/<doctorid>', methods=['PUT'])
def update_doctor(doctorid):
    # Get the request data
    data = request.get_json()

    # Extract the doctor details from the request data
    first_name = data['FirstName']
    last_name = data['LastName']
    specializations = data['Specialization']
    phone_number = data['PhoneNumber']
    email = data['Email']
    hospital_id = data['HospitalID']

    # Update the doctor details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Doctor SET FirstName = ?, LastName = ?, Specialization = ?, HospitalID = ?, PhoneNumber = ?, Email = ? WHERE DoctorID = ?", (first_name, last_name, specializations, hospital_id, phone_number, email, doctorid))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Doctor updated successfully'}), 200

@app.route('/addAppointment', methods=['POST'])
def create_appointment():
    # Get the request data
    data = request.get_json()

    # Extract the appointment details from the request data
    doctor_id = data['DoctorID']
    hospital_id = data['HospitalID']
    date = data['Date']
    time = data['Time']

    # Generate a unique appointment ID
    # You can use a library like uuid to generate a unique ID
    appointment_id = generate_unique_id("Appointment")

    # Insert the appointment details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # create a table if doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Appointment (AppointmentID TEXT PRIMARY KEY, DoctorID TEXT, HospitalID TEXT, Date TEXT, Time TEXT)''')
    cursor.execute("INSERT INTO Appointment (AppointmentID, PatientID, DoctorID, HospitalID, Date, Time) VALUES ( ?,  ?, ?, ?, ?)", ( appointment_id, doctor_id, hospital_id, date, time))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Appointment created successfully'}), 201

@app.route('/getAppointments', methods=['GET'])
def get_appointments():
    # Get all the appointments from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Appointment")
    appointments = cursor.fetchall()
    conn.close()

    # Return the appointments as a JSON response
    return jsonify({'appointments': appointments}), 200

@app.route('/getAppointment/<appointmentid>', methods=['GET'])
def get_appointment(appointmentid):
    # Get the appointment with the specified appointment ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Appointment WHERE AppointmentID = ?", (appointmentid,))
    appointment = cursor.fetchone()
    conn.close()

    # Return the appointment as a JSON response
    return jsonify({'appointment': appointment}), 200


def generate_unique_id(params1):
    if params1 == 'Hospital':
        # Generate a unique ID using a combination of letters and numbers
        return 'H' + str(random.randint(1000, 9999))
    elif params1 == 'Doctor':
        # Generate a unique ID using a combination of letters and numbers
        return 'D' + str(random.randint(1000, 9999))
    # Generate a unique ID using a combination of letters and numbers
    return 'P' + str(random.randint(1000, 9999))