import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones y angulo
ancho_total = 8.0
largo_total = 10.0
grosor_cubierta = 0.2
pendiente_grados = 30.0

# Calculos
pendiente_rad = math.radians(pendiente_grados)
ancho_faldon = (ancho_total / 2) / math.cos(pendiente_rad)
altura_cumbrera = (ancho_total / 2) * math.tan(pendiente_rad)

# Crear Faldon 1 (lado +Y)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0), scale=(largo_total, ancho_faldon, grosor_cubierta))
faldon1 = bpy.context.object
faldon1.name = 'Faldon_Derecho'
faldon1.rotation_euler[0] = pendiente_rad
faldon1.location = (0, ancho_total / 4, altura_cumbrera / 2)

# Crear Faldon 2 (lado -Y)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0), scale=(largo_total, ancho_faldon, grosor_cubierta))
faldon2 = bpy.context.object
faldon2.name = 'Faldon_Izquierdo'
faldon2.rotation_euler[0] = -pendiente_rad
faldon2.location = (0, -ancho_total / 4, altura_cumbrera / 2)