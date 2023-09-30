import pyzed.sl as sl
import math
import numpy as np
import sys
import math
import cv2
import time
import matplotlib.pyplot as plt
PYDEVD_DISABLE_FILE_VALIDATION=1

#Define camera
zed = sl.Camera()

#Define params
init_params = sl.InitParameters()
runtime_parameters = sl.RuntimeParameters()

#set init params
init_params.depth_mode = sl.DEPTH_MODE.ULTRA 
init_params.coordinate_units = sl.UNIT.CENTIMETER 
init_params.depth_minimum_distance = .5 # Set the minimum depth perception distance to 15cm
init_params.depth_maximum_distance = 10000
init_params.camera_resolution = sl.RESOLUTION.HD720
#runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL
print(init_params.camera_resolution)

init_params.camera_fps = 30
#Set camera params
# zed.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_AUTO, 2)
#zed.set_camera_settings(sl.VIDEO_SETTINGS.DENOISING, 50)
init_params.depth_stabilization = False

#Helper Functions

def depthmask(nparr):
    nanless = np.nan_to_num(nparr)
    nanless[nanless == 0] = 1
    #masked = np.ma.masked_array(nanless, mask = False, fill_value = 100) #np.ma.masked_greater_equal(nparr,1), fill_value = 100)
    return nanless

def depth_heat_map(nparr):
    return cv2.applyColorMap(nparr.astype(np.uint8),colormap)

def determine_stop(nparr):
    if(np.mean(nparr)<10): # will need to be a multi-step procedure that assigns some sort of T/F val determine if something is classified as an obstacle.
        # If this is not executed, the car would (and should) see the road below it as preventing its forward motion which cannot happen. As such we need to calculate
        # some sort of disparity that assigns obstacle values only where appropriate and uses the secondary obstacle map (in tandem with the depth map) to isolate
        # points which are BOTH obstacles and within a range that we can (for now) predetermine
        return True
    return False

# def obstacle_map(nparr): should be defined sequentially from one corner of the array and associate a non-zero value with each obstacle
# if we want to ignore the obstacle differentiation and just create a secondary binary map of what is and is not viewed as an obstacle we can
# do that instead

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

while True:
    imgs = [] #accumulator

    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        depth = sl.Mat() #sl.Mat(1280, 720, sl.MAT_TYPE.F32_C1)   # init .mat for float depth for calc
        image = sl.Mat()                                # init .mat for BGR image
        # depth_im = sl.Mat()
        # zed.retrieve_image(depth_im, sl.VIEW.DEPTH)   # fill .mat for int depth for opencv
        zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
        zed.retrieve_image(image, sl.VIEW.LEFT )       # fill .mat for BGR image, VIEW.DEPTH
        depth_nparr = depth.get_data()  
        # print(depth_nparr[1][1].shape)                # get numpy array for calc depth mat
        rgb_nparr = image.get_data()                    # get numpy array for rgb img
        # depth_im_nparr = depth_im.get_data()
    else:
        print('fail')

    depth_masked = depthmask(depth_nparr)     

    # testing would indicate that the current colormap uses all 0 vals as black, which makes them difficult to distinguish from distant values

    print(determine_stop(depth_masked))
    cv2.imshow("Depth-direct",depth_heat_map(depth_masked))
    cv2.waitKey(30)
