import collections
import json
import requests


class MockServerClient(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.expectations = []

    def _call(self, command, data=None):
        return requests.put("{}/{}".format(self.base_url, command), data=data)

    def reset(self):
        self.expectations = []
        self._call("reset")

    def stub(self, request, response, timing=None, time_to_live=None):
        self._call("expectation", json.dumps(_non_null_options_to_dict(
            _Option("httpRequest", request),
            _Option("httpResponse", response),
            _Option("times", (timing or _Timing()).for_expectation()),
            _Option("timeToLive", time_to_live, formatter=_to_time_to_live)
        )))

    def expect(self, request, response, timing, time_to_live=None):
        self.stub(request, response, timing, time_to_live)
        self.expectations.append((request, timing))

    def verify(self):
        for req, timing in self.expectations:
            result = self._call("verify", json.dumps({
                "httpRequest": req,
                "times": timing.for_verification()
            }))
            assert result.status_code == 202, result.content.decode('UTF-8').replace('\n', '\r\n')


def request(method=None, path=None, querystring=None, body=None, headers=None, cookies=None):
    return _non_null_options_to_dict(
        _Option("method", method),
        _Option("path", path),
        _Option("queryStringParameters", querystring, formatter=_to_named_values_list),
        _Option("body", body),
        _Option("headers", headers, formatter=_to_named_values_list),
        _Option("cookies", cookies)
    )


def response(code=None, body=None, headers=None, cookies=None, delay=None):
    return _non_null_options_to_dict(
        _Option("statusCode", code),
        _Option("body", body),
        _Option("headers", headers, formatter=_to_named_values_list),
        _Option("delay", delay, formatter=_to_delay),
        _Option("cookies", cookies)
    )


def times(count):
    return _Timing(count)


def form(form):
    # NOTE(lindycoder): Support for mockservers version before https://github.com/jamesdbloom/mockserver/issues/371
    return collections.OrderedDict((("type", "PARAMETERS"), ("parameters", _to_named_values_list(form))))


def json_equals(payload):
    """Expects that the request payload is equal to the given payload."""
    return collections.OrderedDict((("type", "JSON"), ("json", json.dumps(payload)), ("matchType", "STRICT")))


def json_contains(payload):
    """Expects the request payload to match all given fields. The request may has more fields."""
    return collections.OrderedDict(
        (("type", "JSON"), ("json", json.dumps(payload)), ("matchType", "ONLY_MATCHING_FIELDS")))


def json_response(body=None, headers=None, **kwargs):
    headers = (headers or {})
    headers["Content-Type"] = "application/json"
    return response(body=json.dumps(body), headers=headers, **kwargs)


class _Option:
    def __init__(self, field, value, formatter=None):
        self.field = field
        self.value = value
        self.formatter = formatter or (lambda e: e)


class _Timing:
    def __init__(self, count=None):
        self.count = count

    def for_expectation(self):
        if self.count:
            return {"remainingTimes": self.count, "unlimited": False}
        else:
            return {"unlimited": True}

    def for_verification(self):
        return {"exact": True, "count": self.count}


class _Time:
    def __init__(self, unit, value):
        self.unit = unit
        self.value = value


def seconds(value):
    return _Time("SECONDS", value)


def milliseconds(value):
    return _Time("MILLISECONDS", value)


def microseconds(value):
    return _Time("MICROSECONDS", value)


def nanoseconds(value):
    return _Time("NANOSECONDS", value)


def minutes(value):
    return _Time("MINUTES", value)


def hours(value):
    return _Time("HOURS", value)


def days(value):
    return _Time("DAYS", value)


def _non_null_options_to_dict(*options):
    return {o.field: o.formatter(o.value) for o in options if o.value is not None}


def _to_named_values_list(dictionary):
    return [{"name": key, "values": [value]} for key, value in dictionary.items()]


def _to_time(value):
    if not isinstance(value, _Time):
        value = seconds(value)
    return value


def _to_delay(delay):
    delay = _to_time(delay)
    return {
        "timeUnit": delay.unit,
        "value": delay.value
    }


def _to_time_to_live(time):
    time = _to_time(time)
    return {
        "timeToLive": time.value,
        "timeUnit": time.unit,
        "unlimited": False
    }
