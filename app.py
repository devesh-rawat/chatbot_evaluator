from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

evaluations = []  # Store evaluation records

# Sample questions for different domains
domain_questions = {
    "Computer Science": {
        "Java": [
            {"question": "What is JVM?", "answer": "Java Virtual Machine"},
            {"question": "Explain OOP concepts in Java.", "answer": "Encapsulation, Inheritance, Polymorphism, Abstraction"}
        ],
        "Python": [
            {"question": "What is a Python dictionary?", "answer": "A collection of key-value pairs."},
            {"question": "Explain list vs tuple.", "answer": "Lists are mutable, tuples are immutable."}
        ]
    },
    "Mathematics": {
        "Algebra": [
            {"question": "Solve for x: 2x + 3 = 7", "answer": "x = 2"},
            {"question": "What is the quadratic formula?", "answer": "x = (-b ± sqrt(b^2 - 4ac)) / 2a"}
        ]
    }
}

@app.route("/")
def front_page():
    return render_template("indexcopy.html") 

@app.route("/aichatbot")
def chatbot():
    return render_template("mAI.html") 

@app.route("/evaluation")
def evaluation_page():
    return render_template("index.html") 

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    domain = data.get("domain")
    subject = data.get("subject")
    
    if domain in domain_questions and subject in domain_questions[domain]:
        questions = domain_questions[domain][subject]
        return jsonify({"message": "Answer the following questions:", "questions": questions})
    else:
        return jsonify({"error": "Domain or subject not found."})

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    domain = data.get("domain")
    subject = data.get("subject")
    user = data.get("user")  # Store user identity
    answers = data.get("answers")
    
    if domain not in domain_questions or subject not in domain_questions[domain]:
        return jsonify({"error": "Domain or subject not found."})
    
    correct_answers = domain_questions[domain][subject]
    score = 0
    
    for i, qa in enumerate(correct_answers):
        if i < len(answers) and answers[i].strip().lower() == qa["answer"].strip().lower():
            score += 1
    
    evaluation_record = {"user": user, "domain": domain, "subject": subject, "score": f"{score}/{len(correct_answers)}"}
    evaluations.append(evaluation_record)
    
    return jsonify({"message": "Evaluation complete", "score": evaluation_record["score"]})

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True)
