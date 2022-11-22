#!/bin/bash

set -xeuo pipefail

envsubst < pycsw.conf.template > pycsw.conf
pdm run python3 coat2pycsw.py

exec "$@"
