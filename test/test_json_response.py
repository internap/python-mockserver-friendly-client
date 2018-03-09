import requests
from mockserver import request, json_response
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestJsonResponse(MockServerClientTestCase):
    def test_simple_body(self):
        self.client.stub(
            request(),
            json_response(code=207, body={"pay": {"lo": "ad"}})
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 207)
        self.assertEqual(result.json(), {"pay": {"lo": "ad"}})
        self.assertEqual(result.headers["Content-Type"], "application/json")

    def test_content_type_header_is_added_to_specified(self):
        self.client.stub(
            request(),
            json_response(body={"pay": {"lo": "ad"}}, headers={"i-like": "i-like"})
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.headers["i-like"], "i-like")
        self.assertEqual(result.headers["Content-Type"], "application/json")
