# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription

from launch_ros.actions import Node
from dataclasses import dataclass
from launch_pal.arg_utils import LaunchArgumentsBase


@dataclass(frozen=True)
class LaunchArguments(LaunchArgumentsBase):
    pass


def generate_launch_description():

    # Create the launch description
    ld = LaunchDescription()
    launch_arguments = LaunchArguments()

    launch_arguments.add_to_launch_description(ld)

    declare_actions(ld, launch_arguments)

    return ld


def declare_actions(launch_description: LaunchDescription, launch_args: LaunchArguments):

    # Original code - spawns robot with default extended arm pose:
    robot_entity = Node(package="gazebo_ros", executable="spawn_entity.py",
                        arguments=["-topic", "robot_description",
                                   "-entity", "tiago-pro",
                                   "-x", "0.0", "-y", "1.85", "-z", "0.03",
                                   "-Y", "-1.5708",  # Yaw in radians
                                   ],
                        output="screen")
    launch_description.add_action(robot_entity)

    # NOTE: Initial joint state approach using -J flag doesn't work with this version of Gazebo.
    # Alternative approaches to spawn in home pose:
    # 1. Use tuck_arm.py (current approach) - sends home motion after spawn
    # 2. Create Gazebo SDF file with initial poses
    # 3. Use a gazebo plugin to set initial states
    # The tuck_arm approach is the most reliable and is already configured.

    return
