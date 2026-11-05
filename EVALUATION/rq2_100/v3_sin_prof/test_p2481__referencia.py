import bpy

# --- Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- Definición de parámetros
largo_muro1 = 5.0
largo_muro2 = 4.0
altura_muros = 2.7
espesor_muros = 0.2
espesor_losa = 0.2

# --- Crear losa de piso
bpy.ops.mesh.primitive_cube_add(location=(largo_muro1/2, largo_muro2/2, -espesor_losa/2))
losa = bpy.context.active_object
losa.name = 'Losa_Piso'
losa.dimensions = (largo_muro1, largo_muro2, espesor_losa)

# --- Crear Muro 1 (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(location=(largo_muro1 / 2, espesor_muros / 2, altura_muros / 2))
muro1 = bpy.context.active_object
muro1.name = 'Muro_1'
muro1.dimensions = (largo_muro1, espesor_muros, altura_muros)

# --- Crear Muro 2 (a lo largo del eje Y)
loc_x = largo_muro1 - espesor_muros / 2
loc_y = largo_muro2 / 2
loc_z = altura_muros / 2
bpy.ops.mesh.primitive_cube_add(location=(loc_x, loc_y, loc_z))
muro2 = bpy.context.active_object
muro2.name = 'Muro_2'
muro2.dimensions = (espesor_muros, largo_muro2, altura_muros)

# --- Aplicar transformaciones
for obj in bpy.context.scene.objects:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)