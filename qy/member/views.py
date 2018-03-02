# from werkzeug import secure_filename
from flask import render_template, request, redirect, flash, url_for, current_app, abort

from flask.ext.login import login_required, current_user
from flask.ext.uploads import configure_uploads, UploadSet, UploadNotAllowed

from ..models import User, Twitter, Mark, Follow, Group, Join, Event, Participate, Institution, Track
from . import member
from .forms import EditForm
from .. import db

@member.route('/<int:userid>')
def member_page(userid):
    member = User.query.get_or_404(userid)
    member_twitters = member.twitters.order_by(Twitter.post_time.desc()).paginate(1, 3).items
    member_marks = member.marks.order_by(Mark.mark_time.desc()).paginate(1, 10).items
    member_followers = User.query.join(Follow, Follow.follower_id==User.id).filter(Follow.followed_id==member.id)\
        .order_by(Follow.follow_time.desc()).limit(6).all()
    member_followeds = User.query.join(Follow, Follow.followed_id==User.id).filter(Follow.follower_id==member.id)\
        .order_by(Follow.follow_time.desc()).limit(6).all()
    member_groups = Group.query.join(Join, Join.group_id==Group.id).filter(Join.user_id==member.id)\
        .order_by(Join.join_time.desc()).limit(6).all()
    member_events = Event.query.join(Participate, Participate.event_id==Event.id).filter(Participate.user_id==member.id)\
        .order_by(Participate.partici_time.desc()).limit(6).all()
    return render_template('member/member.html', 
        member=member, twitters=member_twitters, marks=member_marks, 
        followers=member_followers, followeds=member_followeds, groups=member_groups, events=member_events)


@member.route('/edit', methods=['GET', 'POST'])
@login_required #必须登录
def member_edit():
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.name = edit_form.username.data
        avatar = request.files.get('avatar')
        # print(avatar)   # <FileStorage: '' ('application/octet-stream')>
        # print(avatar.filename)
        if avatar.filename is not None: # and avatar.filename!=''
            avatar_upload = UploadSet(name='avatars', extensions=('jpg', 'jpeg', 'png', 'bmp'))
            configure_uploads(current_app, (avatar_upload))    #加载上传集配置
            try:
                filename = avatar_upload.save(avatar)
                # avatar_upload.resolve_conflict(avatar_upload, fname)  #解决可能存在的文件名冲突问题
                user.avatar_url = avatar_upload.url(filename)
            except UploadNotAllowed:
                pass
        else:
            flash('头像上传失败', 'alert-warning')
        portrait = request.files.get('portrait')
        if portrait.filename is not None: 
            portrait_upload = UploadSet(name='portraits', extensions=('jpg', 'jpeg', 'png', 'bmp'))
            configure_uploads(current_app, (portrait_upload))    #加载上传集配置
            try:
                filename = portrait_upload.save(portrait)
                # portrait_upload.resolve_conflict(portrait_upload, fname)  #解决可能存在的文件名冲突问题
                user.portrait_url = portrait_upload.url(filename)
            except UploadNotAllowed:
                pass
        else:
            flash('半身像上传失败', 'alert-warning')
        user.signature = edit_form.signature.data
        user.intro = edit_form.intro.data
        password = edit_form.password.data
        if password is not None and password != '':  #更改密码
            if user.verify_password(edit_form.old_password.data):
                if len(password)> 6 and len(password)< 24:
                    if password == edit_form.password2.data:
                        user.password = password
                        flash('密码更改成功！', 'alert-success')
                    else:
                        flash('两次密码输入不一致，密码未更改', 'alert-warning')
                else:
                    flash('密码长度必须 6-24 位，密码未更改', 'alert-warning')
            else:
                flash('当前密码错误，密码未更改', 'alert-danger')
        db.session.add(user)
        flash('个人资料更新成功！', 'alert-success')
        return redirect(url_for('member.member_page', userid=user.id))
    edit_form.username.data = current_user.name
    edit_form.signature.data = current_user.signature
    edit_form.intro.data = current_user.intro
    return render_template('member/edit.html', form=edit_form)

@member.route('/<int:userid>/<obj>')
def stuff(userid, obj):
    member = User.query.get_or_404(userid)
    page = request.args.get('p', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    if obj == 'twitters':
        pagination = member.twitters.order_by(Twitter.post_time.desc()).paginate(page, per_page=per_page)    #, error_out=False
        twitters = pagination.items
        return render_template('member/twitters.html', twitters=twitters, member=member, pagination=pagination)
    elif obj == 'events':
        pagination = Event.query.join(Participate, Participate.event_id==Event.id).filter(Participate.user_id==member.id)\
            .order_by(Participate.partici_time.desc()).paginate(page, per_page=per_page)
        events = pagination.items
        return render_template('member/events.html', member=member, pagination=pagination, events=events)
    elif obj == 'groups':
        groups = Group.query.join(Join, Join.group_id==Group.id).filter(Join.user_id==member.id)\
            .order_by(Join.join_time.desc()).all()
        return render_template('member/groups.html', member=member, groups=groups)
    elif obj == 'socials':
        followers = User.query.join(Follow, Follow.follower_id==User.id).filter(Follow.followed_id==member.id)\
            .order_by(Follow.follow_time.desc()).all()
        followeds = User.query.join(Follow, Follow.followed_id==User.id).filter(Follow.follower_id==member.id)\
            .order_by(Follow.follow_time.desc()).all()
        return render_template('member/socials.html', member=member, followers=followers, followeds=followeds)
    elif obj == 'marks':
        pagination = member.marks.order_by(Mark.mark_time.desc()).paginate(page)
        marks = pagination.items
        return render_template('member/marks.html', marks=marks, member=member, pagination=pagination)
    elif obj == 'instis':
        instis = Institution.query.join(Track, Track.insti_id==Institution.id).filter(Track.user_id==member.id)\
            .order_by(Track.track_time.desc()).all()
        return render_template('member/instis.html', member=member, instis=instis)
    else:
        abort(404)

@member.route('/follow')
@login_required
def follow():
    userid = request.args.get('userid')
    if userid:
    	user = User.query.get(userid)
    	if user:
    		current_user.follow(user)
    return redirect(url_for('member.member_page', userid=userid))

@member.route('/unfollow')
@login_required
def unfollow():
    userid = request.args.get('userid')
    if userid:
        user = User.query.get(userid)
        if user:
            current_user.unfollow(user)
    return redirect(url_for('member.member_page', userid=userid))