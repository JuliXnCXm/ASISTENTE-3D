import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración de la escena ---
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho_total = 1.2
alto_total = 1.8
profundidad_total = 0.3
num_estantes = 5

# --- Creación del muro base ---
muro_base = bpy.data.objects.new('MuroBase', None)
muro_base.location = (0, 0, 0)
muro_base.dimensions = (ancho_total, profundidad_total, alto_total)
bpy.context.collection.objects.link(muro_base)
bpy.context.view_layer.objects.active = muro_base
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# --- Creación de los estantes ---
espacio_entre_estantes = alto_total / (num_estantes - 1)
for i in range(num_estantes):
    altura_estante = i * espacio_entre_estantes
    if i == 0:
        altura_estante = 0.05
    elif i == num_estantes - 1:
        altura_estante = alto_total - 0.05
    
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, altura_estante),
        scale=(ancho_total, profundidad_total, 0.01)
    )
    estante = bpy.context.active_object
    estante.name = f'Estante_{i+1}'
    bpy.ops.object.transform_apply(scale=True)