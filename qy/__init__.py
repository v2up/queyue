from flask import Flask	#flask框架
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate  #还需pip install pymysql
from flask.ext.mail import Mail
from flask.ext.login import LoginManager    #登录管理
from flask.ext.moment import Moment

from config import config	#不同的配置，不同的运行模式

import os

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong' #登录保护等级
login_manager.login_view = 'auth.login'
login_manager.login_message = '登录后方可访问'
login_manager.login_message_category = "alert-warning"
moment = Moment()

def create_app(config_name):
    '''工厂函数'''
    app = Flask(__name__)	#当前目录为根目录
    app.config.from_object(config[config_name])	#读取配置对象
    config[config_name].init_app(app)	#自己实现的staticmethod

    # 文件上传配置
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads/')    #F:\queyue\qy\uploads
    app.config['UPLOADS_DEFAULT_URL'] = 'http://127.0.0.1:5000/uploads/'

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)  #注册一个蓝本
    from .auth import auth as auth_blueprint 
    app.register_blueprint(auth_blueprint)
    from .member import member as member_blueprint
    app.register_blueprint(member_blueprint, url_prefix='/member')
    from .resource import resource as resource_blueprint
    app.register_blueprint(resource_blueprint)
    from .event import event as event_blueprint
    app.register_blueprint(event_blueprint, url_prefix='/event')
    from .group import group as group_blueprint
    app.register_blueprint(group_blueprint, url_prefix='/group')
    from .institution import institution as institution_blueprint
    app.register_blueprint(institution_blueprint, url_prefix='/institution')
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app