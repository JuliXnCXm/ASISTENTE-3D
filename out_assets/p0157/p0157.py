import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_edificio = 6.0
largo_edificio = 10.0
pendiente_grados = 30.0
alero = 0.5
espesor_cubierta = 0.2

# Cálculos
pendiente_rad = math.radians(pendiente_grados)
ancho_medio_edificio = ancho_edificio / 2
ancho_faldon = (ancho_medio_edificio + alero) / math.cos(pendiente_rad)
altura_cumbrera = (ancho_medio_edificio) * math.tan(pendiente_rad)

# Crear faldón 1
bpy.ops.mesh.primitive_cube_add(size=1)
faldon1 = bpy.context.active_object
faldon1.name = "Cubierta_Faldon_1"
faldon1.scale = (largo_edificio, ancho_faldon, espesor_cubierta)
faldon1.rotation_euler[0] = pendiente_rad
faldon1.location.y = ancho_faldon / 2 * math.cos(pendiente_rad)
faldon1.location.z = altura_cumbrera - ancho_faldon / 2 * math.sin(pendiente_rad)

# Crear faldón 2
bpy.ops.mesh.primitive_cube_add(size=1)
faldon2 = bpy.context.active_object
faldon2.name = "Cubierta_Faldon_2"
faldon2.scale = (largo_edificio, ancho_faldon, espesor_cubierta)
faldon2.rotation_euler[0] = -pendiente_rad
faldon2.location.y = -ancho_faldon / 2 * math.cos(pendiente_rad)
faldon2.location.z = altura_cumbrera - ancho_faldon / 2 * math.sin(pendiente_rad)