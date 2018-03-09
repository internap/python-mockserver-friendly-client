import unittest

from mockserver import MockServerClient
from retry import retry

MOCK_SERVER_URL = "http://localhost:1080"


class MockServerClientTestCase(unittest.TestCase):
    @retry(tries=10, delay=0.5)
    def setUp(self):
        self.client = MockServerClient(MOCK_SERVER_URL)
        self.client.reset()
