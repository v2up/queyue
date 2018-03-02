from . import event
from .. import db
from ..models import Event, User, Participate, Institution, Track

from flask import render_template, redirect, url_for, flash, request, current_app
from flask.ext.login import login_required, current_user

@event.route('/')	#, methods=['GET']
@login_required
def event_index():
    my_events = Event.query.join(Participate, Participate.event_id==Event.id).filter(Participate.user_id==current_user.id)\
        .order_by(Participate.partici_time.desc()).limit(7).all()
    my_instis = Institution.query.join(Track, Track.insti_id==Institution.id).filter(Track.user_id==current_user.id)\
        .order_by(Track.track_time.desc()).limit(6).all()
    new_events = Event.query.order_by(Event.new_time.desc()).limit(7).all()
    new_instis = Institution.query.order_by(Institution.enroll_date.desc()).limit(6).all()
    page = request.args.get('p', 1, type=int)
    pagination = current_user.my_events.order_by(Event.new_time.desc()).paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])
    my_eves = pagination.items
    return render_template('event/event.html', my_events=my_events, my_instis=my_instis, new_events=new_events, new_instis=new_instis, 
        pagination=pagination, events=my_eves)

@event.route('/<int:eid>')
def event_page(eid):
    event = Event.query.get_or_404(eid)
    entrants =  User.query.join(Participate, User.id==Participate.user_id).filter(Participate.event_id==event.id)\
    	.order_by(Participate.partici_time.desc()).all()
    return render_template('event/page.html', event=event, entrants=entrants)

@event.route('/<int:eid>/unpartici')
@login_required
def unpartici(eid):
    try:
        event = Event.query.get_or_404(int(eid))
        current_user.unpartici(event)
        flash('成功退出了活动 %s ' % event.name, 'alert-success')
    except Exception as e:
        flash('出了点错误，暂时无法退出该活动', 'alert-danger')
    return redirect(url_for('event.event_page', eid=eid))


@event.route('/<int:eid>/partici')
@login_required
def partici(eid):
    try:
        event = Event.query.get_or_404(int(eid))
        current_user.partici(event)
        flash('参加活动 %s 成功' % event.name, 'alert-success')
    except Exception as e:
        # flash(str(e), 'alert-danger')
        flash('出错了，暂时无法参加该活动', 'alert-danger')
    return redirect(url_for('event.event_page', eid=eid))

# @event.route('/map')
# def full_map():
#     lng = float(request.args.get('lng', 116.396574))
#     lat = float(request.args.get('lat', 39.992706))
#     return render_template('event/map.html', lng=lng, lat=lat)