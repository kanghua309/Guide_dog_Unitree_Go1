#/bin/bash

source ${ROS_ROOT}/setup.bash 

mkdir -p /root/ros_ws/src && rm -rf /root/ros_ws/src/*
cp -rf /root/ros_ws/demos /root/ros_ws/src
cd /root/ros_ws

#rosdep install -r -y  --from-paths src --ignore-src 
echo "Dep Install Over ..."

# colcon build --packages-select \
#        ball_track_ros2 \
#        republisher_ros2 \
#        ros2_unitree_legged_msgs \
#        unitree_legged_real \
#        --paths src/demos/* 
colcon build --paths src/demos/* 

echo "Build Over ..."
ldconfig
