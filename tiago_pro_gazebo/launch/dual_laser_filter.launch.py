import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    # Get the package share directory for relocatability
    pkg_dir = get_package_share_directory('tiago_pro_gazebo')
    script_path = os.path.join(pkg_dir, '..', '..', 'lib', 'tiago_pro_gazebo', 'diy_laser_filter.py')

    # Process 1: Front Scanner Filter (Default parameters)
    front_filter = ExecuteProcess(
        cmd=['python3', script_path],
        name='diy_laser_filter_front',
        output='screen'
    )

    # Process 2: Rear Scanner Filter (Remapped parameters)
    rear_filter = ExecuteProcess(
        cmd=[
            'python3', script_path,
            '--ros-args',
            '-r', '__node:=diy_laser_filter_rear',
            '-r', '/scan_front_raw:=/scan_rear_raw',
            '-r', '/scan_front_filtered:=/scan_rear_filtered'
        ],
        name='diy_laser_filter_rear',
        output='screen'
    )

    return LaunchDescription([
        front_filter,
        rear_filter
    ])
