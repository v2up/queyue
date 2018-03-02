from . import resource

from flask import send_from_directory, current_app

@resource.route('/uploads/<path:rsc>')
def rtn_rsc(rsc):
    return send_from_directory(directory=current_app.config['UPLOADS_DEFAULT_DEST'], filename=rsc)	#获取资源文件