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
注意：当你跨平台进行构建是，需要注意是否已经支持
```
linux amd64 平台下，编译arm64的镜像需要首先安装qemu（mac 似乎默认安装了）
docker run --privileged --rm tonistiigi/binfmt --install all  #linux 需要安装 qemu
然后
docker buildx ls 可以查看当前默认构建是否支持arm64

如果需要不用默认的构建选项，自己建立一个新的构建器，且设为默认，则如下
docker buildx rm multi-platform
docker buildx create --name multi-platform --use --platform linux/amd64,linux/arm64 --driver docker-container --driver-opt network=host

当构建器已经生成后，则开始创建arm64的镜像
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

这里要注意：
amd64 平台下qemu 运行arm64的镜像发现有很多瑕疵，比如v4l2等软件就没有模拟完备（会提示功能未实现），所以如果要在pc模拟环境中测试，需要制作amd64镜像
PLATFORM=linux/amd64 make -e image-build 
```


注意：
- 当前镜像是使用的opencv-python-headless ，若在pc 上调试，手动安装 opencv-python

其他：
如何缩小镜像，变成runtime 的，而不是devel的
https://unrealcontainers.com/blog/identifying-application-runtime-dependencies/


