from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from monarch.app import create_app
from monarch.corelibs.store import db

application = create_app('monarch')
application.config['DEBUG'] = True

manager = Manager(application)
migrate = Migrate(application, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
