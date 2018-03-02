# datetime.datetime.utcnow(), datetime.datetime.now(), 
# datetime.datetime.today(), datetime.date.today()
from datetime import datetime, date, timedelta
import uuid

from . import db, login_manager

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Follow(db.Model):	#第三表
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    follow_time = db.Column(db.DateTime, default=datetime.now)

class Join(db.Model):
    __tablename__ = 'joins'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

class Participate(db.Model):
	__tablename__ = 'participates'
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
	partici_time = db.Column(db.DateTime, default=datetime.now)

class Track(db.Model):
    __tablename__ = 'tracks'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    insti_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), primary_key=True)
    track_time = db.Column(db.DateTime, default=datetime.now)

class User(UserMixin, db.Model):    #UserMixin对象实现了Flak-Login要求实现的方法
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(24), nullable=False, index=True)
    avatar_url = db.Column(db.String(128), default='/static/images/avatar_default.png') 
    portrait_url = db.Column(db.String(128), default='/static/images/portrait_default.png')
    # location = 
    reg_date = db.Column(db.Date(), default=date.today)
    intro = db.Column(db.TEXT())
    signature = db.Column(db.String(30))

    twitters = db.relationship('Twitter', backref='author', lazy='dynamic')	#碎碎念的作者
    @property
    def foled_twitters(self):
        return Twitter.query.join(Follow, Follow.followed_id==Twitter.author_id).filter(Follow.follower_id==self.id)
    @property
    def my_events(self):
        return Event.query.join(Institution, Event.sponsor_id==Institution.id).join(Track, Institution.id==Track.insti_id)\
            .filter(Track.user_id==self.id)

    topics = db.relationship('Topic', backref='author', lazy='dynamic')
    @property
    def my_topics(self):
        return Topic.query.join(Group, Topic.group_id==Group.id).join(Join, Group.id==Join.group_id).filter(Join.user_id==self.id)

    discus = db.relationship('Discussion', backref='author', lazy='dynamic')

    marks = db.relationship('Mark', backref='marker', lazy='dynamic')
    def is_marked(self, url):	#是否标记了url
        #有点。[] is True为False，[] is False为False，[] is None为False，not []为True
        return self.marks.filter_by(url=url).first() is not None	#必须加.all()才返回结果（不加时返回新查询）

    groups = db.relationship('Group', backref='owner', lazy='dynamic')
    def is_owning(self, group):
    	return self.groups.filter_by(id=group.id).first() is not None
    joined_groups = db.relationship('Join', foreign_keys=[Join.user_id], backref=db.backref('member', lazy='joined'),
    	lazy='dynamic', cascade='all, delete-orphan')
    def is_joining(self, group):
    	return self.joined_groups.filter_by(group_id=group.id).first() is not None
    def join(self, group):
    	if not self.is_joining(group):
            j = Join(group=group, member=self)
            db.session.add(j)
    def exit(self, group):
        j = self.joined_groups.filter_by(group_id=group.id).first()
        if j:
            db.session.delete(j)

    partici_events = db.relationship('Participate', foreign_keys=[Participate.user_id], backref=db.backref('participant', lazy='joined'),
    	lazy='dynamic', cascade='all, delete-orphan')
    def is_partici(self, event):
        return self.partici_events.filter_by(event_id=event.id).first() is not None
    def partici(self, event):
        if not self.is_partici(event):
            p = Participate(participant=self, event=event)
            db.session.add(p)
    def unpartici(self, event):
        if self.is_partici(event):
        	p = self.partici_events.filter_by(event_id=event.id).first()
        	db.session.delete(p)

    track_instis = db.relationship('Track', foreign_keys=[Track.user_id], backref=db.backref('tracker', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan')
    def is_track(self, insti):
        return self.track_instis.filter_by(insti_id=insti.id).first() is not None
    def track(self, insti):
        if not self.is_track(insti):
            t = Track(tracker=self, insti=insti)
            db.session.add(t)
    def untrack(self, insti):
        if self.is_track(insti):
            t = self.track_instis.filter_by(insti_id=insti.id).first()
            db.session.delete(t)

    followeds = db.relationship('Follow', foreign_keys=[Follow.follower_id], 
    	backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')   #lazy='dynamic'
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],
    	backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')  #lazy='subquery'
    def follow(self, user):
        if not self.is_following(user):
        	f = Follow(follower=self, followed=user)
        	db.session.add(f)
    def unfollow(self, user):
        f = self.followeds.filter_by(followed_id=user.id).first()   #good
        if f:
        	db.session.delete(f)
    def is_following(self, user):
        return self.followeds.filter_by(followed_id=user.id).first() is not None    #.query
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None
    @staticmethod
    def add_self_follows():	#所有用户自关注的静态方法
        for user in User.query.all():
            if not user.is_following(user):
            	user.follow(user)
            	db.session.add(user)
            	db.session.commit()

    confirmed = db.Column(db.Boolean, default=False)
    def generate_confirmation_token(self, expiration=48*60*60): #有效期48小时
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirmed': self.id})
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        return True

    password_hash = db.Column(db.String(128))   #不保存明文密码
    @property
    def password(self):
        raise AttributeError('密码不可读')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.followeds.append(Follow(followed=self))	#self.follow(self)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader  #Flak-Login要求的回调函数
def load_user(user_id):
    return User.query.get(int(user_id)) #返回用户对象

class Twitter(db.Model):
    __tablename__ = 'twitters'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT)
    post_time = db.Column(db.DateTime, index=True, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))    #外键

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True)
    icon_url = db.Column(db.String(128))
    intro = db.Column(db.TEXT)
    birthday = db.Column(db.Date, index=True, default=date.today)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id')) #外键
    crew = db.relationship('Join', foreign_keys=[Join.group_id], backref=db.backref('group', lazy='joined'),
    	lazy='dynamic', cascade='all, delete-orphan')

    topics = db.relationship('Topic', backref='group', lazy='dynamic')

    def __init__(self, **kwargs):	#**kwargs不可缺
        super(Group, self).__init__(**kwargs)
        self.crew.append(Join(user_id=self.owner_id))

class Topic(db.Model):
    __tablename__ = 'topics'    #'Topics' --> sqlalchemy.exc.InternalError: (pymysql.err.InternalError) (1050, "Table 'topics'already exists")
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(128))
    description = db.Column(db.TEXT)
    post_time = db.Column(db.DateTime, default=datetime.now, index=True)
    discus = db.relationship('Discussion', backref='topic', lazy='dynamic')

class Discussion(db.Model):
    __tablename__ = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    content = db.Column(db.Text)
    post_time = db.Column(db.DateTime, default=datetime.now, index=True)

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    eno = db.Column(db.String(128), unique=True)
    reg_time = db.Column(db.DateTime, default=datetime.now)

    certis = db.relationship('Certification', backref='inputer', lazy='dynamic')

    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('密码不可读')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Certification(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)

    def generate_uuid():
        return str(uuid.uuid4())
    ucode = db.Column(db.String(40), unique=True, default=generate_uuid)
    certi_date = db.Column(db.Date(), default=date.today)

    def after_one_year():
        return date.today()+timedelta(days=365)
    expiry_date = db.Column(db.Date(), default=after_one_year)
    def is_available(self):
        if self.expiry_date > date.today():
            return True
        return False

    agent_id = db.Column(db.String(20))
    inputer_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    body = db.Column(db.String(128), unique=True, index=True)
    function = db.Column(db.Text)
    description = db.Column(db.Text)
    website = db.Column(db.String(128))
    address = db.Column(db.Text)
    phone = db.Column(db.String(64))
    insti = db.relationship('Institution', backref='certi', uselist=False)  # uselist=False --> one-to-one

class Institution(db.Model):
    __tablename__ = 'institutions'
    id = db.Column(db.Integer, primary_key=True)
    certi_id = db.Column(db.Integer, db.ForeignKey('certifications.id'), unique=True)
    # catri = db.relationship('Certification', backref='insti')
    uurl = db.Column(db.String(64), unique=True, index=True) #个性域名
    name = db.Column(db.String(128), default=uurl)
    logo_url = db.Column(db.String(128))
    poster_url = db.Column(db.String(128))
    intro = db.Column(db.TEXT)

    notis = db.relationship('Notification', backref='publisher', lazy='dynamic')
    events = db.relationship('Event', backref='sponsor', lazy='dynamic')
    track_users = db.relationship('Track', foreign_keys=[Track.insti_id], backref=db.backref('insti', lazy='joined'),
        lazy='dynamic', cascade='all, delete-orphan')
    
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('密码不可读')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    enroll_date = db.Column(db.Date, default=date.today, index=True)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.TEXT)
    post_time = db.Column(db.DateTime, index=True, default=datetime.now)
    publisher_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))    #外键

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    start_time = db.Column(db.DateTime, index=True)
    end_time = db.Column(db.DateTime, index=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    address = db.Column(db.String(256))
    poster_url = db.Column(db.String(128))
    detail = db.Column(db.TEXT)
    new_time = db.Column(db.Date, index=True, default=date.today)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))

    entrants = db.relationship('Participate', foreign_keys=[Participate.event_id], backref=db.backref('event', lazy='joined'),
    	lazy='dynamic', cascade='all, delete-orphan')

    def state(self):
        if datetime.now() < self.start_time:
            return 'state-will', '尚未开始'
        elif datetime.now() < self.end_time:
            return 'state-ing', '进行中……'
        else:
            return 'state-ed', '已结束'

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    events = db.relationship('Event', backref='category', lazy='dynamic')

class Mark(db.Model):
    __tablename__ = 'marks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    url = db.Column(db.String(128), index=True)
    mark_time = db.Column(db.DateTime, index=True, default=datetime.now)
    marker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
