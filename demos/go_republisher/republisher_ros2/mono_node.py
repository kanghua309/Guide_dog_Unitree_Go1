#!/usr/bin/env python3

import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge

class CameraRepublisherNode(Node):
    def __init__(self):
        super().__init__('camera_republisher')
        self.get_logger().info('camera_republisher node started')

        #https://roboticsbackend.com/rclpy-params-tutorial-get-set-ros2-params-with-python/
        device_id = self.get_parameter('device_id').get_parameter_value().integer_value
        camera_name = self.get_parameter('camera_name').get_parameter_value().string_value
        calibration_left = self.get_parameter('calibration_left').get_parameter_value().string_value


        self.left_ci = CameraInfo()

        if calibration_left:
            self.left_ci.load_from_file(calibration_left)

        self.vid = cv2.VideoCapture(device_id)

        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1856)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

        self.pub_left = self.create_publisher(Image, f'{camera_name}/image_raw', 1)
        self.pub_left_ci = self.create_publisher(CameraInfo, f'{camera_name}/camera_info', 1)

        self.bridge = CvBridge()
        self.timer = self.create_timer(0.04, self.publish_image)  # 25 Hz (1/25 = 0.04)

    def publish_image(self):
        ret, frame = self.vid.read()
        if not ret:
            return

        frame_left = frame[0:800, 928:1856]
        img_left = self.bridge.cv2_to_imgmsg(frame_left, "bgr8")

        now = self.get_clock().now().to_msg()

        img_left.header.stamp = now
        img_left.header.frame_id = self.get_parameter('camera_name').get_parameter_value().string_value
        self.pub_left.publish(img_left)

        l_ci = self.left_ci
        l_ci.header = img_left.header
        self.pub_left_ci.publish(l_ci)

def main(args=None):
    print(args)
    rclpy.init(args=args)
    try:
        camera_republisher_node = CameraRepublisherNode()
        rclpy.spin(camera_republisher_node)
    except Exception as e:
        print('Error: ', e)
    finally:
        camera_republisher_node.vid.release()
        cv2.destroyAllWindows()
        camera_republisher_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
