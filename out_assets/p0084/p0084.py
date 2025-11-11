import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
largo_x = 4.0
ancho_y = 3.0
alto_z = 2.5
espesor = 0.15

# Crear y posicionar los 4 muros
def crear_muro(nombre, escala, posicion):
    bpy.ops.mesh.primitive_cube_add(location=posicion)
    muro = bpy.context.active_object
    muro.name = nombre
    muro.scale = escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Muro Norte (a lo largo de X)
crear_muro('Muro_Norte', (largo_x/2, espesor/2, alto_z/2), (0, ancho_y/2 - espesor/2, alto_z/2))

# Muro Sur (a lo largo de X)
crear_muro('Muro_Sur', (largo_x/2, espesor/2, alto_z/2), (0, -ancho_y/2 + espesor/2, alto_z/2))

# Muro Este (a lo largo de Y)
crear_muro('Muro_Este', (espesor/2, (ancho_y-2*espesor)/2, alto_z/2), (largo_x/2 - espesor/2, 0, alto_z/2))

# Muro Oeste (a lo largo de Y)
crear_muro('Muro_Oeste', (espesor/2, (ancho_y-2*espesor)/2, alto_z/2), (-largo_x/2 + espesor/2, 0, alto_z/2))