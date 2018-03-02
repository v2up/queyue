from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, EqualTo, Length, Email
from wtforms.validators import ValidationError


# 用于个人用户
class RegisterForm(Form):
    email_addr = StringField('电子邮箱', validators=[Required('请输入电子邮箱'), Length(1 ,64, '最长 64 位'), 
            Email('请检查电子邮箱的格式是否正确')])	#不能使用email而用email_addr，因为和系统关键字重名
    username = StringField('名号', validators=[Required('请输入名号'), Length(1, 64, '最长 64 位')])
    password = PasswordField('密码', validators=[Required('请输入密码'), Length(6, 24, '密码长度 6-24 位')])
    password2 = PasswordField('确认密码', validators=[EqualTo('password', '两次密码不匹配')])	#EqualTo包含Required，参数是字符串类型
    accept_agreement = BooleanField('已阅读并同意<a href="http://qq.com" target="_blank">《雀跃用户账户协议》</a>')	#这种方法不优雅

    submit = SubmitField('提交注册')

    def validate_accept_agreement(form, field):	#『不是』必填，而是必须返回True
        if field.data != True:
        	raise ValidationError('请阅读并同意网站协议')

class LoginForm(Form):
    email_addr = StringField('电子邮箱', validators=[Required('请输入登录邮箱'), Email('请检查电子邮箱的格式是否正确')])
    password = PasswordField('密码', validators=[Required('请输入密码')])
    remember_me = BooleanField('记住登录状态')

    submit = SubmitField('登录')


# 用来给高校机构的
class SignupForm(Form):
    certi_body = StringField('认证主体', validators=[Required('必填项')])
    certi_ucode = StringField('机构资质编号', validators=[Required('必填项')])
    certi_agent = StringField('认证代理人', validators=[Required('必填项')])
    uurl = StringField('机构名称（将用于主页域名和登录ID）', validators=[Required('必填项')])
    password = PasswordField('密码', validators=[Required('请输入密码'), Length(6, 24, '密码长度 6-24 位')])
    password2 = PasswordField('确认密码', validators=[EqualTo('password', '两次密码不匹配')])

    submit = SubmitField('提交')

class SigninForm(Form):
    uurl = StringField('登录ID', validators=[Required('必填项')])
    password = PasswordField('密码', validators=[Required('请输入密码')])

    submit = SubmitField('进入')