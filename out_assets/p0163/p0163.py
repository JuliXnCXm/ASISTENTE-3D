import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_banco = 2.0
ancho_asiento = 0.4
altura_asiento = 0.45
espesor_tablon = 0.05
ancho_respaldo = 0.3
dimension_pata = 0.3

# Asiento
bpy.ops.mesh.primitive_cube_add(location=(0, 0, altura_asiento - espesor_tablon / 2), scale=(largo_banco / 2, ancho_asiento / 2, espesor_tablon / 2))
asiento = bpy.context.active_object
asiento.name = 'AsientoBanco'

# Respaldo
bpy.ops.mesh.primitive_cube_add(location=(0, -ancho_asiento/2 + espesor_tablon/2, altura_asiento + ancho_respaldo/2), scale=(largo_banco / 2, espesor_tablon / 2, ancho_respaldo / 2))
respaldo = bpy.context.active_object
respaldo.name = 'RespaldoBanco'
respaldo.rotation_euler[0] = 0.17 # ~10 grados de inclinación

# Pata Izquierda
bpy.ops.mesh.primitive_cube_add(location=(-largo_banco/2 + dimension_pata/2, 0, (altura_asiento - espesor_tablon)/2), scale=(dimension_pata/2, ancho_asiento/2, (altura_asiento-espesor_tablon)/2))
pata_izq = bpy.context.active_object
pata_izq.name = 'PataIzquierda'

# Pata Derecha
bpy.ops.mesh.primitive_cube_add(location=(largo_banco/2 - dimension_pata/2, 0, (altura_asiento - espesor_tablon)/2), scale=(dimension_pata/2, ancho_asiento/2, (altura_asiento-espesor_tablon)/2))
pata_der = bpy.context.active_object
pata_der.name = 'PataDerecha'