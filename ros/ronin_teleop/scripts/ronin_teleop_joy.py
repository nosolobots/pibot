#!/usr/bin/env python

# ----------------------------------------------------------------------------
# file: ronin_teleop_joy.py
# pkg:  ronin_teleop
# 
# node: ronin_teleop_joy
# sub:  /joy
# pub:  /cmd_vel
#       /servo_cam
# 
# desc: Subscribes to /joy messages published by ROS joy_node and publish 
#      /cmd_vel and /servo_cam messages
#      
# ver:  0.1 (jul-18)
#
# upd:        
# ----------------------------------------------------------------------------

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from ronin_msgs.msg import CamServo

_NODE_NAME = "ronin_teleop_node"

class TeleopJoy():
    # Default values (PS4)
    _DEFAULT_AXIS_LINEAR_VEL = 1
    _DEFAULT_AXIS_ANGULAR_VEL = 0
    _DEFAULT_AXIS_CAM_PITCH = 5
    _DEFAULT_AXIS_CAM_YAW = 2
    _DEFAULT_AXIS_PAD_UD = 7
    _DEFAULT_AXIS_PAD_RL = 6
    _DEFAULT_AXIS_DEADZONE = 0.2
    _DEFAULT_BUTTON_CENTER_CAM = 1
    
    _DEFAULT_MAX_LINEAR_VEL = 0.4
    _DEFAULT_MAX_ANGULAR_VEL = 1.25
    
    _DEFAULT_USE_CAM = False
    
    def __init__(self):
        # Setting axes&buttons
        self.axis_linear_vel = rospy.get_param("~axis_linear_vel",
                                                self._DEFAULT_AXIS_LINEAR_VEL)
        self.axis_angular_vel = rospy.get_param("~axis_angular_vel",
                                                self._DEFAULT_AXIS_ANGULAR_VEL)
        self.axis_cam_pitch = rospy.get_param("~axis_cam_pitch",
                                              self._DEFAULT_AXIS_CAM_PITCH)
        self.axis_cam_yaw = rospy.get_param("~axis_cam_yaw",
                                            self._DEFAULT_AXIS_CAM_YAW)
        self.axis_pad_UD = rospy.get_param("~axis_pad_UD",
                                             self._DEFAULT_AXIS_PAD_UD)                                            
        self.axis_pad_RL = rospy.get_param("~axis_pad_RL",
                                             self._DEFAULT_AXIS_PAD_RL)                                                    
        self.axis_deadzone = rospy.get_param("~axis_deadzone",
                                             self._DEFAULT_AXIS_DEADZONE)
        self.button_center_cam = rospy.get_param("~button_center_cam",
                                             self._DEFAULT_BUTTON_CENTER_CAM)                                                                                         

        # Setting maximun velocities
        self.max_linear_vel = rospy.get_param("~max_linear_vel",
                                              self._DEFAULT_MAX_LINEAR_VEL)
        self.max_angular_vel = rospy.get_param("~max_angular_vel",
                                               self._DEFAULT_MAX_ANGULAR_VEL)
        
        # Camera activation
        self.use_cam = rospy.get_param("~use_cam", self._DEFAULT_USE_CAM)

        # Subscriber to joy node
        self.sub_joy = rospy.Subscriber('joy', Joy, self.joy_cb, queue_size=10)

        # Publishers
        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        
        if self.use_cam:
            self.pub_servo = rospy.Publisher('/servo_cam', 
                                             CamServo, queue_size=1)
        
    def joy_cb(self, joy):
        # Robot base movement
        vel = Twist()
        vel.linear.x = 0.0
        vel.angular.z = 0.0
        if abs(joy.axes[self.axis_angular_vel]) > self.axis_deadzone:
            #vel.angular.z = (-1.0)*self.max_angular_vel * joy.axes[self.axis_angular_vel]
            vel.angular.z = self.max_angular_vel * joy.axes[self.axis_angular_vel]
        if abs(joy.axes[self.axis_linear_vel]) > self.axis_deadzone:
            vel.linear.x = self.max_linear_vel * joy.axes[self.axis_linear_vel]
        self.pub_cmd_vel.publish(vel)

        # Camera movement
        if self.use_cam:
            # Cam axes
            cam_rotation = CamServo()
    
            # Check cam center
            if(joy.buttons[self.button_center_cam]):
                cam_rotation.center_cam = 1
            else:    
                # Check pitch rotation
                if(joy.axes[self.axis_cam_pitch] < -self.axis_deadzone):
                    cam_rotation.rot_pitch = -1
                elif(joy.axes[self.axis_cam_pitch] > self.axis_deadzone):
                    cam_rotation.rot_pitch = 1
        
                # Check yaw rotation
                if(joy.axes[self.axis_cam_yaw] < -self.axis_deadzone):
                    cam_rotation.rot_yaw = -1
                elif(joy.axes[self.axis_cam_yaw] > self.axis_deadzone):
                    cam_rotation.rot_yaw = 1
    
            self.pub_servo.publish(cam_rotation)

if __name__ == '__main__':
    # init ROS node
    rospy.init_node(_NODE_NAME, log_level=rospy.INFO)
    
    # create joystick object
    teleop_joy = TeleopJoy()

    rospy.spin()

