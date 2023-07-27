sudo apt-get install ros-<distro>-sensor-msgs
python3-sensor-msgs

colcon build --packages-select ball_track_ros2
ros2 run ball_track_ros2 track_node


ros2 pkg create --build-type ament_python dev_opencv_py --dependencies rclpy image_transport cv_bridge sensor_msgs std_msgs opencv2
<depend>opencv-python</depend>
