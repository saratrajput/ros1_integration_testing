cmake_minimum_required(VERSION 3.0.2)
project(ros1_integration_testing)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  cv_bridge
)

catkin_package()

if(CATKIN_ENABLE_TESTING)
  find_package(rostest REQUIRED)
  add_rostest(test/test_image_processing.test)
endif()
