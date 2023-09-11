from flask import Blueprint, render_template, flash, request, redirect,url_for, session
from flask_login import login_required, current_user
from . import db
from website.models import Test, Intrebari, Raspunsuri, Penalisation
from website.models import User
from sqlalchemy import desc
import random
# from datetime import datetime, time

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():

    print(current_user.last_test)

    return render_template('home.html', user = current_user)

@views.route('/team', methods = ['GET', 'POST'])
@login_required
def team():

    echipe= Penalisation.query.filter_by(id=current_user.id).all()

    clasament = get_clasament()
    test = Test.query.filter_by(status='activ').first()
    if not test:
        return render_template('team.html', user = current_user, echipe=echipe, clasament = clasament)
    else:
        session['error'] = 'Punctajele nu sunt actualizate. Vă rugăm aşteptaţi!'
        return redirect(url_for('views.error'))


@views.route('/ranking', methods = ['GET', 'POST'])
@login_required
def ranking():

    clasament = get_clasament()
    echipe = Penalisation.query.filter_by(id=current_user.id).all()
    return render_template('ranking.html', user = current_user,clasament = clasament, echipe=echipe)


@views.route('/check_quiz', methods=['GET', 'POST'])
@login_required
def check_quiz():

    test = Test.query.filter_by(status = 'activ').first()
    if test:
        tip_test = test.tip
    else:
        tip_test = "null"

    if tip_test != "null":
        if current_user.last_test == "A" + test.tip:
            return redirect(url_for("views.quiz"))

    return render_template("check_quiz.html", tip_test = tip_test, user = current_user, durata = 15)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():

    test = Test.query.filter_by(status = 'activ').first()
    if not test:
       return redirect(url_for('views.check_quiz'))

    if current_user.last_test == test.tip:
        session['error'] = 'Ai dat deja acest test'
        return redirect(url_for('views.error'))
    else:
        current_user.change_last_test("A" + test.tip)
        db.session.commit()

    
    durata = test.durata 

    if 'questions' not in session:
        questions = random.sample(test.intrebari, k=10)
        questions_id = []
        for q in questions:
            questions_id.append(q.id)
        session['questions'] = questions_id
    
    questions = []
    for q in session['questions']:
        questions.append(Intrebari.query.filter_by(id = q).first())

    # for i, q in enumerate(questions):
    #     print(i, q.raspunsuri[0].raspuns1)
    #     print(i, q.raspunsuri[0].raspuns2)
    #     print(i, q.raspunsuri[0].raspuns3)
    #     print(i, q.raspunsuri[0].raspuns4)
    #     print(i, q.raspuns_corect)
    #     print("**********************")

    if request.method == "POST":
        current_user.change_last_test = test.tip
        answer_q1 = request.form.get(questions[0].intrebare)
        answer_q2 = request.form.get(questions[1].intrebare)
        answer_q3 = request.form.get(questions[2].intrebare)
        answer_q4 = request.form.get(questions[3].intrebare)
        answer_q5 = request.form.get(questions[4].intrebare)
        answer_q6 = request.form.get(questions[5].intrebare)
        answer_q7 = request.form.get(questions[6].intrebare)
        answer_q8 = request.form.get(questions[7].intrebare)
        answer_q9 = request.form.get(questions[8].intrebare)
        answer_q10 = request.form.get(questions[9].intrebare)

        points = 0

        # print(answer_q1)
        # print(answer_q2)
        # print(answer_q3)
        # print(answer_q4)
        # print(answer_q5)
        # print(answer_q6)
        # print(answer_q7)
        # print(answer_q8)
        # print(answer_q9)
        # print(answer_q10)


        if answer_q1 == questions[0].raspuns_corect:
            points += 10
        if answer_q2 == questions[1].raspuns_corect:          
            points += 10
        if answer_q3 == questions[2].raspuns_corect:       
            points += 10
        if answer_q4 == questions[3].raspuns_corect:
             points += 10
        if answer_q5 == questions[4].raspuns_corect:
            points += 10
        if answer_q6 == questions[5].raspuns_corect:
            points += 10
        if answer_q7 == questions[6].raspuns_corect:          
            points += 10
        if answer_q8 == questions[7].raspuns_corect:       
            points += 10
        if answer_q9 == questions[8].raspuns_corect:
             points += 10
        if answer_q10 == questions[9].raspuns_corect:
            points += 10

        session['points'] = points

        current_user.change_points(current_user.punctaj + points)
        db.session.commit()
        return redirect(url_for('views.results'))
    return render_template('quiz.html', user = current_user, questions = questions, durata = durata, da = "Salut cf")


@views.route('/results', methods = ['GET', 'POST'])
@login_required
def results():

    test = Test.query.filter_by(status = 'activ').first()
    if not test:
       return redirect(url_for('views.check_quiz'))

    if test.tip != current_user.last_test:
        current_user.change_last_test(test.tip)
        db.session.commit()

    if 'questions' in session and 'points' in session:
        questions_id = session['questions']
        questions = []
        for q_id in questions_id:
            new_question = Intrebari.query.filter_by(id = q_id).first()
            questions.append(new_question)
        points = session['points']

    else:
        return redirect(url_for('views.home'))
    return render_template('results.html', user = current_user, questions = questions, points = points)



@views.route('/error', methods = ['GET', 'POST'])
def error():

    if 'error' in session:
        error = session['error']
    else:
        error = "UUPS"

    return render_template('error.html', user = current_user, error = error)


# def cine_alege():
#
#     alege = User.query.filter_by(level = 'team').filter_by(config = 'no',frame= 'no').order_by(desc(User.punctaj)).first()
#
#     return alege.id

def get_clasament():
        
    clasament = User.query.filter_by(level = 'team').order_by(desc(User.punctaj)).all()

    return clasament



