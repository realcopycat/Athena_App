"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, url_for
from athena_App import app
from athena_App.formClass import QuestionForm
#from athena_App.data_process.keywordCompare import Keyword_Compare, Answer
#from athena_App.data_process.word2vecCompareModel import *
import time
from athena_App.data_process.es_QAsearch import *


@app.route('/home', methods=['POST','GET'])
def home():
    """Renders the home page."""
    question = ''
    form = QuestionForm()
    question = form.question.data
    if form.validate_on_submit():
        return redirect(url_for('answer',word=question))
    return render_template(
        'index.html',
        title = 'Index Page',
        year = datetime.now().year,
        form =  form,
        question = question
        )

@app.route('/instruction')
def instruction():
    """Renders the instruction page."""
    return render_template(
        'instruction.html',
        title='说明',
        year=datetime.now().year,
        message='Instruction'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/answer/<word>')
def answer(word):
    """Renders the answer page"""
    print(word)
    start=time.clock()
    finder=answerFinder()
    answer=finder.main(word)
    end=time.clock()
    print(str(end-start))
    return render_template(
        'answer.html',
        title='Answer',
        answer=answer
        )

@app.route('/main')
@app.route('/')
def main():
    return render_template(
        'newMain.html',
        title = 'Welcome Page',
        year = datetime.now().year
        )