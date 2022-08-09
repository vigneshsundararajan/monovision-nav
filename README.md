# Monocular Vision based Navigation of a Robot using ROS

 ## Dependencies
 The following dependencies need to be installed prior to calibrating the camera:
 ```bash
 $ rosdep install camera_calibration
 $ sudo apt install ros-noetic-fiducials
 $ pip install opencv-contrib-python
 $ sudo apt install cairosvg python3-cairosvg
 ```

 ## Camera calibration
 ```bash
 rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.025 image:=/raspicam_node/image camera:=/raspicam_node --no-service-check
 ```

 The calibrated file can then be stored in the `aut_sys/src/raspicam_node/camera_info` folder
 
 
![camera-calib](https://user-images.githubusercontent.com/68025565/183766841-f166648b-b3bc-4b8d-9fe8-8827317d6dd9.jpeg)
