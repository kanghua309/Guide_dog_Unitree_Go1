import codecs
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from ros2_unitree_legged_msgs.msg import HighCmd
from cv_bridge import CvBridge
import cv2
import numpy as np

class AdaFollowRedBallDemo(Node):
    def __init__(self):
        super().__init__('ada_follow_red_ball_demo')

        self.declare_parameter('camera_name', rclpy.Parameter.Type.STRING)
        camera_name = self.get_parameter('camera_name')
        self.subscription = self.create_subscription(Image, f'{camera_name.value}/image_raw', self.image_callback, 10)
        self.publisher = self.create_publisher(HighCmd, '/high_cmd', 10)
        self.bool_publisher = self.create_publisher(Bool, '/idle_mode_checker', 10)

        self.bridge = CvBridge()
        self.speed_y = 0.75
        self.speed_z = 0.6
        self.last_positions = []
        self.no_ball = False

        self.lower_red = np.array([170, 200, 50], dtype=np.uint8)
        self.upper_red = np.array([180, 255, 255], dtype=np.uint8)

    def image_callback(self, msg):
        print("get image raw msg！")
        raw_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        height, width, channels = raw_img.shape
        crop_blurred_img = cv2.blur(raw_img, (5, 5))
        mask_img = self.floor_filter(crop_blurred_img)
        blurred_mask_img = cv2.GaussianBlur(mask_img, (5, 5), 1.5)
        binary_img = self.binarize_mask(blurred_mask_img)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
        #print("4:",num_labels,labels,stats,centroids)
        try:
            largest_component_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
        except ValueError:
            self.get_logger().info('No red ball detected')
            if not self.no_ball:
                self.stop_tracking()
                self.no_ball = True
            self.publish_idle_mode(False)
        else:
            print("Ball be detected!")
            largest_component_pixel_count = stats[largest_component_label, cv2.CC_STAT_AREA]
            floor_coverage = float(100.0 * largest_component_pixel_count / (height * width))
            if floor_coverage > 0.01:
                center_z = centroids[largest_component_label, 0]
                center_y = centroids[largest_component_label, 1]

                cv2.arrowedLine(raw_img, (width//2, height//2), (int(center_z), int(center_y)), color=(0, 255, 0),
                                thickness=3, line_type=8, shift=0, tipLength=0.1)
                print("Control Dog Head ------------------>")
                self.change_pitch_yaw(int(center_z), int(center_y), int(width//2), int(height//2))
                self.publish_idle_mode(True)
        cv2.imshow("Detected Circle", raw_img)
        cv2.waitKey(3)

    def change_pitch_yaw(self, ball_z, ball_y, middle_z, middle_y):
        dist_y = ball_y - middle_y
        dist_z = middle_z - ball_z

        factor_y = float(dist_y) / float(middle_y)
        factor_z = float(dist_z) / float(middle_z)

        euler_cmd = HighCmd()
        euler_cmd.head = np.frombuffer(bytes.fromhex('feef'),dtype=np.uint8)
        #euler_cmd.head = codecs.decode('feef', 'hex_codec')
        euler_cmd.level_flag = 0xee
        euler_cmd.mode = 1
        euler_cmd.gait_type = 1
        euler_cmd.euler[1] = self.speed_y * factor_y
        euler_cmd.euler[2] = self.speed_z * factor_z
        print("Pub Euler Cmd：",euler_cmd)
        self.publisher.publish(euler_cmd)

    def publish_idle_mode(self, status):
        msg = Bool()
        msg.data = status
        self.bool_publisher.publish(msg)

    def stop_tracking(self):
        print("stop track")
        euler_cmd = HighCmd()
        euler_cmd.head = np.frombuffer(bytes.fromhex('feef'),dtype=np.uint8)
        euler_cmd.level_flag = 0xee
        euler_cmd.mode = 1
        euler_cmd.gait_type = 1
        euler_cmd.euler[1] = 0.0
        euler_cmd.euler[2] = 0.0
        self.publisher.publish(euler_cmd)

    def floor_filter(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, self.lower_red, self.upper_red)

    def binarize_mask(self, mask):
        binary_img = mask.copy()
        binary_img[binary_img > 0] = 255
        return binary_img

def main(args=None):
    rclpy.init(args=args)
    try:
        ada_follow_red_ball_demo = AdaFollowRedBallDemo()
        rclpy.spin(ada_follow_red_ball_demo)
    except Exception as e:
        print('Error: ', e)
    finally:
        ada_follow_red_ball_demo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
