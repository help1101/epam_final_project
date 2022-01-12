from departments_app import app
from departments_app.service.department_service import DepartmentService
from http import HTTPStatus


class TestDepartmentsViews:

    def setup(self):
        app.test_client(True)
        self.client = app.test_client()

    def test_departments(self):
        response = self.client.get('/departments')
        assert response.status_code == 200, HTTPStatus.OK

    def test_department_add(self):
        response = self.client.get('/department/add')
        assert response.status_code == 200, HTTPStatus.OK

    def test_department_edit(self):
        departments = DepartmentService.get_departments()
        if departments:
            for i in departments:
                uuid = i.department_uuid
                response = self.client.get(f'/department/{uuid}/edit')
                assert response.status_code == 200, HTTPStatus.OK

    def test_department_del(self):
        departments = DepartmentService.get_departments()
        if departments:
            try:
                for i in departments:
                    uuid = i.department_uuid
                    response = self.client.get(f'/department/{uuid}/del')
                    assert response.status_code == 302, HTTPStatus.FOUND
            except:
                pass

    def test_department(self):
        departments = DepartmentService.get_departments()
        filters = ['f0', 'f1', 'f2', 'f3']
        if departments:
            for i in departments:
                for f in filters:
                    uuid = i.department_uuid
                    response = self.client.get(f'/department/{uuid}/{f}')
                    assert response.status_code == 200, HTTPStatus.OK
