"""
This module is used to manage employees on web application.

Module defines the following:

Functions, that defines employee views;

Variable (employees) that initiating Blueprint.
"""

from flask import render_template, Blueprint, request, redirect
from ..service.employee_service import EmployeeService
from ..service.department_service import DepartmentService

employees = Blueprint('employees_page', __name__)


@employees.route('/employees')
def render_employees():
    """
    Returns rendered 'employees.html' template for url route '/employees'

    :return: Rendered 'employees.html' template
    """
    items = EmployeeService.get_employees()
    return render_template('employees.html', items=items)


@employees.route('/employees/f1')
def render_employees_order_by_name():
    """
    Returns rendered 'employees.html' template for url route '/employees/f1'

    :return: Rendered 'employees.html' template with employees that have been ordered by employee name
    """
    items = EmployeeService.get_employees_ordered_by_name()
    return render_template('employees.html', items=items)


@employees.route('/employees/f2')
def render_employees_order_by_date_of_birth():
    """
    Returns rendered 'employees.html' template for url route '/employees/f2'

    :return: Rendered 'employees.html' template with employees that have been ordered by date of birth
    """
    items = EmployeeService.get_employees_ordered_by_date_of_birth()
    return render_template('employees.html', items=items)


@employees.route('/employees/f3')
def render_employees_order_by_salary():
    """
    Returns rendered 'employees.html' template for url route '/employees/f3'

    :return: Rendered 'employees.html' template with employees that have been ordered by salary
    """
    items = EmployeeService.get_employees_ordered_by_salary()
    return render_template('employees.html', items=items)


@employees.route('/employees/f4')
def render_employees_order_by_department():
    """
    Returns rendered 'employees.html' template for url route '/employees/f4'

    :return: Rendered 'employees.html' template with employees that have been ordered by department name
    """
    items = EmployeeService.get_employees_ordered_by_department()
    return render_template('employees.html', items=items)


@employees.route('/employee/add', methods=['POST', 'GET'])
def render_add_employee():
    """
    Returns rendered 'add_employee.html' template for url route '/employee/add'

    :return: redirects to '/employees' after successful adding

    :return: Rendered 'add_employee.html' template
    """
    select_items = DepartmentService.get_departments()
    if request.method == 'POST':
        employee_name = request.form.get('employee_name')
        employee_date_of_birth = request.form.get('employee_date_of_birth')
        employee_salary = request.form.get('employee_salary')
        department_uuid = request.form.get('department_uuid')

        try:
            EmployeeService.add_employee(employee_name, employee_date_of_birth, employee_salary, department_uuid)
            DepartmentService.calculate_avg_salary(department_uuid)
            return redirect('/employees')
        except:
            return 'Oops! An error has occurred while adding new employee.'
    return render_template('add_employee.html', select_items=select_items)


@employees.route('/employee/<string:uuid>/edit', methods=['POST', 'GET'])
def render_edit_employee(uuid: str):
    """
    Returns rendered 'edit_employee.html' template for url route '/employee/<employee UUID>/edit'

    :return: redirects to '/employees' after successful editing

    :return: Rendered 'edit_employee.html' template
    """
    select_items = DepartmentService.get_departments()
    if request.method == 'POST':
        employee_new_name = request.form.get('employee_new_name')
        employee_date_of_birth = request.form.get('employee_date_of_birth')
        employee_salary = request.form.get('employee_salary')
        employee_department = request.form.get('department_uuid')

        if not employee_new_name:
            employee_new_name = EmployeeService.get_employee_by_uuid(uuid).employee_name

        if not employee_salary:
            employee_salary = EmployeeService.get_employee_by_uuid(uuid).employee_salary

        if not employee_department:
            try:
                department = EmployeeService.get_employee_by_uuid(uuid).department_id
                employee_department = DepartmentService.get_department_by_id(department).department_uuid
            except:
                employee_department = None

        try:
            EmployeeService.update_employee(uuid, employee_new_name, employee_date_of_birth,
                                            employee_salary, employee_department)
            DepartmentService.calculate_avg_salary(employee_department)
            return redirect('/employees')
        except:
            return 'Oops! An error has occurred while editing employee.'

    return render_template('edit_employee.html', select_items=select_items)


@employees.route('/employee/<string:uuid>/del')
def render_del_employee(uuid: str):
    """
    Redirects to '/employees/<employee UUID>/del' and deletes an employee

    :return: Redirects to '/employees' successful deleting
    """
    department = EmployeeService.get_employee_by_uuid(uuid).department_id
    department_uuid = DepartmentService.get_department_by_id(department).department_uuid
    EmployeeService.delete_employee(uuid)
    DepartmentService.calculate_avg_salary(department_uuid)
    return redirect('/employees')
