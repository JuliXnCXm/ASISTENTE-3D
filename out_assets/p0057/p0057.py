import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro de referencia
largo_muro = 3.0
alto_muro = 2.5
espesor_muro = 0.15

# Crear muro
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_muro / 2, espesor_muro / 2, alto_muro / 2),
    scale=(largo_muro, espesor_muro, alto_muro)
)
bpy.context.active_object.name = 'MuroReferencia'

# Dimensiones y posición de la balda
largo_balda = 1.2
profundidad_balda = 0.25
espesor_balda = 0.05
altura_balda_suelo = 1.5

# Posición de la balda (centrada en el muro)
pos_x = largo_muro / 2
pos_y = espesor_muro + profundidad_balda / 2
pos_z = altura_balda_suelo

# Crear la balda
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(pos_x, pos_y, pos_z),
    scale=(largo_balda, profundidad_balda, espesor_balda)
)
bpy.context.active_object.name = 'BaldaFlotante'