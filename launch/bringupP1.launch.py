from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer, LoadComposableNodes
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    container = ComposableNodeContainer(
        name="drone_uoa", 
        package="rclcpp_components",
        executable="component_container_mt",#マルチスレッドの場合component_container_mt,シングルはcomponent_container
        namespace="P1",
        composable_node_descriptions=[
            ComposableNode(
                package="drone_operation",
                plugin="component_operator_gui::DroneGUI",
                name="drone_gui",
                extra_arguments=[{"use_intra_process_comms": True}],
                parameters=[{"mode": "P1"},
                            {"check_duration_sec": 1.0},
                            {"timer_interval_ms": 200}],
                # remappings=[("raw_image" , "/arm_camera/realsense2_camera_node/color/image_raw")]
                remappings=[("raw_image" , "/camera/camera/color/image_raw")]#テスト用
            ),
            ComposableNode( # ここにmisora2_dt_clientを入力
                package="misora2_dt_client",
                plugin="dt_client_component::DTClient",
                name="dt_client",
                extra_arguments=[{"use_intra_process_comms": True}],
                parameters=[{"mode": "P1"}]
            ),
            ComposableNode(
                package="misora2_qr",
                plugin="component_qr::DetectQR",
                name="qr",
                extra_arguments=[{"use_intra_process_comms": True}],
            ),
            ComposableNode(
                package="misora2_pressure",
                plugin="component_pressure::PressureMeasurement",
                name="pressure",
                extra_arguments=[{"use_intra_process_comms": True}],
            )
        ],
        output="screen",
    )
  
    
    # load_composable_nodes = LoadComposableNodes(
    #     target_container="my_container",
    #     composable_node_descriptions=[
    #         ComposableNode(
    #             package="listener",
    #             plugin="Listener",
    #             name="listener",
    #             extra_arguments=[{"use_intra_process_comms": True}],
    #         ),
    #     ],
    # )
    
    return LaunchDescription([
        container, 
        # load_composable_nodes
    ])
