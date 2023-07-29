#!/bin/bash
set -e

#rm guide_dog_unitree_go1 listen_talk_ros2 demos -rf #这里要把src 外的package 删除了，不然报错
# Set the default build type
BUILD_TYPE=RelWithDebInfo
colcon build \
        --base-paths src \
        --symlink-install \
        --cmake-args "-DCMAKE_BUILD_TYPE=$BUILD_TYPE" "-DCMAKE_EXPORT_COMPILE_COMMANDS=On" \
        -Wall -Wextra -Wpedantic
