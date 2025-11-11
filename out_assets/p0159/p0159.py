import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
L, W, H = 4.0, 3.0, 2.8
p_s = 0.15
v_w, v_h = 0.15, 0.20
vg_w, vg_h = 0.10, 0.15
espaciado_viguetas = 0.4

# Postes
posiciones_postes = [
    (-L/2 + p_s/2, -W/2 + p_s/2),
    ( L/2 - p_s/2, -W/2 + p_s/2),
    ( L/2 - p_s/2,  W/2 - p_s/2),
    (-L/2 + p_s/2,  W/2 - p_s/2),
]
for i, (px, py) in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(location=(px, py, H/2), scale=(p_s, p_s, H))
    bpy.context.object.name = f"Poste_{i+1}"

# Vigas perimetrales largas (eje X)
bpy.ops.mesh.primitive_cube_add(location=(0, -W/2 + p_s/2, H + v_h/2), scale=(L, v_w, v_h))
bpy.context.object.name = "Viga_Larga_1"
bpy.ops.mesh.primitive_cube_add(location=(0,  W/2 - p_s/2, H + v_h/2), scale=(L, v_w, v_h))
bpy.context.object.name = "Viga_Larga_2"

# Vigas perimetrales cortas (eje Y)
bpy.ops.mesh.primitive_cube_add(location=(-L/2 + p_s/2, 0, H + v_h/2), scale=(v_w, W - 2*p_s, v_h))
bpy.context.object.name = "Viga_Corta_1"
bpy.ops.mesh.primitive_cube_add(location=( L/2 - p_s/2, 0, H + v_h/2), scale=(v_w, W - 2*p_s, v_h))
bpy.context.object.name = "Viga_Corta_2"

# Viguetas
num_viguetas = int(L / espaciado_viguetas) + 1
for i in range(num_viguetas):
    x_pos = -L/2 + i * espaciado_viguetas
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, H + v_h + vg_h/2), scale=(vg_w, W, vg_h))
    bpy.context.object.name = f"Vigueta_{i+1}"
