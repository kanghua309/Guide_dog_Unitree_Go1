from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare



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
                        default_value='0',
                        choices=['0','1'],
                        description='Camera Device Id For Go1'
                    ),

        DeclareLaunchArgument(
                        name='hz',
                        default_value='0.5',
                        description='Hz For CreateTimer'
                    ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('unitree_legged_real'),
                    'launch',
                    'high.launch.py'
                ])
            ),
            launch_arguments=[
                ('use_rviz', 'false'),
            ],
        ),

        Node(
            package='republisher_ros2',
            executable='mono_node',
            output='screen',
            parameters=[{
                'camera_name': LaunchConfiguration("camera_name"),
                'device_id': LaunchConfiguration("device_id"),
                'hz': LaunchConfiguration("hz")
            }],
            condition=IfCondition(LaunchConfiguration('use_go1_repbulisher_msg')),
        ),

        Node(
            package='ball_track_ros2',
            executable='track_node',
            output='screen',
              parameters=[{
                'camera_name': LaunchConfiguration("camera_name"),
            }],
        ),
    ])