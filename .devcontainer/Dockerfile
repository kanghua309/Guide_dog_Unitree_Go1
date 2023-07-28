FROM althack/ros2:foxy-dev 
#FROM kanghua151/guide_dog_ros_humble:v2
# ** [Optional] Uncomment this section to install additional packages. **
#
# ENV DEBIAN_FRONTEND=noninteractive
# RUN apt-get update \
#    && apt-get -y install --no-install-recommends <your-package-list-here> \
#    #
#    # Clean up
#    && apt-get autoremove -y \


#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*
# ENV DEBIAN_FRONTEND=dialog

RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
RUN sed -i s/security.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple 
RUN pip config set install.trusted-host mirrors.aliyun.com

RUN curl -sSL https://ghproxy.com/https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.aliyun.com/ros2/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

SHELL ["/bin/bash", "-c"]
ENV SKIP_ROSDEP=""

ENV ROS_DISTRO=foxy
ENV USERNAME root
ENV DEBIAN_FRONTEND=noninteractive

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
USER root

# add deps 
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
       vim \
       openssh-client \
       doxygen \
       software-properties-common \
       ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && add-apt-repository universe

RUN apt-get -y update && apt-get install -y --no-install-recommends make gcc-8 g++-8 libglib2.0-dev 
RUN cd /tmp && git clone https://ghproxy.com/https://github.com/lcm-proj/lcm.git && cd lcm && mkdir build && cd build && cmake .. && make -j && make install
RUN cd /tmp/lcm/lcm-python && pip3 install -e .

RUN pip3 install --no-cache-dir setuptools==58.2.0  picovoice==2.1.0 gTTS

# RUN pip3 install rosdepc
# RUN rosdepc init
# RUN rosdepc update

# RUN apt-get update \
#     && apt-get install --yes --no-install-recommends \
#        ros-foxy-desktop \
#        python3-argcomplete \
#        ros-foxy-xacro \
#        ros-foxy-diagnostic-updater \
#        ros-foxy-navigation2 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*


# Set up VNC
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
       tigervnc-standalone-server \ 
       tigervnc-common \
       novnc \
       lxde \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir -p ~/.vnc 
RUN echo -e "lxterminal &\n\
/usr/bin/lxsession -s LXDE " > ~/.vnc/xstartup
RUN chmod +x ~/.vnc/xstartup


# Set up auto-source of workspace for ros user
ARG WORKSPACE
RUN echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/ros/.bashrc



