from . import admin
from .forms import RegForm, LoginForm, CertiForm, CateForm, AdminForm
from ..models import Admin, Certification, Category
from .. import db

from flask import render_template, request, flash, redirect, url_for, json, current_app, make_response
from itsdangerous import URLSafeSerializer

from threading import Thread
from datetime import datetime, timedelta

import requests as reqs

@admin.route('/')
def index():
    return redirect(url_for('.certi'))

# @admin.route('/', methods=['POST', 'GET'])
@admin.route('/certification', methods=['POST', 'GET'])
def certi():
    page = request.args.get('p', 1, type=int)
    cur_admin = current_admin()
    certi_form = CertiForm()
    if request.method=='POST' and certi_form.input.data and certi_form.validate_on_submit():
        certi = Certification.query.filter_by(body=certi_form.body.data).first()
        if certi is None:
            certi = Certification(body=certi_form.body.data, function=certi_form.function.data, 
                description=certi_form.description.data, website=certi_form.website.data, address=certi_form.address.data, 
                phone=certi_form.phone.data, agent_id=certi_form.agent_id.data, inputer_id=cur_admin.id)
            db.session.add(certi)
            flash('录入成功', 'alert-success')
            return redirect(url_for('.index'))
        else:
            flash('已存在的认证主体', 'alert-danger')
    pagination = Certification.query.order_by(Certification.certi_date.desc()).paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])
    certis = pagination.items
    return render_template('admin/certi.html', current_admin=cur_admin, certi_form=certi_form, certis=certis, pagination=pagination)

@admin.route('/delete-certi/<int:id>')
def delete_certi(id):
    try:
        certi = Certification.query.get_or_404(int(id))
        db.session.delete(certi)
        flash('删除成功', 'alert-success')
    except:
        flash('出错了，删除失败', 'alert-danger')
        pass
    return redirect(url_for('.certi'))

@admin.route('/extend/<cid>')
def extend(cid):
    try:
        certi = Certification.query.get_or_404(int(cid))
        certi.expiry_date = certi.expiry_date+timedelta(days=365)
        db.session.add(certi)
        flash('续期成功', 'alert-success')
        print('hello')
    except Exception as e:
        print(str(e))
        flash('续期失败……', 'alert-danger')
    return redirect(url_for('.certi'))

@admin.route('/category', methods=['POST', 'GET'])
def cate():
    cate_form = CateForm()
    if request.method=='POST' and cate_form.add.data and cate_form.validate_on_submit():
        if not (cate_form.name.data is None or cate_form.name.data==''):
            cate = Category.query.filter_by(name=cate_form.name.data).first()
            if cate is None:
                cate = Category(name=cate_form.name.data)
                db.session.add(cate)
                flash('添加成功', 'alert-success')
            else:
                flash('该类型已存在', 'alert-danger')
        else:
            flash('未输入类型名')
        tab_eq = 1
    cates = Category.query.all()
    return render_template('admin/cate.html', current_admin=current_admin(), cate_form=cate_form, cates=cates)

@admin.route('/misc', methods=['POST', 'GET'])
def misc():
    return render_template('admin/misc.html', current_admin=current_admin())

@admin.route('/settings', methods=['POST', 'GET'])
def settings():
    admin_form = AdminForm()
    if request.method=='POST' and admin_form.submit.data and admin_form.validate_on_submit():
        admin = current_admin()
        if admin.verify_password(admin_form.current_password.data):
            admin.password = admin_form.new_password.data
            db.session.add(admin)
            flash('修改成功', 'alert-success')
        else:
            flash('密码错误，修改失败', 'alert-danger')
    return render_template('admin/settings.html', current_admin=current_admin(), admin_form=admin_form)

@admin.route('/delete-category/<int:cid>')
def delete_category(cid):
    if cid is not None:
        try :
            cate = Category.query.get(int(cid))
        except:
            pass
        if cate is not None:
            db.session.delete(cate)
            flash('删除成功', 'alert-success')
    return redirect(url_for('.index', current_admin=current_admin(), tab_eq=1))

@admin.route('/reg', methods=['GET', 'POST'])
def reg():
    reg_form = RegForm()
    if request.method == 'POST' and reg_form.validate_on_submit():
        admin = Admin.query.filter_by(eno=reg_form.eno.data).first()
        if admin is None:
            admin = Admin(eno=reg_form.eno.data, password=reg_form.password.data)
            db.session.add(admin)
            flash('注册成功，可以登录了。', 'alert-success')
            return redirect(url_for('admin.login'))
        else:
            flash('该工号注册过了', 'alert-danger')

    return render_template('admin/reg.html', current_admin=current_admin(), form=reg_form)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        admin = Admin.query.filter_by(eno=login_form.eno.data).first()
        if admin is not None:
            if admin.verify_password(login_form.password.data):
                flash('欢迎回来', 'alert-success')
                # “记住”登录状态
                resp = make_response(redirect(url_for('.index')))
                s = URLSafeSerializer(current_app.config['SECRET_KEY'])
                resp.set_cookie('admin-eno', s.dumps(admin.eno), expires=datetime.now()+timedelta(days=1))  # 24小时有效期
                return resp
            else:
                flash('密码错误', 'alert-danger')
        else:
            flash('不存在的账号', 'alert-danger')

    return render_template('admin/login.html', form=login_form)

@admin.route('/logout')
def logout():
    resp = make_response(redirect(url_for('.login')))
    resp.set_cookie('admin-eno', '', expires=0)
    flash('退出成功', 'alert-success')
    return resp

def current_admin():
    admin_eno = request.cookies.get('admin-eno')
    if admin_eno:
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        eno = s.loads(admin_eno)
        return Admin.query.filter_by(eno=eno).first()
    return None

# def analyze_and_store(app_context, district_list, index, start_index, end_index, parent_id=None):
#     with app_context:
#         for d in district_list[index]:
#             id = d['id']
#             print(id)
#             name = d.get('name', None)
#             fullname = d['fullname']
#             py = d.get('pinyin', None)
#             pinyin = None
#             if py is not None:
#                 pinyin = ''
#                 for w in py:
#                     pinyin = pinyin + w.title()
#             longitude = d['location']['lat']
#             latitude = d['location']['lng']

#             district = District.query.filter_by(add_code=id).first()
#             if district is None:
#                 district = District(add_code=id, name=name, fullname=fullname, pinyin=pinyin, 
#                     longitude=longitude, latitude=latitude, parent_id=parent_id)
#             else:
#                 district.name = name
#                 district.fullname = fullname
#                 district.pinyin = pinyin
#                 district.longitude = longitude
#                 district.latitude = latitude
#                 district.parent_id = parent_id
#             db.session.add(district)

#             cidx = d.get('cidx', None)
#             if cidx is not None:
#                 analyze_and_store(app_context, district_list, index+1, cidx[0], cidx[1], parent_id=district.id)

# @admin.route('/update-district')
# def update_district():
#     # 获得WebService API返回的内容
#     app = current_app._get_current_object()
#     app_config = app.config
#     params = {'key': app_config['TCMAP_KEY']}
#     resp = reqs.get('http://apis.map.qq.com/ws/district/v1/list', params)
#     try:
#         content = resp.json()
#     except:
#         pass    #简化步骤，不处理
#     else:
#         # 下面开始分析和存储
#         if content['status']==0:
#             districts = content['result']   # three arrays
#             try:
#                 thr = Thread(target=analyze_and_store, args=[app.app_context(), districts, 0, 0, len(districts[0])-1])
#                 thr.start()
#             except:
#                 pass
#             else:
#                 flash('更新成功，最新的日期版本为 %r' % content['data_version'], 'alert-success')
#                 return redirect(url_for('admin.index'))
#     # 没成功时走这一步
#     flash('遇到了一些异常，更新失败。', 'alert-danger')
#     return redirect(url_for('admin.index'))