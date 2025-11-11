import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_panel = 4.0
alto_panel = 3.0
grosor_vidrio = 0.02
ancho_montante = 0.05
profundidad_montante = 0.1
num_div_horiz = 3
num_div_vert = 3

# Crear panel de vidrio
bpy.ops.mesh.primitive_cube_add(location=(0, grosor_vidrio/2, alto_panel/2))
vidrio = bpy.context.object
vidrio.scale = (ancho_panel/2, grosor_vidrio/2, alto_panel/2)
bpy.ops.object.transform_apply(scale=True)
vidrio.name = 'Vidrio_Panel'

# Crear montantes horizontales
espacio_h = alto_panel / num_div_horiz
for i in range(num_div_horiz + 1):
    z_pos = i * espacio_h
    bpy.ops.mesh.primitive_cube_add(location=(0, -profundidad_montante/2, z_pos))
    montante_h = bpy.context.object
    montante_h.scale = (ancho_panel/2, profundidad_montante/2, ancho_montante/2)
    bpy.ops.object.transform_apply(scale=True)

# Crear montantes verticales
espacio_v = ancho_panel / num_div_vert
start_x = -ancho_panel / 2
for i in range(num_div_vert + 1):
    x_pos = start_x + i * espacio_v
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, -profundidad_montante/2, alto_panel/2))
    montante_v = bpy.context.object
    montante_v.scale = (ancho_montante/2, profundidad_montante/2, alto_panel/2)
    bpy.ops.object.transform_apply(scale=True)