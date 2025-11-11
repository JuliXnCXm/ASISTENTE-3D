import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_tablero = 0.8
altura_total = 0.45
espesor_tablero = 0.04
radio_pie = 0.1

# Crear el tablero (cilindro)
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_tablero / 2,
    depth=espesor_tablero,
    location=(0, 0, altura_total - espesor_tablero / 2)
)
tablero = bpy.context.active_object
tablero.name = 'TableroMesa'

# Crear el pie (cilindro)
altura_pie = altura_total - espesor_tablero
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_pie,
    depth=altura_pie,
    location=(0, 0, altura_pie / 2)
)
pie = bpy.context.active_object
pie.name = 'PieMesa'