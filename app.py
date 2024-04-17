from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

#Setting some names and constants

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    '''Choose a survey'''

    return render_template("survey_start.html", survey=survey)

@app.route("/begin", methods=[POST])
def start_survey():
    '''Clear session of responses'''

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question"""

    choice = request.form['answer']

    #add response to session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")
    

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Show current question"""
    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        #Trying to skip question
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        #Answered all questions
        return redirect("/complete")
    
    if (len(responses) !=qid):
        #Trying to answer questions out of order
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question
    )

@app.route("/complete")
def complete():
    """Survey complete. Show completion page"""

    return render_template("completion.html")
