from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer, LoadComposableNodes
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    namespace_1 = "drone"
    container = ComposableNodeContainer(
        name="drone_uoa", 
        package="rclcpp_components",
        executable="component_container_mt",#マルチスレッドの場合component_container_mt,シングルはcomponent_container
        namespace="DRONE_P2",
        composable_node_descriptions=[
            
            ComposableNode(
                package="drone_operation",
                plugin="component_operator_gui::DroneGUI",
                name="drone_gui",
                namespace=namespace_1,
                extra_arguments=[{"use_intra_process_comms": True}],
                parameters=[{"mode": "P2"},
                            {"check_duration_sec": 1.0},
                            {"timer_interval_ms": 200},
                            {"top_left_x": 100},
                            {"top_right_y": 100},
                            {"rect_width": 300},
                            {"rect_height": 300}],
                # remappings=[("raw_image" , "/arm_camera/realsense2_camera_node/color/image_raw")]
                # remappings=[("raw_image" , "/camera/camera/color/image_raw")]#テスト用
                remappings=[("raw_image" , "image_raw")]
            ),
            ComposableNode( # ここにmisora2_dt_clientを入力
                package="misora2_dt_client",
                plugin="dt_client_component::DTClient",
                name="confirmation_screen",
                namespace=namespace_1,
                extra_arguments=[{"use_intra_process_comms": True}],
                parameters=[{"mode": "P2"}]
            ),
            ComposableNode(
                package="misora2_qr",
                plugin="component_qr::DetectQR",
                name="qr",
                namespace=namespace_1,
                extra_arguments=[{"use_intra_process_comms": True}],
            ),
            ComposableNode(
                package="misora2_pressure",
                plugin="component_pressure::PressureMeasurement",
                name="pressure",
                namespace=namespace_1,
                extra_arguments=[{"use_intra_process_comms": True}],
            )
        ],
        output="screen",
    )
  
    
    python_node = Node(
        package='misora2_dt_client',
        executable='client_node.py',
        name='client',
        namespace=namespace_1,
        parameters=[{"host": ""},{"robot_id": ""},{"mission": "P2"}],
        output='screen',
    )
    
    return LaunchDescription([
        container, 
        python_node,
        # load_composable_nodes
    ])
