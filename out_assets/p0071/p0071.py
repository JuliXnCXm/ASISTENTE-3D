import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_tablero = 1.0
espesor_tablero = 0.04
alto_base = 0.4
diametro_base = 0.3
altura_total = alto_base + espesor_tablero

# Crear el tablero
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=diametro_tablero / 2.0,
    depth=espesor_tablero,
    location=(0, 0, alto_base + espesor_tablero / 2.0),
    rotation=(0, 0, 0)
)
tablero = bpy.context.active_object
tablero.name = 'TableroMesa'

# Crear la base
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=diametro_base / 2.0,
    depth=alto_base,
    location=(0, 0, alto_base / 2.0),
    rotation=(0, 0, 0)
)
base = bpy.context.active_object
base.name = 'BaseMesa'