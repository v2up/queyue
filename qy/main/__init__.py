from flask import Blueprint	#使用蓝本

main = Blueprint('main', __name__)	#实例化一个蓝本

from . import views, errors