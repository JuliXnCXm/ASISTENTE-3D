import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del edificio ---
num_pisos = 4
ancho_base = 20.0
profundidad_base = 20.0
altura_piso = 3.0
retranqueo = 2.0

# --- Función para crear un piso ---
def crear_piso(nombre, escala, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    piso = bpy.context.active_object
    piso.name = nombre
    piso.scale = escala
    return piso

# --- Creación de los volúmenes ---
vol_tam = (ancho_base, profundidad_base, altura_piso)

for i in range(num_pisos):
    # Calcular la posición del piso actual
    pos_x = -ancho_base / 2 + vol_tam[0] / 2
    pos_y = -profundidad_base / 2 + vol_tam[1] / 2
    
    # Aplicar retranqueo
    pos_x -= i * retranqueo
    pos_y -= i * retranqueo
    
    # Crear el piso
    crear_piso(f"Piso_{i+1}", vol_tam, (pos_x, pos_y, i * altura_piso))