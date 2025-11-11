import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_tablero = 0.80
espesor_tablero = 0.01
diametro_base = 0.30
altura_base = 0.40

# Crear base cilíndrica
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_base / 2,
    depth=altura_base,
    location=(0, 0, altura_base / 2)
)
base = bpy.context.active_object
base.name = "BaseMesa"

# Crear tablero de vidrio
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_tablero / 2,
    depth=espesor_tablero,
    location=(0, 0, altura_base + espesor_tablero / 2)
)
tablero = bpy.context.active_object
tablero.name = "TableroMesa"