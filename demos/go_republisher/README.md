安装依赖
You should install the bridge via apt by doing sudo apt-get install ros-foxy-cv-bridge and sudo apt-get install ros-foxy-vision-opencv


#pip install --extra-index-url https://rospypi.github.io/simple2 rclpy std_msgs
创建包时制定依赖
ros2 pkg create --build-type ament_python republisher_ros2 --dependencies rclpy std_msgs geometry_msgs python3-numpy

编译pakcage
colcon build --packages-select republisher_ros2

启动节点
ros2 run republisher_ros2 mono_node

给定参数启动
ros2 run republisher_ros2 mono_node --ros-args -p device_id:=1 -p camera_name:=camera_face


摄像头检测：（很遗憾mac下docker 中无法使用摄像头）
lsusb 查看usb设备列表
ls /dev/video* 查看摄像头驱动安装
sudo apt-get install cheese 如果已经安装，这步可以省略
cheese 打开摄像头

