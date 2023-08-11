
DEFAULT_DOCKER_RUNTIME = "nvidia"
DEFAULT_DEPLOY_HOST_WORKDIR = "/home/unitree/ros_ws"
DEFAULT_DEPLOY_HOST_LOCATION="unitree@192.168.123.13"


UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Linux)
    # Linux specific CFLAGS or LDFLAGS etc.
    SED = sed
endif

ifeq ($(UNAME_S),Darwin)
    # macOS specific CFLAGS or LDFLAGS etc.
    # you need install - brew install gnu-sed 
    SED = gsed
endif



#=Help Commands
.PHONY: help
help: # Shows the available make commands.
	@${SED} -nr \
		-e 's|^#=(.*)|\n\1:|p' \
		-e 's|^([a-zA-Z-]*):((.*?)# (.*))?|  \1 \4|p' \
		$(lastword $(MAKEFILE_LIST)) \
		| expand -t20
	@echo ""
	@echo "------------------------------------------------------------"
	@echo "PROXY VAR IS ${PROXY}"
	@echo "DEFAULT_DOCKER_RUNTIME VAR IS ${DEFAULT_DOCKER_RUNTIME}"
	@echo "DEFAULT_DEPLOY_HOST_WORKDIR VAR IS ${DEFAULT_DEPLOY_HOST_WORKDIR}"
	@echo "DEFAULT_DEPLOY_HOST_LOCATION VAR IS ${DEFAULT_DEPLOY_HOST_LOCATION}"
	@echo "------------------------------------------------------------"


#=Image Commands
.PHONY: image-build image-import image-clean
image-build: # :Build image For Demos
ifdef PROXY
	docker buildx build --platform linux/arm64 \
		-o type=tar,dest=deployment_image.tar \
		-t jetson-model-deployment \
		--build-arg "HTTP_PROXY=${PROXY}" \
		--build-arg "HTTPS_PROXY=${PROXY}" \
		--no-cache=true \
		. -f ros2_mini.Dockerfile 
else 
	docker buildx build --platform linux/arm64 \
		-o type=tar,dest=deployment_image.tar \
		-t jetson-model-deployment \
		--no-cache=true \
		. -f ros2_mini.Dockerfile
endif

image-import: # :Import Demo Image From Jar Repo 
	@cat deployment_image.tar | docker import - jetson-model-deployment

image-clean: # :Remove Image From Repo
	@docker stop foxy_controller || true
	@docker rm foxy_controller || true
	@docker image rm jetson-model-deployment
	@rm jetson-model-deployment

#=Docker Commands
.PHONY: docker-run docker-build-app docker-autostart-app docker-clean
docker-run: # :Run Demo Docker Base 
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
		--volume="${DEFAULT_DEPLOY_HOST_WORKDIR}:/root/ros_ws" \
		--runtime=${DEFAULT_DOCKER_RUNTIME} \
		--privileged \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment bash

docker-build-app: # :Run Demo Docker And Build Demo
	docker stop foxy_controller || true
	docker rm foxy_controller || true
	docker run -d	\
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--env="XAUTHORITY=${XAUTH}" \
		--env="ROS_DISTRO=foxy" \
		--env="ROS_ROOT=/opt/ros/foxy" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="${DEFAULT_DEPLOY_HOST_WORKDIR}:/root/ros_ws" \
		--runtime=${DEFAULT_DOCKER_RUNTIME} \
		--privileged \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment tail -f /dev/null
	docker start foxy_controller
	docker exec foxy_controller bash -c 'bash /root/ros_ws/demos/build.sh'

docker-autostart-app: # :Run Demo Docker With App Start
	pgrep -f point | grep -v $$ | xargs -r kill || true
	docker stop foxy_controller || true
	docker rm foxy_controller || true
	docker run -d	\
		--env="DISPLAY" \
		--env="QT_X11_NO_MITSHM=1" \
		--env="XAUTHORITY=${XAUTH}" \
		--env="ROS_DISTRO=foxy" \
		--env="ROS_ROOT=/opt/ros/foxy" \
		--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
		--volume="${XAUTH}:${XAUTH}" \
		--volume="${DEFAULT_DEPLOY_HOST_WORKDIR}:/root/ros_ws" \
		--runtime=${DEFAULT_DOCKER_RUNTIME} \
		--privileged \
		--net=host \
		--workdir="/root/ros_ws" \
		--name="foxy_controller" \
		jetson-model-deployment tail -f /dev/null
	docker start foxy_controller
	docker exec foxy_controller bash -c 'source /root/ros_ws/install/setup.bash && ros2 launch ball_track_ros2 track.launch.py use_go1_repbulisher_msg:=true camera_name:=camera_face1 device_id:=0 hz:=25'

docker-clean: # :Docker Stop and Rm
	docker stop foxy_controller || true
	docker rm foxy_controller || true


#=Demo Deploy Commands
.PHONY: demo-deploy
demo-deploy: # :Deploy Demo To Unitree Head Board
	if [ ! -d 'unitree_ros2' ]; then	\
	   git clone git@github.com:kanghua309/unitree_ros2.git; \
	   cp -rf unitree_ros2/go1_description .; \
	   cp -rf unitree_ros2/ros2_unitree_legged_msgs .; \
	   cp -rf unitree_ros2/unitree_legged_real .; \
	fi
	#rm -rf unitree_ros2
	#rsync -av -e ssh --exclude=*.pt --exclude=*.mp4 $PWD/../deploy $PWD/../docker $PWD/../demos unitree@192.168.123.15:/home/unitree/ros_ws
	#rsync -av -e ssh --exclude=*.Dockerfile $PWD/../deploy $PWD/../docker $PWD/../demos unitree@192.168.123.13:/home/unitree/ros_ws
	rsync -av -e ssh --exclude=*.Dockerfile ${PWD}/../demos ${DEFAULT_DEPLOY_HOST_LOCATION}:${DEFAULT_DEPLOY_HOST_WORKDIR}

