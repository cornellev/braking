#!/bin/bash
# Download weights for yolov7
wget -c 'https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov7-tiny.weights' --header "Referer: githubusercontent.com"
# Download cfg for yolov7-tiny
wget - c 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov7-tiny.cfg' --header "Referer: raw.githubusercontent.com"
# Download weights for vanilla YOLOv3
wget -c 'https://pjreddie.com/media/files/yolov3.weights' --header "Referer: pjreddie.com"
# # Download weights for tiny YOLOv3
wget -c "https://pjreddie.com/media/files/yolov3-tiny.weights" --header "Referer: pjreddie.com"
# Download weights for backbone network
wget -c "https://pjreddie.com/media/files/darknet53.conv.74" --header "Referer: pjreddie.com"
