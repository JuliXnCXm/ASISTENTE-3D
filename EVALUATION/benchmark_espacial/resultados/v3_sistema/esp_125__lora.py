import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del edificio ---
num_pisos = 3
altura_piso = 3.0
vol_x = 20.0
vol_y = 20.0
retranqueo = 3.0

# --- Función para crear un piso ---
def crear_piso(nombre, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    piso = bpy.context.active_object
    piso.name = nombre
    piso.dimensions = (vol_x, vol_y, altura_piso)
    return piso

# --- Creación de los volúmenes ---
vol_x_actual = vol_x
vol_y_actual = vol_y

for i in range(num_pisos):
    # Calcular la posición del piso actual
    z_pos = i * altura_piso
    x_pos = -vol_x / 2 + vol_x_actual / 2
    
    # Crear el piso en su ubicación
    crear_piso(f"Piso_{i+1}", (x_pos, 0, z_pos))
    
    # Retranquear el siguiente volumen
    vol_x_actual -= retranqueo
    vol_y_actual -= retranqueo