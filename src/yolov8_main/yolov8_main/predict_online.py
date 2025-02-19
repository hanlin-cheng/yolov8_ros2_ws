import time

import cv2
import numpy as np
from PIL import Image as PILImage

from yolo import YOLO

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from yolov8_msg.msg import DetectionResult
from yolov8_msg.msg import ObjectDetection


class Yolov8Node(Node):
    def __init__(self):
        super().__init__('yolov8_node')

        self.declare_parameter('image_topic0', 'sensors/camera/raw0')

        image_topic = self.get_parameter('image_topic0').get_parameter_value().string_value
        print("'image_topic0' rename to: " + image_topic)

        # Subscriber for raw and processed images
        self.raw_image_subscriber = self.create_subscription(
            Image,
            image_topic,
            self.raw_image_callback,
            10)

        self.bounding_box_publisher = self.create_publisher(DetectionResult, '/detection/objects', 10)

        self.bridge = CvBridge()

        self.yolo = YOLO()

        self.get_logger().info(f"Waiting for camera image...")

    def raw_image_callback(self, msg):
        try:
            catch_time = msg.header.stamp.nanosec
            t1 = time.time()
            # Convert ROS image to OpenCV format
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            if frame is None:
                self.get_logger().info("未能正确读取摄像头（视频），请注意是否正确安装摄像头。")
                return

            fps = 0.0

            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = PILImage.fromarray(np.uint8(frame))
            # 进行检测
            detection_result = self.yolo.detect_image(frame)
            detection_result.image_timestamp = int(catch_time)
            detection_result.camera_id = int(0)
            self.bounding_box_publisher.publish(detection_result)
            fps = (fps + (1. / (time.time() - t1))) / 2

            for i, object_detection in enumerate(detection_result.objects):
                self.get_logger().info(f"Object {i + 1}:")
                self.get_logger().info(f"  Label: {object_detection.label}")
                self.get_logger().info(f"  Confidence: {object_detection.confidence}")
                self.get_logger().info(f"  Coordinates: Left: {object_detection.left}, Top: {object_detection.top}, Right: {object_detection.right}, Bottom: {object_detection.bottom}")
            self.get_logger().info(f"FPS = {fps:.2f}")

        except Exception as e:
            print(f"Error converting image: {str(e)}")

def main():
    rclpy.init()
    node = Yolov8Node()

    rclpy.spin(node)

    # Shutdown
    node.destroy_node()
    rclpy.shutdown()