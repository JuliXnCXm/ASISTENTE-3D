import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del bolardo
altura = 0.8
diametro = 0.3
radio = diametro / 2

# Crear el cilindro para el bolardo
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=radio,
    depth=altura,
    location=(0, 0, altura / 2) # Ubicar la base en Z=0
)

# Asignar nombre al objeto
bolardo = bpy.context.active_object
bolardo.name = 'Bolardo_Hormigon'

# Suavizar el sombreado y aplicar bisel
bpy.ops.object.shade_smooth()
bpy.ops.object.modifier_add(type='BEVEL')
bolardo.modifiers['Bevel'].width = 0.01
bolardo.modifiers['Bevel'].segments = 3