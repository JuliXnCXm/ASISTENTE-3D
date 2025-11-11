import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parametros
num_peldanos = 5
diametro = 0.4
grosor = 0.05
espaciado = 0.6

# Crear peldaños en un bucle
for i in range(num_peldanos):
    pos_x = i * espaciado
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=diametro / 2,
        depth=grosor,
        location=(pos_x, 0, grosor / 2)
    )
    bpy.context.object.name = f'Peldano_{i+1}'