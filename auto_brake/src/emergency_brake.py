import numpy as np
import cv2
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import Bool
from sensor_msgs.msg import Image

cv_bridge = CvBridge()

PYDEVD_DISABLE_FILE_VALIDATION=1
STOPPING_DISTANCE = 1 #m
MAXIMUM_DISTANCE = 70 #m
MINIMUM_DISTANCE = .5 #m
MINAREA = 800 #pixels
CAMERA_VFOV=54 #degrees
CAMERA_VRES = 720 #pixels
CAMERA_HEIGHT = .2 #m
bridge = CvBridge()

def depth_callback(data):
    #print(MINAREA)
    mat = bridge.imgmsg_to_cv2(data, desired_encoding = 'passthrough')
    # print(mat)
    # it=1
    # while 1:
    #     print("11")
    #     if it==1:
    #         cv2.imshow("image", mat)
    #         cv2.waitKey()
    #         it=0
    #     print(it)

    depth_nparr = np.array(mat, dtype=np.float32)
    depth_masked = depthmask(depth_nparr)
    pub.publish(determine_stop(depth_masked))    

def depthmask(nparr):
    nanless = np.nan_to_num(nparr)
    nanless[nanless == 0] = MAXIMUM_DISTANCE
    return nanless

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
        return False
    else:
        for cnt in contours:
            if cv2.contourArea(cnt) >= MINAREA:
                return True
        return False

if __name__ == '__main__':
    while 1:
        try:
            #print("1")
            #print("2")
            rospy.init_node('AEBzed', anonymous=True)
            pub = rospy.Publisher('AEBzed', Bool, queue_size=1)
            depthsub = rospy.Subscriber("/zed/zed_node/depth/depth_registered", Image, depth_callback)
            rospy.spin()
        except rospy.ROSInterruptException:
            pass

