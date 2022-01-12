"""
This module is used for database population and defines the following:

Functions:

'populate_database': populate database with employees and departments.
"""


from departments_app import db
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from datetime import date


def populate_database():
    """
     Populates database with departments and employees.

     :return: None
    """
    example_department_1 = Department('Development', 'Epam')
    example_department_2 = Department('Advertising sales', 'Google')
    example_department_3 = Department('Financial', 'Microsoft')

    db.session.add(example_department_1)
    db.session.add(example_department_2)
    db.session.add(example_department_3)
    db.session.commit()

    example_employee_1 = Employee('James Hetfield', date(1963, 8, 3), 2100,
                                  Department.query.filter_by(department_name='Financial').first().department_id)

    example_employee_2 = Employee('Frank Sinatra', date(1915, 12, 12), 2200,
                                  Department.query.filter_by(department_name='Advertising sales').first().department_id)

    example_employee_3 = Employee('Louis Armstrong', date(1901, 8, 4), 2300,
                                  Department.query.filter_by(department_name='Development').first().department_id)

    example_employee_4 = Employee('Chuck Berry', date(1924, 10, 18), 2400,
                                  Department.query.filter_by(department_name='Financial').first().department_id)

    db.session.add(example_employee_1)
    db.session.add(example_employee_2)
    db.session.add(example_employee_3)
    db.session.add(example_employee_4)

    db.session.commit()


if __name__ == '__main__':
    db_start_data()
