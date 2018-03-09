# MockServer Python Client

[![Build Status](https://travis-ci.org/internap/python-mockserver-client.svg?branch=master)](https://travis-ci.org/internap/python-mockserver-client)

Python client to James D. Bloom's awesome MockServer : http://www.mock-server.com/

## Philosophy

Tests should be readable and Mock Server is already very complete and customizable.  This library tries to keep it
simple and straight-forward using python's kwargs to avoid big declarations.

We think a mock should be able to fit into one 120 char line of code should the expectation be simple enough :) 

```
client.stub(request(method="GET", path="/auth"), response(code=401, body="unauthorized"))
```

## Installation

WARNING: **THIS IS A VERY EARLY VERSION THE API IS MOST LIKELY TO CHANGE**

From source:

```
git clone https://github.com/internap/python-mockserver-client.git
cd python-mockserver-client
python setup.py install
```

From [PyPi](https://pypi.python.org/pypi/kubernetes/) directly:

```
pip install mockserver-client
```

## Prerequisite

You need a running MockServer running, see http://www.mock-server.com/mock_server/getting_started.html#start_mockserver

This project's tests uses the docker image : https://github.com/internap/python-mockserver-client/blob/master/docker-compose.yml

## Usage

**The whole Mock Server API is not all covered**. We just implemented what we needed, if you need something not yet
implemented you can open an issue and/or contribute

### *Stubbing*

(For when you are testing what your code *DOES* with another component's data)

```
from mockserver import MockServerClient, request, response

client = MockServerClient("http://localhost:1080")

client.stub(
    request(method="GET", path="/that/thing", querystring={"is": "good"}, headers={"so": "good"}),
    response(code=418, body="i'm a teapot", headers={"hi": "haa"})
)
```

* You can also add a `times(N)` as a third parameter to limit how many times this stub can be called, default is unlimited
* All parameters are always optional.  When not specified, the match everything.

### *Expecting*

(For when calling another component *IS* what you are testing)

Using the `expect` will remember the request and verify it when `verify` is called.

```
import json
from mockserver import MockServerClient, request, response, times

client = MockServerClient("http://localhost:1080")

client.expect(
    request(method="POST", path="/postme", body=json.dumps({"some": "json"})),
    response(code=204, body=json.dumps({"return": "something"}), headers={"Content-Type": "application/json"}),
    times(1)
)

client.verify()  # AssertionError !
```

* The `times(N)` parameter is mandatory for expect

### *Resetting*

(Because tests shouldn't impact each other)

```
from mockserver import MockServerClient

client = MockServerClient("http://localhost:1080")

client.reset()
```

## Customizing and shortcuts

This client consumes Mock Server's REST API : https://app.swaggerhub.com/apis/jamesdbloom/mock-server-openapi

Here's a few shortcuts already ready, there may be more to come

### Mocking a form post

```
from mockserver import MockServerClient, request, response, form

client = MockServerClient("http://localhost:1080")

client.stub(
    request(method="POST", body=form({"user": "foo", "pass": "bar"})),
    response(code=201)
)
```

This currently takes a 1 level `dict`. For array mocking, use `{"key[index]": "value"}` 

### Returning JSON

```
from mockserver import MockServerClient, request, json_response

client = MockServerClient("http://localhost:1080")

client.stub(
    request(path="/stuff"),
    json_response(code=200, body={"full": "json", "structure": ["with", "stuff", 1]})
)
```

This automatically dumps the body in json and appends the `application/json` Content-Type to the headers.

## More documentation

There is currently no official documentation, however you can consider the tests as a type of documentation, they are
pretty explicit and simple to follow and help to clarify the purpose of each feature.

## Good practices

Having your test setup/teardown like this is probably a good idea.

```
class ServerMockingTestBase(...):
    def setUp(self):
        super(ServerMockingTestBase, self).setUp()
        
        self.client = MockServerClient(MOCK_SERVER_URL)
        self.client.reset()

    def tearDown(self):
        super(ServerMockingTestBase, self).tearDown()
        
        self.client.verify()
```

# Troubleshooting

Checking MockServer's logs is the first place to go.  If you don't see any logs, try another LOG_LEVEL such as INFO.

If the problem is in the code, please open an issue :)

# Contributing

The form may not be final, we would love to hear what you think of the client!

Feel free to raise issues and send some pull request, we'll be happy to look at them!

Make sure all new code is tested, current tests run against a MockServer container.

## Running tests

You can easily run the tests with https://pypi.python.org/pypi/tox

```
tox -e py34
```

You can also call the `test-runner.sh` directly, you will need https://pypi.python.org/pypi/nose installed

You can also launch the container

```
docker-compose up-d
```

and run the tests in your favorite IDE :)
