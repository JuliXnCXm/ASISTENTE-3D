import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
cubierta_x = 12.0
cubierta_y = 10.0
cubierta_z = 0.3
pretil_espesor = 0.25
pretil_alto = 1.0

# Crear la losa de cubierta
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
losa_cubierta = bpy.context.active_object
losa_cubierta.name = "LosaCubierta"
losa_cubierta.dimensions = (cubierta_x, cubierta_y, cubierta_z)

# Posiciones y dimensiones del pretil
pos_z = cubierta_z / 2 + pretil_alto / 2

# Pretil Norte (Y+)
bpy.ops.mesh.primitive_cube_add(location=(0, cubierta_y/2 - pretil_espesor/2, pos_z))
pretil_n = bpy.context.active_object
pretil_n.name = "Pretil_Norte"
pretil_n.dimensions = (cubierta_x, pretil_espesor, pretil_alto)

# Pretil Sur (Y-)
bpy.ops.mesh.primitive_cube_add(location=(0, -cubierta_y/2 + pretil_espesor/2, pos_z))
pretil_s = bpy.context.active_object
pretil_s.name = "Pretil_Sur"
pretil_s.dimensions = (cubierta_x, pretil_espesor, pretil_alto)

# Pretil Este (X+)
bpy.ops.mesh.primitive_cube_add(location=(cubierta_x/2 - pretil_espesor/2, 0, pos_z))
pretil_e = bpy.context.active_object
pretil_e.name = "Pretil_Este"
pretil_e.dimensions = (pretil_espesor, cubierta_y - 2 * pretil_espesor, pretil_alto)

# Pretil Oeste (X-)
bpy.ops.mesh.primitive_cube_add(location=(-cubierta_x/2 + pretil_espesor/2, 0, pos_z))
pretil_o = bpy.context.active_object
pretil_o.name = "Pretil_Oeste"
pretil_o.dimensions = (pretil_espesor, cubierta_y - 2 * pretil_espesor, pretil_alto)