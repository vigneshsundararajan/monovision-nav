#!/usr/bin/env python3

import rospy
import time
from aut_sys.msg import distance, motors, leds, lines, servos


# This class performs the counterclockwise maneuver
class counterclockwise:

    # Creating the class constructor
    def __init__(self):
        rospy.on_shutdown(self.stop)
        self.pub = rospy.Publisher('motors', motors, queue_size=10)
        rospy.sleep(1)

        # Setting a rate of 5Hz = 0.2seconds
        rate = rospy.Rate(5)

        """
         This is the main loop

        """
        while not rospy.is_shutdown():

            # This loop is to repeat the motion 4 times to draw a square
            for i in range(4):
                spd_msg = motors()
                spd_msg.leftSpeed = 1.0
                spd_msg.rightSpeed = 1.0
                
                # Repeating the forward motion for 6*5Hz = 1.2 seconds
                for i in range(6):
                    self.pub.publish(spd_msg)
                    rate.sleep()

                spd_msg = motors()
                # Changing only right motor velocity to perform a left turn
                spd_msg.leftSpeed = 0.0
                spd_msg.rightSpeed = 1.0

                # Repeating the turning motion for 8*5Hz = 1.6 seconds
                for i in range(8):
                    self.pub.publish(spd_msg)
                    rate.sleep()
            break

    def stop(self):
        # This function resets all motor velocity values 
        # to zero to stop the robot
        spd_msg = motors()
        spd_msg.leftSpeed = 0.0
        spd_msg.rightSpeed = 0.0
        self.pub.publish(spd_msg)
 

# This class performs the clockwise maneuver
class clockwise:

    # Creating the class constructor
    def __init__(self):
        rospy.on_shutdown(self.stop)
        self.pub = rospy.Publisher('motors', motors, queue_size=10)
        rospy.sleep(1)

        # Setting a rate of 5Hz = 0.2 seconds
        rate = rospy.Rate(5)

        """
         This is the main loop

        """
        while not rospy.is_shutdown():

            # This loop is to keep on repeating the motion
            while(True):
                spd_msg = motors()
                spd_msg.leftSpeed = 1.0
                spd_msg.rightSpeed = 1.0
                
                # This loop moves the robot straight for 6*5Hz = 2 seconds 
                for i in range(10):
                    self.pub.publish(spd_msg)
                    rate.sleep()

                spd_msg = motors()
                spd_msg.leftSpeed = 1.0
                spd_msg.rightSpeed = 0.0

                # This loop performs the turn maneuver for 8*5Hz = 1.6 seconds
                for i in range(8):
                    self.pub.publish(spd_msg)
                    rate.sleep()
            break

    def stop(self):
        spd_msg = motors()
        spd_msg.leftSpeed = 0.0
        spd_msg.rightSpeed = 0.0
        self.pub.publish(spd_msg)
       
if __name__ == '__main__':
        
    rospy.init_node('counterclockwise') 
    counterclockwise()

    # To perform task 2, uncomment the below lines and comment the previous two lines
    # rospy.init_node('clockwise')
    # clockwise()
