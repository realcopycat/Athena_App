from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class QuestionForm(Form):
    question = StringField('你的疑问是...', validators=[Required()])
    submit = SubmitField('搜索')
