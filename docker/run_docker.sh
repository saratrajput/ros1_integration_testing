#!/usr/bin/env bash
# set -euo pipefail

# SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# IMAGE="ros:noetic"

# RUN_TESTS=false
# if [[ "${1:-}" == "--test" ]]; then
#     RUN_TESTS=true
# fi

# docker run --rm -it \
#     -v "$PROJECT_DIR":/catkin_ws/src/ros1_integration_testing:ro \
#     "$IMAGE" \
#     bash -c "
#         set -e
#         apt-get update -qq
#         apt-get install -y -qq python3-pip > /dev/null
#         source /opt/ros/noetic/setup.bash
#         cd /catkin_ws
#         rosdep update --rosdistro=noetic
#         rosdep install --from-paths src --ignore-src -r -y
#         catkin_make
#         if [ '$RUN_TESTS' = true ]; then
#             catkin_make run_tests
#             catkin_test_results
#         fi
#     "

docker run --rm -it \
    -v ../../../build:/catkin_ws/build \
    -v ../../../devel:/catkin_ws/devel \
    -v ../../../src:/catkin_ws/src \
    --name ros1_integration_testing \
    ros1_integration_testing:latest