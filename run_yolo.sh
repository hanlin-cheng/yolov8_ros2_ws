#!/bin/bash

# 激活conda环境
source install/setup.bash

# 设置ROS 2的Python环境为conda环境中的Python
export PYTHONPATH=/home/slamtec/anaconda3/envs/py310/lib/python3.10/site-packages:$PYTHONPATH

export PYTHONPATH=/home/slamtec/work/detection_ws/src/yolov8_main/yolov8_main:$PYTHONPATH



# 运行ROS 2节点
ros2 run yolov8_main yolov8_node --ros-args -p image_topic0:='/sensors/camera/raw0'

