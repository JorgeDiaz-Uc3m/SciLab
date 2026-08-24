# SciLab — Desarrollo de entorno simulación de laboratorio autónomo robotizado

**Trabajo de Fin de Grado — Universidad Carlos III de Madrid (UC3M)**

- **Autor:** Jorge Díaz Escribano
- **Tutor:** Edwin Daniel Oña Simbaña — Departamento de Ingeniería de Sistemas y Automática, UC3M
- **Titulación:** Grado en Ingeniería en Tecnologías Industriales

## Descripción

Este repositorio contiene el código y los recursos desarrollados para el Trabajo de Fin de Grado consistente en la creación de un entorno de simulación en Gazebo (ROS2) de un laboratorio robótico autónomo, integrando un robot industrial de doble brazo Yaskawa Motoman SDA10F mediante `ros2_control`.

El proyecto abarca:
- La migración a ROS2 Jazzy de paquetes del stack ROS-Industrial (originalmente desarrollados para versiones anteriores de ROS).
- El modelado del entorno físico del laboratorio (mobiliario, pedestal del robot) mediante Xacro.
- La integración y depuración del robot SDA10F con `ros2_control` en Gazebo Harmonic.
## Autoría y atribución

### Trabajo propio
Son autoría de Jorge Díaz Escribano, desarrollados como parte de este TFG:

- **`scilab_ws/src/scilab_world`** — Mundo de Gazebo del laboratorio.
- **`scilab_ws/src/lab_furniture`** — Modelado del mobiliario del laboratorio (mesas, armario, pedestal).
- **`yaskawa_ws/src/sda10f_bringup`** — Lanzamiento, configuración de controladores y spawn del robot SDA10F.
- Modificaciones concretas dentro de `yaskawa_ws/src/motoman/motoman_sda10f_support`:
  - Corrección del bloque `ros2_control` en `sda10f_macro.xacro` (eliminación de la interfaz de comando en `torso_joint_b2`, joint mimic, incompatible con `gz_ros2_control`).
  - Ajuste de la lista de joints controlados en `sda10f_controllers.yaml`.
  - Ajuste de posición y orientación del spawn del robot en `spawn_sda10f.launch.py`.
  - Configuración de `GZ_SIM_RESOURCE_PATH` en `scilab_world/launch/lab_world.launch.py` para la carga automática de las mallas del robot.

### Código de terceros
El paquete **`yaskawa_ws/src/motoman`** corresponde al proyecto [ROS-Industrial](https://rosindustrial.org/) para el robot Yaskawa Motoman SDA10F, incluido en este repositorio como base de partida y adaptado a ROS2 Jazzy y Gazebo Harmonic. Conserva su documentación, licencia y changelog originales (`README.md`, `CONTRIBUTING.md`, `CHANGELOG.rst` dentro dentro de la propia carpeta). No es trabajo original de este TFG salvo por las modificaciones listadas arriba.

## Nota de transparencia sobre el uso de IA

Durante el desarrollo de este proyecto se ha utilizado asistencia de inteligencia artificial como herramienta de apoyo. La autoría intelectual, las decisiones de diseño y la responsabilidad sobre el contenido del TFG son del autor. El detalle completo del uso de IA en la elaboración de la memoria se encuentra en el Anexo correspondiente del documento entregable, conforme a la normativa de la UC3M.
