FROM ros:noetic-ros-base

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-noetic-rospy \
    ros-noetic-sensor-msgs \
    ros-noetic-cv-bridge \
    ros-noetic-rostest \
    ros-noetic-rosunit \
    python3-numpy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /catkin_ws