import bpy

# Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del bolardo
diametro = 0.2
altura = 0.9
radio = diametro / 2

# Creación del bolardo
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura,
    location=(0, 0, altura / 2)
)

bolardo = bpy.context.active_object
bolardo.name = 'Bolardo_Hormigon'

# Suavizar la malla
bpy.ops.object.shade_smooth()