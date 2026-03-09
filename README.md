# ROS1 Integration Testing

Example code for writing integration tests in ROS1. For the full walkthrough and details, check out the blog post at https://www.pattarsuraj.com/blog/a-week-at-ari.

## Getting Started

Build the Docker image from the repository root:

```bash
cd docker
docker build -t ros1_integration_testing -f Dockerfile .
```

For the very first build inside the container, run:

```bash
catkin_make
```

For subsequent runs, simply source the workspace:

```bash
source devel/setup.sh
```

## Running Tests

Run the integration test with:

```bash
catkin_make run_tests
```

Or run it directly with `rostest`:

```bash
rostest ros1_integration_testing test_image_processing.test
```
