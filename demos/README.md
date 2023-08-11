该demo的任务是：让go1 嫩识别红色球，并狗头能跟着红色球的方向转动 —— 代码参考了https://github.com/aatb-ch/go1_republisher 和 网友相关代码 ，我们改造位foxy 版本！
其中go_republisher 目的是把摄像头消息转化为ros2 的msg，并重新发布为新的topic 
其中ball_track 目的是订阅摄像头信息，并识别红色球的移动方向，最后再发送high_cmd主题消息（该消息发给下面提到的high cmd 处理节点）
其中还需要包含git@github.com:kanghua309/unitree_ros2.git 下的两个包（分别是msg 和 high cmd的处理包 -- 该包将消息发送给192.168.123.161上的控制服务）

如何使用，请看
```
make help

-->output
Help Commands:
  help Shows the available make commands.

Image Commands:
  image-build Build image For Demos
  image-import Import Demo Image From Jar Repo 

Docker Commands:
  docker-run Run Demo Docker Base 
  docker-build-app Run Demo Docker And Build Demo
  docker-autostart-app Run Demo Docker With App Start

Demo Deploy Commands:
  demo-deploy Deploy Demo To Unitree Head Board

------------------------------------------------------------
PROXY VAR IS 
DEFAULT_HOST_MAP_WORKDIR VAR IS /home/unitree/ros_ws
DEFAULT_DOCKER_RUNTIME VAR IS nvidia
------------------------------------------------------------
```

1. 创建demo docker image tar 
```
make image-build 
or 
PROXY=<your proxy address> make -e image-build #eg. PROXY=http://192.168.31.250:7890 make -e image-build
```
2. 部署demo 到目标板卡的目标位置
```
make demo-deploy
or
DEFAULT_DEPLOY_HOST_WORKDIR=/tmp/ros_ws DEFAULT_DEPLOY_HOST_LOCATION=king@127.0.0.1 make -e demo-deploy #为了测试目的
```
3. Login in 目标板卡的目标位置/demos, Then 将domo image tar 导入image repos
make image-import
4. 启动docker并编译docker app
```
make docker-build-app
or
DEFAULT_DOCKER_RUNTIME=runc DEFAULT_DEPLOY_HOST_WORKDIR=/home/unitree/ros_ws make -e docker-build-app
``
5. Run App With Docker
```
#Manual Run
make -e docker-run 
or 
DEFAULT_DEPLOY_HOST_WORKDIR=/home/unitree/ros_ws make -e docker-run
source install/setup.bash #in docker 
ros2 launch ball_track_ros2 track.launch.py use_go1_repbulisher_msg:=true camera_name:=camera_face1 device_id:=0 hz:=25 #in docker 

#AutoStart
pkill -f point #kill to free video devices first
DEFAULT_DEPLOY_HOST_WORKDIR=/home/unitree/ros_ws make -e docker-autostart-app

```

其他：
如何缩小镜像，变成runtime 的，而不是devel的
https://unrealcontainers.com/blog/identifying-application-runtime-dependencies/
