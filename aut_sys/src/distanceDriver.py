#!/usr/bin/env python3

import rospy
from gpiozero import DistanceSensor
from aut_sys.msg import distance

class distanceDrive:

  def __init__(self):
    #set default
    self.dist = 0
    self.sensor = DistanceSensor(echo=23,trigger=26)
  
  def init_app(self):
    #ROS publisher
    self.distPub = rospy.Publisher('distance', distance, queue_size=10)
    rospy.init_node('distanceDriver', anonymous=True)
    #this rate will drive the serial read rate
    self.rate=rospy.Rate(10)
  
  #assemble messages and publish
  def publishDist(self, dist):
    msg = distance()
    msg.distance = dist
    rospy.loginfo(msg)
    self.distPub.publish(msg)
  
  #as named...
  def main(self):
    while not rospy.is_shutdown():
      #read from the sensor
      dist = self.sensor.distance
      self.publishDist(dist)
      self.rate.sleep()

if __name__ == '__main__':
  try:
    d = distanceDrive()
    d.init_app()
    d.main()
  except KeyboardInterrupt:
    pass
