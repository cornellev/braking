#!/bin/bash

# CREDIT: https://github.com/pjreddie/darknet/tree/master/scripts/get_coco_dataset.sh

# Clone COCO API
cd trainer
cd data

git clone https://github.com/pdollar/coco
cd coco

mkdir images
cd images

# Download Images
wget -nc "https://pjreddie.com/media/files/train2014.zip" --header "Referer: pjreddie.com"
wget -nc "https://pjreddie.com/media/files/val2014.zip" --header "Referer: pjreddie.com"

# Unzip
unzip -n -q train2014.zip
unzip -n -q val2014.zip

cd ..

# Download COCO Metadata
wget -nc "https://pjreddie.com/media/files/instances_train-val2014.zip" --header "Referer: pjreddie.com"
wget -nc "https://pjreddie.com/media/files/coco/5k.part" --header "Referer: pjreddie.com"
wget -nc "https://pjreddie.com/media/files/coco/trainvalno5k.part" --header "Referer: pjreddie.com"
wget -nc "https://pjreddie.com/media/files/coco/labels.tgz" --header "Referer: pjreddie.com"
tar xzf labels.tgz
unzip -n -q instances_train-val2014.zip

# Set Up Image Lists
# paste <(awk "{print \"$PWD\"}" <5k.part) 5k.part | tr -d '\t' > 5k.txt
# paste <(awk "{print \"$PWD\"}" <trainvalno5k.part) trainvalno5k.part | tr -d '\t' > trainvalno5k.txt
