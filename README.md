# Future Tasks
- Replace self.classify() with equivalent segmentation()
- Prune unused code from main branch after completion of all goals.
# ----------------------------

# Perception Deployment via ROS
Designed by: Adams Anaglo, Bryant Har, Mihir Mishra, Sia Chitnis, Eric Marchetti

- [Summary and Outcomes](#summary-and-outcomes-)
- [Terminology](#terminology-)
- [Dependencies](#dependencies-)
- [Algorithms and Designs](#algorithms-and-designs-)
  - [Algorithm(s) in Use with Rationale](#algorithm-in-use-with-rationale-)
- [Performance](#performance-)
- [Future Work/Updates](#future-work-)
- [Reflection](#reflection-)

## Summary and Outcomes <a name=“summary-and-outcomes”></a>
Spring 2022: Developed a ROS package to deploy computer vision/perception algorithms. The ROS package processes images from the ZED Camera stream and feeds them into a classifier network which outputs the detections.

## Installation
### Installing from source

```bash
git clone https://github.coecis.cornell.edu/Resistance-Racing/Perception-Deployment.git
cd Perception-Deployment/
git checkout master
```

## API

1. Make sure the ZED camera is plugged in.
2. Launch the ZED-ROS wrapper node by running ```roslaunch zed_wrapper zed.launch``` in the terminal.
3. Run ```rosrun object_detection object_detection.py``` in the terminal to begin detection with the default YOLOv3 classifier.
4. The outputs should be stored in the 'detectionoutput' directory.


### Dependencies <a name=“dependencies”></a>

The ROS package depends on the Zed-ROS wrapper. All other required dependencies for the project can be accumulated by running the following commands in terminal:

```bash
pip install pipdeptree
```
```bash
pipdeptree
```


## Algorithms and Designs <a name=“algorithms-and-designs”></a>
### Algorithm(s) in Use with Rationale <a name=“algorithm-in-use-with-rationale”></a>

The YOLOv3 algorithm has lower latency at the cost of some accuracy in comparison to other state-of-the-art object detection algorithms. A more detailed description of how YOLO works can be found in the paper below.

_Joseph Redmon, Ali Farhadi_ <br>

**Abstract** <br>
We present some updates to YOLO! We made a bunch
of little design changes to make it better. We also trained
this new network that’s pretty swell. It’s a little bigger than
last time but more accurate. It’s still fast though, don’t
worry. At 320 × 320 YOLOv3 runs in 22 ms at 28.2 mAP,
as accurate as SSD but three times faster. When we look
at the old .5 IOU mAP detection metric YOLOv3 is quite
good. It achieves 57.9 AP50 in 51 ms on a Titan X, compared
to 57.5 AP50 in 198 ms by RetinaNet, similar performance
but 3.8× faster. As always, all the code is online at
https://pjreddie.com/yolo/.

[[Paper]](https://pjreddie.com/media/files/papers/YOLOv3.pdf) [[Project Webpage]](https://pjreddie.com/darknet/yolo/) [[Authors' Implementation]](https://github.com/pjreddie/darknet)

```
@article{yolov3,
  title={YOLOv3: An Incremental Improvement},
  author={Redmon, Joseph and Farhadi, Ali},
  journal = {arXiv},
  year={2018}
}
```

## Performance <a name=“performance”></a>

| Model                   | mAP (min. 50 IoU) |
| ----------------------- |:-----------------:|
| YOLOv3 608 (paper)      | 57.9              |
| YOLOv3 608 (this impl.) | 57.3              |
| YOLOv3 416 (paper)      | 55.3              |
| YOLOv3 416 (this impl.) | 55.5              |

## Inference
Uses pretrained weights to make predictions on images. Below table displays the inference times when using as inputs images scaled to 256x256. The ResNet backbone measurements are taken from the YOLOv3 paper. The Darknet-53 measurement marked shows the inference time of this implementation on my 1080ti card.

| Backbone                | GPU      | FPS      |
| ----------------------- |:--------:|:--------:|
| ResNet-101              | Titan X  | 53       |
| ResNet-152              | Titan X  | 37       |
| Darknet-53 (paper)      | Titan X  | 76       |
| Darknet-53 (this impl.) | 1080ti   | 74       |


## Future Work/Updates <a name=“future-work”></a>

Next steps include:
1. Fixing the image stream subscriber lag issue by only storing the most recent image from the ZED Camera. A RosPy specific apprroach may be necessary.
2. Redesigning the repository to swap out YOLOv3 for other classifiers.
3. Integrate motion planning algorithms into the current package.


## Reflection <a name=“reflection”></a>
If I were to start this project over, I would redesign the workspace structure and document how they are chained since that can be a little confusing as this project scales.
Potential improvements apart from addressing the concern above would be to modularize more so that swapping out classifiers would be simpler. Consequently, classifier packages would be required to have a particular structure. For example, each object detection package would have a detect script which runs its respective model on a single input image or batch of images. How motion planning is to be integrated into this ROS package is 
yet unclear; perhaps it would be better if it were a stand-alone package, these are all topics for discussion in future semesters.
