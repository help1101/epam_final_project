"""
This package contains modules defining department and employee views:

Modules:

'about_view.py': defines department views;

'departments_view.py': defines department views;

'employees_view.py': defines employee views;

'main_view.py': defines homepage views.
"""

from departments_app import app
from . import main_view
from . import departments_view
from . import employees_view
from . import about_view


def initiating_views():
    app.register_blueprint(main_view.main_page)
    app.register_blueprint(departments_view.departments)
    app.register_blueprint(employees_view.employees)
    app.register_blueprint(about_view.about)
