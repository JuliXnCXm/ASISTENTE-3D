import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la escalera
num_peldanos = 15
ancho = 1.0
huella = 0.3  # Dimensión en Y
contrahuella = 0.18 # Dimensión en Z

# Creación de los peldaños en un bucle
for i in range(num_peldanos):
    # Posición de cada peldaño
    loc_x = 0
    loc_y = i * huella + huella / 2
    loc_z = i * contrahuella + contrahuella / 2
    
    # Crear el peldaño
    bpy.ops.mesh.primitive_cube_add(
        location=(loc_x, loc_y, loc_z),
        scale=(ancho, huella, contrahuella)
    )