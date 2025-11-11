import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho = 1.8
alto = 2.2
fondo = 0.3
grosor_madera = 0.03
num_estantes = 5

# Laterales
bpy.ops.mesh.primitive_cube_add(size=1, location=(grosor_madera/2, fondo/2, alto/2), scale=(grosor_madera, fondo, alto))
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho - grosor_madera/2, fondo/2, alto/2), scale=(grosor_madera, fondo, alto))

# Trasera
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, grosor_madera/2, alto/2), scale=(ancho - 2 * grosor_madera, grosor_madera, alto))

# Base y Tapa
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, fondo/2, grosor_madera/2), scale=(ancho, fondo, grosor_madera))
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, fondo/2, alto - grosor_madera/2), scale=(ancho, fondo, grosor_madera))

# Estantes intermedios
espacio_util = alto - 2 * grosor_madera
separacion = espacio_util / (num_estantes + 1)
for i in range(num_estantes):
    altura_estante = grosor_madera + (i + 1) * separacion
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ancho/2, fondo/2, altura_estante),
        scale=(ancho - 2 * grosor_madera, fondo - grosor_madera, grosor_madera)
    )