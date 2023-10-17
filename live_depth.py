import pyzed.sl as sl
import math
import numpy as np
import sys
import math
import cv2
import time
import matplotlib.pyplot as plt

PYDEVD_DISABLE_FILE_VALIDATION=1
STOPPING_DISTANCE = 100 #mm
MAXIMUM_DISTANCE = 50000 #mm
MINIMUM_DISTANCE = 1 #mm
MINAREA = 800 #pixels
CAMERA_VFOV=54 #degrees
CAMERA_VRES = 720 #pixels
CAMERA_HEIGHT = 100 #mm
#Define camera
zed = sl.Camera()

#Define params
init_params = sl.InitParameters()
runtime_parameters = sl.RuntimeParameters()

#set init params
init_params.depth_mode = sl.DEPTH_MODE.ULTRA 
init_params.coordinate_units = sl.UNIT.MILLIMETER
init_params.depth_minimum_distance = MINIMUM_DISTANCE # Set the minimum depth perception distance to 1mm
init_params.depth_maximum_distance = MAXIMUM_DISTANCE
init_params.camera_resolution = sl.RESOLUTION.HD720
#runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL
init_params.camera_fps = 30
#Set camera params
init_params.depth_stabilization = False
#Helper Functions

def depthmask(nparr):
    nanless = np.nan_to_num(nparr)
    nanless[nanless == 0] = MAXIMUM_DISTANCE
    #masked = np.ma.masked_array(nanless, mask = False, fill_value = 100) #np.ma.masked_greater_equal(nparr,1), fill_value = 100)
    return nanless

def depth_heat_map(nparr):
    return cv2.applyColorMap(nparr.astype(np.uint8),colormap)

# def findCentroid(rectangles):
#     centers = np.array([r[0] for r in rectangles])
#     centroid = np.median(centers, axis=0)
#     # print("centroid : " , centroid)
#     return centroid

def determine_stop(arr):
    nparr = np.array(arr)
    degree_change_pp = (CAMERA_VFOV)/(CAMERA_VRES)

    for i in range(1, len(nparr)+1):
        if i < len(nparr)//2:
            road_filter = np.logical_and(nparr[len(nparr)-i ] < (CAMERA_HEIGHT * np.tan((90 - CAMERA_VFOV/2 + degree_change_pp*i)*np.pi/180)) , nparr[len(nparr)-i ] < STOPPING_DISTANCE)
            road_filter = road_filter*1 #normalizes to ints
            nparr[len(nparr) - i] = road_filter 
        else:
            road_filter = nparr[len(nparr)-i] < STOPPING_DISTANCE
            road_filter = road_filter*1
            nparr[len(nparr) - i] = road_filter
    
    nparr = nparr.astype(np.uint8)
    kernel = np.ones((30,30), np.uint8)
    cv2.erode(nparr, kernel)
    cv2.dilate(nparr,kernel)
    contours, dummy = cv2.findContours(nparr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    nparr = nparr * 255

    if len(contours) == 0:
        return False, nparr
    else:
        for cnt in contours:
            if cv2.contourArea(cnt) >= MINAREA:
                return True, nparr
        return False, nparr

err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print(repr(err))
    print('Fail')
    exit(-1)

#Color map def
colormap = cv2.COLORMAP_INFERNO

#Main loop:
fig, axs = plt.subplots(ncols=3)
fig.set_size_inches(10, 4)

print("attempting to connect to zed (camera)")

while True:
    imgs = [] #accumulator
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        depth = sl.Mat() #sl.Mat(1280, 720, sl.MAT_TYPE.F32_C1)   # init .mat for float depth for calc
        image = sl.Mat()                                # init .mat for BGR image
        zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
        zed.retrieve_image(image, sl.VIEW.LEFT)       # fill .mat for BGR image, VIEW.DEPTH
        depth_nparr = depth.get_data()  
        rgb_nparr = image.get_data()                    # get numpy array for rgb img
    else:
        print('fail')

    depth_masked = depthmask(depth_nparr)
    x,stopmap = determine_stop(depth_masked)
    cv2.applyColorMap(stopmap,colormap)
    cv2.imshow("Depth-filtered",depth_heat_map(stopmap))
    cv2.imshow("Depth-visualization",depth_heat_map(depth_masked))
    if x:
        print("Stop")
    else:
        print("Go")
    cv2.waitKey(30)
