#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/../.."

cmd=$(printf ' %q' "$@" | cut -c 2-)
exec ./run.sh bash -c "cd /usr/src/app/Projects/3_Adversarial\\ Search && $cmd"
