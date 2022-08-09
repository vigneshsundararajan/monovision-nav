#!/usr/bin/env python3

import rospy
import time
from aut_sys.msg import distance, motors, leds, lines, servos

class line_follower:

    # Class constructor
    def __init__(self):
        # Creating the class variables
        self.dist = 0
        self.left = False
        self.right = False
        self.mid = False

    # Callback function which gathers data from the ultrasonic sensor
    def ultra_callback(self, data):
        self.dist = data.distance
        rospy.loginfo('Distance: {}'.format(self.dist))

    # Callback function which sets bool flags for which line is active
    def ir_callback(self, lines):
        self.left = lines.leftLine
        self.right = lines.rightLine
        self.mid = lines.midLine

    def linefollower_node(self):
        rospy.init_node('linefollower_node', anonymous=True)

        # Setting a rate of 100Hz so that the motion gets updated every 0.010 seconds
        rate = rospy.Rate(100)
        motor_pub = rospy.Publisher('/motors', motors, queue_size=1)

        spd_msg = motors()
        
        while not rospy.is_shutdown():
            sub = rospy.Subscriber('/distance', distance, self.ultra_callback)
            irsub = rospy.Subscriber('/lines', lines, self.ir_callback)

            # Setting safe distance as 10 cm
            if self.dist > 0.1:

                # Checking if left sensor is active, then turn left
                if (self.left == True) and (self.right == False) and (self.mid == False):
                    spd_msg.leftSpeed = 0.0
                    spd_msg.rightSpeed = 0.05
                    motor_pub.publish(spd_msg)
                    rate.sleep()

                # Checking if right sensor is active, then turn right
                elif (self.right == True) and (self.left == False) and (self.mid == False):
                    spd_msg.leftSpeed = 0.05
                    spd_msg.rightSpeed = 0.0
                    motor_pub.publish(spd_msg)
                    rate.sleep()

                # Checking if mid sensor is active, then go straight
                elif ((self.mid == True) and (self.right == True)) or ((self.left == True) and (self.mid == True)):
                    spd_msg.leftSpeed = 0.05
                    spd_msg.rightSpeed = 0.05
                    motor_pub.publish(spd_msg)
                    rate.sleep()

                # If none of the above conditions are satisfied, reset motor speeds to 0
                else:
                    spd_msg.leftSpeed = 0.0
                    spd_msg.rightSpeed = 0.0
                    motor_pub.publish(spd_msg)
                    rate.sleep()
            else:
                spd_msg.leftSpeed = 0.0
                spd_msg.rightSpeed = 0.0
                motor_pub.publish(spd_msg)
                rate.sleep()

if __name__ == '__main__':
    lf = line_follower()
    try:
        lf.linefollower_node()
    except ROSInterruptException:
        pass
