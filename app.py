from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey 

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY']="catsarecool1234"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = "response"

@app.route('/')
def show_survey_title():
    """Shows user survey titles available to seleft"""
    return render_template("home.html", satisfaction_survey=satisfaction_survey)

@app.route('/start', methods=['Post'])
def start_survey():
    session[RESPONSES] = [] 
    return redirect('/questions/0')


@app.route('/questions/<int:question_id>')
def show_questions (question_id):
    """Shows users survey questions to select"""
    if (len(RESPONSES) != question_id):
        responses = session.get(RESPONSES)

    if (RESPONSES is None):
        return redirect ('/')
    
             
    if (len(RESPONSES) == len(satisfaction_survey.questions)):       
        return redirect("/complete")
    if (len(RESPONSES) != question_id):
        flash("Please answer questions in order.")
        return redirect(f"/questions/{len(RESPONSES)}")
    else:
        return render_template("questions.html",question=satisfaction_survey.questions[question_id])





@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    response=session[RESPONSES]
    response.append(choice) 
    session[RESPONSES] = response
    return redirect(f"/questions/{len(RESPONSES)}")


@app.route("/complete")
def show_completed():
    return render_template("thanks.html")

## Review adding methods=["POST"] to the /answer route









