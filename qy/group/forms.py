from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Required, Length
from flask.ext.wtf.file import FileField, FileAllowed	#, FileRequired

class GroupForm(Form):
    name = StringField('小组名称', validators=[Required('必填项'), Length(1, 24, '名称最长24个字符')])
    icon = FileField('小组图标（建议尺寸120px*120px，只限jpg和png格式）', 
    	validators=[Required('小组图标必须有'), FileAllowed(['jpg', 'png'], '只限jpg和png格式')])
    intro = TextAreaField('介绍', validators=[Required('说说这个小组的事儿嘛')])
    save = SubmitField('确认')

class TopicForm(Form):
    title = StringField('标题', validators=[Required('标题必填'), Length(1, 128, '标题太长了 :(')])
    description = TextAreaField('详细描述（可不填）')
    post= SubmitField('发布')

class DiscuForm(Form):
    content = TextAreaField('也说点儿什么吧……', validators=[Required('还没填写呢')])
    reply = SubmitField('回复')