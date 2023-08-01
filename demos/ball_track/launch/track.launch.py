from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    return LaunchDescription([

        DeclareLaunchArgument(
            name='use_go1_repbulisher_msg',
            default_value='true',
            choices=['true','false'],
            description='Run Go1 Republisher Ros2 First'
        ),


        DeclareLaunchArgument(
                        name='camera_name',
                        default_value='camera_face',
                        description='Camera Name For Go1'
                     ),


        DeclareLaunchArgument(
                        name='device_id',
                        default_value=0,
                        choices=[0,1],
                        description='Camera Device Id For Go1'
                    ),

       
        Node(
            package='republisher_ros2',
            executable='mono_node',
            output='screen',
            parameters=[{
                'camera_name': LaunchConfiguration("camera_name"),
                'device_id': LaunchConfiguration("device_id")
            }],
            condition=IfCondition(LaunchConfiguration('use_go1_repbulisher_msg')),
        ),

        Node(
            package='ball_track_ros2',
            executable='track_node',
            output='screen',
        ),
    ])