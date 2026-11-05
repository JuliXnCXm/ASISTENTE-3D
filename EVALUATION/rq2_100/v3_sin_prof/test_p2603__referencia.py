import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 2.0
profundidad = 0.3
espesor_panel = 0.02
num_baldas = 5

# Crear paneles laterales
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + espesor_panel/2, 0, alto/2))
lateral_izq = bpy.context.active_object
lateral_izq.name = 'Estanteria_Lateral_Izq'
lateral_izq.scale = (espesor_panel, profundidad, alto)

bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - espesor_panel/2, 0, alto/2))
lateral_der = bpy.context.active_object
lateral_der.name = 'Estanteria_Lateral_Der'
lateral_der.scale = (espesor_panel, profundidad, alto)

# Crear panel trasero
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -profundidad/2 + espesor_panel/2, alto/2))
trasero = bpy.context.active_object
trasero.name = 'Estanteria_Trasera'
trasero.scale = (ancho - 2 * espesor_panel, espesor_panel, alto)

# Crear baldas
espacio_baldas = alto / (num_baldas + 1)
ancho_balda = ancho - 2 * espesor_panel
for i in range(num_baldas):
    z_pos = (i + 1) * espacio_baldas
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    balda = bpy.context.active_object
    balda.name = f'Estanteria_Balda_{i+1}'
    balda.scale = (ancho_balda, profundidad - espesor_panel, espesor_panel)
    
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)