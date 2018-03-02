from flask import Blueprint, redirect, url_for, request, flash

admin = Blueprint('admin', __name__)

from . import views


def before_request():
    '''验证登录'''
    # print(request.endpoint)
    if request.endpoint=='admin.reg' or request.endpoint=='admin.login':
        pass
    else:
        if views.current_admin() is None:
            flash('需要登录', 'alert-warning')
            return redirect(url_for('admin.login'))

admin.before_request(before_request)