import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 0.8
alto = 1.2
fondo = 0.3
grosor = 0.02

# Paneles verticales
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + grosor/2, 0, alto/2))
panel_izq = bpy.context.active_object
panel_izq.scale = (grosor, fondo, alto)

bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - grosor/2, 0, alto/2))
panel_der = bpy.context.active_object
panel_der.scale = (grosor, fondo, alto)

# Baldas
num_baldas = 3
separacion_baldas = alto / (num_baldas + 1)

baldas = []
for i in range(num_baldas):
    z_pos = separacion_baldas * (i + 1)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    balda = bpy.context.active_object
    balda.scale = (ancho - 2 * grosor, fondo, grosor)
    baldas.append(balda)

# Unir objetos
bpy.ops.object.select_all(action='DESELECT')
panel_izq.select_set(True)
panel_der.select_set(True)
for balda in baldas:
    balda.select_set(True)
bpy.context.view_layer.objects.active = panel_izq
bpy.ops.object.join()

estanteria = bpy.context.active_object
estanteria.name = 'Estanteria'
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)