import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    xacro_file = os.path.join(
        get_package_share_directory('motoman_sda10f_support'),
        'urdf',
        'sda10f.xacro'
    )
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'sda10f', '-topic', 'robot_description', '-x', '0.0', '-y', '0.10', '-z', '0.10', '-Y', '-1.5708'],
        output='screen'
    )

    load_jsb = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'joint_state_broadcaster'],
        output='screen'
    )
    load_torso = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'torso_controller'],
        output='screen'
    )
    load_left = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'left_arm_controller'],
        output='screen'
    )
    load_right = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active', 'right_arm_controller'],
        output='screen'
    )

    delayed_controllers = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[load_jsb, load_torso, load_left, load_right],
        )
    )

    return LaunchDescription([
        robot_state_publisher_node,
        spawn_robot,
        delayed_controllers,
    ])
