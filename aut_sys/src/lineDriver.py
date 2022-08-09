#!/usr/bin/env python3

import rospy
from gpiozero import DigitalInputDevice
from aut_sys.msg import lines

class lineDriver:

  def __init__(self):
    #set default
    self.left = DigitalInputDevice(17)
    self.mid = DigitalInputDevice(27)
    self.right = DigitalInputDevice(22)
  
  def init_app(self):
    #ROS publisher
    self.linePub = rospy.Publisher('lines', lines, queue_size=10)
    rospy.init_node('lineDriver', anonymous=True)
    #this rate will drive the serial read rate
    self.rate=rospy.Rate(20)
  
  #assemble messages and publish
  def __publishLines(self, left,mid,right):
    msg = lines()
    msg.leftLine = left
    msg.midLine = mid
    msg.rightLine = right
    rospy.loginfo(msg)
    self.linePub.publish(msg)
  
  #as named...
  def main(self):
    while not rospy.is_shutdown():
      #read from the sensor
      self.__publishLines(self.left.value,self.mid.value,self.right.value)
      self.rate.sleep()

if __name__ == '__main__':
  try:
    l = lineDriver()
    l.init_app()
    l.main()
  except KeyboardInterrupt:
    pass
