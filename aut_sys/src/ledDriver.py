#!/usr/bin/env python3

import rospy
import board
import neopixel
from aut_sys.msg import leds
from time import sleep

class ledDriver:
  '''
  ..ledDriver
  ..This class is aimed to handle the RGB LEDs of the UCTRONICS car robot.
  '''
  def __init__(self):
    self.__pixels = neopixel.NeoPixel(board.D18,3)
    
  def __update_led_cbk(self,data):
    self.__pixels[0]=(data.r1,data.g1,data.b1)
    self.__pixels[1]=(data.r2,data.g2,data.b2)
    self.__pixels[2]=(data.r3,data.g3,data.b3)

  def init_app(self):
    rospy.Subscriber('leds',leds,self.__update_led_cbk)
    rospy.init_node('ledDriver',anonymous=True)
    self.rate = rospy.Rate(10)

  def main(self):
    while not rospy.is_shutdown():#run at 10Hz
      self.rate.sleep()

if __name__ == '__main__':
  try:
    ld = ledDriver()
    ld.init_app()
    ld.main()
  except KeyboardInterrupt:
    pass


