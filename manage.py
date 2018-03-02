import os

from qy import create_app

from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')	#不同的运行模式
manager = Manager(app)

def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
