#!/usr/bin/env bash

cd $(dirname $0)

exec docker run 2_classical_planning "$@"
