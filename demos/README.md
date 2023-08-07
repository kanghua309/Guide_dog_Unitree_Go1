该demo的任务是：让go1 嫩识别红色球，并狗头能跟着红色球的方向转动 —— 代码参考了https://github.com/aatb-ch/go1_republisher 和 网友相关代码 ，我们改造位foxy 版本！
其中go_republisher 目的是把摄像头消息转化为ros2 的msg，并重新发布为新的topic 
其中ball_track 目的是订阅摄像头信息，并识别红色球的移动方向，最后再发送high_cmd主题消息(？ 这个消息需要转化ros1？)

？？？
我们自己搭建highcmd的接收节点！ 然后这个节点接受cmd消息，再把其转化到狗的控制服务消息，发出去？ 161节点？

https://github.com/kanghua309/unitree_ros2/blob/main/unitree_legged_real/src/udp_high.cpp
https://github.com/kanghua309/unitree_ros2/blob/main/unitree_legged_real/launch/high.launch.py
https://github.com/kanghua309/unitree_ros2/blob/main/unitree_legged_real/unitree_legged_sdk-master/CMakeLists.txt
https://github.com/kanghua309/unitree_ros2/blob/main/unitree_legged_real/package.xml



如何缩小镜像，变成runtime 的，而不是devel的
https://unrealcontainers.com/blog/identifying-application-runtime-dependencies/