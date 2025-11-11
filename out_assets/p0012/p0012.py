import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones comunes
altura = 2.5
espesor = 0.15

# Dimensiones muro 1 (Norte-Sur)
largo_muro1 = 4.0
loc_muro1 = (espesor / 2, largo_muro1 / 2, altura / 2)
scale_muro1 = (espesor, largo_muro1, altura)

# Crear muro 1
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_muro1)
muro1 = bpy.context.active_object
muro1.name = "MuroNorteSur"
muro1.scale = scale_muro1

# Dimensiones muro 2 (Este-Oeste)
largo_muro2 = 3.0
loc_muro2 = (largo_muro2 / 2 + espesor, espesor / 2, altura / 2)
scale_muro2 = (largo_muro2, espesor, altura)

# Crear muro 2
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_muro2)
muro2 = bpy.context.active_object
muro2.name = "MuroEsteOeste"
muro2.scale = scale_muro2