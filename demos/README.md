该demo的任务是：让go1 嫩识别红色球，并狗头能跟着红色球的方向转动 —— 代码参考了https://github.com/aatb-ch/go1_republisher 和 网友相关代码 ，我们改造位foxy 版本！
其中go_republisher 目的是把摄像头消息转化为ros2 的msg，并重新发布为新的topic 
其中ball_track 目的是订阅摄像头信息，并识别红色球的移动方向，最后再发送high_cmd主题消息（该消息发给下面提到的high cmd 处理节点）
其中还需要包含git@github.com:kanghua309/unitree_ros2.git 下的两个包（分别是msg 和 high cmd的处理包 -- 该包将消息发送给192.168.123.161上的控制服务）

如何使用，请看
```
make help
```


其他：
如何缩小镜像，变成runtime 的，而不是devel的
https://unrealcontainers.com/blog/identifying-application-runtime-dependencies/