# yolov8_ros2_ws

本仓库基于[yolov8代码仓库](https://github.com/bubbliiiing/yolov8-pytorch)封装了一层ros2的接口，用于实时接收相机数据检测目标，也支持离线demo和训练

## 测试环境

ubuntu 20.04

ros2 humble

torch==1.2.0

yolo相关安装和训练配置可以参考[yolov8代码仓库](https://github.com/bubbliiiing/yolov8-pytorch)

## 说明

根据自己的测试环境修改订阅话题和输出话题

```python
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
```

## 运行

```
colcon build
./run_yolo.sh
```

