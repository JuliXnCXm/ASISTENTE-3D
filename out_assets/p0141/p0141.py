import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
interior_x = 5.0
interior_y = 4.0
altura = 2.5
espesor = 0.2

# Posiciones
loc_piso_techo_z = [-espesor / 2, altura + espesor / 2]

# Crear Losa de Piso
bpy.ops.mesh.primitive_cube_add(size=1, location=((interior_x + espesor) / 2, (interior_y + espesor) / 2, loc_piso_techo_z[0]), scale=(interior_x + espesor*2, interior_y + espesor*2, espesor))
bpy.context.active_object.name = "LosaPiso"

# Crear Losa de Techo
bpy.ops.mesh.primitive_cube_add(size=1, location=((interior_x + espesor) / 2, (interior_y + espesor) / 2, loc_piso_techo_z[1]), scale=(interior_x + espesor*2, interior_y + espesor*2, espesor))
bpy.context.active_object.name = "LosaTecho"

# Crear Muros
# Muro Norte (largo en X)
bpy.ops.mesh.primitive_cube_add(size=1, location=((interior_x + espesor) / 2, interior_y + espesor/2, altura / 2), scale=(interior_x + espesor*2, espesor, altura))
bpy.context.active_object.name = "MuroNorte"
# Muro Sur (largo en X)
bpy.ops.mesh.primitive_cube_add(size=1, location=((interior_x + espesor) / 2, -espesor/2, altura / 2), scale=(interior_x + espesor*2, espesor, altura))
bpy.context.active_object.name = "MuroSur"
# Muro Este (largo en Y)
bpy.ops.mesh.primitive_cube_add(size=1, location=(interior_x + espesor/2, (interior_y) / 2, altura / 2), scale=(espesor, interior_y, altura))
bpy.context.active_object.name = "MuroEste"
# Muro Oeste (largo en Y)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-espesor/2, (interior_y) / 2, altura / 2), scale=(espesor, interior_y, altura))
bpy.context.active_object.name = "MuroOeste"