from flask_script import Manager

from app import app

# migrate = Migrate(app, db)
manager = Manager(app)



if __name__ == '__main__':
    manager.run()
