import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
asiento_largo = 2.0
asiento_ancho = 0.5
asiento_grosor = 0.1
altura_suelo = 0.45
base_tam = 0.4
base_altura = altura_suelo - asiento_grosor

# Crear asiento
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, base_altura + asiento_grosor / 2))
asiento = bpy.context.active_object
asiento.name = "AsientoBanco"
asiento.dimensions = (asiento_largo, asiento_ancho, asiento_grosor)

# Crear primera base
pos_x_base1 = -asiento_largo / 2 + base_tam / 2 + 0.1
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x_base1, 0, base_altura / 2))
base1 = bpy.context.active_object
base1.name = "BaseBanco1"
base1.dimensions = (base_tam, asiento_ancho, base_altura)

# Crear segunda base
pos_x_base2 = asiento_largo / 2 - base_tam / 2 - 0.1
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x_base2, 0, base_altura / 2))
base2 = bpy.context.active_object
base2.name = "BaseBanco2"
base2.dimensions = (base_tam, asiento_ancho, base_altura)