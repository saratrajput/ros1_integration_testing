#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class ImageProcessor:
    def __init__(self):
        rospy.init_node('image_processor', anonymous=False)

        self.bridge = CvBridge()

        # Subscriber and Publisher
        self.sub = rospy.Subscriber('/camera/image_raw', Image, self.image_callback, queue_size=10)
        self.pub = rospy.Publisher('/processed/edges', Image, queue_size=10)

        # Parameters for edge detection
        self.threshold1 = rospy.get_param('~canny_threshold1', 50)
        self.threshold2 = rospy.get_param('~canny_threshold2', 150)

        self.msg_count = 0

        rospy.loginfo("Image processor initialized")

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Apply Canny edge detection
            edges = cv2.Canny(gray, self.threshold1, self.threshold2)

            # Convert back to 3-channel for consistency
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            # Convert back to ROS Image message
            output_msg = self.bridge.cv2_to_imgmsg(edges_bgr, encoding="bgr8")
            output_msg.header = msg.header  # Preserve timestamp and frame_id

            # Publish processed image
            self.pub.publish(output_msg)

            self.msg_count += 1
            if self.msg_count % 50 == 0:
                rospy.loginfo(f"Processed {self.msg_count} images")

        except CvBridgeError as e:
            rospy.logerr(f"CV Bridge Error: {e}")
        except Exception as e:
            rospy.logerr(f"Processing error: {e}")

if __name__ == '__main__':
    try:
        node = ImageProcessor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
