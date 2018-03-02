from . import group
from .forms import GroupForm, TopicForm, DiscuForm
from ..models import Group, User, Join, Topic, Discussion
from .. import db

from flask import render_template, request, redirect, flash, url_for, current_app

from flask.ext.login import login_required, current_user
from flask.ext.uploads import configure_uploads, UploadSet, UploadNotAllowed

@group.route('/')
@login_required	#需要登录才能查看小组话题
def group_index():	#注意：函数名不要和蓝本重名
    new_groups = Group.query.order_by(Group.birthday.desc()).limit(7)
    new_topics = Topic.query.order_by(Topic.post_time.desc()).limit(7)
    page = request.args.get('p', 1, type=int)
    pagination = current_user.my_topics.order_by(Topic.post_time.desc()).paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])
    topics = pagination.items
    return render_template('group/group.html', new_groups=new_groups, new_topics=new_topics, pagination=pagination, topics=topics)

@group.route('/new', methods=['GET', 'POST'])
@login_required
def group_new():
    group_form = GroupForm()
    if request.method == 'POST' and group_form.validate_on_submit():
        name = group_form.name.data
        intro = group_form.intro.data
        icon = request.files.get('icon')
        if not (icon is None or icon == ''):
            icon_upload = UploadSet('icons', ('jpg', 'png'))
            configure_uploads(current_app, (icon_upload))
            try:
                filename = icon_upload.save(icon)
                icon_url = icon_upload.url(filename)	#得到icon的URL
            except UploadNotAllowed:
                flash('请上传小组图标', 'alert-danger')
                return render_template('group/new.html', form=group_form)
        else:
            flash('小组图标没上传', 'alert-danger')
            return render_template('group/new.html', form=group_form)

        group = Group(name=name, icon_url=icon_url, intro=intro, owner_id=current_user.id) #_get_current_object()
        db.session.add(group)
        flash('新建小组 %s 成功！' % name, 'alert-success')
        return redirect(url_for('group.group_index'))
    return render_template('group/new.html', form=group_form)

@group.route('/<int:gid>', methods=['GET', 'POST'])  #拿小组id当参数
def group_page(gid):
    group = Group.query.get_or_404(gid)
    group_members = User.query.join(Join, User.id==Join.user_id).filter(Join.group_id==group.id)\
        .order_by(Join.join_time.desc()).all()  #超屌查询
    topic_form = TopicForm()
    if request.method == 'POST' and topic_form.validate_on_submit():
        topic = Topic(title=topic_form.title.data, description=topic_form.description.data, 
            group_id=group.id, author_id=current_user.id)
        db.session.add(topic)
        flash('新发了话题 %s' % topic.title, 'alert-success')
    page = request.args.get('p', 1, type=int)
    pagination = group.topics.order_by(Topic.post_time.desc()).paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])
    topics = pagination.items
    return render_template('group/page.html', group=group, form=topic_form, members=group_members, pagination=pagination, topics=topics)

@group.route('/<int:gid>/topic/<int:tid>', methods=['GET', 'POST'])
def topic_page(gid, tid):
    discu_form = DiscuForm()
    topic = Topic.query.get_or_404(tid)
    if request.method=='POST' and discu_form.validate_on_submit():
        discussion = Discussion(author_id=current_user.id, topic_id=topic.id, content=discu_form.content.data)
        db.session.add(discussion)
        flash('回复成功', 'alert-success')
        return redirect(url_for('.topic_page', gid=gid, tid=tid))
    page = request.args.get('p', 1, type=int)
    pagination = topic.discus.order_by(Discussion.post_time.desc()).paginate(page, per_page=10) #
    discus = pagination.items
    return render_template('group/topic_page.html', topic=topic, form=discu_form, pagination=pagination, discus=discus)

@group.route('/<int:gid>/topic/<int:tid>/delete-topic', methods=['GET', 'POST'])
def delete_topic(gid, tid):
    try:
        topic = Topic.query.get_or_404(int(tid))
        db.session.delete(topic)
        flash('删除成功', 'alert-success')
    except:
        flash('出错了，删除失败……', 'alert-danger')
    return redirect(url_for('group.group_page', gid=gid)) 

@group.route('/<int:gid>/topic/<int:tid>/delete-discu/<int:did>')
def delete_discu(gid, tid, did):
    try:
        discu = Discussion.query.get_or_404(int(did))
        db.session.delete(discu)
        flash('删除成功', 'alert-success')
    except:
        flash('出错了，删除失败……', 'alert-danger')
    return redirect(url_for('group.topic_page', gid=gid, tid=tid))

@group.route('/<int:gid>/join')
@login_required
def join(gid):
    group = Group.query.get_or_404(gid)
    current_user.join(group)
    flash('你加入了 %s 。' % group.name, 'alert-success')
    return redirect(url_for('group.group_page', gid=group.id))

@group.route('/<int:gid>/exit')
@login_required
def exit(gid):  #别忘了把参数写在列表中！
    group = Group.query.get_or_404(gid)
    current_user.exit(group)
    flash('你退出了 %s 。' % group.name, 'alert-success')
    return redirect(url_for('group.group_page', gid=group.id))
