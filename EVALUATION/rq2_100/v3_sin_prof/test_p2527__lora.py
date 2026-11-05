import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho = 1.2
alto = 2.0
profundidad = 0.3
num_baldas = 5
grosor_panel = 0.02

# --- Creación de los paneles laterales ---
ancho_util = ancho - grosor_panel * 2
pos_x_lateral = ancho / 2 - grosor_panel / 2
bpy.ops.mesh.primitive_cube_add(location=(-pos_x_lateral, 0, alto / 2))
lateral_izq = bpy.context.active_object
lateral_izq.name = "Lateral_Izquierdo"
lateral_izq.dimensions = (grosor_panel, profundidad, alto)

bpy.ops.mesh.primitive_cube_add(location=(pos_x_lateral, 0, alto / 2))
lateral_der = bpy.context.active_object
lateral_der.name = "Lateral_Derecho"
lateral_der.dimensions = (grosor_panel, profundidad, alto)

# --- Creación de las baldas ---
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas / 2
    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, z_pos),
        scale=(ancho_util, profundidad, grosor_panel)
    )
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"