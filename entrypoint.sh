#!/bin/bash

set -xeuo pipefail

envsubst < pycsw.conf.template > pycsw.conf
/wait-for --timeout "$TIMEOUT" "$COAT_URL" -- pdm run python3 coat2pycsw.py

exec "$@"
