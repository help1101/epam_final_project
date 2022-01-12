"""
This module used to represent employees model and defines following:

Classes:

'Employee', employee database model.
"""

from uuid import uuid4
from departments_app import db
from .department import Department


class Employee(db.Model):
    """
    Model that represents department

    :param int employee_id: Id of an employee in database
    :param str employee_name: Name of an employee
    :param class 'datetime.date' employee_date_of_birth: Employee's birthday date
    :param int employee_salary: Salary of an employee
    :param str employee_uuid: UUID (Universal Unique Identifier) of an employee
    :param int department_id: Id of the department in database where an employee works
    :param str department_name: Name of the department where an employee works
    """

    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(50), nullable=False)
    employee_date_of_birth = db.Column(db.Date)
    employee_salary = db.Column(db.Integer)
    employee_uuid = db.Column(db.String, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    department_name = db.Column(db.String(50))

    def __init__(self, name, date_of_birth, salary, department_id):
        self.employee_name = name
        self.employee_date_of_birth = date_of_birth
        self.employee_salary = salary
        self.employee_uuid = str(uuid4())
        self.department_id = department_id
        self.department_name = Department.query.with_entities(Department.department_name).filter_by(
            department_id=self.department_id).first()[0]

    def __repr__(self):
        """
        Returns string representation of employee
        :return: String representation of employee
        """
        return f'{self.employee_name} {self.employee_date_of_birth} {self.employee_salary} {self.department_name}'
