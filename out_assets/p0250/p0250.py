import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 0.3
altura_total = 0.9
radio = diametro / 2

# La altura del cilindro es la altura total menos el radio (para la semiesfera)
altura_cilindro = altura_total - radio

# Crear parte cilindrica
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=radio,
    depth=altura_cilindro,
    location=(0, 0, altura_cilindro / 2)
)
bpy.context.object.name = 'Bolardo_Cuerpo'

# Crear parte semiesferica
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=32,
    ring_count=16,
    radius=radio,
    location=(0, 0, altura_cilindro)
)
bpy.context.object.name = 'Bolardo_Cabeza'