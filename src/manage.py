import os
import unittest
from flask_migrate import MigrateCommand
from flask_script import Manager

from main import create_app


app = create_app(os.getenv('APP_ENV') or 'dev')
app.app_context().push()

manager = Manager(app)
manager.add_command("db", MigrateCommand)

@manager.command
def run():
    app.run()


@manager.command
def test():
    """Run the unit tests"""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()