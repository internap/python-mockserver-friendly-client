import unittest

from mockserver_friendly import _to_delay, seconds, milliseconds, microseconds, nanoseconds, minutes, \
    hours, days


class TestJsonResponse(unittest.TestCase):
    def test_default_delay_is_seconds(self):
        payload = _to_delay(10)
        self.assertEqual(payload, {"timeUnit": "SECONDS", "value": 10})

    def test_seconds(self):
        payload = _to_delay(seconds(10))
        self.assertEqual(payload, {"timeUnit": "SECONDS", "value": 10})

    def test_milliseconds(self):
        payload = _to_delay(milliseconds(10))
        self.assertEqual(payload, {"timeUnit": "MILLISECONDS", "value": 10})

    def test_microseconds(self):
        payload = _to_delay(microseconds(10))
        self.assertEqual(payload, {"timeUnit": "MICROSECONDS", "value": 10})

    def test_nanoseconds(self):
        payload = _to_delay(nanoseconds(10))
        self.assertEqual(payload, {"timeUnit": "NANOSECONDS", "value": 10})

    def test_minutes(self):
        payload = _to_delay(minutes(10))
        self.assertEqual(payload, {"timeUnit": "MINUTES", "value": 10})

    def test_hours(self):
        payload = _to_delay(hours(10))
        self.assertEqual(payload, {"timeUnit": "HOURS", "value": 10})

    def test_days(self):
        payload = _to_delay(days(10))
        self.assertEqual(payload, {"timeUnit": "DAYS", "value": 10})
