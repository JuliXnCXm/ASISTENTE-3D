import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones generales
ancho = 1.2
alto = 1.8
fondo = 0.3
grosor_panel = 0.03
num_estantes = 4

# Crear paneles verticales
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=((ancho / 2 - grosor_panel / 2) * i, 0, alto / 2)
    )
    panel = bpy.context.active_object
    panel.dimensions = (grosor_panel, fondo, alto)

# Crear paneles horizontales (base y tapa)
for i in [0, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, (grosor_panel / 2) + i * (alto - grosor_panel))
    )
    panel = bpy.context.active_object
    panel.dimensions = (ancho - 2 * grosor_panel, fondo, grosor_panel)

# Crear estantes interiores
espacio_util = alto - 2 * grosor_panel
separacion = espacio_util / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = grosor_panel + (i + 1) * separacion
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(0, 0, z_pos)
    )
    estante = bpy.context.active_object
    estante.dimensions = (ancho - 2 * grosor_panel, fondo, grosor_panel)

# Unir todas las partes
bpy.ops.object.select_all(action='SELECT')
bpy.context.view_layer.objects.active = bpy.data.objects[0]
bpy.ops.object.join()