from flask import render_template, request, flash, redirect, url_for, current_app

from flask.ext.login import current_user, login_required

from . import main
from .forms import TwitterForm
from ..models import Twitter, Mark, Event, Topic, User
from .. import db

@main.route('/', methods=['GET', 'POST'])
def index():
    twitter_form = TwitterForm()
    if request.method == 'POST' and twitter_form.validate_on_submit():
        twitter = Twitter(content=twitter_form.content.data, author=current_user._get_current_object())	#author与model中的User一致
        db.session.add(twitter)
        flash('发布成功', 'alert-success')
        return redirect(url_for('main.index'))
    some_events = Event.query.order_by(Event.new_time.desc()).limit(7)
    some_topics = Topic.query.order_by(Topic.post_time.desc()).limit(7)
    some_members = User.query.order_by(User.reg_date.desc()).limit(7)
    pagination = None;
    foled_twitters = None;
    if current_user.is_authenticated:
        page = request.args.get('p', 1, type=int)
        pagination = current_user.foled_twitters.order_by(Twitter.post_time.desc()).paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'])
        foled_twitters = pagination.items
    return render_template('index.html', form=twitter_form, events=some_events, topics=some_topics,
         members=some_members, twitters=foled_twitters, pagination=pagination)

@main.route('/delete-twitter')
@login_required
def delete_twitter():
    twitter_id = request.args.get('id', type=int)
    if twitter_id is not None:
        twitter = Twitter.query.get(twitter_id) #get函数只需传入主键即可
        if twitter is not None and twitter.author_id == current_user.id:
            db.session.delete(twitter)
            flash('删除成功', 'alert-success')
    else:
        flash('因为某种原因，删除失败', 'alert-danger')
    return redirect(request.args.get('next') or url_for('main.index'))

@main.route('/mark')
@login_required
def mark():
    url = request.args.get('url')
    title = request.args.get('title') or '无标题'
    if url and title:
        mark = Mark(url=url, title=title, marker_id=current_user.id)
        db.session.add(mark)
        flash('标记成功。可到 个人主页->我的标记 中查看', 'alert-success')
    return redirect(url)

@main.route('/unmark')
@login_required
def unmark():
    url = request.args.get('url')
    if url:
        mark = Mark.query.filter_by(url=url, marker_id=current_user.id).first()
        if mark:
            db.session.delete(mark)
    return redirect(url)

@main.route('/test')
def test():
    # app = current_app._get_current_object()
    # params = {'key': app.config['TCMAP_KEY']}
    # resp = reqs.get('http://apis.map.qq.com/ws/district/v1/list', params)
    # content = resp.json()
    # provinces = []
    # cities = []
    # countys = []
    # if content['status']==0:
    #     provs = content['result'][0]
    #     for p in provs:
    #         provinces.append({'id': p['id'], 'name':p['name']})

    #     citys = content['result'][1]
    #     for c in citys:
    #         cities.append({'id': c['id'], 'name': c['name']})

    #     couns = content['result'][2]
    #     for coun in couns:
    #         countys.append({'id': coun['id'], 'name': coun['fullname']})
    # return render_template('test.html', provinces=provinces, cities=cities, countys=countys)
    return render_template('test.html')
