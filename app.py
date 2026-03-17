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

# ===============================
# NEW DARK MODERN UI
# ===============================
@app.route('/students')
def list_students():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Manager</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
            }

            .container {
                max-width: 1100px;
                margin: 40px auto;
                padding: 20px;
            }

            h1 {
                text-align: center;
                margin-bottom: 20px;
            }

            .card {
                background: #1e293b;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.5);
            }

            .top-bar {
                display: flex;
                justify-content: space-between;
                margin-bottom: 15px;
            }

            .btn {
                padding: 8px 14px;
                border-radius: 6px;
                text-decoration: none;
                font-size: 14px;
                transition: 0.2s;
            }

            .add { background: #22c55e; color: white; }
            .edit { background: #3b82f6; color: white; }
            .delete { background: #ef4444; color: white; }

            .btn:hover {
                opacity: 0.85;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            th, td {
                padding: 12px;
                text-align: center;
            }

            th {
                background: #334155;
            }

            tr:nth-child(even) {
                background: #1e293b;
            }

            tr:nth-child(odd) {
                background: #0f172a;
            }

            tr:hover {
                background: #334155;
            }

            .grade {
                font-weight: bold;
            }

            .high { color: #22c55e; }
            .mid { color: #facc15; }
            .low { color: #ef4444; }

            .actions a {
                margin: 0 5px;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🎓 Student Dashboard</h1>

            <div class="card">
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
                        <td class="grade 
                            {% if s.grade >= 85 %}high
                            {% elif s.grade >= 75 %}mid
                            {% else %}low
                            {% endif %}">
                            {{s.grade}}
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
        </div>
    </body>
    </html>
    """
    return render_template_string(html, students=students)

# ===============================
# SIMPLE FORMS (MATCH DARK UI)
# ===============================
@app.route('/add_student_form')
def add_student_form():
    return """
    <body style='background:#0f172a;color:white;font-family:Arial;text-align:center;margin-top:60px;'>
        <h2>Add Student</h2>
        <form method='POST' action='/add_student'>
            <input placeholder='Name' name='name'><br><br>
            <input type='number' placeholder='Grade' name='grade'><br><br>
            <input placeholder='Section' name='section'><br><br>
            <button>Add</button>
        </form>
        <br><a href='/students' style='color:#38bdf8;'>Back</a>
    </body>
    """

@app.route('/add_student', methods=['POST'])
def add_student():
    students.append({
        "id": max([s["id"] for s in students]) + 1 if students else 1,
        "name": request.form.get("name"),
        "grade": int(request.form.get("grade")),
        "section": request.form.get("section")
    })
    return redirect(url_for('list_students'))

@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    return render_template_string("""
    <body style='background:#0f172a;color:white;font-family:Arial;text-align:center;margin-top:60px;'>
        <h2>Edit Student</h2>
        <form method='POST'>
            <input name='name' value='{{student.name}}'><br><br>
            <input type='number' name='grade' value='{{student.grade}}'><br><br>
            <input name='section' value='{{student.section}}'><br><br>
            <button>Update</button>
        </form>
        <br><a href='/students' style='color:#38bdf8;'>Back</a>
    </body>
    """, student=student)

@app.route('/api/students')
def api_students():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)

