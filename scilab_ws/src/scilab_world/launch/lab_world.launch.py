import os
from os import environ, pathsep
from launch.actions import AppendEnvironmentVariable
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def get_model_paths(packages_names):
    model_paths = ''
    for package_name in packages_names:
        if model_paths != '':
            model_paths += pathsep
        package_path = get_package_prefix(package_name)
        model_paths += os.path.join(package_path, 'share')

    if 'GZ_SIM_RESOURCE_PATH' in environ:
        model_paths += pathsep + environ['GZ_SIM_RESOURCE_PATH']

    return model_paths


def generate_launch_description():

    pkg_path = get_package_share_directory('scilab_world')

    declare_world_name = DeclareLaunchArgument(
        'world_name',
        default_value='mi_laboratorio',
        description='Nombre del fichero .world (sin extension) dentro de scilab_world/worlds'
    )

    world_name = LaunchConfiguration('world_name')

    # Modelos de los robots que luego querramos spawnear bajo demanda,
    # para que Gazebo pueda resolver sus mallas (meshes) aunque aun no
    # esten spawneados en el momento de abrir el mundo.
    robot_description_packages = [
        'tiago_description', 'pmb2_description',
        'pal_hey5_description', 'pal_gripper_description',
        'pal_robotiq_description', 'omni_base_description',
    ]
    model_path = get_model_paths(robot_description_packages)

    set_model_path = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', model_path)

    world_file = [pkg_path, '/worlds/', world_name, '.world']

    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r -s ', *world_file]}.items()
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': [' -g ']}.items()
    )

    ld = LaunchDescription()
    ld.add_action(declare_world_name)
    ld.add_action(set_model_path)

    set_motoman_sda10f_path = AppendEnvironmentVariable(
         name='GZ_SIM_RESOURCE_PATH',
         value=os.path.dirname(get_package_share_directory('motoman_sda10f_support'))
    )
    set_motoman_resources_path = AppendEnvironmentVariable(
         name='GZ_SIM_RESOURCE_PATH',
         value=os.path.dirname(get_package_share_directory('motoman_resources'))
    )

    ld.add_action(set_motoman_sda10f_path)
    ld.add_action(set_motoman_resources_path)

    ld.add_action(start_gazebo_server)
    ld.add_action(start_gazebo_client)

    return ld
