安装依赖
You should install the bridge via apt by doing sudo apt-get install ros-foxy-cv-bridge and sudo apt-get install ros-foxy-vision-opencv



创建包时制定依赖
ros2 pkg create --build-type ament_python republisher_ros2 --dependencies rclpy std_msgs geometry_msgs python3-numpy

编译pakcage
colcon build --packages-select republisher_ros2


启动
ros2 run republisher_ros2 mono_node --ros-args -p device_id:=0 -p camera_name:=camera_face -p hz:=0.5 -p debug:=False #虚拟机中这个值设置大了，就服务调用失败， 默认本应该是25
如果在PC上则可使用debug参数
ros2 run republisher_ros2 mono_node --ros-args -p device_id:=0 -p camera_name:=camera_face -p hz:=0.5 -p debug:=True

调试：
查看msg(静态)
ros2 interface package republisher_ros2 #空
ros2 interface show xxx 
ros2 interface show sensor_msgs/msg/Image
查看参数（动态）
ros2 param list #camera_name and device_id
查看topic（动态）
ros2 topic info #camera_face/image_raw
ros2 topic echo /camera_face/image_raw
ros2 topic type /camera_face/image_raw --> 输出关于消息的msg, 然后使用ros2 interface show查看吗？


其他：
摄像头检测：（很遗憾mac下docker 中无法使用摄像头）
lsusb 查看usb设备列表
ls /dev/video* 查看摄像头驱动安装
sudo apt-get install cheese 如果已经安装，这步可以省略
cheese 打开摄像头

