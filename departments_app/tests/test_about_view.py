from departments_app import app
from http import HTTPStatus


class TestAboutView:

    def setup(self):
        app.test_client(True)
        self.client = app.test_client()

    def test_index_page(self):
        response = self.client.get('/about')
        assert response.status_code == 200, HTTPStatus.OK
