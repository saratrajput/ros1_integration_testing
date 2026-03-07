#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class ResultMonitor:
    def __init__(self):
        rospy.init_node('result_monitor', anonymous=False)

        self.bridge = CvBridge()

        # Subscriber
        self.sub = rospy.Subscriber('/processed/edges', Image, self.result_callback, queue_size=10)

        self.msg_count = 0
        self.total_edge_pixels = 0

        rospy.loginfo("Result monitor initialized")

    def result_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Count edge pixels (non-zero pixels)
            edge_pixels = np.count_nonzero(cv_image)
            self.total_edge_pixels += edge_pixels
            self.msg_count += 1

            avg_edge_pixels = self.total_edge_pixels / self.msg_count

            if self.msg_count % 20 == 0:
                rospy.loginfo(f"Received {self.msg_count} processed images. "
                            f"Current edge pixels: {edge_pixels}, "
                            f"Average: {avg_edge_pixels:.1f}")

        except CvBridgeError as e:
            rospy.logerr(f"CV Bridge Error: {e}")
        except Exception as e:
            rospy.logerr(f"Monitor error: {e}")

if __name__ == '__main__':
    try:
        node = ResultMonitor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
