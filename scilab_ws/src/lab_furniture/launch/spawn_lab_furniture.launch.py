import os
import tempfile
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

# (nombre del modelo == nombre de carpeta en models/, x, y, z) -- posiciones aproximadas
FURNITURE = [
    ('mesa_fondo', -0.25,  0.66, 0.0),
    ('mesa_izq',   -0.64, -0.25, 0.0),
    ('mesa_dcha',   0.60,  0.36, 0.0),
    ('armario',     0.74, -0.54, 0.0),
    ('pedestal',    0.0,   0.0,  0.0),
]


def generate_launch_description():
    share_dir = get_package_share_directory('lab_furniture')
    nodes = []
    for model_name, x, y, z in FURNITURE:
        xacro_path = os.path.join(share_dir, 'models', model_name, 'model.sdf.xacro')
        sdf_xml = xacro.process_file(xacro_path).toxml()

        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.sdf', delete=False)
        tmp.write(sdf_xml)
        tmp.close()

        nodes.append(Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-file', tmp.name, '-name', model_name,
                       '-x', str(x), '-y', str(y), '-z', str(z)],
            output='screen'
        ))

    return LaunchDescription(nodes)
