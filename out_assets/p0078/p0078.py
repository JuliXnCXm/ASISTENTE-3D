import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del peldaño
ancho = 1.0
huella = 0.30
contrahuella = 0.18
num_peldanos = 3

# Crear peldaños en un bucle
for i in range(num_peldanos):
    # Calcular posición de cada peldaño
    pos_x = 0
    pos_y = i * huella + huella / 2.0
    pos_z = i * contrahuella + contrahuella / 2.0
    
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, pos_y, pos_z),
        scale=(ancho, huella, contrahuella)
    )
    peldano = bpy.context.active_object
    peldano.name = f'Peldano_{i+1}'