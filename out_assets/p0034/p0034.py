import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho = 1.5
alto = 2.2
profundidad = 0.3
espesor_madera = 0.02
num_baldas = 6

# Laterales
ancho_util = ancho - 2 * espesor_madera
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + espesor_madera/2, 0, alto/2), scale=(espesor_madera, profundidad, alto))
bpy.context.object.name = "Lateral_Izquierdo"
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - espesor_madera/2, 0, alto/2), scale=(espesor_madera, profundidad, alto))
bpy.context.object.name = "Lateral_Derecho"

# Baldas
espacio_entre_baldas = alto / (num_baldas - 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas
    # La primera y ultima balda se ajustan para quedar al ras
    if i == 0:
        z_pos = espesor_madera / 2
    elif i == num_baldas - 1:
        z_pos = alto - espesor_madera / 2
    else:
        z_pos = (alto - 2*espesor_madera) * (i / (num_baldas - 1.0)) + espesor_madera

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_util, profundidad, espesor_madera)
    )
    bpy.context.object.name = f"Balda_{i+1}"