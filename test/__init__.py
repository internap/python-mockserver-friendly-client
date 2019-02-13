import time
import unittest
from contextlib import contextmanager

from mockserver_friendly import MockServerFriendlyClient

MOCK_SERVER_URL = "http://localhost:1080"


class MockServerClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MockServerFriendlyClient(MOCK_SERVER_URL)

    def tearDown(self):
        with mock_server_breathing():
            self.client.reset()


@contextmanager
def mock_server_breathing():
    time.sleep(0.1)
    yield
    time.sleep(0.1)
