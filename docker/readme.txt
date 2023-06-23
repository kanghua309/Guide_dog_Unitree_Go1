$ eval $(ssh-agent)
$ ssh-add ~/.ssh/id_rsa

$ export REGISTRY=<your dockerhub username>
# create new buildx that support multiple platforms
$ docker buildx create --use  --driver-opt network=host --name MultiPlatform

# build the image for two different platforms and push the images
$ DOCKER_BUILDKIT=1 docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --ssh default=${SSH_AUTH_SOCK} \
  -f xxxx.Dockerfile \
  -t ${REGISTRY}/ros2_base:latest \
  --push .


#!!!
DOCKER_BUILDKIT=1 docker build --platform linux/arm64 --ssh default=/root/.ssh/id_rsa . -f ros2_dev_0.Dockerfile
