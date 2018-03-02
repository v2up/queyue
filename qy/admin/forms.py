from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, EqualTo, Length

class RegForm(Form):
    eno = StringField('工号', validators=[Required('必填项')])
    password = PasswordField('密码', validators=[Required('请输入密码'), Length(6, 24, '密码长度 6-24 位')])
    password2 = PasswordField('确认密码', validators=[EqualTo('password', '两次密码不匹配')])
    submit = SubmitField('确认并注册')

class LoginForm(Form):
    eno = StringField('工号', validators=[Required('必填项')])
    password = PasswordField('密码', validators=[Required('请输入密码')])
    submit = SubmitField('进入')

class CertiForm(Form):
    body = StringField('认证主体', validators=[Required('必填')])
    function = TextAreaField('机构职能', validators=[Required('必填')])
    description = TextAreaField('描述')
    website = StringField('官方网站')
    address = TextAreaField('地址', validators=[Required('必填')])
    phone = StringField('服务电话')
    agent_id = StringField('代理人（身份证号）', validators=[Required('必填')])
    input = SubmitField('录入')

class CateForm(Form):
    name = StringField('添加新类型', validators=[Length(1, 32, '')])
    add = SubmitField('添加')

class AdminForm(Form):
    current_password = PasswordField('当前密码', validators=[Required('必填项')])
    new_password = PasswordField('新密码', validators=[Required('请输入新密码'), Length(6, 24, '密码长度 6-24 位')])
    new_password2 = PasswordField('确认新密码', validators=[EqualTo('new_password', '两次密码不匹配')])
    submit = SubmitField('确认更改')