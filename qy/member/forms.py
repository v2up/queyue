from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, FileField, PasswordField
from wtforms.validators import Required, Length, EqualTo

class EditForm(Form):
    username = StringField('名号', validators=[Required('请输入名号'), Length(1, 64, '最长 64 位')])
    avatar = FileField('上传头像（建议尺寸120px*120px）')
    portrait = FileField('上传半身像（建议尺寸240px*360px）')
    signature = StringField('个人签名', validators=[Length(0, 30, '最长 30 个字符')])
    intro = TextAreaField('简单的自我介绍')
    old_password = PasswordField('当前密码（修改密码时必填）')
    password = PasswordField('新密码（修改密码时必填）')
    password2 = PasswordField('确认新密码（修改密码时必填）', validators=[EqualTo('password', '两次新密码不一致')])
    save = SubmitField('确认更新')