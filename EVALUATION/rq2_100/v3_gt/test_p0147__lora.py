import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
alto_total = 1.8
ancho_total = 1.0
fondo_total = 0.3
num_estantes = 5
grosor_panel = 0.02

# Crear marco vertical
ancho_panel = ancho_total / 2
pos_x = ancho_panel
pos_y = fondo_total / 2
pos_z = alto_total / 2
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x, pos_y, pos_z))
panel_izq = bpy.context.active_object
panel_izq.name = "Panel_Izquierdo"
panel_izq.dimensions = (grosor_panel, fondo_total, alto_total)

pos_x = -ancho_panel
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x, pos_y, pos_z))
panel_der = bpy.context.active_object
panel_der.name = "Panel_Derecho"
panel_der.dimensions = (grosor_panel, fondo_total, alto_total)

# Crear estantes horizontales
espacio_entre_estantes = alto_total / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes + grosor_panel/2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"
    estante.dimensions = (ancho_total - 2*grosor_panel, fondo_total, grosor_panel)