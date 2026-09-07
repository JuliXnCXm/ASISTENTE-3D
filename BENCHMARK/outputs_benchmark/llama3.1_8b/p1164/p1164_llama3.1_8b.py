import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el piso de parquet
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
piso = bpy.context.active_object
piso.name = "Piso"
piso.scale = (5, 4, 0.1)

# Crea la pared del fondo
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -2, 0))
pared_fondo = bpy.context.active_object
pared_fondo.name = "Pared Fondo"
pared_fondo.scale = (5, 4, 2)
pared_fondo.location = (0, -2, 1)

# Crea la pared del lado izquierdo
bpy.ops.mesh.primitive_cube_add(size=2, location=(-2.5, 0, 0))
pared_lado_izquierdo = bpy.context.active_object
pared_lado_izquierdo.name = "Pared Lado Izquierdo"
pared_lado_izquierdo.scale = (4, 2, 2)
pared_lado_izquierdo.location = (-2.5, 0, 1)

# Crea la pared del lado derecho
bpy.ops.mesh.primitive_cube_add(size=2, location=(2.5, 0, 0))
pared_lado_derecho = bpy.context.active_object
pared_lado_derecho.name = "Pared Lado Derecho"
pared_lado_derecho.scale = (4, 2, 2)
pared_lado_derecho.location = (2.5, 0, 1)

# Crea la pared del techo
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -2, 2))
pared_techo = bpy.context.active_object
pared_techo.name = "Pared Techo"
pared_techo.scale = (5, 4, 1)
pared_techo.location = (0, -2, 3)

# Crea la cama de matrimonio
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -2.5, 1))
cama = bpy.context.active_object
cama.name = "Cama"
cama.scale = (4, 2, 1)
cama.location = (0, -2.5, 2)

# Crea el armario
bpy.ops.mesh.primitive_cube_add(size=1, location=(-2.5, 2.5, 1))
armario = bpy.context.active_object
armario.name = "Armario"
armario.scale = (2, 1, 1)
armario.location = (-2.5, 2.5, 2)

# Guarda el archivo .blend si se especificó la ruta de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])