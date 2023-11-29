import numpy as np
from numpy import inf
import rospy
from std_msgs.msg import Float32,Float32MultiArray
from sensor_msgs.msg import Joy
from joy_control.msg import Suffer

MAX_STEER = 60 #degrees

def callback(data):
    x = determine_drive(data.axes)
    pub.publish(x)

def determine_drive(axes_arr):
    msg = Suffer()
    drive_out = 1 - ((axes_arr[5] +1) /2)
    steer_out = -axes_arr[3] * MAX_STEER/2
    msg.throttle = drive_out
    msg.steer = steer_out

    return msg

if __name__ == '__main__':
    try:
        rospy.init_node('joyride_sender', anonymous=True)
        pub = rospy.Publisher('joyride', Suffer, queue_size=1)
        depthsub = rospy.Subscriber("/joy", Joy, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

