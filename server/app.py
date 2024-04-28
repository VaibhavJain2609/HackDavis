# Store this code in 'app.py' file
from flask import *
import sqlite3
import re
import random
from propelauth_flask import init_auth
app = Flask(__name__)
auth = init_auth("https://7606143.propelauthtest.com",
                 "28f707599ab2007acda499948bc38cdad0d8ab3db761d7b866691e2d45e002cb6f3160c70379aaf81cbd53ec151328e2")
DATABASE_FILE = 'var/data.sqlite3'

@app.route("/api/whoami")
@auth.require_user
def who_am_i():
    """This route is protected, current_user is always set"""
    return {"user_id": current_user.user_id}
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

@app.route('/deleteAppointment/<appointmentid>', methods=['DELETE'])
def delete_appointment(appointmentid):
    # Delete the appointment with the specified appointment ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Appointment WHERE AppointmentID = ?", (appointmentid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Appointment deleted successfully'}), 200

@app.route('/updateAppointment/<appointmentid>', methods=['PUT'])
def update_appointment(appointmentid):
    # Get the request data
    data = request.get_json()

    # Extract the appointment details from the request data
    doctor_id = data['DoctorID']
    hospital_id = data['HospitalID']
    date = data['Date']
    time = data['Time']

    # Update the appointment details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE Appointment SET DoctorID = ?, HospitalID = ?, Date = ?, Time = ? WHERE AppointmentID = ?", (doctor_id, hospital_id, date, time, appointmentid))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Appointment updated successfully'}), 200

@app.route('/addDoctorAssignment', methods=['POST'])
def create_doctor_assignment():
    # Get the request data
    data = request.get_json()

    # Extract the doctor assignment details from the request data
    doctor_id = data['DoctorID']
    hospital_id = data['HospitalID']

    # Generate a unique doctor assignment ID
    # You can use a library like uuid to generate a unique ID
    doctor_assignment_id = generate_unique_id("DoctorAssignment")

    # Insert the doctor assignment details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO DoctorAssignment (AssignmentID, DoctorID, HospitalID) VALUES ( ?, ?, ?)", ( doctor_assignment_id, doctor_id, hospital_id))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Doctor assignment created successfully'}), 201

@app.route('/getDoctorAssignments', methods=['GET'])
def get_doctor_assignments():
    # Get all the doctor assignments from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DoctorAssignment")
    doctor_assignments = cursor.fetchall()
    conn.close()

    # Return the doctor assignments as a JSON response
    return jsonify({'doctor_assignments': doctor_assignments}), 200

@app.route('/getDoctorAssignment/<assignmentid>', methods=['GET'])
def get_doctor_assignment(assignmentid):
    # Get the doctor assignment with the specified assignment ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DoctorAssignment WHERE AssignmentID = ?", (assignmentid,))
    doctor_assignment = cursor.fetchone()
    conn.close()

    # Return the doctor assignment as a JSON response
    return jsonify({'doctor_assignment': doctor_assignment}), 200

@app.route('/deleteDoctorAssignment/<assignmentid>', methods=['DELETE'])
def delete_doctor_assignment(assignmentid):
    # Delete the doctor assignment with the specified assignment ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM DoctorAssignment WHERE AssignmentID = ?", (assignmentid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Doctor assignment deleted successfully'}), 200

@app.route('/updateDoctorAssignment/<assignmentid>', methods=['PUT'])
def update_doctor_assignment(assignmentid):
    # Get the request data
    data = request.get_json()

    # Extract the doctor assignment details from the request data
    doctor_id = data['DoctorID']
    hospital_id = data['HospitalID']

    # Update the doctor assignment details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE DoctorAssignment SET DoctorID = ?, HospitalID = ? WHERE AssignmentID = ?", (doctor_id, hospital_id, assignmentid))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Doctor assignment updated successfully'}), 200

@app.route('/addhealthrecord', methods = ['POST'])
def create_health_record():
    # Get the request data
    data = request.get_json()
    record_id = generate_unique_id('HealthRecord')
    # Extract the health record details from the request data
    health_id = data['HealthID']
    doctor_id = data['DoctorID']
    hospital_id = data['HospitalID']
    date_of_visit = data['DateOfCheck']
    diagnosis = data['Diagnosis']
    prescription = data['Prescription']
    notes = data['Notes']

    # Insert the health record details into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO HealthRecord (RecordID, HealthID, DoctorID, HospitalID, DateOfVisit, Diagnosis, Prescription, Notes) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)", ( record_id, health_id, doctor_id, hospital_id, date_of_visit, diagnosis, prescription, notes))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Health record created successfully'}), 201

@app.route('/getHealthRecords', methods=['GET'])
def get_health_records():
    # Get all the health records from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HealthRecord")
    health_records = cursor.fetchall()
    conn.close()

    # Return the health records as a JSON response
    return jsonify({'health_records': health_records}), 200

@app.route('/getHealthRecord/<recordid>', methods=['GET'])
def get_health_record(recordid):
    # Get the health record with the specified record ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HealthRecord WHERE RecordID = ?", (recordid,))
    health_record = cursor.fetchone()
    conn.close()

    # Return the health record as a JSON response
    return jsonify({'health_record': health_record}), 200

@app.route('/deleteHealthRecord/<recordid>', methods=['DELETE'])
def delete_health_record(recordid):
    # Delete the health record with the specified record ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM HealthRecord WHERE RecordID = ?", (recordid,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Health record deleted successfully'}), 200

@app.route('/updateHealthRecord/<recordid>', methods=['PUT'])
def update_health_record(recordid):
    # Get the request data
    data = request.get_json()

    # Extract the health record details from the request data
    health_id = data['HealthID']
    doctor_id = data['DoctorID']
    hospital_id = data['HospitalID']
    date_of_visit = data['DateOfCheck']
    diagnosis = data['Diagnosis']
    prescription = data['Prescription']
    notes = data['Notes']

    # Update the health record details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE HealthRecord SET HealthID = ?, DoctorID = ?, HospitalID = ?, DateOfVisit = ?, Diagnosis = ?, Prescription = ?, Notes = ? WHERE RecordID = ?", (health_id, doctor_id, hospital_id, date_of_visit, diagnosis, prescription, notes, recordid))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Health record updated successfully'}), 200

@app.route('/getPatientHealthRecords/<healthid>', methods=['GET'])
def get_patient_health_records(healthid):
    # Get the health records for the patient with the specified health ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HealthRecord WHERE HealthID = ?", (healthid,))
    health_records = cursor.fetchall()
    conn.close()

    # Return the health records as a JSON response
    return jsonify({'health_records': health_records}), 200

@app.route('/getDoctorAppointments/<doctorid>', methods=['GET'])
def get_doctor_appointments(doctorid):
    # Get the appointments for the doctor with the specified doctor ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Appointment WHERE DoctorID = ?", (doctorid,))
    appointments = cursor.fetchall()
    conn.close()

    # Return the appointments as a JSON response
    return jsonify({'appointments': appointments}), 200

@app.route('/getHospitalDoctors/<hospitalid>', methods=['GET'])
def get_hospital_doctors(hospitalid):
    # Get the doctors for the hospital with the specified hospital ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor WHERE HospitalID = ?", (hospitalid,))
    doctors = cursor.fetchall()
    conn.close()

    # Return the doctors as a JSON response
    return jsonify({'doctors': doctors}), 200

@app.route('/getDoctorHospitals/<doctorid>', methods=['GET'])
def get_doctor_hospitals(doctorid):
    # Get the hospitals for the doctor with the specified doctor ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DoctorAssignment WHERE DoctorID = ?", (doctorid,))
    hospitals = cursor.fetchall()
    conn.close()

    # Return the hospitals as a JSON response
    return jsonify({'hospitals': hospitals}), 200

@app.route('/getPatientAppointments/<healthid>', methods=['GET'])
def get_patient_appointments(healthid):
    # Get the appointments for the patient with the specified health ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Appointment WHERE PatientID = ?", (healthid,))
    appointments = cursor.fetchall()
    conn.close()

    # Return the appointments as a JSON response
    return jsonify({'appointments': appointments}), 200

@app.route('/addFile/<record_id>', methods=['POST'])
def upload_file(record_id):
    # Get the file from the request
    file = request.files['file']
    recordid = record_id
    # Save the file to the uploads folder
    file.save('uploads/' + file.filename)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Files (RecordID, FileName) VALUES ( ?, ?)", (recordid, file.filename))
    conn.commit()
    conn.close()
    # Return a success response
    return jsonify({'message': 'File uploaded successfully'}), 201

@app.route('/getFiles/<record_id>', methods=['GET'])
def get_files(record_id):
    # Get the files for the health record with the specified record ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Files WHERE RecordID = ?", (record_id,))
    files = cursor.fetchall()
    conn.close()

    # Return the files as a JSON response
    return jsonify({'files': files}), 200

@app.route('/getPrescription/<record_id>', methods=['GET'])
def get_prescription(record_id):
    # Get the files for the health record with the specified record ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT Prescription FROM HealthRecord WHERE RecordID = ?", (record_id,))
    prescription = cursor.fetchone()
    conn.close()

    # Return the files as a JSON response
    return jsonify({'prescription': prescription}), 200

@app.route('/getDoctorsBySpecialization/<specialization>', methods=['GET'])
def get_doctors_by_specialization(specialization):
    # Get the doctors with the specified specialization from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Doctor WHERE Specialization = ?", (specialization,))
    doctors = cursor.fetchall()
    conn.close()

    # Return the doctors as a JSON response
    return jsonify({'doctors': doctors}), 200


@app.route('/addPrescription/<record_id>', methods=['PUT'])
def add_prescription(record_id):
    # Get the request data
    data = request.get_json()

    # Extract the prescription details from the request data
    prescription = data['Prescription']

    # Update the prescription details in the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE HealthRecord SET Prescription = ? WHERE RecordID = ?", (prescription, record_id))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'Prescription added successfully'}), 200

@app.route('/deleteFile/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    # Delete the file with the specified file ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Files WHERE FileID = ?", (file_id,))
    conn.commit()
    conn.close()

    # Return a success response
    return jsonify({'message': 'File deleted successfully'}), 200

@app.route('/getPatientFiles/<healthid>', methods=['GET'])
def get_patient_files(healthid):
    # Get the files for the patient with the specified health ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Files WHERE HealthID = ?", (healthid,))
    files = cursor.fetchall()
    conn.close()

    # Return the files as a JSON response
    return jsonify({'files': files}), 200

@app.route('/getDoctorFiles/<doctorid>', methods=['GET'])
def get_doctor_files(doctorid):
    # Get the files for the doctor with the specified doctor ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Files WHERE DoctorID = ?", (doctorid,))
    files = cursor.fetchall()
    conn.close()

    # Return the files as a JSON response
    return jsonify({'files': files}), 200

@app.route('/getHospitalFiles/<hospitalid>', methods=['GET'])
def get_hospital_files(hospitalid):
    # Get the files for the hospital with the specified hospital ID from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Files WHERE HospitalID = ?", (hospitalid,))
    files = cursor.fetchall()
    conn.close()

    # Return the files as a JSON response
    return jsonify({'files': files}), 200


def generate_unique_id(params1):
    if params1 == 'Hospital':
        # Generate a unique ID using a combination of letters and numbers
        return 'H' + str(random.randint(1000, 9999))
    elif params1 == 'Doctor':
        # Generate a unique ID using a combination of letters and numbers
        return 'D' + str(random.randint(1000, 9999))
    elif params1 == 'Appointment':
        # Generate a unique ID using a combination of letters and numbers
        return 'A' + str(random.randint(1000, 9999))
    elif params1 == 'DoctorAssignment':
        # Generate a unique ID using a combination of letters and numbers
        return 'DA' + str(random.randint(1000, 9999))
    elif params1 == 'HealthRecord':
        # Generate a unique ID using a combination of letters and numbers
        return 'HR' + str(random.randint(1000, 9999))
    # Generate a unique ID using a combination of letters and numbers
    return 'P' + str(random.randint(1000, 9999))