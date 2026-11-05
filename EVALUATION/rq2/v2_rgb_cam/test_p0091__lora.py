import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
alto = 1.8
ancho = 1.0
fondo = 0.3
num_baldas = 5
grosor_panel = 0.02

# Crear panel frontal
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, fondo/2, alto/2))
panel_frontal = bpy.context.active_object
panel_frontal.name = 'Panel_Frontal'
panel_frontal.dimensions = (ancho, grosor_panel, alto)

# Crear panel trasero
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2, fondo/2, alto/2))
panel_trasero = bpy.context.active_object
panel_trasero.name = 'Panel_Trasero'
panel_trasero.dimensions = (ancho, grosor_panel, alto)

# Crear baldas
espacio_entre_baldas = alto / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    balda = bpy.context.active_object
    balda.name = f'Balda_{i+1}'
    balda.dimensions = (ancho, fondo, grosor_panel)