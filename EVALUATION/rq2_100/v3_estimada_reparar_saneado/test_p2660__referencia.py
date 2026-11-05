import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- Dimensiones de la habitacion ---
largo_hab = 5.0
ancho_hab = 4.0
alto_hab = 2.8
espesor_muro = 0.15
espesor_losa = 0.20

# --- Construccion de la habitacion ---
# Losa de piso
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, ancho_hab/2, -espesor_losa/2), scale=(largo_hab, ancho_hab, espesor_losa))
bpy.context.active_object.name = 'Losa_Piso'

# Losa de techo
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, ancho_hab/2, alto_hab + espesor_losa/2), scale=(largo_hab, ancho_hab, espesor_losa))
bpy.context.active_object.name = 'Losa_Techo'

# Muros
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, espesor_muro/2, alto_hab/2), scale=(largo_hab, espesor_muro, alto_hab))
bpy.context.active_object.name = 'Muro_Fondo'
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, ancho_hab - espesor_muro/2, alto_hab/2), scale=(largo_hab, espesor_muro, alto_hab))
bpy.context.active_object.name = 'Muro_Frente'
bpy.ops.mesh.primitive_cube_add(location=(espesor_muro/2, ancho_hab/2, alto_hab/2), scale=(espesor_muro, ancho_hab, alto_hab))
bpy.context.active_object.name = 'Muro_Izquierdo'
bpy.ops.mesh.primitive_cube_add(location=(largo_hab - espesor_muro/2, ancho_hab/2, alto_hab/2), scale=(espesor_muro, ancho_hab, alto_hab))
bpy.context.active_object.name = 'Muro_Derecho'

# --- Mobiliario ---
# Sofa
ancho_sofa = 2.0
prof_sofa = 0.9
alto_asiento_sofa = 0.4
alto_respaldo_sofa = 0.8

# Base del sofa
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, 1.0, alto_asiento_sofa/2), scale=(ancho_sofa, prof_sofa, alto_asiento_sofa))
# Respaldo del sofa
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, 1.0 - prof_sofa/2 + 0.1, (alto_respaldo_sofa + alto_asiento_sofa)/2), scale=(ancho_sofa, 0.2, alto_respaldo_sofa - alto_asiento_sofa))
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects[-1].select_set(True)
bpy.data.objects[-2].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[-2]
bpy.ops.object.join()
bpy.context.active_object.name = 'Sofa'

# Mesa de centro
ancho_mesa = 1.2
prof_mesa = 0.6
alto_mesa = 0.45
bpy.ops.mesh.primitive_cube_add(location=(largo_hab/2, 2.5, alto_mesa/2), scale=(ancho_mesa, prof_mesa, alto_mesa))
bpy.context.active_object.name = 'Mesa_Centro'

# Aplicar escalas
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)