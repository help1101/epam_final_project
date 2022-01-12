from departments_app import db
from datetime import date
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from departments_app.service.employee_service import EmployeeService


class TestEmployeeService:

    @staticmethod
    def setup():
        department1 = Department('test_dep1', 'test_org1')
        department2 = Department('test_dep2', 'test_org2')

        db.session.add(department1)
        db.session.add(department2)

        db.session.commit()

        employee1 = Employee('test_employee1', date(1999, 9, 9), 2500, 1)
        employee2 = Employee('test_employee2', date(1990, 1, 2), 2400, 2)
        employee3 = Employee('test_employee3', date(1992, 4, 3), 2300, 2)
        employee4 = Employee('test_employee4', date(1991, 1, 8), 2200, 1)
        employee5 = Employee('test_employee1', date(1998, 5, 6), 2100, 1)

        db.session.add(employee1)
        db.session.add(employee2)
        db.session.add(employee3)
        db.session.add(employee4)
        db.session.add(employee5)

        db.session.commit()
        db.session.close()

        print('test data has been created')

    def test_get_employees(self):
        assert Employee.query.all() == EmployeeService.get_employees()

    def test_get_employees_ordered_by_name(self):
        assert Employee.query.order_by(Employee.employee_name).all() == EmployeeService.get_employees_ordered_by_name()

    def test_get_employees_ordered_by_date_of_birth(self):
        assert Employee.query.order_by(
            Employee.employee_date_of_birth).all() == EmployeeService.get_employees_ordered_by_date_of_birth()

    def test_get_employees_ordered_by_salary(self):
        from sqlalchemy import desc
        assert Employee.query.order_by(
            desc(Employee.employee_salary)).all() == EmployeeService.get_employees_ordered_by_salary()

    def test_get_employees_ordered_by_department(self):
        assert Employee.query.order_by(
            Employee.department_name).all() == EmployeeService.get_employees_ordered_by_department()

    def test_get_employee_by_uuid(self):
        employees = Employee.query.all()

        for i in employees:
            assert Employee.query.filter_by(
                employee_uuid=i.employee_uuid).first() == EmployeeService.get_employee_by_uuid(i.employee_uuid)

    def test_get_employee_by_name(self):
        employees = Employee.query.all()
        for i in employees:
            assert Employee.query.filter_by(
                employee_name=i.employee_name).first() == EmployeeService.get_employee_by_name(i.employee_name)

    def test_add_employee(self):
        test_name = 'new_test_employee_name'
        test_date = '2000-01-01'
        test_salary = 20000
        test_dep = Department.query.first().department_uuid

        EmployeeService.add_employee(test_name, test_date, test_salary, test_dep)

        test_employee = Employee.query.filter_by(employee_name=test_name, employee_salary=test_salary).first()

        result = [test_employee.employee_name, test_employee.employee_salary, test_employee.department_id]

        assert [test_name, test_salary, Department.query.first().department_id] == result

    def test_update_employee(self):
        new_test_name = 'test_employee_name'
        new_test_date = '2000-01-01'
        new_test_salary = 20000
        employees_uuid = []
        department_uuid = []
        dep_id = []
        for i in Employee.query.all():
            employees_uuid.append(i.employee_uuid)

        for i in Department.query.all():
            department_uuid.append(i.department_uuid)
            dep_id.append(i.department_id)

        department_uuid = department_uuid[0]

        counter = 0
        for i in employees_uuid:
            counter += 1
            EmployeeService.update_employee(i, f'{new_test_name}{counter}', new_test_date, new_test_salary,
                                            department_uuid)

        departments = []

        for i in Employee.query.with_entities(Employee.employee_name,
                                              Employee.employee_salary, Employee.department_id).all():
            departments.append(list(i))

        counter = 0
        for i in departments:
            counter += 1
            assert [new_test_name + f'{counter}', new_test_salary, dep_id[0]] == i

    def test_delete_employee(self):
        uuid = []
        for i in Employee.query.all():
            uuid.append(i.employee_uuid)

        for i in uuid:
            EmployeeService.delete_employee(i)
            assert Employee.query.filter_by(employee_uuid=i).first() is None

    @staticmethod
    def teardown():
        departments = Department.query.all()

        for i in departments:
            db.session.delete(i)
            db.session.commit()

        db.session.close()

        print('\ntest data has been deleted')
