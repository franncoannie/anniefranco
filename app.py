from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Zechariah"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Zechariah"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# ===============================
# HOME
# ===============================
@app.route('/')
def home():
    return redirect(url_for('list_students'))

# ===============================
# MAIN DASHBOARD
# ===============================
@app.route('/students')
def list_students():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Dashboard</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0f172a, #020617);
                color: #e2e8f0;
            }

            .container {
                max-width: 1100px;
                margin: 50px auto;
                padding: 20px;
            }

            h1 {
                text-align: center;
                margin-bottom: 25px;
                font-weight: 600;
                letter-spacing: 1px;
                background: linear-gradient(90deg, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .card {
                background: rgba(30, 41, 59, 0.6);
                backdrop-filter: blur(12px);
                border-radius: 16px;
                padding: 25px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: 0 10px 40px rgba(0,0,0,0.7);
            }

            .top-bar {
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }

            .btn {
                padding: 8px 16px;
                border-radius: 999px;
                text-decoration: none;
                font-size: 13px;
                font-weight: 500;
                transition: all 0.25s ease;
                display: inline-block;
            }

            .add {
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
            }

            .edit {
                background: linear-gradient(135deg, #3b82f6, #2563eb);
                color: white;
            }

            .delete {
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
            }

            .btn:hover {
                transform: translateY(-2px) scale(1.05);
                box-shadow: 0 5px 15px rgba(0,0,0,0.5);
            }

            table {
                width: 100%;
                border-collapse: collapse;
                border-radius: 12px;
                overflow: hidden;
            }

            th {
                background: rgba(51, 65, 85, 0.7);
                font-weight: 600;
            }

            th, td {
                padding: 14px;
                text-align: center;
            }

            tr {
                transition: 0.2s;
            }

            tr:nth-child(even) {
                background: rgba(15, 23, 42, 0.6);
            }

            tr:nth-child(odd) {
                background: rgba(2, 6, 23, 0.6);
            }

            tr:hover {
                background: rgba(56, 189, 248, 0.15);
                transform: scale(1.01);
            }

            .grade {
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 999px;
                display: inline-block;
            }

            .high {
                background: rgba(34,197,94,0.15);
                color: #22c55e;
            }

            .mid {
                background: rgba(250,204,21,0.15);
                color: #facc15;
            }

            .low {
                background: rgba(239,68,68,0.15);
                color: #ef4444;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🎓 Student Dashboard</h1>

            <div class="card">
                <div class="top-bar">
                    <div></div>
                    <a class="btn add" href="/add_student_form">➕ Add Student</a>
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
                            <span class="grade
                                {% if s.grade >= 85 %}high
                                {% elif s.grade >= 75 %}mid
                                {% else %}low
                                {% endif %}">
                                {{s.grade}}
                            </span>
                        </td>
                        <td>{{s.section}}</td>
                        <td>
                            <a class="btn edit" href="/edit_student/{{s.id}}">Edit</a>
                            <a class="btn delete" href="/delete_student/{{s.id}}" onclick="return confirm('Delete?')">Delete</a>
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
# FORM TEMPLATE (REUSABLE STYLE)
# ===============================
form_style = """
<style>
    body {
        background: linear-gradient(135deg, #0f172a, #020617);
        font-family: 'Segoe UI', sans-serif;
        color: white;
        text-align: center;
        padding-top: 80px;
    }

    .box {
        background: rgba(30,41,59,0.6);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 16px;
        width: 300px;
        margin: auto;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }

    input {
        width: 90%;
        padding: 10px;
        margin: 8px 0;
        border-radius: 8px;
        border: none;
        outline: none;
    }

    button {
        padding: 10px 20px;
        border: none;
        border-radius: 999px;
        background: linear-gradient(135deg, #38bdf8, #6366f1);
        color: white;
        cursor: pointer;
    }

    a {
        color: #38bdf8;
        display: inline-block;
        margin-top: 10px;
    }
</style>
"""

# ===============================
# ADD STUDENT
# ===============================
@app.route('/add_student_form')
def add_student_form():
    return form_style + """
    <div class="box">
        <h2>Add Student</h2>
        <form method='POST' action='/add_student'>
            <input name='name' placeholder='Name' required>
            <input type='number' name='grade' placeholder='Grade' required>
            <input name='section' placeholder='Section' required>
            <br><br>
            <button>Add</button>
        </form>
        <a href='/students'>Back</a>
    </div>
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

# ===============================
# DELETE
# ===============================
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

# ===============================
# EDIT
# ===============================
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    return render_template_string(form_style + """
    <div class="box">
        <h2>Edit Student</h2>
        <form method='POST'>
            <input name='name' value='{{student.name}}'>
            <input type='number' name='grade' value='{{student.grade}}'>
            <input name='section' value='{{student.section}}'>
            <br><br>
            <button>Update</button>
        </form>
        <a href='/students'>Back</a>
    </div>
    """, student=student)

# ===============================
# API
# ===============================
@app.route('/api/students')
def api_students():
    return jsonify(students)

# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    
    app.run(debug=True)
