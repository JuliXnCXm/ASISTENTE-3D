import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 0.8
profundidad = 0.3
alto_total = 1.8
num_baldas = 5

# Paneles verticales
ancho_panel = 0.02
pos_x_panel = (ancho / 2) - (ancho_panel / 2)

bpy.ops.mesh.primitive_cube_add(location=(-pos_x_panel, 0, alto_total / 2))
panel_izq = bpy.context.active_object
panel_izq.name = "Panel_Izquierdo"
panel_izq.dimensions = (ancho_panel, profundidad, alto_total)

bpy.ops.mesh.primitive_cube_add(location=(pos_x_panel, 0, alto_total / 2))
panel_der = bpy.context.active_object
panel_der.name = "Panel_Derecho"
panel_der.dimensions = (ancho_panel, profundidad, alto_total)

# Baldas
espacio_entre_baldas = alto_total / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + (espesor_bala / 2)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, z_pos))
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"
    balda.dimensions = (ancho - 2 * ancho_panel, profundidad, espesor_bala)