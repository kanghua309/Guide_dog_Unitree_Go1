#!/usr/bin/env python
import rospy
import math
import numpy as np
from  geometry_msgs.msg import Twist
from unitree_legged_msgs.msg import HighCmd
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from std_msgs.msg import Bool 
import codecs

bridge = CvBridge()
speed_y = 0.75
speed_z = 0.6

rospy.init_node('ada_follow_red_ball_demo')
rate = rospy.Rate(50)
pub = rospy.Publisher('/high_cmd', HighCmd, queue_size=10)
high_cmd = HighCmd()
high_cmd.head = codecs.decode('feef', 'hex_codec')
high_cmd.levelFlag = 0xee
high_cmd.mode = 1
high_cmd.gaitType = 1


boolpublisher = rospy.Publisher('/idle_mode_checker', Bool, queue_size=10)
checker=Bool()


lower_red = np.array([170, 200, 50], dtype=np.uint8)
upper_red = np.array([180, 255, 255], dtype=np.uint8)


# gets an image of the camera_face of Ada
# Node subscribes /camera_face/image_raw topic, msg type is Image
def image_acquisition():
    rospy.Subscriber('/camera_face/image_raw', Image, callback)
    rospy.spin()

# TODO
def callback(image_data):
    #acquiring images
    raw_img=bridge.imgmsg_to_cv2(image_data, "bgr8")
    height, width, channels = raw_img.shape

    crop_blurred_img = cv2.blur(raw_img, (5, 5))
    mask_img=floor_filter(crop_blurred_img)

    # blurs image for better circle detection
    blurred_mask_img = cv2.GaussianBlur(mask_img, (5,5), 1.5)

    # get binarized image
    binary_img = binarize_mask(blurred_mask_img)

    #CCL Connected Component Labeling on the binarized image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
    no_ball = False
    try:
        largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) +1
    except ValueError:
        rospy.loginfo("No red ball detected")
        if no_ball == False:
            high_cmd.euler[1] = 0.0
            high_cmd.euler[2] = 0.0
            pub.publish(high_cmd)
            no_ball = True
        last_positions = []
        checker.data=False
        boolpublisher.publish(checker)
    else:
        largest_component_pixel_count = stats[largest_component_label, cv2.CC_STAT_AREA]
        floor_coverage = float(100.0*largest_component_pixel_count/(height*width))
        if floor_coverage > 0.01:
            center_z = centroids[largest_component_label,0]
            center_y = centroids[largest_component_label,1]            

            cv2.arrowedLine(raw_img, (width/2,height/2), (int(center_z), int(center_y)), color=(0, 255, 0), thickness=3, line_type=8, shift=0, tipLength=0.1) # red arrow from the middle of the screen to the detected red ball
            
            change_pitch_yaw(int(center_z), int(center_y), int(width/2), int(height/2))

            #Publishen des Booleans fuer Idle Mode, wenn Ball zu sehen ist
            checker.data=True
            boolpublisher.publish(checker)
    finally:
        cv2.imshow("Detected Circle", raw_img)
        cv2.waitKey(3)

def change_pitch_yaw(ball_z,ball_y,middle_z, middle_y):
    dist_y = ball_y - middle_y
    dist_z = middle_z - ball_z# x -> z

    factor_y = float(dist_y) / float(middle_y)
    factor_z = float(dist_z) / float(middle_z)
    rospy.loginfo("factor_y: " + str(factor_y))
    rospy.loginfo("factor_z: " + str(factor_z))
    high_cmd.euler[1] = speed_y * factor_y
    high_cmd.euler[2] = speed_z * factor_z
    rospy.loginfo("Twist Angular Y: " + str(high_cmd.euler[1]))
    rospy.loginfo("Twist Angular Z: " + str(high_cmd.euler[2]))

    pub.publish(high_cmd) # wieder hinzufuegen
    rate.sleep()

# binarizes a mask
def binarize_mask(mask):
    binary_img = mask.copy()
    binary_img[binary_img > 0] = 255
    return binary_img

def floor_filter(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # converts image in hsv-color space
    # preparing the mask to overlay
    return  cv2.inRange(hsv, lower_red, upper_red)

if __name__ == '__main__':
    image_acquisition()