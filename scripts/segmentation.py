"""
Import 
Statements
"""
import numpy as np
import time
import sys
import os
import cv2
import rospy
from PIL import Image
import ObjectDetectionROS.trainer.pytorchyolo.yolov7.seg.segment.predict as predict
from ObjectDetectionROS.trainer.pytorchyolo.yolov7.seg.utils.general import (
    non_max_suppression,
    scale_coords,
)

# sys.path.append(os.path.join(os.path.dirname(__file__)+"/yolov7_main/"))
# from yolov7_main.utils.general import non_max_suppression, scale_coords
# import tensorflow as tf
# import keras as k


"""
Takes in image annotates with image segments
Optional: reshape image to consistent aspect ratio 480p
Inputs
- (n, m, 3) numpy array (image with RGB values)  

Outputs
- (n,m,3) numpy array (masked image with RGB values)

"""


class Segmentation:
    def __init__(self, model_path):
        pass

    def detect(self, image: np.ndarray):
        weights_path = (
            os.path.dirname(__file__)
            + "/ObjectDetectionROS/trainer/pytorchyolo/yolov7/seg/yolov7-seg.pt"
        )
        temp_path = "detections/temp.jpg"
        self.save_image(image, temp_path)
        detection = predict.run(
            weights=weights_path, source=temp_path, return_mask=True
        )
        return detection

    def save_image(self, image, path):
        img = Image.fromarray(image)
        img.save(path)

    def segmentation(self, image):
        """
        To implement
        """

        # detection
        img = np.uint8(image)
        results = self.detect(img)
        results = non_max_suppression(
            results, confidences_threshold=0.5, iou_threshold=0.45
        )

        # mask
        mask = np.zeros_like(img[:, :, 0])
        for result in results:
            if result is not None:
                for detection in result:
                    class_idx = int(detection[-1])
                    if class_idx != 0:  # Skip the background class
                        box = detection[:4]
                        box = scale_coords(img.shape[0:2], box, mask.shape).astype(
                            np.int32
                        )
                        mask[box[1]: box[3], box[0]: box[2]] = 255

        # save mask
        path = os.path.dirname(__file__) + "/detections/mask/"
        self.save_image(mask, path)


if __name__ == "__main__":
    try:
        Segmentation()
    except rospy.ROSInterruptException:
        rospy.logerr("Could not start Segmentation node.")
