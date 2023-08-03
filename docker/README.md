


#$ eval $(ssh-agent)
#$ ssh-add ~/.ssh/id_rsa

需要如下设置
$ export REGISTRY=<your dockerhub username>
# create new buildx that support multiple platforms
#$ docker buildx create --use  --driver-opt network=host --name MultiPlatform

$ docker buildx rm multi-platform
$ docker buildx create --name multi-platform --use --platform linux/amd64,linux/arm64 --driver docker-container --driver-opt network=host
$ docker run --privileged --rm tonistiigi/binfmt --install all  #linux 需要安装 qemu

# build the image for two different platforms and push the images
#$ DOCKER_BUILDKIT=1 docker buildx build \
#  --platform linux/amd64,linux/arm64 \
#  --ssh default=${SSH_AUTH_SOCK} \
#  -f xxxx.Dockerfile \
#  -t ${REGISTRY}/ros2_base:latest \
#  --push .

登陆自己的仓库账号
$sudo docker login --username=kangh*****@msn.com registry.cn-hangzhou.aliyuncs.com

编译ARM64的镜像
DOCKER_BUILDKIT=1 docker build --platform linux/arm64 --ssh default=~/.ssh/id_rsa  -f ros2_dev_1.Dockerfile  -t ${REGISTRY}/ros2_guide_dog:latest  --push .

编译AMD64上镜像
DOCKER_BUILDKIT=1 docker build --platform linux/amd64 --ssh default=~/.ssh/id_rsa  -f ros2_dev_1.Dockerfile  -t ${REGISTRY}/ros2_guide_dog:latest  --push .

两个平台一起创建则
--platform linux/amd64,linux/arm64


运行如下
docker run \
  --rm \
  -it \
  --runtime nvidia \
  --network host \
  --gpus all \
  -e DISPLAY \
  ${REGISTRY}/ros2_guide_dog:latest \
  bash
