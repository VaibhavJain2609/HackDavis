-- Patient Table
CREATE TABLE Patient (
    HealthID INT UNIQUE PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255),
    EmergencyContactID INT,
    FOREIGN KEY (EmergencyContactID) REFERENCES EmergencyContact(EmergencyContactID)
);

-- Doctor Table
CREATE TABLE Doctor (
    DoctorID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Specialization VARCHAR(255),
    HospitalID INT,
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255),
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);

-- Hospital Table
CREATE TABLE Hospital (
    HospitalID INT PRIMARY KEY,
    HospitalName VARCHAR(255),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255)
);

-- HealthRecord Table
CREATE TABLE HealthRecord (
    RecordID INT PRIMARY KEY,
    HealthID INT,
    DoctorID INT,
    HospitalID INT,
    DateOfCheck DATE,
    Diagnosis VARCHAR(255),
    Prescription VARCHAR(255),
    Notes VARCHAR(255),
    FOREIGN KEY (HealthID) REFERENCES Patient(HealthID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);

-- Files Table
CREATE TABLE Files (
    FileID INT PRIMARY KEY,
    RecordID INT,
    FileName VARCHAR(255),
    FilePath VARCHAR(255),
    FOREIGN KEY (RecordID) REFERENCES HealthRecord(RecordID)
);

-- EmergencyContact Table
CREATE TABLE EmergencyContact (
    EmergencyContactID INT PRIMARY KEY,
    HealthID INT,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Relationship VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255),
    FOREIGN KEY (HealthID) REFERENCES Patient(HealthID)
);

-- User Table
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255),
    PasswordHash VARCHAR(255),
    Role VARCHAR(20),
    HospitalID INT,
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);

-- DoctorAssignment Table
CREATE TABLE DoctorAssignment (
    AssignmentID INT PRIMARY KEY,
    DoctorID INT,
    HospitalID INT,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);

-- AccessControl Table
CREATE TABLE AccessControl (
    AccessID INT PRIMARY KEY,
    UserID INT,
    HospitalID INT,
    AccessLevel VARCHAR(20),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);