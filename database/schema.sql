-- =========================================================
-- Database: FixFlowDB
-- Project: Repair Request and Tracking System for UC Main Facilities
-- Management Tool: SSMS (SQL Server Management Studio)
-- =========================================================

USE FixFlowDB;
GO

-- Drop tables in reverse order of dependencies if they already exist
DROP TABLE IF EXISTS ASSIGNMENT;
DROP TABLE IF EXISTS REQUEST;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS LOCATION;
DROP TABLE IF EXISTS FLOOR;
DROP TABLE IF EXISTS STATUS;
DROP TABLE IF EXISTS CATEGORIES;
DROP TABLE IF EXISTS ROLE;
DROP TABLE IF EXISTS DEPARTMENT;
GO

-- 1. Create Independent Tables
CREATE TABLE DEPARTMENT (
    department_id INT IDENTITY(1,1) PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_desc VARCHAR(255) NULL
);

CREATE TABLE ROLE (
    role_id INT IDENTITY(1,1) PRIMARY KEY,
    role_name VARCHAR(30) NOT NULL
);

CREATE TABLE CATEGORIES (
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE STATUS (
    status_id INT IDENTITY(1,1) PRIMARY KEY,
    status_name VARCHAR(30) NOT NULL,
    description VARCHAR(255) NULL
);

CREATE TABLE FLOOR (
    floor_id INT IDENTITY(1,1) PRIMARY KEY,
    building VARCHAR(50) NOT NULL,
    floor_name VARCHAR(20) NOT NULL
);

-- 2. Create Dependent Tables
CREATE TABLE LOCATION (
    location_id INT IDENTITY(1,1) PRIMARY KEY,
    building VARCHAR(50) NOT NULL,
    room VARCHAR(20) NOT NULL,
    floor_id INT NOT NULL,
    CONSTRAINT FK_LOCATION_FLOOR FOREIGN KEY (floor_id) REFERENCES FLOOR(floor_id)
);

CREATE TABLE USERS (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    school_id_no VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    contact_no VARCHAR(15) NULL,
    created_at DATETIME DEFAULT GETDATE(),
    department_id INT NOT NULL,
    role_id INT NOT NULL,
    CONSTRAINT FK_USERS_DEPARTMENT FOREIGN KEY (department_id) REFERENCES DEPARTMENT(department_id),
    CONSTRAINT FK_USERS_ROLE FOREIGN KEY (role_id) REFERENCES ROLE(role_id)
);

CREATE TABLE REQUEST (
    request_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NULL, -- Optional foreign key
    category_id INT NOT NULL,
    location_id INT NOT NULL,
    status_id INT NOT NULL,
    occurrence INT NOT NULL DEFAULT 1,
    request_date DATETIME NOT NULL DEFAULT GETDATE(),
    description_label VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    priority VARCHAR(10) DEFAULT 'Medium',
    image_url VARCHAR(255) NULL,
    CONSTRAINT FK_REQUEST_USERS FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    CONSTRAINT FK_REQUEST_CATEGORIES FOREIGN KEY (category_id) REFERENCES CATEGORIES(category_id),
    CONSTRAINT FK_REQUEST_LOCATION FOREIGN KEY (location_id) REFERENCES LOCATION(location_id),
    CONSTRAINT FK_REQUEST_STATUS FOREIGN KEY (status_id) REFERENCES STATUS(status_id)
);

CREATE TABLE ASSIGNMENT (
    assignment_id INT IDENTITY(1,1) PRIMARY KEY,
    date_assigned DATETIME NOT NULL DEFAULT GETDATE(),
    date_started DATETIME NULL,
    date_completed DATETIME NULL,
    remarks VARCHAR(255) NULL,
    request_id INT NOT NULL, -- FK1
    staff_id INT NOT NULL,   -- FK2
    CONSTRAINT FK_ASSIGNMENT_REQUEST FOREIGN KEY (request_id) REFERENCES REQUEST(request_id),
    CONSTRAINT FK_ASSIGNMENT_STAFF FOREIGN KEY (staff_id) REFERENCES USERS(user_id)
);
GO

-- =========================================================
-- Initial Seed Data for UC Main Facilities
-- =========================================================

-- Departments
INSERT INTO DEPARTMENT (department_name, department_desc) VALUES
('College of Allied Engineering', 'CAE Department at UC Main'),
('College of Arts and Sciences', 'CAS Department at UC Main'),
('College of Business and Accountancy', 'CBA Department at UC Main'),
('College of Computer Studies', 'CCS Department at UC Main'),
('College of Criminal Justice', 'CCJ Department at UC Main'),
('College of Customs and Administration', 'CCA Department at UC Main'),
('College of Engineering', 'COE Department at UC Main'),
('College of Hospitality Management', 'CHM Department at UC Main'),
('College of Nursing', 'CON Department at UC Main'),
('College of Social Work', 'CSW Department at UC Main'),
('College of Teacher Education', 'CTE Department at UC Main'),
('Facilities & Physical Plant Office', 'Maintenance and Campus Operations'),
('General Services Office', 'Custodial and Campus Services');

-- Roles
INSERT INTO ROLE (role_name) VALUES
('Admin'),
('Staff'),
('Faculty'),
('Student');

-- Categories
INSERT INTO CATEGORIES (category_name, description) VALUES
('Air Conditioning / HVAC', 'Aircon repair, maintenance, cleaning, and temperature control'),
('Electrical', 'Lighting, power outlets, circuit breakers, wiring issues'),
('Plumbing & Restroom', 'Water leaks, clogged pipes, broken faucets, CR fixtures'),
('Carpentry & Furniture', 'Broken desks, chairs, doors, locks, whiteboards, windows'),
('IT & AV Equipment', 'Projectors, sound system, lab computers, network cabling'),
('General Facilities', 'Wall paint, floor damage, ceiling leaks, physical hazards');

-- Status
INSERT INTO STATUS (status_name, description) VALUES
('Pending', 'Request submitted and awaiting review/assignment'),
('Assigned', 'Assigned to a maintenance technician'),
('In Progress', 'Technician is actively working on the repair'),
('Completed', 'Repair has been verified and resolved'),
('Cancelled', 'Request was cancelled or marked as duplicate');

-- Floors (UC Main Buildings)
INSERT INTO FLOOR (building, floor_name) VALUES
('Main Building', 'Ground Floor'),
('Main Building', '2nd Floor'),
('Main Building', '3rd Floor'),
('Main Building', '4th Floor'),
('Main Building', '5th Floor'),
('Engineering Building', '1st Floor'),
('Engineering Building', '2nd Floor'),
('Engineering Building', '3rd Floor');

-- Locations
INSERT INTO LOCATION (building, room, floor_id) VALUES
('Main Building', 'Room 101', 1),
('Main Building', 'Faculty Room G/F', 1),
('Main Building', 'Room 205 (Lecture)', 2),
('Main Building', 'Room 208', 2),
('Main Building', 'CCS Computer Lab 1', 3),
('Main Building', 'CCS Computer Lab 2', 3),
('Main Building', 'Male CR 3F', 3),
('Main Building', 'Room 401', 4),
('Main Building', 'Audio Visual Hall', 4),
('Main Building', 'Room 502', 5),
('Engineering Building', 'Circuits Lab 1F', 6),
('Engineering Building', 'Drawing Room 2F', 7);
GO
