import requests
from mockserver_friendly import request, response, form
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestFormRequests(MockServerClientTestCase):
    def test_form_request(self):
        self.client.stub(
            request(body=form({
                "a": "b",
                "c[0]": "d"
            })),
            response()
        )

        result = requests.post(MOCK_SERVER_URL, data={"a": "b"})
        self.assertEqual(result.status_code, 404)

        result = requests.post(MOCK_SERVER_URL, data={"a": "b", "c[0]": "d"})
        self.assertEqual(result.status_code, 200)
