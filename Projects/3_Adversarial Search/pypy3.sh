#!/usr/bin/env bash

cd "$(dirname "$0")"

exec ./run.sh pypy3 "$@"
