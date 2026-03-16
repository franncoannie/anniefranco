from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/student')
def student():
    grade = int(request.args.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"

    return jsonify({
        "name": "Annie Franco",
        "grade": grade,
        "section": "BSIT",
        "remarks": remarks
    })

@app.route('/result')
def result():
    grade = int(request.args.get('grade', 0))
    remarks = "Pass" if grade >= 75 else "Fail"

    return render_template("result.html", grade=grade, remarks=remarks)

if __name__ == '__main__':
    app.run(debug=True)
