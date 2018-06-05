import requests
from mockserver import request, response, times
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicStubbing(MockServerClientTestCase):
    def test_catch_all(self):
        self.client.stub(
            request(),
            response()
        )

        result = requests.get(MOCK_SERVER_URL + "/whatever")
        self.assertEqual(result.status_code, 200)

    def test_path_stubbing(self):
        self.client.stub(
            request(path="/path"),
            response(code=200)
        )

        result = requests.get(MOCK_SERVER_URL + "/whatrver")
        self.assertEqual(result.status_code, 404)

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

    def test_method_stubbing(self):
        self.client.stub(
            request(method="POST"),
            response(code=200)
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 404)

        result = requests.post(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 200)

    def test_querystring_stubbing(self):
        self.client.stub(
            request(querystring={"a": "b", "c[0]": "d"}),
            response(code=200)
        )

        result = requests.get(MOCK_SERVER_URL + "/?e=f")
        self.assertEqual(result.status_code, 404)

        result = requests.get(MOCK_SERVER_URL + "/?a=b&c[0]=d")
        self.assertEqual(result.status_code, 200)

    def test_body_stubbing(self):
        self.client.stub(
            request(body="hey there"),
            response(code=200)
        )

        result = requests.post(MOCK_SERVER_URL, data="sup?")
        self.assertEqual(result.status_code, 404)

        result = requests.post(MOCK_SERVER_URL, data="hey there")
        self.assertEqual(result.status_code, 200)

    def test_headers_stubbing(self):
        self.client.stub(
            request(headers={"i-am-special": "yeah you are"}),
            response(code=200)
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 404)

        result = requests.get(MOCK_SERVER_URL, headers={"i-am-special": "yeah you are"})
        self.assertEqual(result.status_code, 200)

    def test_cookies_stubbing(self):
        self.client.stub(
            request(cookies={"i-am-cookie": "sweet-cookie"}),
            response(code=200)
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 404)

        result = requests.get(MOCK_SERVER_URL, cookies={"i-am-cookie": "sweet-cookie"})
        self.assertEqual(result.status_code, 200)

    def test_count_stubbing(self):
        self.client.stub(
            request(),
            response(),
            times(1)
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 404)

    def test_default_count_for_stubs_is_unlimited(self):
        self.client.stub(
            request(),
            response()
        )

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)

        result = requests.get(MOCK_SERVER_URL + "/path")
        self.assertEqual(result.status_code, 200)
