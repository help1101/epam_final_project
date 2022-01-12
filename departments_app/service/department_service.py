"""
This module is used to execute database queries.

Module defines the following:

Classes:

'DepartmentService', department service.
"""

from departments_app import db
from departments_app.models.department import Department
from departments_app.models.employee import Employee


class DepartmentService:
    """
    This class is used to execute database queries to department table.
    """

    @staticmethod
    def get_departments():
        """
        This method fetches all departments from the database.

        :return: List of all departments
        """
        return Department.query.all()

    @staticmethod
    def get_departments_ordered_by_name():
        """
        This method fetches all departments from the database ordered by name.

        :return: List of all departments ordered by department name.
        """
        return Department.query.order_by(Department.department_name).all()

    @staticmethod
    def get_departments_ordered_by_organisation():
        """
        This method fetches all departments from the database ordered by organisation name.

        :return: List of all departments ordered by organisation name.
        """
        return Department.query.order_by(Department.department_organisation).all()

    @staticmethod
    def get_departments_ordered_by_salary():
        """
        This method fetches all departments from the database order by descending average salary.

        :return: List of all departments ordered by descending average salary.
        """
        from sqlalchemy import desc
        return Department.query.order_by(desc(Department.avg_salary)).all()

    @staticmethod
    def get_department_by_uuid(department_uuid: str):
        """
        This method fetches department by given UUID from database.

        :param department_uuid: Received UUID (Universal Unique Identifier) of department
        :raise ValueError: If given department UUID is not in database
        :return: Department with given UUID
        """
        department = Department.query.filter_by(department_uuid=department_uuid).first()
        if department is None:
            raise ValueError('Invalid department UUID')
        return department

    @staticmethod
    def get_department_by_name(department_name: str):
        """
        This method fetches department by given department name from database.

        :param department_name: Received name of the department

        :raise ValueError: If given department name is not on database

        :return: Department with given department name
        """
        department = Department.query.filter_by(department_name=department_name).first()
        if department is None:
            raise ValueError('Invalid name of department')
        return department

    @staticmethod
    def get_department_by_id(department_id: int):
        """
        This method fetches department by given department id from database.

        :param department_id: Received id of the department

        :raise ValueError: If given department id is not in database

        :return: Department with given department id
        """
        department = Department.query.filter_by(department_id=department_id).first()

        if department is None:
            raise ValueError('Invalid department id')

        return department

    @staticmethod
    def add_department(name: str, organisation: str):
        """
        This method creates a new department and adds it to the database.

        :param name: Received department name of the new department

        :param organisation: Received organisation name of the new department

        :return: None
        """
        added_department = Department(name, organisation)

        db.session.add(added_department)
        db.session.commit()
        db.session.close()

    @staticmethod
    def update_department(department_uuid: str, new_name: str, new_organisation: str):
        """
        This method takes department from the database and updates its department name and organisation name.

        :param department_uuid: Received UUID (Universal Unique Identifier) of department

        :param new_name: Received new department name of department

        :param new_organisation: Received new organisation name of department

        :raise ValueError: If given department UUID is not in database

        :return: None
        """
        updated_department = Department.query.filter_by(department_uuid=department_uuid).first()

        if updated_department is None:
            raise ValueError('Invalid department UUID')

        updated_department.department_name = new_name
        updated_department.department_organisation = new_organisation

        db.session.add(updated_department)
        db.session.commit()
        db.session.close()

    @staticmethod
    def delete_department(department_uuid: str):
        """
        This method deletes the department from the database.

        :param department_uuid: Received UUID (Universal Unique Identifier) of department

        :raise ValueError: If given department UUID is not in database

        :return: None
        """
        deleted_department = Department.query.filter_by(department_uuid=department_uuid).first()

        if deleted_department is None:
            raise ValueError('Invalid department UUID')

        db.session.delete(deleted_department)
        db.session.commit()
        db.session.close()

    @staticmethod
    def calculate_avg_salary(department_uuid: str):
        """
        This method calculates an average salary of given department and adds the result in database.

        :param department_uuid: Received UUID (Universal Unique Identifier) of department

        :raise ValueError: If given department UUID is not in database

        :except ZeroDivisionError: If quantity of department employees equals zero

        :return: None
        """
        calculated_department = Department.query.filter_by(department_uuid=department_uuid).first()

        if calculated_department is None:
            raise ValueError('Invalid department UUID')

        department_employees = Employee.query.with_entities(Employee.employee_salary).filter_by(
            department_id=calculated_department.department_id).all()

        salaries = []

        for i in department_employees:
            for j in i:
                salaries.append(j)

        try:
            result = sum(salaries) / len(salaries)
        except ZeroDivisionError:
            result = sum(salaries)

        calculated_department.avg_salary = result

        db.session.add(calculated_department)
        db.session.commit()
        db.session.close()
