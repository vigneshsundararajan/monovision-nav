#!/usr/bin/env python3

#import necessary libraries and files
import rospy
import math
from aut_sys import motors
from fiducial_msgs.msg import FiducialTransformArray
import time

class Fiducials:
    def __init__(self):
        self.v=0.5
        self.r=0.13
        self.w= (2*self.v)/self.l
        self.rate=rospy.Rate(10)
        self.sub=rospy.Subscriber('/fiducial_transforms', FiducialTransformArray, self.fid_callback)
        self.pub = rospy.Publisher('/motors', motors, queue_size=10)

    def fid_callback(self,msg):
        for m in msg.transforms:
            self.tx=m.transform.translation.x
            self.ty=m.transform.translation.y
            self.tz=m.transform.translation.z

            self.rx=m.transform.rotation.x
            self.ry=m.transform.rotation.y
            self.rz=m.transform.rotation.z
            self.rw=m.transform.rotation.w

            q0=2*((self.rw*self.rx)+(self.ry*self.rz))
            q1=1-(2*(self.rx**2)+(self.ry**2))
            q2=2*((self.rw*self.ry)-(self.rx*self.rz))
            if q2>1:
                q2=1
            elif q2<-1:
                q2=-1
            else:
                q2=q2
            q3=2*((self.rw*self.rz)+(self.ry*self.rx))
            q4=q1=1-(2*(self.ry**2)+(self.rz**2))

            self.roll=math.atan(q0,q1)
            self.pitch=math.asin(q2)
            self.yaw=math.atan(q3,q4)
    
    def fiducials(self,msg):
        rospy.init_node('fiducials', anonymous=True)
        self.sub=rospy.Subscriber('/fiducial_transforms', FiducialTransformArray, self.fid_callback)
        vel=motors()
        while not rospy.is_shutdown():
            if msg.transforms:
                currentangle=self.yaw
                targetangle=math.atan((self.tx+1)/(-self.tz+1.5))
                theta=(targetangle-currentangle)
                time_theta=abs(theta)/self.w

                rot_dur=0
                rot_start=time.time()
                while(abs(rot_dur)<=time_theta):
                    rot_dur=time.time()-rot_start
                    if(theta>0):
                        vel.leftSpeed=-self.v
                        vel.rightSpeed=self.v
                    else:
                        vel.leftSpeed=self.v
                        vel.rightSpeed=-self.v
                    self.pub.publish(vel)
                
                dist=math.sqrt((self.tx+1)**2 + (self.tz-1.5)**2)
                time_dist=abs(dist)/0.2
                trans_dur=0
                trans_start=time.time()
                while(abs(trans_dur)<=time_dist):
                    trans_dur=time.time()-trans_start
                    vel.leftSpeed=0.2
                    vel.rightSpeed=0.2
                    self.pub.publish(vel)
                
            vel.leftSpeed=0.0
            vel.rightSpeed=0.0
            self.pub.publish(vel)

            self.rate.sleep()
    
if __name__ == '__main__':
    f=Fiducials()
    try:
        f.Fiducials()
    except KeyboardInterrupt:
        pass


                








        

