将tar的image发送给unitree 的办卡上！
在远程机器上执行  ——  
```
cd deploy && ./transfer_image.sh 
```

在unitree的192.168.123.15机器上执行：揭压镜像，然后加载到docker image库中上
```
chmod +x install_deployment_code.sh
sh install_deployment_code.sh
```

在unitree的192.168.123.15机器上执行
```
cd docker
make autostart
```
