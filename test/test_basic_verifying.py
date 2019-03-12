import requests
from mockserver_friendly import request, response, times
from test import MOCK_SERVER_URL, MockServerClientTestCase


class TestBasicVerifying(MockServerClientTestCase):
    def test_verify_request_received_once(self):
        self.client.stub(request(), response())
        requests.get(MOCK_SERVER_URL)
        self.client.verify(request(), times(1))

    def test_verify_request_never_received(self):
        self.client.verify(request(), times(0))

    def test_verify_request_not_received_fail(self):
        with self.assertRaises(AssertionError):
            self.client.verify(request(), times(1))

    def test_verify_all_expectations(self):
        self.client.expect(request(), response(), times(1))
        requests.get(MOCK_SERVER_URL)
        self.client.verify_expectations()
