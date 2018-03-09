import requests
from mockserver import request, response
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicResponses(MockServerClientTestCase):
    def test_code_response(self):
        self.client.stub(
            request(),
            response(code=418)
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 418)

    def test_body_response(self):
        self.client.stub(
            request(),
            response(body="hey there")
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.content.decode(), "hey there")

    def test_headers_response(self):
        self.client.stub(
            request(),
            response(headers={"i-like": "i-like"})
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.headers["i-like"], "i-like")
