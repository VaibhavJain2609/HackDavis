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
def generate_unique_id():
    # Generate a unique ID using a combination of letters and numbers
    return 'P' + str(random.randint(1000, 9999))