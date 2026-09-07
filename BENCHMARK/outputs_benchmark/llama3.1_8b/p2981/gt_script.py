import bpy

# --- Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del bolardo
altura = 0.9
diametro = 0.3
radio = diametro / 2
posicion = (0, 0, altura / 2)

# --- Creación del bolardo
bpy.ops.mesh.primitive_cylinder_add(
    vertices=32,
    radius=radio,
    depth=altura,
    location=posicion,
    end_fill_type='NGON'
)

bolardo = bpy.context.active_object
bolardo.name = 'Bolardo_Hormigon'