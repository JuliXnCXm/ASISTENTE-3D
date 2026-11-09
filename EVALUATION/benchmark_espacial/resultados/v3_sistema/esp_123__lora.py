import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del edificio ---
num_pisos = 3
vol_ancho = 24.0
vol_fondo = 16.0
vol_alto_piso = 3.0
retranqueo = 2.0

# --- Función para crear un piso ---
def crear_piso(nombre, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    piso = bpy.context.active_object
    piso.name = nombre
    piso.dimensions = (vol_ancho, vol_fondo, vol_alto_piso)
    bpy.ops.object.transform_apply(scale=True)
    return piso

# --- Creación de los volúmenes ---
vol_actual = vol_ancho
vol_ancho_nuevo = vol_ancho - retranqueo
vol_fondo_nuevo = vol_fondo - retranqueo

for i in range(num_pisos):
    # Piso inferior del volumen
    crear_piso(f"Piso_{i+1}_Inf", (0, 0, i * vol_alto_piso))
    
    # Piso superior del volumen
    crear_piso(f"Piso_{i+1}_Sup", (0, 0, (i + 1) * vol_alto_piso))
    
    # Muro trasero del volumen
    crear_piso(f"Muro_Trasero_{i+1}", (0, vol_fondo/2 - vol_fondo_nuevo/2, (i + 1) * vol_alto_piso))
    muro_trasero = bpy.context.active_object
    muro_trasero.dimensions = (vol_ancho_nuevo, vol_fondo_nuevo, vol_alto_piso)
    bpy.ops.object.transform_apply(scale=True)
    
    # Muro frontal del volumen
    crear_piso(f"Muro_Frontal_{i+1}", (0, -vol_fondo/2 + vol_fondo_nuevo/2, (i + 1) * vol_alto_piso))
    muro_frontal = bpy.context.active_object
    muro_frontal.dimensions = (vol_ancho_nuevo, vol_fondo_nuevo, vol_alto_piso)
    bpy.ops.object.transform_apply(scale=True)

    # Muro izquierdo del volumen
    crear_piso(f"Muro_Izquierdo_{i+1}", (-vol_ancho/2 + vol_ancho_nuevo/2, 0, (i + 1) * vol_alto_piso))
    muro_izq = bpy.context.active_object
    muro_izq.dimensions = (vol_ancho_nuevo, vol_fondo_nuevo, vol_alto_piso)
    bpy.ops.object.transform_apply(scale=True)
    
    # Muro derecho del volumen
    crear_piso(f"Muro_Derecho_{i+1}", (vol_ancho/2 - vol_ancho_nuevo/2, 0, (i + 1) * vol_alto_piso))
    muro_der = bpy.context.active_object
    muro_der.dimensions = (vol_ancho_nuevo, vol_fondo_nuevo, vol_alto_piso)
    bpy.ops.object.transform_apply(scale=True)