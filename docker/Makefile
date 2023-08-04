default: build_arm64

#build:
#	docker build -t jetson-model-deployment . -f ros2_runtime.Dockerfile
#clean-build:
#	docker build -t jetson-model-deployment . -f ros2_runtime.Dockerfile --no-cache=true
build_arm64:

ifdef PROXY
	docker buildx build --platform linux/arm64 \
		-o type=tar,dest=deployment_image.tar \
		-t jetson-model-deployment \
		--build-arg "HTTP_PROXY=${PROXY}" \
		--build-arg "HTTPS_PROXY=${PROXY}" \
		--no-cache=true \
		. -f ros2_runtime.Dockerfile 
else 
	docker buildx build --platform linux/arm64 \
		-o type=tar,dest=deployment_image.tar \
		-t jetson-model-deployment \
		--no-cache=true \
		. -f ros2_runtime.Dockerfile
endif
run:
	docker stop foxy_controller || true
	docker rm foxy_controller || true
	docker run -it \
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--env="XAUTHORITY=${XAUTH}" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="/home/unitree/ros_ws:/root/ros_ws" \
		--privileged \
		--runtime=nvidia \
		--net=host \
		--workdir="/root/ros_ws" \  
		--name="foxy_controller" \
		jetson-model-deployment bash


		
autostart:
	docker stop foxy_controller || true
	docker rm foxy_controller || true
	docker run -d\
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--env="XAUTHORITY=${XAUTH}" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="/home/unitree/ros_ws:/root/ros_ws" \
		--privileged \
		--runtime=nvidia \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment tail -f /dev/null
	docker start foxy_controller
	docker exec foxy_controller bash -c 'bash -x /root/ros_ws/demos/build.sh && ls && ros2 launch ball_track_ros2 track.launch.py use_go1_repbulisher_msg:=true camera_name:=camera_face1 device_id:=0 hz:=25'
