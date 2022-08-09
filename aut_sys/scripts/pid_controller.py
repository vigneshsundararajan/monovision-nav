#!/usr/bin/env python3

import rospy
from aut_sys.msg import distance, motors, leds, lines, servos
import time

integral = 0
derivative = 0
previous_error = 0
output = 0
class pidcontrol:
    def __init__(self):
        self.rate = rospy.Rate(10)
        self.pub = rospy.Publisher('/motors', motors, queue_size=1)
        self.dt = 0.1

    def dist_callback(self,data):
        global integral, derivative, previous_error, output
        feedback = data.distance

        # Setting PID gains
        kp = 1.2
        ki = 0.1
        kd = 0

        # Setting the setpoint distance for error calculation
        setpoint = 0.5

        # Creating the motors object
        spd_msg = motors()

        error = -setpoint + feedback
        integral = integral + (error * self.dt)
        derivative = (error - previous_error) / self.dt
        output = (kp*error) + (ki*integral) + (kd*derivative)
        previous_error = error

        spd_msg.leftSpeed = output
        spd_msg.rightSpeed = output
        self.pub.publish(spd_msg)

        self.rate.sleep()
        rospy.loginfo('Distance: {}'.format(feedback))

    def pidcontrol_node(self):
        sub = rospy.Subscriber('/distance', distance, self.dist_callback) 

        while not rospy.is_shutdown():
            self.rate.sleep()
            rospy.spin()


if __name__ == '__main__':

    rospy.init_node('pidcontrol_node', anonymous=True)
    pid = pidcontrol()
    try:
        pid.pidcontrol_node()
    except rospy.ROSInterruptExecution():
        pass
