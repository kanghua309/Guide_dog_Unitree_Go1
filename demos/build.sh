#/bin/bash

source /opt/foxy/setup.bash 

mkdir -p /root/ws/src
cp -rf /root/demo /root/ws/src
cd /root/ws
colcon build --packages-select \
       ball_track_ros2 \
       republisher_ros2 \
       ros2_unitree_legged_msgs \
       --symlink-install

