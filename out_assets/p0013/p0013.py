import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 0.80
altura = 0.45
radio = diametro / 2

# Crear la mesa
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=radio,
    depth=altura,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, altura / 2)
)
mesa = bpy.context.active_object
mesa.name = "MesaCentroCilindrica"