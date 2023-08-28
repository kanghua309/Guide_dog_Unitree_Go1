我们希望使用chatgpt的归纳推理能力，从而实现我们子动作组合（类似状态机），简单说就是告诉他我的任务，让他来帮我规划子动作。
除此以外，我们也用chatgpt作一点自然语言识别的事，具体是把我自然语言含糊的描述，转化为较为准确的指令语言

部署依赖：
Go1 nav 包（https://github.com/kanghua309/unitree_nav）, 该包实现了指挥狗动作的服务（对应我们说的子命令）
Go1 ros2 包（https://github.com/kanghua309/unitree_ros2）,该包被上述包调用，负责解析high cmd 命令,并发给狗的161控制服务控制狗的动作
openai 包, 你得有api key ，且要有调用配额
- pip install openai
speech_recognition 包 - 语音识别很是牛逼 
- pip install SpeechRecognition

具体部署运行办法：
启动相关的ros2节点组
ros2 launch unitree_nav control.launch.py use_rviz:=false
启动后我们监听high state 中的mode状态，该状态用于任务规划（我们没有编码，而使用现成的ros2命令来做演验证）
ros2 topic echo /high_state --no-arr|grep mode: >/tmp/xxx.log  #状态不断的被写入了文件
运行voice_controller程序，接收自然语言命令，转化为子命令执行如：
python3 voice_controller.py
‘’‘
屏幕打印大概如下： 
请开始说话...
正在识别...
识别结果: 机器狗请你行走吧       ——   自然语言中文输入
ChatGpt 返回内容: 行走         ——   抽象出命令
需要执行的命令: 行走            
当前mode: mode7               ——  获取go1当前所处于的mode（从上面的xxx.log来）
ChatGpt 返回内容: mode7 -> mode5 -> mode6 -> mode1 -> mode2   —— 要执行的序列内容
开始执行
command: ros2 service call /damping std_srvs/srv/Empty
command: ros2 service call /lay_down std_srvs/srv/Empty
command: ros2 service call /stand_up std_srvs/srv/Empty
command: ros2 service call /stand_in_force std_srvs/srv/Empty
command: ros2 service call /walk_forward std_srvs/srv/Empty
’‘’