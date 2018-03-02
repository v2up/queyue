from . import institution
from .forms import InstiForm, NotiForm, EventForm, SecurityForm, EditForm
from .decorators import insti_required
from .. import db
from ..models import Institution, Notification, Event, Category, User, Track

from itsdangerous import URLSafeSerializer
from flask import render_template, abort, request, flash, redirect, url_for, current_app
from flask.ext.uploads import configure_uploads, UploadSet, UploadNotAllowed
from flask.ext.login import login_required, current_user

from datetime import datetime, timedelta
from functools import wraps

@institution.route('/')
def index():
    return 'hey!'

@institution.route('/<uurl>/<obj>')
def stuff(uurl, obj):
    insti = Institution.query.filter_by(uurl=uurl).first() or abort(404)
    page = request.args.get('p', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    if obj == 'notis':
        pagination = insti.notis.order_by(Notification.post_time.desc()).paginate(page, per_page=per_page)    #, error_out=False
        notis = pagination.items
        return render_template('institution/notis.html', notis=notis, insti=insti, pagination=pagination)
    elif obj == 'events':
        pagination = insti.events.order_by(Event.new_time.desc()).paginate(page, per_page=per_page)    #, error_out=False
        events = pagination.items
        return render_template('institution/events.html', events=events, insti=insti, pagination=pagination)
    else:
        abort(404)

@institution.route('/<uurl>')
# @insti_required
def page(uurl):
    insti = Institution.query.filter_by(uurl=uurl).first() or abort(404)
    trackers = User.query.join(Track, Track.user_id==User.id).filter(Track.insti_id==insti.id)\
    	.order_by(Track.track_time.desc()).limit(9).all()	# filter_by --> filter
    new_notis = Notification.query.filter_by(publisher_id=insti.id).order_by(Notification.post_time.desc()).limit(7).all()
    new_events = Event.query.filter_by(sponsor_id=insti.id).order_by(Event.new_time.desc()).limit(5).all()
    return render_template('/institution/page.html', insti=insti, trackers=trackers, 
        notis=new_notis, events=new_events)

@institution.route('/<uurl>/track')
@login_required
def track(uurl):
    try:
        insti = Institution.query.filter_by(uurl=uurl).first() or abort(404)
        current_user.track(insti)
        flash('成功关注了 %s' % insti.name, 'alert-success')
    except:
        flash('出错了，，关注失败', 'alert-danger')
    return redirect(url_for('institution.page', uurl=uurl))

@institution.route('/<uurl>/untrack')
@login_required
def untrack(uurl):
    try:
        insti = Institution.query.filter_by(uurl=uurl).first() or abort(404)
        current_user.untrack(insti)
        flash('不再关注 %s' % insti.name, 'alert-success')
    except:
        flash('出错了，，稍后再试试吧', 'alert-danger')
    return redirect(url_for('institution.page', uurl=uurl))

@institution.route('/<uurl>/panel')
def panel(uurl):
    return redirect(url_for('.notifi', uurl=uurl))

@institution.route('/<uurl>/panel/notification', methods=['GET', 'POST'])
def notifi(uurl):
    insti = current_insti()
    page = request.args.get('p', 1, type=int)
    pagination = Notification.query.filter_by(publisher_id=insti.id).order_by(Notification.post_time.desc())\
    	.paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])	#
    notis = pagination.items
    noti_form = NotiForm()
    if request.method=='POST' and noti_form.publish.data and noti_form.validate_on_submit():
        notification = Notification(content=noti_form.content.data, publisher_id=insti.id)
        db.session.add(notification)
        flash('发布成功', 'alert-success')
        return redirect(url_for('.notifi', uurl=uurl))
    return render_template('institution/notification.html', insti=insti, noti_form=noti_form, notis=notis, pagination=pagination)

@institution.route('/<uurl>/panel/delete-noti/<int:id>')
def delete_noti(uurl, id):
    try:
        notifi = Notification.query.get_or_404(int(id))
        db.session.delete(notifi)
        flash('删除成功', 'alert-success')
    except:
        flash('出错了，删除失败', 'alert-danger')
        pass
    return redirect(url_for('.notifi', uurl=uurl))

@institution.route('/<uurl>/panel/event', methods=['GET', 'POST'])
def event(uurl):
    insti = current_insti()
    page = request.args.get('p', 1, type=int)
    pagination = Event.query.filter_by(sponsor_id=insti.id).order_by(Event.new_time.desc())\
    	.paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])
    events = pagination.items
    return render_template('institution/event.html', insti=insti, events=events, pagination=pagination)

@institution.route('/<uurl>/panel/edit-event/<int:eid>', methods=['GET', 'POST'])
def edit_event(uurl, eid):
    event = Event.query.get_or_404(int(eid))
    edit_form = EditForm()
    if request.method=='POST' and edit_form.validate_on_submit():
        event.detail = edit_form.detail.data
        poster = request.files.get('poster')
        if poster.filename is not None: 
            poster_upload = UploadSet(name='posters', extensions=('jpg', 'jpeg', 'png', 'bmp'))
            configure_uploads(current_app, (poster_upload))    #加载上传集配置
            try:
                filename = poster_upload.save(poster)
                event.poster_url = poster_upload.url(filename)
            except UploadNotAllowed:
                pass
        else:
            flash('海报上传失败……', 'alert-warning')
        db.session.add(event)
        flash('更新成功', 'alert-success')
        return redirect(url_for('event.event_page', eid=event.id))
    edit_form.detail.data = event.detail
    return render_template('institution/event_edit.html', insti=current_insti(), event=event, edit_form=edit_form)

@institution.route('/<uurl>/panel/delete-event/<int:id>')
def delete_event(uurl, id):
    try:
        event = Event.query.get_or_404(int(id))
        db.session.delete(event)
        flash('删除成功', 'alert-success')
    except:
        flash('出错了，删除失败', 'alert-danger')
        pass
    return redirect(url_for('.event', uurl=uurl))

def cate_list():
    cates = Category.query.all()
    if cates is not None:
        return [(cate.id, cate.name) for cate in cates]
    return []

def event_handler(form, insti):
    try:
        name = form.name.data
        category = form.category.data
        # try:
        #     start_time = datetime.strptime(form.start_time.data, '%Y-%m-%d %H:%M')
        #     end_time = datetime.strptime(form.end_time.data, '%Y-%m-%d %H:%M')
        #     if start_time > end_time:
        #         return False, '结束时间不能大于开始时间'
        # except Exception as e:
        #     print(str(e))
        #     return False ,'出错了……讨厌的感觉。'
        start_time = form.start_time.data
        end_time = form.end_time.data
        longitude = form.longitude.data
        latitude = form.latitude.data
        address = form.address.data
        detail = form.detail.data
        event = Event(name=name, category_id=category, start_time=start_time, end_time=end_time, 
            longitude=longitude, latitude=latitude, address=address, detail=detail, sponsor_id=insti.id)
        db.session.add(event)
        return True, '发布成功'
    except Exception as e:
        # print(str(e))
        return False ,'出错了……讨厌的感觉。'

@institution.route('/<uurl>/panel/new-event', methods=['GET', 'POST'])
def new_event(uurl):
    insti = current_insti()
    event_form = EventForm()
    event_form.category.choices = cate_list()
    if request.method=='POST'and event_form.new.data and event_form.validate_on_submit():
        status, msg = event_handler(event_form, insti)
        if status:
            flash(msg, 'alert-success')
        else:
            flash(msg, 'alert-danger')
        return redirect(url_for('institution.new_event', uurl=uurl))
    return render_template('institution/new-event.html', insti=insti, event_form=event_form)

def profile_handler(form, insti, req):
    insti.name = form.name.data
    insti.intro = form.intro.data
    logo = request.files.get('logo')
    if not (logo.filename is None or logo.filename==''):
        logo_upload = UploadSet('logos', ('jpg', 'png'))
        configure_uploads(current_app, (logo_upload))
        try:
            filename = logo_upload.save(logo)
            logo_url = logo_upload.url(filename)
            insti.logo_url = logo_url
        except UploadNotAllowed:
            return (False, '上传LOGO时出错')
    poster = request.files.get('poster')
    if not (poster.filename is None or poster.filename==''):
        poster_upload = UploadSet('posters', ('jpg', 'png'))
        configure_uploads(current_app, (poster_upload))
        try:
            filename = poster_upload.save(poster)
            poster_url = poster_upload.url(filename)
            insti.poster_url = poster_url
        except UploadNotAllowed:
            return (False, '上传海报时出错')
    db.session.add(insti)
    return (True, '资料更新成功')

@institution.route('/<uurl>/panel/profile', methods=['GET', 'POST'])
def profile(uurl):
    insti = current_insti()    
    insti_form = InstiForm()
    if request.method=='POST' and insti_form.save.data and insti_form.validate_on_submit():
        status, msg = profile_handler(insti_form, insti, request)
        if status:
            flash(msg, 'alert-success')
        else:
            flash(msg, 'alert-danger')
        return redirect(url_for('institution.profile', uurl=uurl))
    insti_form.name.data = insti.name
    insti_form.intro.data = insti.intro
    return render_template('institution/profile.html', insti=insti, insti_form=insti_form)

@institution.route('/<uurl>/panel/settings', methods=['GET', 'POST'])
def settings(uurl):
    insti = current_insti()
    security_form = SecurityForm()
    if request.method=='POST' and security_form.submit.data and security_form.validate_on_submit():
        if insti.verify_password(security_form.current_password.data):
            insti.password = security_form.new_password.data
            db.session.add(insti)
            flash('修改成功', 'alert-success')
        else:
            flash('密码错误，修改失败', 'alert-danger')
    return render_template('institution/settings.html', insti=insti, security_form=security_form)

def current_insti():
    insti_uurl = request.cookies.get('insti-uurl')
    if insti_uurl:
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        uurl = s.loads(insti_uurl)
        return Institution.query.filter_by(uurl=uurl).first()
    return None