?
pip install --extra-index-url https://rospypi.github.io/simple2 rclpy std_msgs ros2py-init
?
ros2 pkg create --build-type ament_python my_new_ros2_numpy_pkg --dependencies rclpy std_msgs geometry_msgs python3-numpy

编译pakcage
colcon build --packages-select republisher_ros2

启动节点
ros2 run republisher_ros2 mono_node

给定参数启动
ros2 run republisher_ros2 mono_node --ros-args -p --device_id:=1 --camera_name:=camera_face
