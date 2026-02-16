🛡️ Dockerized SQL Injection Training Lab
Pacific International School Simulation
A safe, isolated, and containerized environment for learning and practicing SQL Injection (SQLi) attacks. Features a custom Attack Analysis Engine that provides real-time educational feedback.

📖 Table of Contents
About the Project

Key Features

Technology Stack

Getting Started

How to Use the Lab

Project Architecture

Disclaimer

About the Project
This project simulates a realistic school management system web application ("Pacific International School"). Unlike standard vulnerability labs that just say "Success" or "Fail," this application includes a backend analysis engine.

When a user attempts an SQL injection, the system intercepts the query, analyzes the payload logic, and generates a detailed educational report. This bridges the gap between executing an attack and understanding the underlying database logic.

The entire environment is containerized using Docker, ensuring that the vulnerable database is isolated from the host machine and can be reset instantly.

🚀 Key Features
1. 🔓 Vulnerable Login Portals (In-Band SQLi)
Student & Faculty Logins: Intentionally vulnerable to authentication bypass.

Attack Type: In-Band / Error-Based SQL Injection.

Goal: Log in as an administrator or student without knowing the password.

2. 🕵️ Course Lookup System (Blind SQLi)
Catalog Search: A feature that checks if a course exists.

Attack Type: Inferential (Boolean-Based) Blind SQL Injection.

Goal: Infer database structure by asking "True/False" questions via the search bar.

3. 📊 Real-Time Attack Reports
The standout feature of this lab. Upon a successful (or failed) injection, the application displays:

The Raw Input: Exactly what the user typed.

The Final Query: How the server constructed the command (highlighting the injected code).

Educational Explanation: A breakdown of why the attack worked (e.g., explaining how comment operators -- neutralized the password check).

4. 🐳 Full Containerization
Zero manual installation of MySQL or Python required.

One command (docker compose up) sets up the network, database, and web server.

🛠 Technology Stack
Backend: Python 3.9 (Flask Framework)

Database: MySQL 8.0 (Official Docker Image)

Frontend: HTML5, CSS3, Jinja2 Templates

Containerization: Docker & Docker Compose

Database Connector: mysql-connector-python

🏁 Getting Started
Prerequisites
Docker Desktop installed and running.

Git (optional, to clone the repo).

Bash
docker compose up --build

Access the Lab
Open your web browser and navigate to:

http://localhost:5000

Stop the Lab
Press Ctrl + C in the terminal, or run docker compose down.

🧪 How to Use the Lab
Scenario 1: The Login Bypass
Navigate to School Home.

Locate the Student Portal.

The Vulnerability: The backend code directly concatenates user input into the SQL query:

Python
query = f"SELECT * FROM students WHERE username = '{username}' AND password = '{password}'"
The Payload: Enter ' OR '1'='1' --  as the username.

The Result: You will be logged in, and a Detailed Report will appear at the top of the screen explaining the syntax.

Scenario 2: Blind Data Extraction
Navigate to Academics.

Locate the Course Lookup form.

The Vulnerability: The system only replies with "Found" or "Not Found," making it perfect for Blind SQLi practice.

The Payload: Try injecting logic statements like ' AND '1'='1 vs ' AND '1'='0.

📂 Project Architecture
Plaintext
.
├── app.py                # Main Flask application (Vulnerability logic & Report Engine)
├── docker-compose.yml    # Orchestrates the Web and DB services
├── Dockerfile            # Builds the Python environment
├── requirements.txt      # Python dependencies
├── init.sql              # Creates the database schema and dummy data
├── .gitignore            # Specifies files to exclude from Git
└── templates/            # HTML frontend files
    ├── schoolHomePage.html  # Contains the Report View logic
    ├── academics.html
    └── ...


⚠️ Disclaimer
For Educational Purposes Only.
This project is designed intentionally with security vulnerabilities to teach defensive coding and penetration testing concepts.

DO NOT upload this application to a public web server or cloud hosting provider without securing it first.

DO NOT use the techniques learned here on any system where you do not have explicit permission.

Author
Prashant Bhattarai
B.tech CSE student 
Built as a Mini Project for 3rd yearx