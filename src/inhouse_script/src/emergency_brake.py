#!/usr/bin/python3

import numpy as np
from numpy import inf
import rospy
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan

PYDEVD_DISABLE_FILE_VALIDATION = 1
STOPPING_DISTANCE = 5 #m
MAXIMUM_DISTANCE = 12 #m
MINIMUM_DISTANCE = .5 #m
MINAREA = 3

deg = 40

def depth_callback(data):
    x = determine_stop(data.ranges)
    pub.publish(x)

def inf_clean(arr):
    num_arr = np.array(arr)
    num_arr[num_arr == inf] = MINIMUM_DISTANCE
    return num_arr


def determine_stop(arr):
    out = False
    for i in range(-(int(deg / 2)), int(deg / 2)):
        if arr[i - 1] < STOPPING_DISTANCE and arr[i] < STOPPING_DISTANCE and arr[i + 1] < STOPPING_DISTANCE:
            return True
    return False


if __name__ == '__main__':
    try:
        rospy.init_node('AEBLidar_sender', anonymous=True)
        pub = rospy.Publisher('AEBlidar', Bool, queue_size=1)
        depthsub = rospy.Subscriber("/scan", LaserScan, depth_callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
