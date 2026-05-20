#!/usr/bin/env python3
# Copyright (c) 2024 PAL Robotics S.L. All rights reserved.
#
# Simple launch file to spawn TIAGo Pro in Gazebo without navigation/moveit

import os
from os import environ, pathsep
from ament_index_python.packages import get_package_prefix, get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    SetEnvironmentVariable,
    SetLaunchConfiguration,
    IncludeLaunchDescription,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def get_model_paths(packages_names):
    model_paths = ''
    for package_name in packages_names:
        if model_paths != '':
            model_paths += pathsep

        package_path = get_package_prefix(package_name)
        model_path = os.path.join(package_path, 'share')
        model_paths += model_path

    if 'GAZEBO_MODEL_PATH' in environ:
        model_paths += pathsep + environ['GAZEBO_MODEL_PATH']

    return model_paths


def generate_launch_description():
    # Package directories
    gazebo_ros_pkg = get_package_share_directory('gazebo_ros')
    tiago_pro_description_pkg = get_package_share_directory('tiago_pro_description')
    pal_gazebo_worlds_pkg = get_package_share_directory('pal_gazebo_worlds')
    
    # Gazebo model paths
    packages = ['tiago_pro_description', 'pal_sea_arm_description',
                'omni_base_description', 'pal_pro_gripper_description',
                'tiago_pro_head_description', 'pal_urdf_utils']
    
    model_path = get_model_paths(packages)
    
    # Declare arguments
    world_name_arg = DeclareLaunchArgument(
        'world_name',
        default_value='pal_office',
        description='Gazebo world name'
    )
    
    gzclient_arg = DeclareLaunchArgument(
        'gzclient',
        default_value='True',
        description='Start Gazebo client (GUI)'
    )
    
    camera_model_arg = DeclareLaunchArgument(
        'camera_model',
        default_value='realsense-d435',
        description='Head camera model'
    )
    
    # Set use_sim_time
    set_sim_time = SetLaunchConfiguration('use_sim_time', 'True')
    
    # Set Gazebo model path
    gazebo_model_path_env = SetEnvironmentVariable(
        'GAZEBO_MODEL_PATH', model_path
    )
    
    # World file path
    world_file = os.path.join(pal_gazebo_worlds_pkg, 'worlds', 'pal_office.world')
    
    # Gazebo server
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_pkg, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={
            'world': world_file,
            'verbose': 'true',
        }.items()
    )
    
    # Gazebo client
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_pkg, 'launch', 'gzclient.launch.py')
        ),
        condition=IfCondition(LaunchConfiguration('gzclient'))
    )
    
    # Robot state publisher
    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tiago_pro_description_pkg, 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'True',
            'is_public_sim': 'True',
            'camera_model': LaunchConfiguration('camera_model'),
        }.items()
    )
    
    # Spawn robot
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'tiago_pro',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0',
        ],
        output='screen'
    )
    
    # Joint state broadcaster (with correct configuration)
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager', '/controller_manager',
            '--controller-manager-timeout', '120'
        ],
        output='screen'
    )
    
    return LaunchDescription([
        world_name_arg,
        gzclient_arg,
        camera_model_arg,
        set_sim_time,
        gazebo_model_path_env,
        gzserver,
        gzclient,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
    ])
