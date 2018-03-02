from flask import Blueprint, redirect, url_for, request, flash

institution = Blueprint('institution', __name__)

from . import views


def before_request():
    '''验证登录'''
    # print(request.endpoint)
    allowed_endpoints = ['institution.page', 'institution.index', 'institution.track', 'institution.untrack', 'institution.stuff']
    if request.endpoint in allowed_endpoints:
        pass
    else:
        # request.args.get('uurl')
        if views.current_insti() is None:
            flash('需要登录', 'alert-warning')
            return redirect(url_for('auth.signin'))

institution.before_request(before_request)