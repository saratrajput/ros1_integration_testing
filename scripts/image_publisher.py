#!/usr/bin/env python3

import os

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImagePublisher:
    def __init__(self):
        rospy.init_node('image_publisher', anonymous=False)

        self.bridge = CvBridge()
        self.pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

        self.rate = rospy.get_param('~publish_rate', 10.0)

        # Load the dog image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'dog.jpeg')
        self.image = cv2.imread(image_path)
        if self.image is None:
            rospy.logfatal(f"Failed to load image: {image_path}")
            raise RuntimeError(f"Failed to load image: {image_path}")

        rospy.loginfo(f"Image publisher initialized with {image_path} @ {self.rate}Hz")

    def run(self):
        rate = rospy.Rate(self.rate)

        while not rospy.is_shutdown():
            msg = self.bridge.cv2_to_imgmsg(self.image, encoding="bgr8")
            msg.header.stamp = rospy.Time.now()
            msg.header.frame_id = "camera_frame"

            self.pub.publish(msg)
            rate.sleep()

if __name__ == '__main__':
    try:
        node = ImagePublisher()
        node.run()
    except rospy.ROSInterruptException:
        pass
