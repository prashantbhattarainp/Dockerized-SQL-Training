from flask import Flask, render_template, request
import mysql.connector
import os

app = Flask(__name__)

# --- Database Connection Details ---
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_NAME = os.environ.get('DB_NAME', 'school_db')

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error:
        return None

# --- Helper: Payload Analysis ---
def analyze_payload(input_str, query_type="login"):
    """Provides educational context based on common SQLi patterns."""
    explanation = "The server took your input and directly inserted it into the query string."
    
    if "'" in input_str:
        explanation += " You successfully used a single quote (') to close the string literal intended for the username/ID."
    
    if "--" in input_str or "#" in input_str:
        explanation += " You used a comment operator (-- or #) to neutralize the rest of the query, effectively removing password checks or other conditions."
        
    if "OR" in input_str.upper() or "AND" in input_str.upper():
        explanation += " You injected logical operators (OR/AND) to manipulate the query's WHERE clause condition."

    if query_type == "blind" and ("=1" in input_str or "=2" in input_str):
         explanation += " In a Blind scenario, you are using true/false conditions to infer information based on whether the application returns a 'Found' or 'Not Found' response."

    return explanation

# --- Page Routes ---
# (These remain unchanged)
@app.route('/')
def intro_page(): return render_template('index.html')
@app.route('/schoolHomePage.html')
def school_home(): return render_template('schoolHomePage.html')
@app.route('/academics.html')
def academics(): return render_template('academics.html')
@app.route('/admissions.html')
def admissions(): return render_template('admissions.html')
@app.route('/campus-life.html')
def campus_life(): return render_template('campus-life.html')

# --- Login Logic Routes (Updated with Reporting) ---

@app.route('/student_login', methods=['POST'])
def student_login():
    username = request.form.get('student_username')
    # Password is ignored in SQLi, but we capture it for realism
    password = request.form.get('student_password') 
    
    conn = get_db_connection()
    sqli_report = {
        'type': 'In-Band (Login Bypass)',
        'target_field': 'Student Username',
        'user_input': username,
        'final_query': '',
        'outcome_status': '', # 'success', 'fail', or 'error'
        'outcome_detail': '',
        'explanation': analyze_payload(username, "login")
    }

    if conn:
        cursor = conn.cursor(dictionary=True)
        # VULNERABLE QUERY
        query = f"SELECT * FROM students WHERE username = '{username}' AND password = '{password}'"
        sqli_report['final_query'] = query
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                account = results[0]
                sqli_report['outcome_status'] = 'success'
                sqli_report['outcome_detail'] = f"SUCCESS: Authentication Bypassed! Logged in as: {account['full_name']} (Role: {account['roll_no']})"
            else:
                sqli_report['outcome_status'] = 'fail'
                sqli_report['outcome_detail'] = "FAILURE: The injection did not result in a valid login. The query logic evaluated to false."
        except mysql.connector.Error as e:
            sqli_report['outcome_status'] = 'error'
            sqli_report['outcome_detail'] = f"DATABASE SYNTAX ERROR: {e}"
            sqli_report['explanation'] += " Your payload broke the SQL syntax. Look closely at the error message to see where quotes or logic went wrong."
        finally:
            cursor.close()
            conn.close()
    else:
        sqli_report['outcome_status'] = 'error'
        sqli_report['outcome_detail'] = "Database connection failed."

    # Pass the entire report object to the template
    return render_template('schoolHomePage.html', report=sqli_report)


@app.route('/faculty_login', methods=['POST'])
def faculty_login():
    # (Similar update for Faculty login - simplified for brevity, but follows same pattern)
    email = request.form.get('faculty_username')
    password = request.form.get('faculty_password')
    conn = get_db_connection()
    
    sqli_report = {
        'type': 'In-Band (Login Bypass)',
        'target_field': 'Faculty Email',
        'user_input': email,
        'final_query': '',
        'outcome_status': '',
        'outcome_detail': '',
        'explanation': analyze_payload(email, "login")
    }

    if conn:
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM faculty WHERE email = '{email}' AND password = '{password}'"
        sqli_report['final_query'] = query
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                account = results[0]
                sqli_report['outcome_status'] = 'success'
                sqli_report['outcome_detail'] = f"SUCCESS: Authentication Bypassed! Logged in as: {account['full_name']} (Position: {account['position']})"
            else:
                 sqli_report['outcome_status'] = 'fail'
                 sqli_report['outcome_detail'] = "FAILURE: Login failed."
        except mysql.connector.Error as e:
            sqli_report['outcome_status'] = 'error'
            sqli_report['outcome_detail'] = f"DATABASE SYNTAX ERROR: {e}"
        finally:
            cursor.close()
            conn.close()
    else:
         sqli_report['outcome_status'] = 'error'
         sqli_report['outcome_detail'] = "Connection failed."

    return render_template('schoolHomePage.html', report=sqli_report)

@app.route('/course_lookup', methods=['POST'])
def course_lookup():
    course_id = request.form.get('course_id')
    conn = get_db_connection()

    sqli_report = {
        'type': 'Blind (Inferential)',
        'target_field': 'Course ID Search',
        'user_input': course_id,
        'final_query': '',
        'outcome_status': '',
        'outcome_detail': '',
        'explanation': analyze_payload(course_id, "blind")
    }

    if conn:
        cursor = conn.cursor()
        query = f"SELECT course_name FROM courses WHERE course_id = '{course_id}'"
        sqli_report['final_query'] = query
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                sqli_report['outcome_status'] = 'success'
                sqli_report['outcome_detail'] = "TRUE RESPONSE: The application says 'Course Found'."
                sqli_report['explanation'] += " In a Blind attack, this 'True' response confirms your injected condition evaluated to true."
            else:
                sqli_report['outcome_status'] = 'fail'
                sqli_report['outcome_detail'] = "FALSE RESPONSE: The application says 'Course Not Found'."
        except mysql.connector.Error as e:
            # In true Blind SQLi, errors are usually suppressed, but for training we show them in the report
            sqli_report['outcome_status'] = 'error'
            sqli_report['outcome_detail'] = f"DATABASE ERROR (Often suppressed in real Blind SQLi): {e}"
        finally:
            cursor.close()
            conn.close()
    else:
         sqli_report['outcome_status'] = 'error'
         sqli_report['outcome_detail'] = "Connection failed."

    return render_template('academics.html', report=sqli_report)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)