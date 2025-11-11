import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_mesa = 3.0
ancho_mesa = 1.2
alto_mesa = 0.75
espesor_tablero = 0.05

# Dimensiones de las bases
ancho_base = 0.8
profundidad_base = 0.10
alto_base = alto_mesa - espesor_tablero
separacion_bases = 1.5

# Crear tablero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_mesa - espesor_tablero / 2),
    scale=(largo_mesa, ancho_mesa, espesor_tablero)
)
bpy.context.active_object.name = 'TableroMesa'

# Crear base 1
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-separacion_bases / 2, 0, alto_base / 2),
    scale=(profundidad_base, ancho_base, alto_base)
)
bpy.context.active_object.name = 'BaseMesa_1'

# Crear base 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(separacion_bases / 2, 0, alto_base / 2),
    scale=(profundidad_base, ancho_base, alto_base)
)
bpy.context.active_object.name = 'BaseMesa_2'