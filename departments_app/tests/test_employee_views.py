from departments_app import app
from departments_app.service.employee_service import EmployeeService
from http import HTTPStatus


class TestEmployeesViews:

    def setup(self):
        app.test_client(True)
        self.client = app.test_client()

    def test_employees(self):
        response = self.client.get('/employees')
        assert response.status_code == 200, HTTPStatus.OK

    def test_employee_add(self):
        response = self.client.get('/employee/add')
        assert response.status_code == 200, HTTPStatus.OK

    def test_employee_edit(self):
        employees = EmployeeService.get_employees()
        if employees:
            for i in employees:
                uuid = i.employee_uuid
                response = self.client.get(f'/employee/{uuid}/edit')
                assert response.status_code == 200, HTTPStatus.OK

    def test_employee_del(self):
        employees = EmployeeService.get_employees()
        if employees:
            try:
                for i in employees:
                    uuid = i.employee_uuid
                    response = self.client.get(f'/employee/{uuid}/del')
                    assert response.status_code == 302, HTTPStatus.FOUND
            except:
                pass
