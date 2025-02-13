# PX4 Formation Control with ROS

This repository contains a Python script for controlling a formation of multiple UAVs (Unmanned Aerial Vehicles) using the **PX4** autopilot system and **ROS** (Robot Operating System). The script allows a group of UAVs to follow a leader UAV in a predefined formation, where the leader's position is tracked, and the followers adjust their positions accordingly.

> **Disclaimer**: This script is intended for educational and research purposes. Make sure to use it responsibly and in a controlled environment.

## Features

- **Leader-Follower Formation**: The leader UAV's position is tracked, and the follower UAVs maintain a specified offset to the leader.
- **Mode Switching**: UAVs are switched to **OFFBOARD mode** for autonomous control, and are then armed to be ready for flight.
- **ROS Integration**: The script uses ROS topics, services, and messages to communicate with the UAVs, including pose updates and control commands.
- **Multiple UAVs Control**: Supports controlling multiple UAVs (in this example, two followers) and sending formation control commands.

## Requirements

- **ROS** (Robot Operating System), compatible with **ROS Noetic** (or other compatible versions)
- **PX4 autopilot** (configured to work with ROS and MAVROS)
- **MAVROS**: ROS package that allows communication between ROS and PX4
- Python 3.x with `rospy` and `geometry_msgs`

You will also need to have the following ROS nodes running:
- **MAVROS** node connected to PX4 for communication.

## How to Set Up

### 1. Install ROS and MAVROS

Follow the instructions in the [official ROS installation guide](http://wiki.ros.org/ROS/Installation) and [MAVROS installation guide](http://wiki.ros.org/mavros) to set up your environment.

### 2. Launch the PX4 Autopilot System

Make sure the PX4 system is running and connected to ROS. You can launch the PX4 autopilot and MAVROS in a compatible environment with the following command:

```bash
roslaunch mavros px4.launch
