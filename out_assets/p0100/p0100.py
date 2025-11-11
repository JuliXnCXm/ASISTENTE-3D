import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_total = 1.2
alto_total = 2.0
profundidad_total = 0.3
grosor_madera = 0.03
num_baldas = 5

# Crear laterales
ancho_lateral = grosor_madera
alto_lateral = alto_total
profundidad_lateral = profundidad_total

# Lateral izquierdo
bpy.ops.mesh.primitive_cube_add(
    location=(-ancho_total / 2 + ancho_lateral / 2, 0, alto_lateral / 2),
    scale=(ancho_lateral, profundidad_lateral, alto_lateral)
)
bpy.context.active_object.name = 'LateralIzquierdo'

# Lateral derecho
bpy.ops.mesh.primitive_cube_add(
    location=(ancho_total / 2 - ancho_lateral / 2, 0, alto_lateral / 2),
    scale=(ancho_lateral, profundidad_lateral, alto_lateral)
)
bpy.context.active_object.name = 'LateralDerecho'

# Crear baldas
ancho_balda = ancho_total - (2 * grosor_madera)
alto_balda = grosor_madera
profundidad_balda = profundidad_total
espacio_entre_baldas = (alto_total - grosor_madera) / (num_baldas -1)

for i in range(num_baldas):
    z_pos = (i * espacio_entre_baldas) + alto_balda / 2
    if i == num_baldas -1: # La balda superior
        z_pos = alto_total - alto_balda / 2
    if i == 0: # La balda inferior
        z_pos = alto_balda / 2
        
    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, z_pos),
        scale=(ancho_balda, profundidad_balda, alto_balda)
    )
    bpy.context.active_object.name = f'Balda_{i+1}'