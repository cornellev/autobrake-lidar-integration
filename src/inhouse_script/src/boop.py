#!/usr/bin/python3

import numpy as np
import rospy

from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

def callback(data):
    pub.publish(str(data.ranges[0]))

if __name__ == "__main__":
    try:
    	rospy.init_node("boop", anonymous=True)
    	pub = rospy.Publisher("boop_out", String, queue_size=1)
    	sub = rospy.Subscriber("/scan", LaserScan, callback)
    	rospy.spin()
    except rospy.ROSInterruptException:
    	pass
