# -*- coding: utf-8 -*-

"""


created: 2017-05-31

by: Yr
"""
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import User, Result

app = create_app(os.getenv('ATOMPAI_CONFIG') or 'development')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """
    为shell命令添加上下文
    注册程序,数据库实例,模型,使得这些对象能直接导入shell
    :return:
    """
    return dict(app=app, db=db, User=User, Result=Result)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    # manager.run()
    app.run(host='172.11.30.21', port=8006, threaded=True)
