#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class ImagePublisher:
    def __init__(self):
        rospy.init_node('image_publisher', anonymous=False)

        self.bridge = CvBridge()
        self.pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

        # Get parameters
        self.rate = rospy.get_param('~publish_rate', 10.0)
        self.width = rospy.get_param('~image_width', 640)
        self.height = rospy.get_param('~image_height', 480)

        rospy.loginfo(f"Image publisher initialized: {self.width}x{self.height} @ {self.rate}Hz")

    def create_dummy_image(self):
        """Create a simple dummy image with a moving pattern"""
        t = rospy.Time.now().to_sec()

        # Create a gradient pattern that changes over time
        x = np.linspace(0, 2*np.pi, self.width)
        y = np.linspace(0, 2*np.pi, self.height)
        X, Y = np.meshgrid(x, y)

        # Moving wave pattern
        pattern = np.sin(X + t) * np.cos(Y + t)
        image = ((pattern + 1) * 127.5).astype(np.uint8)

        # Convert to 3-channel BGR image
        image_bgr = np.stack([image, image, image], axis=2)

        return image_bgr

    def run(self):
        rate = rospy.Rate(self.rate)

        while not rospy.is_shutdown():
            # Create and publish dummy image
            image = self.create_dummy_image()
            msg = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")
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
