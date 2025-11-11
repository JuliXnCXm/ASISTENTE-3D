import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la habitación
largo_ext = 5.0
ancho_ext = 4.0
altura_muro = 2.7
espesor_muro = 0.15
espesor_losa = 0.2

# Crear Losa de Piso
bpy.ops.mesh.primitive_cube_add(size=1, location=(largo_ext/2, ancho_ext/2, -espesor_losa/2))
losa = bpy.context.active_object
losa.name = "LosaPiso"
losa.scale = (largo_ext, ancho_ext, espesor_losa)

# Crear Muro Norte
loc_n = (largo_ext / 2, ancho_ext - espesor_muro / 2, altura_muro / 2)
scale_n = (largo_ext, espesor_muro, altura_muro)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_n)
muro_n = bpy.context.active_object
muro_n.name = "MuroNorte"
muro_n.scale = scale_n

# Crear Muro Sur
loc_s = (largo_ext / 2, espesor_muro / 2, altura_muro / 2)
scale_s = (largo_ext, espesor_muro, altura_muro)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_s)
muro_s = bpy.context.active_object
muro_s.name = "MuroSur"
muro_s.scale = scale_s

# Crear Muro Este
loc_e = (largo_ext - espesor_muro / 2, ancho_ext / 2, altura_muro / 2)
scale_e = (espesor_muro, ancho_ext - 2 * espesor_muro, altura_muro)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_e)
muro_e = bpy.context.active_object
muro_e.name = "MuroEste"
muro_e.scale = scale_e

# Crear Muro Oeste
loc_o = (espesor_muro / 2, ancho_ext / 2, altura_muro / 2)
scale_o = (espesor_muro, ancho_ext - 2 * espesor_muro, altura_muro)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_o)
muro_o = bpy.context.active_object
muro_o.name = "MuroOeste"
muro_o.scale = scale_o