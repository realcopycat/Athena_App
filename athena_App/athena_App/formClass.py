from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class QuestionForm(Form):
    question = StringField('请告诉我你的疑问？', validators=[Required()])
    submit = SubmitField('submit')
