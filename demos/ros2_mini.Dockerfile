FROM  ros:foxy-ros-base-focal as amd64_foxy_base
RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
RUN sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list

FROM  arm64v8/ros:foxy-ros-base-focal as arm64_foxy_base
RUN sed -i 's/ports.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

FROM ${TARGETARCH}_foxy_base as dev

SHELL ["/bin/bash", "-c"]
ENV SKIP_ROSDEP=""

ENV ROS_DISTRO foxy
ENV ROS_ROOT /opt/ros/foxy
ENV USERNAME root
ENV HOME /root

ENV DEBIAN_FRONTEND=noninteractive
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

#https://mirrors.tuna.tsinghua.edu.cn/help/ros2/
# RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.aliyun.com/ros2/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
       python3-pip \
       ros-foxy-cv-bridge \
       ros-foxy-xacro \
       python3-cv-bridge \
       libglib2.0-dev \
       libboost-all-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

RUN cd /tmp && git clone https://github.com/lcm-proj/lcm.git && cd lcm && mkdir build && cd build && cmake .. && make -j && make install && rm -rf /tmp/lcm
RUN ldconfig


#https://blog.csdn.net/JasonXu94/article/details/129698868
RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple \
&& pip3 config set install.trusted-host mirrors.aliyun.com \
&& pip3 install --no-cache-dir setuptools==58.2.0 \
&& pip3 install --no-cache-dir opencv-python-headless
