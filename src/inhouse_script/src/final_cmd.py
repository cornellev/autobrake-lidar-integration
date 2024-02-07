#!/usr/bin/env python3

from pickle import FALSE, TRUE
from tokenize import String
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import Bool
# from std_msgs.msg import String
from pacmod3_msgs.msg import SystemCmdFloat
from pacmod3_msgs.msg import SteeringCmd
from geometry_msgs.msg import Point



latest_vertical_command = 0  # Variable to store the latest command
latest_horizontal_command=0
latest_task=5
horizontal_position = 0
vertical_position = 0   
is_working = 0
last_emergency= TRUE

def state_callback(msg):
    # Interpret the received state message
    global horizontal_position
    global vertical_position
    global is_working

    horizontal_position = msg.x
    vertical_position = msg.y
    is_working = bool(msg.z)

    print("Horizontal Position:", horizontal_position)
    print("Vertical Position:", vertical_position)
    print("Is Working:", is_working)


def vertical_callback(data):
    global latest_vertical_command
    print(data)
    latest_vertical_command = data.command # Assuming 'command' is a Float32 in the SystemCmdFloat message

def horizontal_callback(data):
    global latest_horizontal_command
    print(data)
    latest_horizontal_command = data.command # Assuming 'command' is a Float32 in the SystemCmdFloat message
    if abs(latest_horizontal_command)<0.15:
        latest_horizontal_command=0

def task_callback(data):
    global latest_task
    print(data)
    latest_task=data.data
    if latest_task==0:
        latest_task=5    

def emergency_brake(data):
    global last_emergency
    print("emergency", data.data)
    last_emergency=data.data


if __name__ == '__main__':

    max_extension_horizontal=4997
    max_extension_vertical=1100
    threshold_both_motion=1300
    desired_x=0
    desired_y=max_extension_vertical
    rospy.init_node('command_to_brake_publisher')

    # Initialize the publisher for the 'brake' topic
    vertical_motion = rospy.Publisher('motion_command_vertical', Int32, queue_size=1)
    horizontal_motion = rospy.Publisher('motion_command_horizontal', Int32, queue_size=1)
    # horizontal_motion = rospy.Publisher('motion_command_horizontal', Int32, queue_size=1)
    # Initialize the subscriber for the topic with the provided message structure
    rospy.Subscriber('/pacmod/brake_cmd', SystemCmdFloat, vertical_callback)
    rospy.Subscriber('/pacmod/steering_cmd', SteeringCmd, horizontal_callback)
    rospy.Subscriber('/AEBlidar', Bool, emergency_brake)
    rospy.Subscriber('/tasks', Int32, task_callback)
    rospy.Subscriber('arduino_state', Point, state_callback)

    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():

        if latest_task == 1:
            desired_x=0
            desired_y=max_extension_vertical-200
            horizontal_motion.publish(desired_x)  # Adjust values as needed
            if abs(horizontal_position-desired_x) <= threshold_both_motion:
                vertical_motion.publish(max_extension_vertical-200)
            else:
                vertical_motion.publish(0)

        elif latest_task == 2:
            desired_x=1*max_extension_horizontal
            horizontal_motion.publish(desired_x)  # Adjust values as needed
            if abs(horizontal_position-desired_x) <= threshold_both_motion:
                desired_y=max_extension_vertical
                vertical_motion.publish(max_extension_vertical)
            else:
                vertical_motion.publish(0)
        elif latest_task == 3:
            desired_x=2*max_extension_horizontal
            horizontal_motion.publish(desired_x)  # Adjust values as needed
            if abs(horizontal_position-desired_x) <= threshold_both_motion:
                desired_y=max_extension_vertical
                vertical_motion.publish(max_extension_vertical)
            else:
                vertical_motion.publish(0)
        elif latest_task == 4:
            desired_x=3*max_extension_horizontal
            horizontal_motion.publish(desired_x)  # Adjust values as needed
            if abs(horizontal_position-desired_x) <= threshold_both_motion:
                desired_y=max_extension_vertical
                vertical_motion.publish(max_extension_vertical)
            else:
                vertical_motion.publish(0)
        elif latest_task == 5:
            if not last_emergency:
                y=int(max_extension_vertical*1)
            else:    
                y=int(max_extension_vertical*latest_vertical_command)
            x=int(horizontal_position + latest_horizontal_command * -50)
            # x = int(min(x, 100000))
            # y = int(min(y, max_extension_vertical))
            # x=max(x,0)
            # y=max(y,0)
            if x<0:
                x=0
            if x>15500:
                x=15500
            vertical_motion.publish(y)
            horizontal_motion.publish(x)
    
        if horizontal_position == desired_x and vertical_position==desired_y:
            rospy.sleep(1)  # introduce a 3-second delay
            vertical_motion.publish(0)
            latest_task=5

        is_working = 1
        # latest_task = 5
        rate.sleep()



