import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
planta_x = 4.0
planta_y = 3.0
altura = 2.8
seccion_poste = 0.15
seccion_viga_h = 0.20
seccion_viga_w = 0.10
seccion_vigueta_h = 0.15
seccion_vigueta_w = 0.08
num_viguetas = 7

# Crear Postes
posiciones_postes = [
    (planta_x/2, planta_y/2, altura/2),
    (-planta_x/2, planta_y/2, altura/2),
    (planta_x/2, -planta_y/2, altura/2),
    (-planta_x/2, -planta_y/2, altura/2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    poste = bpy.context.active_object
    poste.name = f"Poste.{i+1:02d}"
    poste.dimensions = (seccion_poste, seccion_poste, altura)

# Crear Vigas Principales (a lo largo de X)
posiciones_y_vigas = [planta_y/2, -planta_y/2]
for i, y_pos in enumerate(posiciones_y_vigas):
    bpy.ops.mesh.primitive_cube_add(location=(0, y_pos, altura + seccion_viga_h/2))
    viga = bpy.context.active_object
    viga.name = f"Viga.{i+1:02d}"
    viga.dimensions = (planta_x + seccion_poste, seccion_viga_w, seccion_viga_h)

# Crear Viguetas Transversales (a lo largo de Y)
separacion_viguetas = planta_x / (num_viguetas - 1)
for i in range(num_viguetas):
    x_pos = -planta_x/2 + i * separacion_viguetas
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, altura + seccion_viga_h + seccion_vigueta_h/2))
    vigueta = bpy.context.active_object
    vigueta.name = f"Vigueta.{i+1:02d}"
    vigueta.dimensions = (seccion_vigueta_w, planta_y + seccion_poste, seccion_vigueta_h)