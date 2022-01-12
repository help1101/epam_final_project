"""
This module is used to manage departments on web application.

Module defines the following:

Functions, that defines department views;

Variable (departments) that initiating Blueprint.
"""

from flask import render_template, Blueprint, request, redirect
from ..service.department_service import DepartmentService
from ..service.employee_service import EmployeeService

departments = Blueprint('departments_page', __name__)


@departments.route('/departments')
def render_departments():
    """
    Returns rendered 'departments.html' template for url route '/departments'

    :return: Rendered 'departments.html' template
    """
    items = DepartmentService.get_departments()
    return render_template('departments.html', items=items)


@departments.route('/departments/f1')
def render_departments_order_by_name():
    """
    Returns rendered 'departments.html' template for url route '/departments/f1'

    :return: Rendered 'departments.html' template with departments that have been ordered by department name
    """
    items = DepartmentService.get_departments_ordered_by_name()
    return render_template('departments.html', items=items)


@departments.route('/departments/f2')
def render_departments_order_by_organisation():
    """
    Returns rendered 'departments.html' template for url route '/departments/f2'

    :return: Rendered 'departments.html' template with departments that have been ordered by organisation name
    """
    items = DepartmentService.get_departments_ordered_by_organisation()
    return render_template('departments.html', items=items)


@departments.route('/departments/f3')
def render_departments_filter3():
    """
    Returns rendered 'departments.html' template for url route '/departments/f3'

    :return: Rendered 'departments.html' template with departments that have been ordered by average salary
    """
    items = DepartmentService.get_departments_ordered_by_salary()
    return render_template('departments.html', items=items)


@departments.route('/department/<string:uuid>/<string:f>')
def render_department(uuid: str, f: str):
    """
    Returns rendered 'department.html' template for url route '/department/f0'

    :return: Rendered 'department.html' template with employees that have been ordered by name, salary or date of birth
    """
    employee_list = []
    department = DepartmentService.get_department_by_uuid(uuid)
    if f == 'f0':
        employees = EmployeeService.get_employees()
    elif f == 'f1':
        employees = EmployeeService.get_employees_ordered_by_name()
    elif f == 'f2':
        employees = EmployeeService.get_employees_ordered_by_salary()
    elif f == 'f3':
        employees = EmployeeService.get_employees_ordered_by_date_of_birth()

    for i in employees:
        if i.department_id == department.department_id:
            employee_list.append(i)
    number_of_employees = len(employee_list)

    return render_template('department.html', department=department, employee_list=employee_list,
                           number_of_employees=number_of_employees)


@departments.route('/department/add', methods=['POST', 'GET'])
def render_add_department():
    """
    Returns rendered 'add_department.html' template for url route '/department/add'

    :return: Redirects to '/departments' after successful adding

    :return: Rendered 'add_department.html' template
    """
    if request.method == 'POST':
        department_name = request.form.get('department_name')
        department_organisation = request.form.get('department_organisation')
        try:
            DepartmentService.add_department(department_name, department_organisation)
            return redirect('/departments')
        except:
            return 'Oops! An error has occurred while adding a department'
    return render_template('add_department.html')


@departments.route('/department/<string:uuid>/edit', methods=['POST', 'GET'])
def render_edit_department(uuid: str):
    """
    Returns rendered 'edit_department.html' template for url route '/department/<department UUID>/edit'

    :return: Redirects to '/departments' after successful editing

    :return: Rendered 'edit_department.html' template
    """
    if request.method == 'POST':
        new_department_name = request.form.get('department_name')
        new_department_org = request.form.get('department_org')

        try:
            DepartmentService.update_department(uuid, new_department_name,
                                                new_department_org)
            return redirect('/departments')
        except:
            return 'Oops! An error has occurred while editing department.'

    return render_template('edit_department.html')


@departments.route('/department/<string:uuid>/del')
def render_del_department(uuid: str):
    """
    Redirects to '/departments/<department UUID>/del' and deletes department

    :return: Redirects to '/departments' successful deleting
    """
    DepartmentService.delete_department(uuid)
    return redirect('/departments')
