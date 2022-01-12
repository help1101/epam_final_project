"""
This module used to represent departments model and defines following:

Classes:

'Department', department database model.
"""

from uuid import uuid4
from departments_app import db


class Department(db.Model):
    """
    Model that represents department

    :param int department_id: Id of the department in database
    :param str department_name: Name of the department
    :param str department_organisation: Organisation that owns the department
    :param str department_uuid: UUID (Universal Unique Identifier) of department
    :param float avg_salary: Average salary of the department
    :param employees: Employees that work in the department
    """

    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50))
    department_organisation = db.Column(db.String(50))
    department_uuid = db.Column(db.String, unique=True)
    avg_salary = db.Column(db.FLOAT)
    employees = db.relationship('Employee', cascade="all,delete", backref='department')

    def __init__(self, name: str, organisation: str):
        self.department_name = name
        self.department_organisation = organisation
        self.department_uuid = str(uuid4())
        self.avg_salary = 0

    def __repr__(self):
        """
        Returns string representation of department
        :return: String representation of department
        """
        return f'{self.department_name} {self.department_organisation} {self.avg_salary}'
