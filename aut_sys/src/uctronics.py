#!/usr/bin/env python3

import rospy
import time
from aut_sys.msg import distance, motors, leds, lines, servos

class UCTRONICS:

    # Creating the class constructor
    def __init__(self, dist):
        self.dist = dist

    # This function reads distance from the subscriber
    def dist_callback(self, data):
        self.dist = data.distance
        rospy.loginfo("Distance: {}".format(self.dist))

    def uctronics_node(self):

       # Creating the distance message object
        dst_msg = distance()

        # Creating a publisher
        pub = rospy.Publisher('motors', motors, queue_size=10)

        # Declaring a node and then registering it
        rospy.init_node('uctronics_node', anonymous=True)

        # Creating a subscriber
        sub = rospy.Subscriber('/distance', distance, self.dist_callback)

        # Setting execution rate to 10Hz
        rate = rospy.Rate(10)


        """
         This is the main loop

        """
        start_time = time.time()
        duration = 2

        while not rospy.is_shutdown():
            # Creating the speed message object
            spd_msg = motors()
     
            # Setting current time
            current_time = time.time()
            elapsed_time = current_time - start_time

            # Breaking out of loop if more than 2 seconds have passed
            if elapsed_time > duration:

                # Resetting motor speeds to zero 
                spd_msg.leftSpeed = 0.0
                spd_msg.rightSpeed = 0.0

                pub.publish(spd_msg)

                rate.sleep()
                break

            else:
                self.distance = dst_msg.distance

                spd_msg.leftSpeed = 1.0
                spd_msg.rightSpeed = 1.0

                # Logging info on console
                rospy.loginfo('[uctronics_node] Running')

                # Publishing data
                pub.publish(spd_msg)

                # Sleep the necessary amount of time to keep a 10Hz execution rate
                rate.sleep()


if __name__ == '__main__':
        
    dist = 0
    uctronics = UCTRONICS(dist)
    
    try:
        uctronics.uctronics_node()
    except rospy.ROSInterruptException:
        pass
