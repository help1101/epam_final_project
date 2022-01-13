from setuptools import setup

setup(
    name='Departments app project',
    version='1.0',
    description='Web application to manage departments and employees.',
    author='Mykola Kutsenko',
    author_email='kucenko1998@gmail.com',
    url='https://github.com/help1101/epam_final_project',
    packages=['departments_app', 'departments_app.views', 'departments_app.models', 'departments_app.service']
)
