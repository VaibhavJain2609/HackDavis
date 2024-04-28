-- Sample data for Patient Table
INSERT INTO Patient (HealthID, FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber, Email, EmergencyContactID)
VALUES
( 1001, 'John', 'Doe', '1990-05-15', 'Male', '123 Main St, Anytown, USA', '123-456-7890', 'johndoe@example.com', 1),
(1002, 'Jane', 'Smith', '1985-08-25', 'Female', '456 Elm St, Othertown, USA', '987-654-3210', 'janesmith@example.com', 2);

-- Sample data for Doctor Table
INSERT INTO Doctor (DoctorID, FirstName, LastName, Specialization, HospitalID)
VALUES
(1, 'Dr. Sarah', 'Jones', 'Cardiology', 1),
(2, 'Dr. Michael', 'Brown', 'Pediatrics', 2);

-- Sample data for Hospital Table
INSERT INTO Hospital (HospitalID, HospitalName, Address, PhoneNumber, Email)
VALUES
(1, 'City General Hospital', '789 Oak Ave, Citytown, USA', '111-222-3333', 'info@cityhospital.com'),
(2, 'County Children Hospital', '321 Pine St, Countyville, USA', '444-555-6666', 'info@childrenshospital.com');

-- Sample data for HealthRecord Table
INSERT INTO HealthRecord (RecordID, HealthID, DoctorID, HospitalID, DateOfCheck, Diagnosis, Prescription, Notes)
VALUES
(1, 1001, 1, 1, '2024-04-15', 'Hypertension', 'Medication A', 'Follow-up in 3 months'),
(2, 1002, 2, 2, '2024-03-20', 'Common cold', 'Rest and fluids', 'Symptoms improving');

-- Sample data for Files Table
INSERT INTO Files (FileID, RecordID, FileName, FilePath)
VALUES
(1, 1, 'Scan1.pdf', '/path/to/scan1.pdf'),
(2, 2, 'LabResults.pdf', '/path/to/labresults.pdf');

-- Sample data for EmergencyContact Table
INSERT INTO EmergencyContact (EmergencyContactID, HealthID, FirstName, LastName, Relationship, PhoneNumber, Email)
VALUES
(1, 1, 'Emily', 'Doe', 'Spouse', '555-123-4567', 'emilydoe@example.com'),
(2, 2, 'Mark', 'Smith', 'Sibling', '999-888-7777', 'marksmith@example.com');

-- Sample data for User Table
INSERT INTO User (UserID, Username, PasswordHash, Role, HospitalID)
VALUES
(1, 'admin1', 'passwordhash1', 'Admin', 1),
(2, 'user1', 'passwordhash2', 'User', 2);

-- Sample data for DoctorAssignment Table
INSERT INTO DoctorAssignment (AssignmentID, DoctorID, HospitalID, StartDate, EndDate)
VALUES
(1, 1, 1, '2024-01-01', '2025-01-01'),
(2, 2, 2, '2023-12-01', '2024-12-01');

-- Sample data for AccessControl Table
INSERT INTO AccessControl (AccessID, UserID, HospitalID, AccessLevel)
VALUES
(1, 1, 1, 'FullAccess'),
(2, 2, 2, 'LimitedAccess');
