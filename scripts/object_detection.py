#!/usr/bin/env python

import time
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
import os
import csv

# from classifier.yolo import YOLO
from ObjectDetectionROS.trainer.pytorchyolo import detect
from ObjectDetectionROS.trainer.pytorchyolo.utils import utils
from yolov7.utils.general import non_max_suppression, scale_coords
import rospkg
import yaml
from cv_bridge import CvBridge
import ros_numpy
import torch
from segmentation import Segmentation


class ObjectDetection:
    yolo = None
    config = None
    bridge = None

    def __init__(self):

        rospy.init_node("object_detection_node")

        self.bridge = CvBridge()
        self.count = 0

        # model_path = (
        #     os.path.dirname(__file__)
        #     + "/ObjectDetectionROS/trainer/config/yolov7-tiny.cfg"
        # )
        # # print("model path: ", model_path)
        # weights_path = (
        #     os.path.dirname(__file__)
        #     + "/ObjectDetectionROS/trainer/weights/yolov7-tiny.weights"
        # )
        # print("Began loading model....")
        # self.model = detect.load_model(model_path, weights_path)
        # print("Model loaded.....")

        # # change the camera topic if it is different
        # print("Spinning ros node......")
        rospy.Subscriber(
            "/zed/zed_node/right_raw/image_raw_color", Image, self.classify
        )
        rospy.spin()

    def classify(self, image):
        "Classify function running...."
        # img = self.bridge.imgmsg_to_cv2(image, "bgr8")
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        # TODO: Fix subscriber lag issue
        start_time_secs = image.header.stamp.secs
        start_time_nsecs = float("0." + str(image.header.stamp.nsecs))
        start_time = start_time_secs + start_time_nsecs

        img = ros_numpy.numpify(image)
        img = img[:, :, :3]
        img = img.astype(np.uint8)
        # img = torch.from_numpy(img)
        # print("IMG SHAPE: ", img.shape)
        # print("IMG: ", np.info(img))
        print("Image retrieved, detections starting...")
        detections = self.seg.detect(img)

        latency = time.time() - start_time
        print("Latency: ", str(latency))

        output_path = os.path.dirname(__file__) + "/detectionoutput/"
        self.seg.save_image(detections, os.path.join(
            output_path, f"latest{self.count}.png"))
        self.count += 1

    def get_segmentation_mask(self, image):
        img = ros_numpy.numpify(image)
        img = img[:, :, :3]
        img = img.astype(np.uint8)
        print("Image retrieved, detections starting...")
    # object detection
        results = self.model(img)
        results = non_max_suppression(
            results, confidence_threshold=0.5, iou_threshold=0.45)

    # mask
        mask = np.zeros_like(img[:, :, 0])
        for result in results:
            if result is not None:
                for detection in result:
                    class_idx = int(detection[-1])
                    if class_idx != 0:  # Skip the background class
                        box = detection[:4]
                        box = scale_coords(
                            img.shape[0:2], box, mask.shape).astype(np.int32)
                        mask[box[1]:box[3], box[0]:box[2]] = 255
        output_path = os.path.dirname(__file__) + "/detectionoutput/"
        classes = utils.load_classes(os.path.dirname(
            __file__) + "/ObjectDetectionROS/trainer/data/coco.names")
        detect.save_output_image(
            img, results, 416, output_path, classes, self.count)
        self.count += 1

        return mask


if __name__ == "__main__":
    try:
        ObjectDetection()
    except rospy.ROSInterruptException:
        rospy.logerr("Could not start object detection node.")
