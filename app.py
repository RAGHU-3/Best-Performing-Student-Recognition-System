from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database and create the students table if it doesn't exist
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gpa REAL,
            attendance REAL,
            hackathons INTEGER,
            papers INTEGER,
            mentoring INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Call the init_db function to ensure the database is ready
init_db()

# Route to render the frontend HTML page
@app.route('/')
def home():
    return render_template('index.html')

# API to add a student to the database
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    name = data['name']
    gpa = data['gpa']
    attendance = data['attendance']
    hackathons = data['hackathons']
    papers = data['papers']
    mentoring = data['mentoring']

    # Insert the student data into the database
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, gpa, attendance, hackathons, papers, mentoring)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, gpa, attendance, hackathons, papers, mentoring))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student added successfully!'}), 200

# API to rank students and return the top 3 based on weighted scores
@app.route('/rank', methods=['GET'])
def rank_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # Calculate the score using a weighted formula
    cursor.execute('''
        SELECT name, gpa, attendance, hackathons, papers, mentoring,
               (gpa * 0.5 + attendance * 0.3 + hackathons * 0.1 +
                papers * 0.05 + mentoring * 0.05) AS score
        FROM students
        ORDER BY score DESC
        LIMIT 3
    ''')
    students = cursor.fetchall()
    conn.close()

    # Return the top 3 students as JSON
    return jsonify(students), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
