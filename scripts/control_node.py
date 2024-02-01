#!/usr/bin/env python3

# import ROS for node developing 
import rospy 
# import geometry msg for turtle control commands
from geometry_msgs.msg import Twist
# import Pose for getting turtle position 
from turtlesim.msg import Pose 
# import created message type for turtle control 
from robotics_lab1.msg import Turtlecontrol 

#create variables to records position and control parameters
pos_msg = Pose()
turtle_control_msg = Turtlecontrol() 

# create callback functions to receive positions and control parameters
def pose_callback(current_pose):
	global pos_msg
	pos_msg = current_pose
	rospy.loginfo("x is %.02f", pos_msg.x)

def control_params_callback(current_control):
	global turtle_control_msg
	turtle_control_msg.kp = current_control.kp
	turtle_control_msg.xd = current_control.xd

if __name__ == '__main__':
	# initialize the node
	rospy.init_node('pos_converter', anonymous = True)
	# set a 10Hz freaquency for this node
	loop_rate = rospy.Rate(10)
	# add a subscriber to it to recieve the position information
	rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
	# add a subscriber to it to recieve the control parameters
	rospy.Subscriber('/turtle1/control_params', Turtlecontrol, control_params_callback)
	#create variable to records movements parameters
	vel_cmd = Twist()
	# create publisher to publish velocity commands
	cmd_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10) 
	# run this control loop regularly 
	while not rospy.is_shutdown(): 
		# set the linear and angular velocity command
		# velocity is determited by proportional controller 
		vel_cmd.linear.x = turtle_control_msg.kp*(turtle_control_msg.xd-pos_msg.x)	
		vel_cmd.angular.x = 0.0 
		# publish the command to the defined topic
		cmd_pub.publish(vel_cmd)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
	
	
