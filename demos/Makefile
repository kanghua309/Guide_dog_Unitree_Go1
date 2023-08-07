default: build_image


.PHONY: no_targets__ list
no_targets__:
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | sort"

# get_depend:
# 	svn checkout https://github.com/kanghua309/unitree_ros2/trunk/ros2_unitree_legged_msgs
# 	svn checkout https://github.com/kanghua309/unitree_ros2/trunk/unitree_legged_real

image_build:
ifdef PROXY
	docker buildx build --platform linux/arm64 \
		-o type=tar,dest=deployment_image.tar \
		-t jetson-model-deployment \
		--build-arg "HTTP_PROXY=${PROXY}" \
		--build-arg "HTTPS_PROXY=${PROXY}" \
		--no-cache=false \
		. -f ros2_mini.Dockerfile 
else 
	docker buildx build --platform linux/arm64 \
		-o type=tar,dest=deployment_image.tar \
		-t jetson-model-deployment \
		--no-cache=true \
		. -f ros2_mini.Dockerfile
endif


image_import:
	@cat deployment_image.tar | docker import - jetson-model-deployment

docker_run:
	docker stop foxy_controller || true
	docker rm foxy_controller || true
	docker run -it \
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--env="XAUTHORITY=${XAUTH}" \
		--env="ROS_DISTRO=foxy" \
                --env="ROS_ROOT=/opt/ros/foxy" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="/home/unitree/ros_ws:/root/ros_ws" \
		--privileged \
		--runtime=nvidia \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment bash

docker_buiild_app:
	docker run -d	\
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--env="XAUTHORITY=${XAUTH}" \
		--env="ROS_DISTRO=foxy" \
		--env="ROS_ROOT=/opt/ros/foxy" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="/home/unitree/ros_ws:/root/ros_ws" \
		--privileged \
		--runtime=nvidia \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment tail -f /dev/null
	docker start foxy_controller
	docker exec foxy_controller bash -c 'bash /root/ros_ws/demos/build.sh'


docker_autostart:
	docker stop foxy_controller || true
	docker rm foxy_controller || true
	docker run -d\
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--env="XAUTHORITY=${XAUTH}" \
		--env="ROS_DISTRO=foxy" \
		--env="ROS_ROOT=/opt/ros/foxy" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="/home/unitree/ros_ws:/root/ros_ws" \
		--privileged \
		--runtime=nvidia \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment tail -f /dev/null
	docker start foxy_controller
	docker exec foxy_controller bash -c 'source ${ROS_ROOT}/setup.bash && ros2 launch ball_track_ros2 track.launch.py use_go1_repbulisher_msg:=true camera_name:=camera_face1 device_id:=0 hz:=25'

demo_deploy:
    git clone git@github.com:kanghua309/unitree_ros2.git 
	mv ros2_unitree_legged_msgs .
	mv unitree_legged_real .
	rm -rf unitree_ros2
	#rsync -av -e ssh --exclude=*.pt --exclude=*.mp4 $PWD/../deploy $PWD/../docker $PWD/../demos unitree@192.168.123.15:/home/unitree/ros_ws
	rsync -av -e ssh --exclude=*.Dockerfile $PWD/../deploy $PWD/../docker $PWD/../demos unitree@192.168.123.13:/home/unitree/ros_ws

