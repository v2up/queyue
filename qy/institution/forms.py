from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, FileField, SelectField, DateTimeField, FloatField, PasswordField
from wtforms.validators import Required, Length, EqualTo
from wtforms.widgets import HiddenInput

from datetime import datetime, date, timedelta

class InstiForm(Form):
    name = StringField('机构名称', validators=[Length(1, 128, '请输入机构名称（不长于128个字符）')])
    logo = FileField('上传机构LOGO')
    poster = FileField('上传一张海报')
    intro = TextAreaField('简单介绍')
    save = SubmitField('确认更新')

class NotiForm(Form):
    content = TextAreaField('发布通知', validators=[Required()])
    publish = SubmitField('发布')

class EventForm(Form):
    name = StringField('活动名称', validators=[Required('请输入活动名称'), Length(1, 32, '最长32个字符')])
    category = SelectField('活动类型', coerce=int, validators=[Required('必须指定类型')])
    start_time = DateTimeField('开始时间', format='%Y-%m-%d %H:%M', validators=[Required('请指定活动的开始时间')])
    end_time = DateTimeField('结束时间', format='%Y-%m-%d %H:%M', validators=[Required('指定活动的结束时间')])
    longitude = FloatField('经度', widget=HiddenInput(), validators=[Required('选择活动地点')])
    latitude = FloatField('纬度', widget=HiddenInput(), validators=[Required('选择活动地点')])
    address = StringField('地址', validators=[Required(), Length(1, 256)], render_kw={"placeholder": "在地图中标记地点后，只需填写具体的地点"})
    detail = TextAreaField('活动详情', validators=[Required('活动详情必填')], render_kw={"placeholder": "详细地描述这个活动"})
    new = SubmitField('确 认 并 发 布')

class SecurityForm(Form):
    current_password = PasswordField('当前密码', validators=[Required('必填项')])
    new_password = PasswordField('新密码', validators=[Required('请输入新密码'), Length(6, 24, '密码长度 6-24 位')])
    new_password2 = PasswordField('确认新密码', validators=[EqualTo('new_password', '两次密码不匹配')])
    submit = SubmitField('确认更改')

class EditForm(Form):
    detail = TextAreaField('活动描述')
    poster = FileField('上传/更新活动海报')
    save = SubmitField('确认并提交')