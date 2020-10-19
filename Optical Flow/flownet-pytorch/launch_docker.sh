#!/bin/bash

sudo nvidia-docker build -t $USER/flownet2:latest .
echo $(pwd)
sudo nvidia-docker run --rm -ti --volume=/home/ubuntu/niviru/poseflow-pie/:/poseflow-pie:rw --workdir=/poseflow-pie --ipc=host $USER/flownet2:latest /bin/bash
