import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_x = 3.0
largo_y = 1.8
altura = 1.1
profundidad = 0.6

# Parte larga (eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_x / 2, -profundidad / 2, altura / 2),
    scale=(largo_x, profundidad, altura)
)
parte_larga = bpy.context.object
parte_larga.name = "Mostrador_Largo"

# Parte corta (eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-profundidad / 2, largo_y / 2 - profundidad, altura / 2),
    scale=(profundidad, largo_y - profundidad, altura)
)
parte_corta = bpy.context.object
parte_corta.name = "Mostrador_Corto"

# Unir las dos partes con un booleano para un objeto limpio
bool_mod = parte_larga.modifiers.new(name='Union', type='BOOLEAN')
bool_mod.object = parte_corta
bool_mod.operation = 'UNION'
bpy.ops.object.select_all(action='DESELECT')
parte_larga.select_set(True)
bpy.context.view_layer.objects.active = parte_larga
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

bpy.data.objects.remove(parte_corta)
parte_larga.name = "Mostrador_En_L"