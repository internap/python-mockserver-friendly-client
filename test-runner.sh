#!/bin/bash -ex

test_failed=""

teardown() {
    if [ -n "${test_failed}" ]; then
        docker-compose logs mock-server
    fi

    docker-compose down
}

docker-compose up -d

trap teardown INT TERM EXIT

nosetests --verbose --detailed-errors --debug=DEBUG || test_failed=1

