import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_riel = 3.0
altura_techo = 2.8
num_focos = 4

# Dimensiones Riel
ancho_riel = 0.03
alto_riel = 0.03

# Dimensiones Foco
radio_foco = 0.05
largo_foco = 0.1

# Crear riel
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_techo - alto_riel / 2),
    scale=(largo_riel, ancho_riel, alto_riel)
)
riel = bpy.context.active_object
riel.name = "RielIluminacion"

# Crear focos
espaciado = largo_riel / num_focos

for i in range(num_focos):
    x_pos = -largo_riel / 2 + espaciado * (i + 0.5)
    z_pos_conector = altura_techo - alto_riel - 0.025 # Pequeño conector

    # Conector
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.015, 
        depth=0.05, 
        location=(x_pos, 0, z_pos_conector)
    )
    bpy.context.object.name = f"ConectorFoco_{i+1}"

    # Cuerpo del foco
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio_foco,
        depth=largo_foco,
        location=(x_pos, 0, z_pos_conector - 0.025 - largo_foco/2)
    )
    foco = bpy.context.active_object
    foco.name = f"CuerpoFoco_{i+1}"
    # Rotar focos para dar apariencia orientable
    foco.rotation_euler[0] = math.radians(45)
    foco.rotation_euler[2] = math.radians(i * 90) # Rotación variada