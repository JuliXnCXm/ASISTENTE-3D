import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del edificio ---
num_pisos = 3
altura_piso = 3.0
vol_x = 24.0
vol_y = 20.0
retranqueo = 3.0

# --- Función para crear un piso ---
def crear_piso(nombre, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    piso = bpy.context.active_object
    piso.name = nombre
    piso.dimensions = (vol_x, vol_y, altura_piso)
    return piso

# --- Creación de los volúmenes escalonados ---
vol_actual_x = vol_x
vol_actual_y = vol_y
for i in range(num_pisos):
    # Crear el piso actual
    crear_piso(f"Piso_{i+1}", (0, 0, i * altura_piso))
    
    # Retranquear para el siguiente volumen
    vol_actual_x -= retranqueo
    vol_actual_y -= retranqueo