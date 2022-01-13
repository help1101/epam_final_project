"""
Sources root package.

Initializes web application and web service, contains following subpackages and
modules:

Subpackages:

- 'db_data': contains module used to populate database;
- 'migrations': contains migration files used to manage database schema;
- 'models': contains modules with Python classes describing database models;
- 'service': contains modules with classes used to work with database;
- 'static': contains web application static files (styles, images);
- 'templates': contains web application html templates;
- 'views': contains modules with Python functions used to work with web application views;
- 'tests': contains modules with tests.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os


app = Flask(__name__)

# database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///department_app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# migration
migration_dir = os.path.join('departments_app', 'migrations')
migration = Migrate(app, db, migration_dir)

from .views import initiating_views

initiating_views()

from .models import department, employee

logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

if __name__ == '__main__':
    app.run()
