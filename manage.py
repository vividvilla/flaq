from flaq import app, db
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

#Import models to get discovered by our app
import flaq.models

#Adding command shell for database migrations
migrate = Migrate(app, db)
manager = Manager(app)

#Initialize shell with pre imports for testing
def make_shell_context():
    return dict(
        app = app,
        db = db,
        user = flaq.models.user,
        question = flaq.models.question,
        answer = flaq.models.answer)

#Add shell command alias
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test():
    """Run unit tests(under tests folder) through commandline"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def recreatedb():
    """Drops all table and recreates everything"""
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    manager.run()