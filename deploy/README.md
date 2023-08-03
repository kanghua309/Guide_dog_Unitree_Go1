制作部署镜像,在当前目录下产生deployment_image.tar镜像压缩问价加
```
cd docker
PROXY=http://172.24.216.1:7890 make build_arm64 #modify proxy as yours
```

将上面的tar的image发送给unitree 的板卡上（路径为unitree@192.168.123.15:/home/unitree/demo）
在go1的背班机器上执行  ——  
```
mv docker/deployment_image.tar ../deploy
cd deploy && bash ./transfer_image.sh 
```

在unitree的192.168.123.15机器上执行：解压镜像，然后加载到docker image库中上
```
cd /home/unitree/demo/deploy
#chmod +x install_deployment_code.sh
bash install_deployment_code.sh
```

在unitree的192.168.123.15机器上执行
```
cd docker
make autostart
```
