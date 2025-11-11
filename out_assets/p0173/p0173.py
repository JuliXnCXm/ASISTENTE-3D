import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
longitud_banco = 2.0
profundidad_asiento = 0.45
altura_asiento = 0.4
altura_respaldo = 0.5
espesor_tablon = 0.05
ancho_pata = 0.1

# Crear asiento
bpy.ops.mesh.primitive_cube_add(location=(0, profundidad_asiento/2, altura_asiento - espesor_tablon/2), scale=(longitud_banco, profundidad_asiento, espesor_tablon))
asiento = bpy.context.active_object
asiento.name = "AsientoBanco"

# Crear respaldo
loc_z_respaldo = altura_asiento + altura_respaldo/2 - espesor_tablon
bpy.ops.mesh.primitive_cube_add(location=(0, 0, loc_z_respaldo), scale=(longitud_banco, espesor_tablon, altura_respaldo))
respaldo = bpy.context.active_object
respaldo.name = "RespaldoBanco"
respaldo.rotation_euler[0] = math.radians(10) # Inclinación

# Crear patas (soportes traseros que continúan del respaldo)
altura_pata_total = altura_asiento + altura_respaldo
pos_x_pata = longitud_banco/2 - ancho_pata*1.5

bpy.ops.mesh.primitive_cube_add(location=(-pos_x_pata, profundidad_asiento/2, altura_pata_total/2 - espesor_tablon), scale=(ancho_pata, ancho_pata, altura_pata_total))
pata1 = bpy.context.active_object
pata1.name = "SoporteIzquierdo"
pata1.rotation_euler[0] = math.radians(10)

bpy.ops.mesh.primitive_cube_add(location=(pos_x_pata, profundidad_asiento/2, altura_pata_total/2 - espesor_tablon), scale=(ancho_pata, ancho_pata, altura_pata_total))
pata2 = bpy.context.active_object
pata2.name = "SoporteDerecho"
pata2.rotation_euler[0] = math.radians(10)