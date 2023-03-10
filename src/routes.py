from src import application, db
from src.forms import AddQuestion, UpdateQuestion, AddOptions, UpdateOptions, AnswerQuestion, AddQuiz, SelectQuiz
from src.models import Questions, Options, Answer, Result, Quiz
from flask import render_template, request, redirect, url_for
from datetime import date

@application.route('/')
@application.route('/home')
def home():
    return render_template('home.html')

@application.route('/questions')
def questions():
    quizzes = Quiz.query.all()
    return render_template('questions.html', quizzes=quizzes)

@application.route('/question-<int:qid>')
def question(qid):
    question = Questions.query.filter_by(id=qid).first()
    maxid = Questions.query.order_by(Questions.id.desc()).first().id
    return render_template('question.html', question=question, maxid=maxid)

@application.route('/add-quiz', methods=['GET', 'POST'])
def add_quiz():
    form = AddQuiz()
    if request.method == 'POST':
        name = form.quiz_name.data
        quiz = Quiz(quiz_name = name)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('add_q'))
    return render_template('add_quiz.html', form=form)

@application.route('/add-question', methods=['GET','POST'])
def add_q():
    form = AddQuestion()
    quizzes = Quiz.query.all()
    for quiz in quizzes:
        form.quiz.choices.append((quiz.id, quiz.quiz_name))
    if request.method == 'POST':
        q_num = form.q_num.data
        q_name = form.q_name.data
        quiz_id = form.quiz.data
        newquest = Questions(num = q_num, question = q_name, quiz_id = quiz_id)
        db.session.add(newquest)
        db.session.commit()
        return redirect(url_for('add_o', qid=newquest.id))
    return render_template('add_question.html', form=form)

@application.route('/bounce/<int:qid>', methods=['GET'])
def bounce(qid):
    return redirect(url_for('add_o', qid=qid))

@application.route('/add-options/<int:qid>', methods=['GET','POST'])
def add_o(qid):
    form = AddOptions()
    if request.method == 'POST':
        o_letter = form.o_letter.data
        option = form.o_option.data
        o_status = form.o_status.data
        newopt = Options(optletter = o_letter, o_option = option, o_status = o_status, question_id = qid)
        db.session.add(newopt)
        db.session.commit()
        question = Questions.query.filter_by(id = qid).first()
        question.options = Options.query.filter_by(question_id = qid).all()
        db.session.commit()
        return redirect(url_for('bounce', qid=qid))
    return render_template('add_options.html', form=form)

@application.route('/update-question/<int:qid>', methods=['GET','POST'])
def update_q(qid):
    form = UpdateQuestion()
    if request.method == 'POST':
        q_name = form.q_name.data
        question = Questions.query.filter_by(id=qid).first()
        question.question = q_name
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('update_question.html', form=form)

@application.route('/update-options/<int:oid>', methods=['GET','POST'])
def update_o(oid):
    form = UpdateOptions()
    if request.method == 'POST':
        o_letter = form.o_letter.data
        option = form.o_option.data
        o_status = form.o_status.data
        opt = Options.query.filter_by(id=oid).first()
        qid = Questions.query.filter_by(id=opt.question_id).first().id
        opt.optletter = o_letter
        opt.o_option = option
        opt.o_status = o_status
        db.session.commit()
        return redirect(url_for('question', qid=qid))
    return render_template('update_options.html', form=form)

@application.route('/delete-option/<int:oid>')
def delete_o(oid):
    option = Options.query.filter_by(id=oid).first()
    qid = Questions.query.filter_by(id=option.question_id).first().id
    db.session.delete(option)
    db.session.commit()
    return redirect(url_for('question', qid=qid))

@application.route('/delete-question/<int:qid>')
def delete_q(qid):
    question = Questions.query.filter_by(id=qid).first()
    options = question.options
    db.session.delete(question)
    for option in options:
        db.session.delete(option)
    db.session.commit()
    return redirect(url_for('questions'))

@application.route('/choose-quiz', methods=['GET', 'POST'])
def select_quiz():
    form = SelectQuiz()
    for quiz in Quiz.query.all():
        form.q_id.choices.append((quiz.id, quiz.quiz_name))
    if request.method == 'POST':
        qid = form.q_id.data
        return redirect(url_for('answer_q', qid=qid, qnum=1))
    return render_template('select_quiz.html', form=form)

@application.route('/answer-<int:qid>/<int:qnum>', methods=['GET','POST'])
def answer_q(qid, qnum):
    form = AnswerQuestion()
    question = Questions.query.filter_by(quiz_id=qid, num=qnum).first()
    options = question.options
    for option in options:
        form.sel_opt.choices.append((option.id, option.o_option))
    if request.method == 'POST':
        ans_opt = form.sel_opt.data
        ans = Options.query.filter_by(id = ans_opt).first()
        newans = Answer(name = ans.__str__(), status = ans.o_status)
        db.session.add(newans)
        db.session.commit()
        if qnum == Questions.query.filter_by(quiz_id=qid).order_by(Questions.num.desc()).first().num:
            return redirect(url_for('show_results'))
        else:
            return redirect(url_for('answer_q', qid=qid, qnum=qnum + 1))
    return render_template('answer-question.html', form=form, question=question, options=options)

@application.route('/results')
def show_results():
    answers = Answer.query.all()
    score = Answer.query.filter_by(status='correct').count()
    maxscore = Answer.query.count()
    return render_template('results.html', answers=answers, score=score, maxscore=maxscore)

@application.route('/reset')
def housekeeping():
    score = Answer.query.filter_by(status='correct').count()
    newresult = Result(score = score, date = date.today())
    db.session.add(newresult)
    db.session.commit()
    answers = Answer.query.all()
    for answer in answers:
        db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('home'))
