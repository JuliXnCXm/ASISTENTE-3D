import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del edificio ---
num_pisos = 3
ancho_base = 20.0
profundidad_base = 20.0
altura_piso = 3.0
retranqueo = 3.0

# --- Función para crear un piso ---
def crear_piso(nombre, escala, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    piso = bpy.context.active_object
    piso.name = nombre
    piso.scale = escala
    bpy.ops.object.transform_apply(scale=True)
    return piso

# --- Creación de los volúmenes ---
vol1 = crear_piso("Volumen_1", (ancho_base, profundidad_base, altura_piso), (0, 0, 0))
vol2 = crear_piso("Volumen_2", (ancho_base - retranqueo, profundidad_base - retranqueo, altura_piso), (0, 0, altura_piso))
vol3 = crear_piso("Volumen_3", (ancho_base - 2 * retranqueo, profundidad_base - 2 * retranqueo, altura_piso), (0, 0, 2 * altura_piso))