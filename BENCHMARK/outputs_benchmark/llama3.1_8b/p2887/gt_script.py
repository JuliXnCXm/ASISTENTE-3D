import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones del bolardo
altura = 0.9
diametro = 0.3
radio = diametro / 2

# Crear el bolardo en el origen
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura,
    location=(0, 0, altura / 2) # La base se apoya en z=0
)

bolardo = bpy.context.active_object
bolardo.name = 'Bolardo_Hormigon'

# Suavizar el sombreado
bpy.ops.object.shade_smooth()