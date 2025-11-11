import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_mesa = 3.0
ancho_mesa = 1.2
altura_total = 0.75
espesor_tablero = 0.05
radio_base = 0.4

# Crear el tablero ovalado
# Se crea un cilindro y se escala para hacerlo ovalado
bpy.ops.mesh.primitive_cylinder_add(
    radius=1, 
    depth=espesor_tablero, 
    location=(0, 0, altura_total - espesor_tablero / 2),
    vertices=128
)
tablero = bpy.context.object
tablero.name = "TableroOvalado"
tablero.scale.x = largo_mesa / 2
tablero.scale.y = ancho_mesa / 2
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear la base cilíndrica
altura_base = altura_total - espesor_tablero
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_base,
    depth=altura_base,
    location=(0, 0, altura_base / 2),
    vertices=64
)
base = bpy.context.object
base.name = "BaseCilindrica"