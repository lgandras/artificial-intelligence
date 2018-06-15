#!/usr/bin/env bash

cd $(dirname "$0")

exec docker-compose run pypy3 "$@"
