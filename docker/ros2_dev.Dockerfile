# https://www.docker.com/blog/faster-multi-platform-builds-dockerfile-cross-compilation-guide/


#https://blog.csdn.net/qf0129/article/details/124838756
FROM  registry.cn-hangzhou.aliyuncs.com/robot/ros:foxy-cuda-gazebo-nvidia-2023-06-16 as amd64_foxy_base
#RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
#RUN sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
RUN sed -i s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list
RUN sed -i s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

FROM  registry.cn-hangzhou.aliyuncs.com/robot/ros:foxy-ros-base-l4t-r35.3.1 as arm64_foxy_base
RUN sed -i 's/ports.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
#RUN sed -i 's/ports.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
RUN dpkg --purge --force-remove-reinstreq opencv-libs ; exit 0 
RUN dpkg --purge --force-remove-reinstreq opencv-dev  ; exit 0 

FROM ${TARGETARCH}_foxy_base as dev

SHELL ["/bin/bash", "-c"]
ENV SKIP_ROSDEP=""

ENV ROS_DISTRO=foxy

ENV USERNAME root
ENV HOME /root

# add new sudo user
#ENV USERNAME ros
#ENV HOME /home/$USERNAME
#RUN useradd -m $USERNAME && \
#        echo "$USERNAME:$USERNAME" | chpasswd && \
#        usermod --shell /bin/bash $USERNAME && \
#        usermod -aG sudo $USERNAME && \
#        mkdir /etc/sudoers.d && \
#        echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
#        chmod 0440 /etc/sudoers.d/$USERNAME && \
#        # Replace 1000 with your user/group id
#        usermod  --uid 1000 $USERNAME && \
#        groupmod --gid 1000 $USERNAME

ENV DEBIAN_FRONTEND=noninteractive

#https://blog.csdn.net/JasonXu94/article/details/129698868
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple 
RUN pip config set install.trusted-host mirrors.aliyun.com

#https://mirrors.tuna.tsinghua.edu.cn/help/ros2/
RUN curl -sSL https://ghproxy.com/https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
#RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.aliyun.com/ros2/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

#RUN dpkg --purge --force-remove-reinstreq opencv-libs ; exit 0 
#RUN dpkg --purge --force-remove-reinstreq opencv-dev  ; exit 0 
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
       vim \
       openssh-client \
       doxygen \
       software-properties-common \
       libglib2.0-dev \
       ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && add-apt-repository universe

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
USER root

RUN apt-get -y update && apt-get install -y --no-install-recommends make gcc-8 g++-8
RUN cd /tmp && git clone https://ghproxy.com/https://github.com/lcm-proj/lcm.git && cd lcm && mkdir build && cd build && cmake .. && make -j && make install
RUN cd /tmp/lcm/lcm-python && pip3 install -e .

RUN pip3 install --no-cache-dir setuptools==58.2.0  picovoice==2.1.0 gTTS



RUN pip3 install rosdepc
RUN rosdepc init
RUN rosdepc update


ENV ROS2_WS=/opt/ros/$ROS_DISTRO
ENV GUIDE_DOG_REPO=https://ghproxy.com/https://github.com/kanghua309/Guide_dog_Unitree_Go1.git
ENV GUIDE_DOG_BRANCH=main
ENV MY_WS=$HOME/ros_ws

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
       ros-foxy-xacro \
       ros-foxy-diagnostic-updater \
       ros-foxy-navigation2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN --mount=type=ssh mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR $MY_WS/src
RUN --mount=type=ssh \
    git clone $GUIDE_DOG_REPO -b $GUIDE_DOG_BRANCH && \
    cd $MY_WS && \
    mv src/Guide_dog_Unitree_Go1/guide_dog.repos . && \
    rm -rf src/Guide_dog_Unitree_Go1

WORKDIR $MY_WS
RUN sed -i "s#git@#https://ghproxy.com/https://#g" guide_dog.repos
RUN sed -i "s#github.com:#github.com/#g" guide_dog.repos
RUN --mount=type=ssh \
    vcs import src < ./guide_dog.repos && \
    find ./ -name ".git" | xargs rm -rf

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && rosdepc install -r -y \
      --from-paths src \
      --ignore-src \
      --rosdistro $ROS_DISTRO


RUN apt-get update \
        && apt-get install -y ros-foxy-ament-* \
 	&& apt-get clean \
        && rm -rf /var/lib/apt/lists/*

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
#RUN --mount=type=cache,target=/root/.ccache \
RUN    source $ROS2_WS/setup.bash \
    && colcon build \
      --symlink-install

RUN echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> ~/.bashrc

COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

