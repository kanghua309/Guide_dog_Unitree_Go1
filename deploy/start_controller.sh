#!/bin/bash
docker stop foxy_controller || true
docker rm foxy_controller || true
cd ~/ros_ws/docker/
make autostart
