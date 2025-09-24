from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer, LoadComposableNodes
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    namespace_1 = "drone"
    container = ComposableNodeContainer(
        name="drone_uoa", 
        package="rclcpp_components",
        executable="component_container_mt",#マルチスレッドの場合component_container_mt,シングルはcomponent_container
        namespace="DRONE_P6",
        composable_node_descriptions=[
            ComposableNode(
                package="drone_operation",
                plugin="component_operator_gui::DroneGUI",
                name="drone_gui",
                namespace=namespace_1,
                extra_arguments=[{"use_intra_process_comms": True}],
                parameters=[{"mode": "P6"},
                            {"top_left_x": 128},
                            {"top_left_y": 55},
                            {"rect_width": 1000},
                            {"rect_height": 564}],
            ),
            ComposableNode(
                package="misora2_distribute_image",
                plugin="component_distribute_image::DistributeImage",
                name="distribute_image",
                namespace=namespace_1,
                extra_arguments=[{"use_intra_process_comms": True}],
                parameters=[{"mode": "P6"}, 
                            {"check_duration_sec": 1.0}, 
                            {"timer_interval_ms": 100}], #画像を何millisec間隔で流すか、また何s間流すか
                remappings=[("raw_image" , "drone_image_cropped")],
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
        executable='client_node_value.py',
        name='client',
        namespace=namespace_1,
        parameters=[{"host": "stg.rms-cloud.jp"},{"robot_id": "61"},{"mission": "P6"},{"mac_id": "5beff8bdeb4f"}],
        output='screen',
    )
    
    return LaunchDescription([
        container, 
        python_node,
        # load_composable_nodes
    ])
