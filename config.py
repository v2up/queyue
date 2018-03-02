import os

class Config:
    SECRET_KEY = 'Poetry and The Far Afield'	#在跨站请求伪造CSRF防御中有作用
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ITEMS_PER_PAGE = 9

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True	#打开调试
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1/quey'	#数据库连接qqqyyy

    # 跟邮件相关的配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    # MAIL_USE_SSL = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'v2up@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'yhgzvxkmmrtpbbid'
    QY_MAIL_SENDER = '雀跃团队<v2up@qq.com>'
    QY_ADMIN = 'v2up@qq.com'
    QY_MAIL_SUBJECT_PREFIX = '[雀跃]'

    # 文件上传配置（已在工厂函数定义）
    # UPLOADS_DEFAULT_DEST = os.path.abspath(__file__)    #F:\queyue\qy\uploads
    # UPLOADS_DEFAULT_URL = 'http://127.0.0.1:5000/uploads/'

    # 腾讯地图开发密钥
    AMAP_KEY = '8323ea875aa64454ec94dd60df766ffa'

config = {
    'dev': DevelopmentConfig,

    'default': DevelopmentConfig
}
