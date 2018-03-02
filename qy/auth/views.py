from . import auth
from .. import db
from .forms import RegisterForm, LoginForm, SignupForm, SigninForm
from ..models import User, Certification, Institution
from ..email import send_confirm_mail

from flask import render_template, redirect, request, url_for, flash, make_response, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeSerializer

from datetime import datetime, timedelta

@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == 'POST' and register_form.validate_on_submit():
        user = User(email=register_form.email_addr.data, name=register_form.username.data, password=register_form.password.data)
        if User.query.filter_by(email=user.email).first():
            flash('该邮箱已被注册', 'alert-danger')
            return render_template('auth/register.html', form=register_form)
        else:
            db.session.add(user)    #添加到数据库会话
            db.session.commit()
            # token = user.generate_confirmation_token()
            # send_confirm_mail(user.email, '确认您的账户', 'email/confirmation', token=token) #to, subject, template, **kwargs
            flash('已向您的邮箱发送一封确认邮件，请注意查收', 'alert-info')
            return redirect(url_for('auth.login'))	#蓝本.视图函数
    return render_template('auth/register.html', form=register_form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email_addr.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data) #登录使用Flask-Login来协助
            return redirect(request.args.get('next') or url_for('main.index'))  #request.args.get('next')是原地址，由Flask-Login存入
        else:
            flash('登录邮箱或者密码不正确', 'alert-danger')
    return render_template('auth/login.html', form=login_form)

@auth.route('/logout')
@login_required # 要求登录
def logout():
    logout_user()
    flash('您已成功登出', 'alert-success')
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('您已经确认过了', 'alert-info')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('确认成功。谢谢！', 'alert-success')
    else:
        flash('无法确认。可能是确认时间过期了')
    return redirect(url_for('main.index'))

def query_certi_id(body, ucode, agent): #认证为合法返回认证ID，否则返回None
    certi = Certification.query.filter_by(ucode=ucode).first()
    if certi is not None:   #是否存在
        if certi.body==body and certi.agent_id==agent:  #是否对上号
            if certi.is_available():    #有没有过期
                if Institution.query.filter_by(certi_id=certi.id).first() is None:  #有没有被使用
                    return certi.id
    return None

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    signup_form = SignupForm()
    if request.method == 'POST' and signup_form.validate_on_submit():
        certi_id = query_certi_id(signup_form.certi_body.data, signup_form.certi_ucode.data, signup_form.certi_agent.data)
        if certi_id is not None:
            insti = Institution.query.filter_by(uurl=signup_form.uurl.data).first()
            if insti is None:
                insti = Institution(certi_id=certi_id, uurl=signup_form.uurl.data, password=signup_form.password.data)
                db.session.add(insti)
                flash('机构账户成功激活了。登录后请完善账户信息。', 'alert-success')
                return redirect(url_for('.signin'))
            else:
                flash('名称被占用了', 'alert-danger')
        else:
            flash('认证信息不可用', 'alert-danger')

    return render_template('auth/signup.html', form=signup_form)

@auth.route('/signin', methods=['POST', 'GET'])
def signin():
    signin_form = SigninForm()
    if request.method=='POST' and signin_form.validate_on_submit():
        insti = Institution.query.filter_by(uurl=signin_form.uurl.data).first()
        if insti is not None:
            if insti.verify_password(signin_form.password.data):
                flash('欢迎你，' ,'alert-success')
                # “记住”登录状态
                resp = make_response(redirect(url_for('institution.panel', uurl=insti.uurl)))
                s = URLSafeSerializer(current_app.config['SECRET_KEY'])
                resp.set_cookie('insti-uurl', s.dumps(insti.uurl), expires=datetime.now()+timedelta(days=1))  # 24小时有效期
                return resp
            else:
                flash('密码不正确', 'alert-danger')
        else:
            flash('不存在的登录ID', 'alert-danger')

    return render_template('auth/signin.html', form=signin_form)

@auth.route('/signout')
def signout():
    resp = make_response(redirect(url_for('.signin')))
    resp.set_cookie('insti-uurl', '', expires=0)
    flash('退出成功', 'alert-success')
    return resp