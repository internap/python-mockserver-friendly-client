#!/bin/bash -ex

get_timeout() {
    o="timeout"
    which gnutimeout 1>/dev/null 2>/dev/null && o="gnutimeout"
    which gtimeout 1>/dev/null 2>/dev/null && o="gtimeout"
    echo $o
}

show_failures() {
    docker-compose logs --timestamps mock-server
    exit 1
}

teardown() {
    docker-compose down
}

wait_until() {
    local command="$1"

    $(get_timeout) 10 bash -c "while true; do echo \"checking\"; ${command} && break || sleep 1; done"
}

docker-compose up -d

trap teardown INT TERM EXIT

wait_until "curl -XPUT http://localhost:1080/reset"

nosetests --verbose --detailed-errors --debug=DEBUG || show_failures

