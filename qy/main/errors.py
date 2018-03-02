from flask import render_template, flash

from . import main

@main.app_errorhandler(404)	#全局错误处理app_errorhandler
def page_not_found(e):
    flash('所请求的页面不存在', 'alert-warning')
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def inernal_server_error(e):
    flash('服务器出错了，实在抱歉', 'alert-danger')
    return render_template('500.html'), 500