import rospy
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from ackermann_msgs.msg import AckermannDrive
import numpy as np
from scipy.integrate import ode
from std_msgs.msg import Float32MultiArray
from utilities import euler_to_quaternion, quaternion_to_euler

class vehicleController():

    def __init__(self):
        # Publisher to publish the control input to the vehicle model
        self.controlPub = rospy.Publisher("/ackermann_cmd", AckermannDrive, queue_size = 1)

    def getModelState(self):
        # Get the current state of the vehicle
        # Input: None
        # Output: 
        #   ModelState, the state of the vehicle, contain the
        #   position, orientation, linear velocity, angular velocity
        #   of the vehicle
        rospy.wait_for_service('/gazebo/get_model_state')
        try:
            serviceResponse = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            modelState = serviceResponse(model_name='gem')
        except rospy.ServiceException as exc:
            rospy.loginfo("Service did not process request: "+str(exc))
        return modelState

    def execute(self, currentPose, referencePose):
        # Compute the control input to the vehicle according to the 
        # current and reference pose of the vehicle
        # Input:
        #   currentPose: ModelState, the current state of the vehicle
        #   referencePose: list, the reference state of the vehicle, 
        #       the element in the list are [ref_x, ref_y, ref_theta, ref_v]
        # Output: None

        # TODO: Implement this function


        #Pack computed velocity and steering angle into Ackermann command
        newAckermannCmd = AckermannDrive()

        # Publish the computed control input to vehicle model
        self.controlPub.publish(newAckermannCmd)
