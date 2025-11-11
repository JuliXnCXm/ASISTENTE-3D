import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del cuarto (interiores)
largo_int = 6.0
ancho_int = 4.0
alto_int = 2.8
espesor_muro = 0.2
espesor_losa = 0.2

# Crear Losa de Piso
largo_ext = largo_int + 2 * espesor_muro
ancho_ext = ancho_int + 2 * espesor_muro
bpy.ops.mesh.primitive_cube_add(location=(0, 0, -espesor_losa / 2), scale=(largo_ext / 2, ancho_ext / 2, espesor_losa / 2))
bpy.context.object.name = "LosaPiso"

# Crear Muro Norte (+Y)
bpy.ops.mesh.primitive_cube_add(location=(0, ancho_int / 2 + espesor_muro / 2, alto_int / 2), scale=(largo_ext / 2, espesor_muro / 2, alto_int / 2))
bpy.context.object.name = "MuroNorte"

# Crear Muro Sur (-Y)
bpy.ops.mesh.primitive_cube_add(location=(0, -ancho_int / 2 - espesor_muro / 2, alto_int / 2), scale=(largo_ext / 2, espesor_muro / 2, alto_int / 2))
bpy.context.object.name = "MuroSur"

# Crear Muro Este (+X)
bpy.ops.mesh.primitive_cube_add(location=(largo_int / 2 + espesor_muro / 2, 0, alto_int / 2), scale=(espesor_muro / 2, ancho_int / 2, alto_int / 2))
bpy.context.object.name = "MuroEste"

# Crear Muro Oeste (-X)
bpy.ops.mesh.primitive_cube_add(location=(-largo_int / 2 - espesor_muro / 2, 0, alto_int / 2), scale=(espesor_muro / 2, ancho_int / 2, alto_int / 2))
bpy.context.object.name = "MuroOeste"