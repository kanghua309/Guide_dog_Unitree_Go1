sudo apt-get install ros-foxy-sensor-msgs
pip install python3-sensor-msgs


编译pakcage
colcon build --packages-select ball_track_ros2

启动节点
ros2 run ball_track_ros2 track_node

lunch 启动集体启动
ros2 launch track -s 

调试：
查看msg(静态)
ros2 interface show xxx 
ros2 interface show sensor_msgs/msg/Image
查看参数（动态）
ros2 param list 
查看topic（动态）
ros2 topic info #camera_face/image_raw
ros2 topic echo /camera_face/image_raw
ros2 topic type /camera_face/image_raw --> 输出关于消息的msg, 然后使用ros2 interface show查看吗？


colcon build --packages-select ball_track_ros2
ros2 run ball_track_ros2 track_node


ros2 pkg create --build-type ament_python dev_opencv_py --dependencies rclpy image_transport cv_bridge sensor_msgs std_msgs opencv2
<depend>opencv-python</depend>
