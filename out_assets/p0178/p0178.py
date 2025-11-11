import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
longitud = 4.0
ancho = 3.0
altura = 2.5
seccion_poste = 0.15
seccion_viga = (0.1, 0.2) # ancho, alto
seccion_vigueta = (0.08, 0.15) # ancho, alto
num_viguetas = 7

# Crear postes
posiciones_postes = [
    (-longitud/2, -ancho/2),
    (longitud/2, -ancho/2),
    (-longitud/2, ancho/2),
    (longitud/2, ancho/2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], altura/2),
        scale=(seccion_poste, seccion_poste, altura)
    )
    bpy.context.active_object.name = f"Poste_{i+1}"

# Crear vigas principales (a lo largo de la longitud)
loc_z_viga = altura + seccion_viga[1]/2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -ancho/2, loc_z_viga),
    scale=(longitud + seccion_poste, seccion_viga[0], seccion_viga[1])
)
bpy.context.active_object.name = "Viga_1"

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, ancho/2, loc_z_viga),
    scale=(longitud + seccion_poste, seccion_viga[0], seccion_viga[1])
)
bpy.context.active_object.name = "Viga_2"

# Crear viguetas transversales
loc_z_vigueta = loc_z_viga + seccion_viga[1]/2 + seccion_vigueta[1]/2
espaciado = longitud / (num_viguetas - 1)

for i in range(num_viguetas):
    pos_x = -longitud/2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, loc_z_vigueta),
        scale=(seccion_vigueta[0], ancho + seccion_poste, seccion_vigueta[1])
    )
    bpy.context.active_object.name = f"Vigueta_{i+1}"