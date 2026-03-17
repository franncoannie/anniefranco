from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

@app.route('/')
def home():
    return redirect(url_for('list_students'))

# MODERN UI
@app.route('/students')
def list_students():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Manager</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                margin: 0;
                padding: 0;
                color: #333;
            }

            .container {
                max-width: 1000px;
                margin: 40px auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }

            h2 {
                text-align: center;
                margin-bottom: 20px;
            }

            .top-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }

            .btn {
                padding: 8px 15px;
                border-radius: 8px;
                text-decoration: none;
                color: white;
                font-size: 14px;
                transition: 0.3s;
            }

            .add { background: #4CAF50; }
            .edit { background: #2196F3; }
            .delete { background: #f44336; }

            .btn:hover {
                opacity: 0.8;
                transform: scale(1.05);
            }

            table {
                width: 100%;
                border-collapse: collapse;
                overflow: hidden;
                border-radius: 10px;
            }

            th {
                background: #667eea;
                color: white;
                padding: 12px;
            }

            td {
                padding: 12px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }

            tr:hover {
                background: #f5f5f5;
            }

            .actions a {
                margin: 0 5px;
            }

            .badge {
                padding: 5px 10px;
                border-radius: 20px;
                color: white;
                font-size: 12px;
            }

            .high { background: #4CAF50; }
            .mid { background: #FF9800; }
            .low { background: #f44336; }
        </style>
    </head>

    <body>
        <div class="container">
            <h2>📘 Student Manager</h2>

            <div class="top-bar">
                <div></div>
                <a class="btn add" href="/add_student_form">+ Add Student</a>
            </div>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Section</th>
                    <th>Actions</th>
                </tr>

                {% for s in students %}
                <tr>
                    <td>{{s.id}}</td>
                    <td>{{s.name}}</td>
                    <td>
                        {% if s.grade >= 85 %}
                            <span class="badge high">{{s.grade}}</span>
                        {% elif s.grade >= 75 %}
                            <span class="badge mid">{{s.grade}}</span>
                        {% else %}
                            <span class="badge low">{{s.grade}}</span>
                        {% endif %}
                    </td>
                    <td>{{s.section}}</td>
                    <td class="actions">
                        <a class="btn edit" href="/edit_student/{{s.id}}">Edit</a>
                        <a class="btn delete" href="/delete_student/{{s.id}}" onclick="return confirm('Delete this student?')">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# KEEP OTHER ROUTES SAME
@app.route('/add_student_form')
def add_student_form():
    return """
    <div style='font-family:Poppins;text-align:center;margin-top:50px;'>
        <h2>Add Student</h2>
        <form method='POST' action='/add_student'>
            <input placeholder='Name' name='name' required><br><br>
            <input type='number' placeholder='Grade' name='grade' required><br><br>
            <input placeholder='Section' name='section' required><br><br>
            <button>Add</button>
        </form>
        <br><a href='/students'>Back</a>
    </div>
    """

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    new_student = {
        "id": max([s["id"] for s in students]) +
