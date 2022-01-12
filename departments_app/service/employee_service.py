"""
This module is used to execute database queries.

Module defines the following:

Classes:

'EmployeeService', employee service.
"""

from departments_app import db
from departments_app.models.employee import Employee
from departments_app.models.department import Department
from datetime import date


class EmployeeService:
    """
    This class is used to execute database queries to employee table.
    """

    @staticmethod
    def get_employees():
        """
        This method fetches all employees from the database.

        :return: List of all employees
        """
        return Employee.query.all()

    @staticmethod
    def get_employees_ordered_by_name():
        """
        This method fetches all employees from the database ordered by name.

        :return: List of all employees ordered by department name.
        """
        return Employee.query.order_by(Employee.employee_name).all()

    @staticmethod
    def get_employees_ordered_by_date_of_birth():
        """
        This method fetches all employees from the database ordered by their date of birth.

        :return: List of all employees ordered by their date of birth.
        """
        return Employee.query.order_by(Employee.employee_date_of_birth).all()

    @staticmethod
    def get_employees_ordered_by_salary():
        """
        This method fetches all employees from the database order by descending salary.

        :return: List of all employees ordered by descending salary.
        """
        from sqlalchemy import desc
        return Employee.query.order_by(desc(Employee.employee_salary)).all()

    @staticmethod
    def get_employees_ordered_by_department():
        """
        This method fetches all employees from the database ordered by department name.

        :return: List of all employees ordered by department department name.
        """
        return Employee.query.order_by(Employee.department_name).all()

    @staticmethod
    def get_employee_by_uuid(uuid: str):
        """
        This method fetches an employee by given UUID from database.

        :param uuid: Received UUID (Universal Unique Identifier) of employee

        :raise ValueError: If given employee UUID is not in database

        :return: Employee with given UUID
        """
        employee = Employee.query.filter_by(employee_uuid=uuid).first()
        if employee is None:
            raise ValueError('Invalid employee UUID')
        return employee

    @staticmethod
    def get_employee_by_name(name: str):
        return Employee.query.filter_by(employee_name=name).first()

    @staticmethod
    def add_employee(name: str, date_of_birth: str, salary: str, department_uuid: str):
        """
        This method creates a new employee and adds it to the database.

        :param name: Received name of a new employee

        :param date_of_birth: Received date of birth of a new employee

        :param salary: Received salary of new a employee

        :param department_uuid: Received UUID (Universal Unique Identifier) of department

        :return: None
        """
        date_list = []
        for i in date_of_birth.split('-'):
            date_list.append(int(i))
        date_of_birth = date(date_list[0], date_list[1], date_list[2])
        department_id = Department.query.filter_by(department_uuid=department_uuid).first().department_id
        added_employee = Employee(name, date_of_birth, salary, department_id)

        db.session.add(added_employee)
        db.session.commit()
        db.session.close()

    @staticmethod
    def update_employee(uuid: str, new_name: str, new_date_of_birth: str, new_salary: str, new_department_uuid: str):
        """
        This method takes the employee from the database and updates its name, date of birth, salary, department.

        :param uuid: Received UUID (Universal Unique Identifier) of an employee

        :param new_name: Received new name of an employee

        :param new_date_of_birth: Received date of birth of a new employee

        :param new_salary: Received new salary of new an employee

        :param new_department_uuid: Received UUID (Universal Unique Identifier) of department

        :raise ValueError: If given employee UUID is not in database

        :return: None
        """
        updated_employee = Employee.query.filter_by(employee_uuid=uuid).first()

        if updated_employee is None:
            raise ValueError('Invalid employee UUID')

        date_list = []

        if new_date_of_birth:
            for i in new_date_of_birth.split('-'):
                date_list.append(int(i))
            new_date_of_birth = date(date_list[0], date_list[1], date_list[2])
        else:
            new_date_of_birth = updated_employee.employee_date_of_birth

        updated_employee.employee_name = new_name
        updated_employee.employee_date_of_birth = new_date_of_birth
        updated_employee.employee_salary = new_salary

        new_department = Department.query.filter_by(department_uuid=new_department_uuid).first()

        if updated_employee.department_id and updated_employee.department_name:
            updated_employee.department_id = new_department.department_id
            updated_employee.department_name = new_department.department_name
        else:
            updated_employee.department_id = None
            updated_employee.department_name = None

        db.session.add(updated_employee)
        db.session.commit()
        db.session.close()

    @staticmethod
    def delete_employee(uuid: str):
        """
        This method deletes the employee from the database.

        :param uuid: Received UUID (Universal Unique Identifier) of an employee

        :raise ValueError: If given employee UUID is not in database

        :return: None
        """
        deleted_employee = Employee.query.filter_by(employee_uuid=uuid).first()

        if deleted_employee is None:
            raise ValueError('Invalid employee UUID')

        db.session.delete(deleted_employee)
        db.session.commit()
        db.session.close()
