import time

import requests
from mockserver_friendly import request, response, milliseconds
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicResponses(MockServerClientTestCase):
    def test_code_response(self):
        self.client.stub(
            request(),
            response(code=418)
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.status_code, 418)

    def test_reason_phrase_response(self):
        reason_phrase = "Custom reasonPhrase"
        self.client.stub(
            request(),
            response(reason=reason_phrase)
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.reason, reason_phrase)

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

    def test_cookies_response(self):
        self.client.stub(
            request(),
            response(cookies={"i-am-cookie": "sweet-cookie"})
        )

        result = requests.get(MOCK_SERVER_URL)
        self.assertEqual(result.cookies["i-am-cookie"], "sweet-cookie")

    def test_delay_response(self):
        self.client.stub(
            request(),
            response(delay=1)
        )

        start = time.time()
        requests.get(MOCK_SERVER_URL)
        elapsed = time.time() - start
        self.assertGreater(elapsed, 1)

    def test_delay_response_with_special_unit(self):
        self.client.stub(
            request(),
            response(delay=milliseconds(500))
        )

        start = time.time()
        requests.get(MOCK_SERVER_URL)
        elapsed = time.time() - start
        self.assertGreater(elapsed, 0.5)
