import bpy
import bmesh

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del sofá ---
largo = 2.2
fondo = 0.95
alto = 0.75
alto_asiento = 0.45
alto_brazos = 0.70
ancho_brazo = 0.25

# --- Crear la base del sofá ---
escala_base = (largo, fondo, alto_asiento)
loc_base = (0, 0, alto_asiento / 2)
bpy.ops.mesh.primitive_cube_add(size=1, scale=escala_base, location=loc_base)
base = bpy.context.active_object
base.name = "BaseSofa"

# --- Crear el respaldo ---
largo_respaldo = largo
alto_respaldo = alto - alto_asiento
fondo_respaldo = 0.20
escala_respaldo = (largo_respaldo, fondo_respaldo, alto_respaldo)
loc_respaldo = (0, -fondo / 2 + fondo_respaldo / 2, alto_asiento + alto_respaldo / 2)
bpy.ops.mesh.primitive_cube_add(size=1, scale=escala_respaldo, location=loc_respaldo)
respaldo = bpy.context.active_object
respaldo.name = "RespaldoSofa"

# --- Crear los brazos ---
alto_brazo_cubo = alto_brazos
ancho_brazo_cubo = ancho_brazo
fondo_brazo_cubo = fondo
escala_brazo = (ancho_brazo_cubo, fondo_brazo_cubo, alto_brazo_cubo)

# Brazo Izquierdo
loc_brazo_izq = (-largo / 2 + ancho_brazo_cubo / 2, 0, alto_brazo_cubo / 2)
bpy.ops.mesh.primitive_cube_add(size=1, scale=escala_brazo, location=loc_brazo_izq)
brazo_izq = bpy.context.active_object
brazo_izq.name = "BrazoIzquierdo"

# Brazo Derecho
loc_brazo_der = (largo / 2 - ancho_brazo_cubo / 2, 0, alto_brazo_cubo / 2)
bpy.ops.mesh.primitive_cube_add(size=1, scale=escala_brazo, location=loc_brazo_der)
brazo_der = bpy.context.active_object
brazo_der.name = "BrazoDerecho"

# --- Simular capitoné con esferas (a modo de representación) ---
radio_boton = 0.02
def crear_capitone(obj, num_x, num_y):
    dims = obj.dimensions
    loc_start = obj.location - dims / 2
    for i in range(1, num_x):
        for j in range(1, num_y):
            x = loc_start.x + i * (dims.x / num_x)
            y = obj.location.y + dims.y/2 + 0.01 # Ligeramente fuera
            z = loc_start.z + j * (dims.z / num_y)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_boton, location=(x, y, z), segments=16, ring_count=8)
            bpy.context.object.name = f"Boton_{obj.name}_{i}_{j}"

# Añadir botones al respaldo
crear_capitone(respaldo, 12, 3)