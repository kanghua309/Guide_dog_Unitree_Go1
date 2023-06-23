#!/bin/bash
set -e

# setup ros environment
source "/ros2_foxy/install/setup.bash"
exec "$@"
