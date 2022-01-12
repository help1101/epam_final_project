from departments_app import db
from datetime import date
from departments_app.models.department import Department
from departments_app.models.employee import Employee
from departments_app.service.department_service import DepartmentService


class TestDepartmentService:

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

    def test_get_departments(self):
        assert Department.query.all() == DepartmentService.get_departments()

    def test_get_departments_ordered_by_name(self):
        assert Department.query.order_by(
            Department.department_name).all() == DepartmentService.get_departments_ordered_by_name()

    def test_get_departments_ordered_by_organisation(self):
        assert Department.query.order_by(
            Department.department_organisation).all() == DepartmentService.get_departments_ordered_by_name()

    def test_get_departments_ordered_by_salary(self):
        from sqlalchemy import desc

        assert Department.query.order_by(
            desc(Department.avg_salary)).all() == DepartmentService.get_departments_ordered_by_salary()

    def test_get_department_by_uuid(self):
        for i in Department.query.all():
            assert i == Department.query.filter_by(department_uuid=i.department_uuid).first()

    def test_get_department_by_name(self):
        for i in Department.query.all():
            assert i == Department.query.filter_by(department_name=i.department_name).first()

    def test_get_department_by_id(self):
        for i in Department.query.all():
            assert i == Department.query.filter_by(department_id=i.department_id).first()

    def test_add_department(self):
        test_name = 'Test_name1'
        test_org = 'Test_org1'
        result = []

        DepartmentService.add_department(test_name, test_org)
        test_dep = Department.query.filter_by(department_name=test_name).first()
        result.append(test_dep.department_name)
        result.append(test_dep.department_organisation)

        assert [test_name, test_org] == result

    def test_update_department(self):
        departments_list = []
        new_name = 'Test_name'
        new_org = 'Test_org'
        uuid = []
        for i in Department.query.all():
            departments_list.append(i)
            uuid.append(i.department_uuid)

        counter = 0
        for i in uuid:
            counter += 1
            DepartmentService.update_department(i, f'Test_name{counter}', f'Test_org{counter}')

        departments_list = []

        for i in Department.query.with_entities(Department.department_name, Department.department_organisation).all():
            departments_list.append(list(i))

        counter = 0
        for i in departments_list:
            counter += 1
            assert i == [new_name + str(counter), new_org + str(counter)]

    def test_delete_department(self):
        uuid = []
        for i in Department.query.all():
            uuid.append(i.department_uuid)

        for i in uuid:
            DepartmentService.delete_department(i)
            assert Department.query.filter_by(department_uuid=i).first() is None

    def test_calculate_avg_salary(self):
        department_list = []
        uuid = []
        result = []
        salaries = [[2500, 2200, 2100], [2400, 2300]]
        for i in salaries:
            result.append(sum(i) / len(i))

        for i in Department.query.all():
            department_list.append(i)
            uuid.append(i.department_uuid)

        for i in uuid:
            DepartmentService.calculate_avg_salary(i)

        department_list = []

        for i in Department.query.with_entities(Department.avg_salary).all():
            department_list.append(*i)

        for i in range(len(result)):
            assert result[i] == department_list[i]

    @staticmethod
    def teardown():
        departments = Department.query.all()

        for i in departments:
            db.session.delete(i)
            db.session.commit()

        db.session.close()

        print('\ntest data has been deleted')
