import collections
import json

import requests


class MockServerClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.expectations = []

    def _call(self, command, data=None):
        return requests.put("{}/{}".format(self.base_url, command), data=data)

    def reset(self):
        self.expectations = []
        self._call("reset")

    def stub(self, request, response, timing=None):
        self._call("expectation", json.dumps({
            "httpRequest": request,
            "httpResponse": response,
            "times": (timing or _Timing()).for_expectation()
        }))

    def expect(self, request, response, timing):
        self.stub(request, response, timing)
        self.expectations.append((request, timing))

    def verify(self):
        for req, timing in self.expectations:
            result = self._call("verify", json.dumps({
                "httpRequest": req,
                "times": timing.for_verification()
            }))
            assert result.status_code == 202, result.content.decode('UTF-8').replace('\n', '\r\n')


def request(method=None, path=None, querystring=None, body=None, headers=None):
    return _non_null_options_to_json(
        _Option("method", method),
        _Option("path", path),
        _Option("queryStringParameters", querystring, formatter=_to_named_values_list),
        _Option("body", body),
        _Option("headers", headers, formatter=_to_named_values_list)
    )


def response(code=None, body=None, headers=None):
    return _non_null_options_to_json(
        _Option("statusCode", code),
        _Option("body", body),
        _Option("headers", headers, formatter=_to_named_values_list)
    )


def times(count):
    return _Timing(count)


def form(form):
    # NOTE(lindycoder): Support for mockservers version before https://github.com/jamesdbloom/mockserver/issues/371
    return collections.OrderedDict((("type", "PARAMETERS"), ("parameters", _to_named_values_list(form))))


def json_response(code=None, body=None, headers=None):
    headers = (headers or {})
    headers["Content-Type"] = "application/json"
    return response(code, json.dumps(body), headers)


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


def _non_null_options_to_json(*options):
    return {o.field: o.formatter(o.value) for o in options if o.value is not None}


def _to_named_values_list(dictionary):
    return [{"name": key, "values": [value]} for key, value in dictionary.items()]
