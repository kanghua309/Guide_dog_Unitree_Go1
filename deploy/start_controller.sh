#!/bin/bash
docker stop foxy_controller || true
docker rm foxy_controller || true
cd ~/docker/
make autostart