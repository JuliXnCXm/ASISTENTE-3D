import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la torre ---
diametro_torre = 20.0
altura_piso = 3.0
num_pisos = 6
radio_torre = diametro_torre / 2

# --- Creación de la torre ---
altura_total = altura_piso * num_pisos
altura_actual = 0

for i in range(num_pisos):
    altura_actual += altura_piso
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio_torre,
        depth=altura_piso,
        location=(0, 0, altura_actual),
        vertices=128
    )
    bpy.context.object.name = f'Losa_Piso_{i+1}'