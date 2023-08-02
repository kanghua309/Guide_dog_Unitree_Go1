#!/bin/bash
docker stop foxy_controller || true
docker rm foxy_controller || true
cd ~/go1_gym/go1_gym_deploy/docker/
make autostart