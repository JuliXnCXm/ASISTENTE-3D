import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
largo = 2.2
profundidad = 0.9
alto_total = 0.8
alto_asiento = 0.4

# Crear la base/asiento
alto_base = alto_asiento
loc_base = (largo/2, profundidad/2, alto_base/2)
scale_base = (largo, profundidad, alto_base)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_base)
base = bpy.context.active_object
base.name = "BaseSofa"
base.scale = scale_base

# Crear el respaldo
espesor_respaldo = 0.2
alto_respaldo = alto_total - alto_asiento
loc_respaldo = (largo/2, espesor_respaldo/2, alto_asiento + alto_respaldo/2)
scale_respaldo = (largo, espesor_respaldo, alto_respaldo)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_respaldo)
respaldo = bpy.context.active_object
respaldo.name = "RespaldoSofa"
respaldo.scale = scale_respaldo

# Crear los reposabrazos
espesor_brazo = 0.2
alto_brazo = 0.2
loc_brazo_izq = (espesor_brazo/2, profundidad/2, alto_asiento + alto_brazo/2)
loc_brazo_der = (largo - espesor_brazo/2, profundidad/2, alto_asiento + alto_brazo/2)
scale_brazo = (espesor_brazo, profundidad, alto_brazo)

bpy.ops.mesh.primitive_cube_add(size=1, location=loc_brazo_izq)
brazo_izq = bpy.context.active_object
brazo_izq.name = "ReposabrazosIzquierdo"
brazo_izq.scale = scale_brazo

bpy.ops.mesh.primitive_cube_add(size=1, location=loc_brazo_der)
brazo_der = bpy.context.active_object
brazo_der.name = "ReposabrazosDerecho"
brazo_der.scale = scale_brazo