import unittest
from server import app, db
from server.models import User
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    db.create_all()

@manager.command
def create_users():
    user = User(name='Marceli', last_name='Wydra', password='1234', username='mwydra')
    db.session.add(user)
    db.session.commit()

@manager.command
def runserver():
    app.run(port=8000)

@manager.command
def tests():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('server/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()