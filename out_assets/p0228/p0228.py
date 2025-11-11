import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros
ancho_edif = 6.0
largo_edif = 10.0
pendiente_grados = 30.0
espesor_cubierta = 0.2

# Cálculos
pendiente_rad = math.radians(pendiente_grados)
ancho_faldon = (ancho_edif / 2) / math.cos(pendiente_rad)
altura_cumbrera = (ancho_edif / 2) * math.tan(pendiente_rad)

# Crear primer faldón
bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
faldon1 = bpy.context.active_object
faldon1.name = "FaldonDerecho"
faldon1.dimensions = (ancho_faldon, largo_edif, espesor_cubierta)
faldon1.rotation_euler[1] = pendiente_rad
faldon1.location = (
    (ancho_edif / 4),
    0,
    (altura_cumbrera / 2)
)

# Crear segundo faldón
bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
faldon2 = bpy.context.active_object
faldon2.name = "FaldonIzquierdo"
faldon2.dimensions = (ancho_faldon, largo_edif, espesor_cubierta)
faldon2.rotation_euler[1] = -pendiente_rad
faldon2.location = (
    -(ancho_edif / 4),
    0,
    (altura_cumbrera / 2)
)