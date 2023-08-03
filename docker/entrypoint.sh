#!/bin/bash
set -e

# setup ros environment
source "/opt/foxy/setup.bash"
exec "$@"
