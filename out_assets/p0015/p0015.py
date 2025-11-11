import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_base = 0.30
altura_base = 0.05
altura_mastil = 1.5
radio_mastil = 0.02
diametro_esfera = 0.40

# Crear Base
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_base / 2, 
    depth=altura_base, 
    location=(0, 0, altura_base / 2))
base = bpy.context.active_object
base.name = "BaseLampara"

# Crear Mástil
loc_mastil_z = altura_base + altura_mastil / 2
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_mastil, 
    depth=altura_mastil, 
    location=(0, 0, loc_mastil_z))
mastil = bpy.context.active_object
mastil.name = "MastilLampara"

# Crear Esfera de Luz
loc_esfera_z = altura_base + altura_mastil
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=diametro_esfera / 2, 
    location=(0, 0, loc_esfera_z))
esfera = bpy.context.active_object
esfera.name = "EsferaLuz"