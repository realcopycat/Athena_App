"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, url_for, request, jsonify
from athena_App import app
from athena_App.formClass import QuestionForm

import time

#attention:
#this module include large word vector which need a lot of time to load
#turn it off when when you debugging other module
#
#from athena_App.data_process.es_QAsearch import *
#

#from athena_App.data_process.keywordCompare import Keyword_Compare, Answer
#from athena_App.data_process.word2vecCompareModel import *

#from athena_App.data_process.graph_query import *

#from athena_App.openlaw.graphOfcase_query_echart import *

#reconstruct series

from athena_App.layer_frontInteracting.qa_module import answerFinder
from athena_App.layer_frontInteracting.kg_module import knowledgeSearch
from athena_App.layer_frontInteracting.case_module import caseQuery


@app.route('/QAsearch', methods=['POST','GET'])
def QAsearch():
    """Renders the QAsearch page."""
    question = ''
    form = QuestionForm()
    question = form.question.data
    if form.validate_on_submit():
        return redirect(url_for('answer',word=question))
    return render_template(
        'QAsearch.html',
        title = 'QAsearch Page',
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
    answer=finder.findANDpack(word)
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

@app.route('/graph_search',methods=['get','post'])
def graph_search():
    return render_template(
        'graph_search.html',
        title = 'Graph search page',
        year = datetime.now().year)

@app.route('/knowledge_search',methods=['get','post'])
def knowledge_search():

    #initialize graph search object
    searchKnowledge=knowledgeSearch()

    des=request.args.get('description')
    json_data=searchKnowledge.getTotalData_forKnowledgeSearch(des)
    print(json_data)

    return jsonify(json_data)

@app.route('/case_search_Test',methods=['get','post'])
def case_search_Test():
    return render_template(
        'case_search_Test.html',
        title = 'Case search page',
        year = datetime.now().year)

@app.route('/case_graph_search',methods=['get','post'])
def case_graph_search():

    caseDes=request.args.get('caseDes')
    #initialize graph search object
    case_graph_result=caseQuery(caseDes)

    pre_json_data=case_graph_result.getData()
    print(pre_json_data)

    return jsonify(pre_json_data)

@app.route('/knife',methods=['get','post'])
def knife():
    return render_template(
        'knife.html',
        title = 'KNIFE SEARCH',
        year = datetime.now().year
        )

@app.route('/searchAll',methods=['get','post'])
def searchAll():
    pass