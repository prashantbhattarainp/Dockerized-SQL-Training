-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS school_db;
USE school_db;

-- Drop existing tables to ensure a clean slate on restart
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS students;

-- Create the 'students' table with detailed columns
CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  roll_no VARCHAR(20) NOT NULL UNIQUE,
  full_name VARCHAR(100) NOT NULL,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  class VARCHAR(20),
  address VARCHAR(255),
  sex ENUM('Male', 'Female', 'Other'),
  year_of_admission INT
);

-- Create the 'faculty' table with detailed columns
CREATE TABLE faculty (
  id INT AUTO_INCREMENT PRIMARY KEY,
  faculty_id VARCHAR(20) NOT NULL UNIQUE,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  department VARCHAR(50),
  position VARCHAR(50),
  sex ENUM('Male', 'Female', 'Other')
);

-- Create the 'courses' table for the search feature
CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_id VARCHAR(10) NOT NULL UNIQUE,
  course_name VARCHAR(100) NOT NULL,
  department VARCHAR(50)
);

--  dataset for 'students'
INSERT INTO students (roll_no, full_name, username, password, class, address, sex, year_of_admission) VALUES
('S001', 'Priya Sharma', 'priya_s', 'pass123', '12th A', '123 MG Road, Mumbai', 'Female', 2022),
('S002', 'Rohan Gupta', 'rohan_g', 'pass456', '12th B', '456 Park Street, Delhi', 'Male', 2022),
('S003', 'Anjali Singh', 'anjali_s', 'pass789', '11th A', '789 Jubilee Hills, Hyderabad', 'Female', 2023),
('S004', 'Vikram Kumar', 'vikram_k', 'pass101', '11th C', '101 Koramangala, Bangalore', 'Male', 2023),
('S005', 'Sneha Reddy', 'sneha_r', 'pass202', '10th B', '202 Anna Nagar, Chennai', 'Female', 2024),
('S006', 'Amit Patel', 'amit_p', 'pass303', '10th A', '303 Satellite, Ahmedabad', 'Male', 2024),
('S007', 'Kavita Joshi', 'kavita_j', 'pass404', '9th C', '404 Viman Nagar, Pune', 'Female', 2025),
('S008', 'Sandeep Verma', 'sandeep_v', 'pass505', '9th A', '505 Sector 17, Chandigarh', 'Male', 2025),
('S009', 'Meera Iyer', 'meera_i', 'pass606', '12th A', '606 Salt Lake, Kolkata', 'Female', 2022),
('S010', 'admin', 'adminpassword', 'Aditya Chauhan', 'N/A', 'School Admin Block', 'Male', 2020);

--  dataset for 'faculty'
INSERT INTO faculty (faculty_id, full_name, email, password, department, position, sex) VALUES
('F01', 'Dr. Rajesh Kumar', 'rajesh.kumar@pacific.edu', 'faculty123', 'Physics', 'Professor', 'Male'),
('F02', 'Dr. Sunita Menon', 'sunita.menon@pacific.edu', 'faculty456', 'Chemistry', 'Professor', 'Female'),
('F03', 'Mr. Arjun Desai', 'arjun.desai@pacific.edu', 'faculty789', 'Computer Science', 'Assistant Professor', 'Male'),
('F04', 'Mrs. Deepa Krishnan', 'deepa.k@pacific.edu', 'faculty101', 'Mathematics', 'Head of Department', 'Female'),
('F05', 'Dr. Alok Nath', 'dean.office@pacific.edu', 'deanpass', 'Administration', 'Dean of Academics', 'Male');

--  list of courses
INSERT INTO courses (course_id, course_name, department) VALUES
('CS101', 'Introduction to Computer Science', 'Computer Science'),
('PHY203', 'Modern Physics', 'Physics'),
('ENG301', 'Advanced English Literature', 'English'),
('MTH201', 'Linear Algebra', 'Mathematics'),
('CHM102', 'Organic Chemistry', 'Chemistry'),
('BIO101', 'Introduction to Biology', 'Biology'),
('HIS105', 'History of Modern India', 'History'),
('ECO210', 'Macroeconomics', 'Economics'),
('ART100', 'Introduction to Fine Arts', 'Arts'),
('CSC310', 'Database Management Systems', 'Computer Science');