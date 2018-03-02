from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required, Length

class TwitterForm(Form):
    content = TextAreaField('你在做什么/有什么想法？', validators=[Length(1, 140, '字数限定在 1-140 之间')])	#Required('输入你的想法'), 
    
    post = SubmitField('发布')