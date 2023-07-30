# Guide_dog_Unitree_Go1
This repo is for ros2 foxy only!!!!!!!!!!!!!!!!!!!!


Guide dogs have been used for decades to assist visually impaired individuals in navigating their surroundings. However, these dogs come at a high cost, ranging from $20,000 to $40,000. Additionally, they are red-green color blind, which limits their ability to interpret street signs and other visual cues.

To address these limitations, a I Programmed the Unitree Go1 quadruped robot dog to become an autonomous guide dog. By incorporating advanced technologies such as speech recognition, object recognition, and autonomous navigation, the robot dog will be able to help visually impaired individuals navigate their surroundings and avoid obstacles. And because a robot dog can be updated through machine learning and software updates, it is possible to continually improve its abilities over time.

Overall, this project represents an exciting advancement in assistive technology, providing a cost-effective and long-lasting alternative to traditional guide dogs. By combining the latest in robotics and machine learning, the Unitree Go1 robot dog has the potential to revolutionize the way visually impaired individuals navigate the world around them.

- [Link to portfolio post for this project](https://marnonel6.github.io/projects/1-guidedog-unitreego1)

Demo video:

https://user-images.githubusercontent.com/60977336/226094090-aa75a276-06a2-4fda-96bf-263f29d1d173.mp4


# Main launch file on external computer:
`guide_dog.launch.py`:
* This launches all the required nodes for Go1 to operate in guide dog mode.
```
ros2 launch guide_dog_unitree_go1 guide_dog.launch.py use_nav2:=true use_object_detection:=true
```
# Launch file on Go1:
* This launches all the required nodes on Go1 to operate in guide dog mode.
```
ros2 launch guide_dog_unitree_go1 guide_dog.launch.py use_voice_control:=true use_speech_recognition:=true use_Go1_vision:=true
```

# Voice recognition
The use of the Picovoice deep learning voice recognition library has enabled the creation of a custom wake word "Hey Willie" and commands like walk, stop, stand up, lay down, bark, and increase or decrease speed. By implementing this library, the user is able to control the movements of Go1 with their voice while navigating around. A ROS2 C++ and Python package was developed to hadle the voice recognition and translate the voice commands to desired controls. I utilized gTTS (Google Text-to-Speech), a Python library that generates text to speech audio files. I generate audio files that Go1 uses to effectively communicate with the user. The package was deployed on a Nvidia Jetson Nano on Go1.

# Packages used:
- [Voice recognition](https://github.com/Marnonel6/Guide_dog_Unitree_Go1/tree/main/listen_talk_ros2)
- [Object detection - YOLOv7](https://github.com/Marnonel6/YOLOv7_ROS2)
- [Unitree navigation](https://github.com/kanghua309/unitree_nav/tree/main)
- [Unitree ROS 2](https://github.com/kanghua309/unitree_ros2/tree/main)
- [velodyne](https://github.com/ros-drivers/velodyne/tree/foxy-devel)

# Use [VCS tool](https://github.com/dirk-thomas/vcstool) to clone all the required packages:
- The vcs import command clones all repositories of a previously exported file with the following command:
```
vcs import < guide_dog.repos
```
### Steps for setting up the guide dog workspace:
1) Create a workspace:
```
mkdir -p ws/src
```
2) Go into source directory:
```
cd ws/src
```
4) Git clone the Guide_dog_Unitree_Go1 repository:
```
git clone <ssh:Guide_dog_Unitree_Go1 repository>
```
5) Move .repos folder into source directory:
```
mv Guide_dog_Unitree_Go1/guide_dog.repos guide_dog.repos
```
6) Use vcs tool to clone dependency repos:
```
vcs import < guide_dog.repos
```
7) Build package in workspace directory:
```
colcon build
```
### 使用vscode集成环境下进行开发的步骤
1) 先下载vscode的集成环境（针对ros2-foxy）
```
git clone git@github.com:kanghua309/vscode_foxy_ws.git
```

2) 进入vscode_foxy_ws目录后，下载guide_dog.repos
```
cd vscode_foxy_ws
wget https://raw.githubusercontent.com/kanghua309/Guide_dog_Unitree_Go1/main/guide_dog.repos
wget https://ghproxy.com/https://raw.githubusercontent.com/kanghua309/Guide_dog_Unitree_Go1/main/guide_dog.repos
```

3）打开vscode，通过devcontainer创建容器（记得启动docker服务，构建过程需要一些时间）
![image](https://github.com/kanghua309/Guide_dog_Unitree_Go1/assets/25759038/f58e8f53-c0e6-47ee-830a-004394a2ad0a)

4）容器创建后，进行环境安装 - 执行setup.sh （从终端执行）或者从vs的task中选择setup 执行

5）编译ros2对应的包（即可src下的包）

6）其他debug等功能慢慢实验吧


## Significant people who contributed to the project:
The guide dog project was my own individual project, but some subsets of this project had collaborations with Nick Morales, Katie Hughes, Ava Zahedi and Rintaroh Shima. Thank you all for you contributions.
