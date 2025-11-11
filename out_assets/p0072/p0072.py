import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_base = 0.30
alto_base = 0.02
alto_mastil = 1.5
diametro_mastil = 0.03
diametro_bombilla = 0.10

# Crear la base
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_base / 2.0,
    depth=alto_base,
    location=(0, 0, alto_base / 2.0)
)
base = bpy.context.active_object
base.name = 'BaseLampara'

# Crear el mástil
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_mastil / 2.0,
    depth=alto_mastil,
    location=(0, 0, alto_base + alto_mastil / 2.0)
)
mastil = bpy.context.active_object
mastil.name = 'MastilLampara'

# Crear la bombilla
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=diametro_bombilla / 2.0,
    location=(0, 0, alto_base + alto_mastil + diametro_bombilla / 2.0)
)
bombilla = bpy.context.active_object
bombilla.name = 'Bombilla'