from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- Question Bank ----------------
skill_questions = {
    "ML": [
        {"type": "one", "q": "Algorithm used for classification?", "ans": "svm"},
        {"type": "mcq", "q": "Which is supervised learning?",
         "options": ["K-means", "Linear Regression", "Apriori", "PCA"],
         "ans": "linear regression"}
    ],
    "DL": [
        {"type": "one", "q": "Basic unit of neural network?", "ans": "neuron"},
        {"type": "mcq", "q": "Which activation function is common?",
         "options": ["Sigmoid", "ReLU", "Tanh", "Softmax"],
         "ans": "relu"}
    ],
    "Data Analytics": [
        {"type": "one", "q": "Removing errors from data is called?", "ans": "cleaning"},
        {"type": "mcq", "q": "Tool used for visualization?",
         "options": ["Excel", "PowerBI", "Tableau", "All"],
         "ans": "all"}
    ],
    "Python": [
        {"type": "one", "q": "Keyword to define function?", "ans": "def"},
        {"type": "mcq", "q": "Which data type is mutable?",
         "options": ["Tuple", "String", "List", "Integer"],
         "ans": "list"}
    ],
    "HTML": [
        {"type": "one", "q": "Root tag of HTML?", "ans": "html"},
        {"type": "mcq", "q": "Tag used for hyperlink?",
         "options": ["<img>", "<a>", "<p>", "<h1>"],
         "ans": "<a>"}
    ]
}

selected_questions = []
selected_skills = []
score = 0
student_name = ""

# ---------------- APIs ----------------

@app.route("/select-skills", methods=["POST"])
def select_skills():
    global selected_questions, score, selected_skills, student_name
    score = 0
    selected_questions = []

    data = request.json
    selected_skills = data["skills"]
    student_name = data["name"]

    for s in selected_skills:
        selected_questions.extend(skill_questions[s])

    return jsonify({"total": len(selected_questions)})

@app.route("/get-question/<int:i>")
def get_question(i):
    if i < len(selected_questions):
        return jsonify(selected_questions[i])
    return jsonify({"done": True})

@app.route("/evaluate/<int:i>", methods=["POST"])
def evaluate(i):
    global score
    user_answer = request.json["answer"].strip().lower()
    correct = selected_questions[i]["ans"]

    if user_answer == correct:
        score += 1

    return jsonify({"next": i + 1 < len(selected_questions)})

@app.route("/final-result")
def final_result():
    total = len(selected_questions)
    percent = (score / total) * 100

    # ---- Job Role Logic ----
    if "ML" in selected_skills and "DL" in selected_skills and percent >= 70:
        role = "Machine Learning Engineer"
    elif "Data Analytics" in selected_skills and percent >= 60:
        role = "Data Analyst"
    elif "Python" in selected_skills and "HTML" in selected_skills:
        role = "Junior Web Developer"
    else:
        role = "Trainee / Intern"

    advice = (
        "Strong fundamentals. Start applying for internships."
        if percent >= 70 else
        "Practice basics and revise core concepts before interviews."
    )

    return jsonify({
        "name": student_name,
        "score": round(percent, 2),
        "role": role,
        "advice": advice
    })

if __name__ == "__main__":
    app.run(debug=True)
