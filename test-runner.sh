#!/bin/bash -ex

teardown() {
    docker-compose down
}

docker-compose up -d

trap teardown INT TERM EXIT

nosetests

