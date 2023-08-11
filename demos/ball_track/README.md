sudo apt-get install ros-foxy-sensor-msgs
pip install python3-sensor-msgs


编译pakcage
colcon build --packages-select ball_track_ros2 --ros-args -p camera_name:=camera_face

启动节点
ros2 run ball_track_ros2 track_node

lunch 启动集体启动
ros2 launch ball_track_ros2 track.launch.py -s
ros2 launch ball_track_ros2 track.launch.py use_go1_repbulisher_msg:=true camera_name:=camera_face1 device_id:=0 hz:=25
如果PC上则可加debug参数
ros2 launch ball_track_ros2 track.launch.py use_go1_repbulisher_msg:=true camera_name:=camera_face1 device_id:=0 hz:=25 debug:=True


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
