#/bin/bash

source /opt/foxy/setup.bash 

mkdir -p /root/ros_ws/src
rm -rf /root/ros_ws/src/*
mv /root/ros_ws/demos /root/ros_ws/src
cd /root/ros_ws
colcon build --packages-select \
       ball_track_ros2 \
       republisher_ros2 \
       ros2_unitree_legged_msgs \
       --symlink-install

source /root/ros_ws/install/setup.bash

